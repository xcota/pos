#!/usr/bin/env python3
"""memory_index.py — node-level semantic index for the vault (Path A).

Design decisions (all measured, not guessed):
  - granularity = one node per markdown section + baked-in header-path → the
    biggest lever (roughly 2x over file-level embedding). Section chunking
    matters more than model choice.
  - model = EmbeddingGemma-300m q8 ONNX (ungated), 768d — quality in the
    BGE-M3 tier (hit@5 ~0.92) at ~15x less weight (309 MB vs 4.5 GB).
  - storage = ONE .npz sidecar in git, brute-force numpy cosine, NO index / DB
    → nothing to corrupt (an embedded vector store under concurrent read+write
    once blew up to 100+ GB; a single flat file has no such failure mode).
  - ONLY full-rebuild + atomic replace. NEVER an incremental upsert into the store.

Usage:
  python scripts/memory_index.py build            # rebuild sidecar (full vault)
  python scripts/memory_index.py update           # re-embed ONLY changed files (for /dream)
  python scripts/memory_index.py search "question"  # top-K path + header + snippet
  python scripts/memory_index.py serve            # warm server (lazy, TTL suicide)
  python scripts/memory_index.py dupes [0.85]     # semantic duplicate nodes (graph upkeep)

Latency: a cold query is ~7s (model load). So `search` first knocks on a warm
server (127.0.0.1:8765, ms), and if absent searches cold AND spawns the server
in the background for next time. The server dies on its own after 30 min idle —
not a daemon, a cache with a TTL. It is read-only over the .npz, and re-reads
the file when its mtime changes.
Architecture note: knowledge/concepts/memory-embedding-layer.md
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

# --- vault root, derived from this script's location (scripts/ lives at root/scripts) ---
# Path-agnostic: works from any fresh clone, no hardcoded absolute path.
ROOT = Path(__file__).resolve().parent.parent

# --- model (parameterised: switch to BGE / another quant = edit here) ---
REPO = "onnx-community/embeddinggemma-300m-ONNX"
ONNX_FILE = "onnx/model_quantized.onnx"        # q8: quality == fp32, weight 309 MB
ONNX_DATA = "onnx/model_quantized.onnx_data"
DIM = 768                                       # MRL: can drop to 256 (3x lighter sidecar, hit@5 holds)
Q_PROMPT = "task: search result | query: {}"
D_PROMPT = "title: none | text: {}"

# --- corpus = the real searchable surface of the graph ---
# `memory` and `inbox` are in the list on purpose: the person's own verbatim stories
# (memory/svoboda/{id}/stories/) and whatever they drop into inbox/ are exactly what
# "find what I said about X" has to reach. A wing that doesn't exist yet is skipped.
WINGS = ["knowledge", "daily", "context", "reports", "state", "memory", "inbox", "projects"]
EXCLUDE = ("/node_modules/", "/.venv/", "/.memory_venv/", "/build/", "/.git/", "/memory-index/")

# --- storage ---
INDEX_DIR = ROOT / "state/memory-index"
NPZ = INDEX_DIR / "nodes.npz"
MANIFEST = INDEX_DIR / "manifest.json"


# ---------- chunk into nodes (sections by header + header-path) ----------
def _hpath(stem, h2, h3):
    return " > ".join([p for p in (stem, h2, h3) if p])


def chunk_by_headers(text, stem):
    nodes, buf, h2, h3 = [], [], "", ""

    def flush():
        t = "\n".join(buf).strip()
        if t:
            nodes.append((_hpath(stem, h2, h3), t))

    for ln in text.split("\n"):
        m3 = re.match(r"^###\s+(.+)", ln)
        m2 = re.match(r"^##\s+(.+)", ln)
        if m3:
            flush(); buf = []; h3 = m3.group(1).strip()
        elif m2:
            flush(); buf = []; h2 = m2.group(1).strip(); h3 = ""
        else:
            buf.append(ln)
    flush()
    if not nodes:
        nodes = [(stem, text.strip())]
    return nodes


def _aliases_of(text):
    """aliases: [a, b] from frontmatter — a bridge for jargon/synonyms.
    Baked into the text of EVERY node of the file → a jargon query still hits
    the entity."""
    if not text.startswith("---"):
        return ""
    try:
        fm = text[3:text.index("---", 3)]
    except ValueError:
        return ""
    m = re.search(r"^aliases:\s*\[([^\]]*)\]", fm, re.M)
    if not m:
        return ""
    vals = [v.strip().strip("\"'") for v in m.group(1).split(",") if v.strip()]
    return ", ".join(vals)


def file_nodes(p, txt):
    """File → list of (relpath, header_path, body, embed_text)."""
    relpath = str(p.relative_to(ROOT))
    aka = _aliases_of(txt)
    aka_line = f"aka: {aka}\n" if aka else ""
    out = []
    for hp, body in chunk_by_headers(txt, p.stem):
        out.append((relpath, hp, body, f"{hp}\n{aka_line}{body[:2000]}"))
    return out


def walk_nodes():
    """Walk the graph → list of (relpath, header_path, body, embed_text)."""
    out = []
    for wing in WINGS:
        wing_dir = ROOT / wing
        if not wing_dir.is_dir():
            continue
        for p in wing_dir.rglob("*.md"):
            rel = "/" + str(p.relative_to(ROOT)) + "/"
            if any(x in rel for x in EXCLUDE):
                continue
            try:
                txt = p.read_text(errors="ignore")
            except Exception:
                continue
            if not txt.strip():
                continue
            out.extend(file_nodes(p, txt))
    return out


# ---------- embedding (EmbeddingGemma q8 ONNX) ----------
_SESS = None
_TOK = None


def _load_model():
    global _SESS, _TOK
    if _SESS is not None:
        return
    import onnxruntime as ort
    from huggingface_hub import hf_hub_download
    from transformers import AutoTokenizer
    onnx_path = hf_hub_download(REPO, ONNX_FILE)
    try:
        hf_hub_download(REPO, ONNX_DATA)
    except Exception:
        pass
    _TOK = AutoTokenizer.from_pretrained(REPO)
    _SESS = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])


def embed(texts, batch=16):
    _load_model()
    in_names = {i.name for i in _SESS.get_inputs()}
    out_names = [o.name for o in _SESS.get_outputs()]
    target = "sentence_embedding" if "sentence_embedding" in out_names else out_names[0]
    vecs = []
    for s in range(0, len(texts), batch):
        enc = _TOK(texts[s:s + batch], padding=True, truncation=True,
                   max_length=512, return_tensors="np")
        feed = {"input_ids": enc["input_ids"].astype(np.int64),
                "attention_mask": enc["attention_mask"].astype(np.int64)}
        if "token_type_ids" in in_names:
            feed["token_type_ids"] = np.zeros_like(enc["input_ids"], dtype=np.int64)
        out = _SESS.run([target], feed)[0]
        if out.ndim == 3:  # fallback: last_hidden_state → masked mean-pool
            mask = enc["attention_mask"][:, :, None].astype(np.float32)
            out = (out * mask).sum(1) / np.clip(mask.sum(1), 1e-9, None)
        if DIM and out.shape[1] > DIM:      # MRL truncation
            out = out[:, :DIM]
        out = out / np.clip(np.linalg.norm(out, axis=1, keepdims=True), 1e-9, None)
        vecs.append(out.astype(np.float32))
    return np.vstack(vecs)


# ---------- build ----------
def _save(vecs, relpaths, headers, snippets, n_files):
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    # tmp name MUST end in .npz — otherwise np.savez appends the suffix itself
    tmp = INDEX_DIR / "nodes.tmp.npz"
    np.savez(tmp, vecs=vecs, relpaths=relpaths, headers=headers, snippets=snippets)
    os.replace(tmp, NPZ)   # atomic replace — never an upsert
    try:
        head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                                       text=True).strip()
    except Exception:
        head = "unknown"
    MANIFEST.write_text(json.dumps({
        "model": REPO, "onnx": ONNX_FILE, "dim": DIM,
        "n_nodes": len(relpaths), "n_files": int(n_files),
        "built_at": datetime.now().isoformat(timespec="seconds"),
        "git_head": head,
    }, ensure_ascii=False, indent=2))
    print(f"OK → {NPZ.relative_to(ROOT)} ({NPZ.stat().st_size/1e6:.1f} MB)")


def build():
    print("walk graph → nodes...")
    quads = walk_nodes()
    n_files = len({r for r, _, _, _ in quads})
    print(f"nodes: {len(quads)} from {n_files} files")

    embed_texts = [D_PROMPT.format(et) for _, _, _, et in quads]
    print("embedding (EmbeddingGemma q8 ONNX)... ~35 min on CPU")
    vecs = embed(embed_texts)

    relpaths = np.array([r for r, _, _, _ in quads])
    headers = np.array([hp for _, hp, _, _ in quads])
    snippets = np.array([body[:300].replace("\n", " ") for _, _, body, _ in quads])
    _save(vecs, relpaths, headers, snippets, n_files)


# ---------- update (incremental RE-COMPUTE, full atomic write) ----------
def update():
    """git-diff from manifest.git_head + worktree → re-embed only the nodes of
    changed files → assemble a NEW full array → atomic replace.
    The re-compute is incremental; the write is ALWAYS full."""
    if not NPZ.exists() or not MANIFEST.exists():
        print("no index — full build")
        return build()
    head_then = json.loads(MANIFEST.read_text()).get("git_head", "")

    changed = set()
    try:
        if head_then and head_then != "unknown":
            diff = subprocess.check_output(
                ["git", "-C", str(ROOT), "diff", "--name-only", head_then, "HEAD"],
                text=True, stderr=subprocess.DEVNULL)
            changed.update(l.strip() for l in diff.splitlines() if l.strip())
        porc = subprocess.check_output(
            ["git", "-C", str(ROOT), "status", "--porcelain"], text=True)
        for l in porc.splitlines():
            changed.add(l[3:].strip().strip('"'))
    except subprocess.CalledProcessError:
        print("manifest git_head does not resolve — full build")
        return build()

    def in_graph(rp):
        if not rp.endswith(".md"):
            return False
        if not any(rp.startswith(w + "/") for w in WINGS):
            return False
        return not any(x in "/" + rp + "/" for x in EXCLUDE)

    changed = {rp for rp in changed if in_graph(rp)}
    if not changed:
        print("no changed graph files — index is current")
        return

    print(f"changed files: {len(changed)}")
    d = np.load(NPZ, allow_pickle=False)
    vecs, relpaths = d["vecs"], d["relpaths"]
    headers, snippets = d["headers"], d["snippets"]
    keep = ~np.isin(relpaths, list(changed))

    new_quads = []
    for rp in sorted(changed):
        p = ROOT / rp
        if not p.exists():
            continue   # deleted file — its nodes simply drop out via the keep mask
        txt = p.read_text(errors="ignore")
        if txt.strip():
            new_quads.extend(file_nodes(p, txt))
    print(f"nodes to re-compute: {len(new_quads)} (old dropped: {int((~keep).sum())})")

    if new_quads:
        new_vecs = embed([D_PROMPT.format(et) for _, _, _, et in new_quads])
        vecs = np.vstack([vecs[keep], new_vecs])
        relpaths = np.concatenate([relpaths[keep],
                                   np.array([r for r, _, _, _ in new_quads])])
        headers = np.concatenate([headers[keep],
                                  np.array([h for _, h, _, _ in new_quads])])
        snippets = np.concatenate([snippets[keep],
                                   np.array([b[:300].replace("\n", " ")
                                             for _, _, b, _ in new_quads])])
    else:
        vecs, relpaths = vecs[keep], relpaths[keep]
        headers, snippets = headers[keep], snippets[keep]

    _save(vecs, relpaths, headers, snippets, len(set(relpaths.tolist())))


# ---------- dupes (graph upkeep: semantic duplicate nodes) ----------
def dupes(threshold=0.85, top=40):
    """Pairs of nodes from DIFFERENT files with cos>threshold = merge candidates."""
    d = np.load(NPZ, allow_pickle=False)
    vecs, relpaths, headers = d["vecs"], d["relpaths"], d["headers"]
    skip = np.array(["INDEX" in r or "AGENTS" in r or "MOC_" in r for r in relpaths])
    pairs = []
    step = 2000
    for s in range(0, len(vecs), step):
        block = vecs[s:s + step] @ vecs.T          # (step, N)
        for bi in range(block.shape[0]):
            i = s + bi
            if skip[i]:
                continue
            row = block[bi]
            for j in np.where(row > threshold)[0]:
                if j <= i or skip[j] or relpaths[j] == relpaths[i]:
                    continue
                pairs.append((float(row[j]), i, int(j)))
    pairs.sort(reverse=True)
    print(f"node pairs from different files with cos>{threshold}: {len(pairs)} (top {top}):\n")
    for score, i, j in pairs[:top]:
        print(f"[{score:.3f}] {relpaths[i]} § {headers[i][:60]}")
        print(f"        ⇄ {relpaths[j]} § {headers[j][:60]}")


# ---------- search (core) ----------
_NPZ_CACHE = {"mtime": None, "data": None}


def _load_npz():
    """Cache .npz by mtime — the server re-reads the file after a rebuild."""
    mt = NPZ.stat().st_mtime
    if _NPZ_CACHE["mtime"] != mt:
        d = np.load(NPZ, allow_pickle=False)
        _NPZ_CACHE["data"] = (d["vecs"], d["relpaths"], d["headers"], d["snippets"])
        _NPZ_CACHE["mtime"] = mt
    return _NPZ_CACHE["data"]


def search_core(query, k=8):
    """→ list of result lines (shared by CLI and server)."""
    vecs, relpaths, headers, snippets = _load_npz()
    q = embed([Q_PROMPT.format(query)])[0]
    sims = vecs @ q
    best = {}
    for i in np.argsort(-sims):   # collapse: best node per file
        f = relpaths[i]
        if f not in best:
            best[f] = i
        if len(best) >= k:
            break
    lines = []
    for rank, (f, i) in enumerate(best.items(), 1):
        lines.append(f"{rank}. [{sims[i]:.3f}] {f}")
        if headers[i] and headers[i] != Path(f).stem:
            lines.append(f"     § {headers[i]}")
        lines.append(f"     {snippets[i][:160]}")
    return lines


# ---------- warm server (lazy, TTL suicide) ----------
HOST, PORT = "127.0.0.1", 8765
IDLE_TTL = 30 * 60   # 30 min idle → server dies on its own


def serve():
    import threading
    import time as _t
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.parse import urlparse, parse_qs

    _load_model()      # warm the model once
    _load_npz()        # and the vectors
    last_hit = [_t.time()]

    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            last_hit[0] = _t.time()
            u = urlparse(self.path)
            if u.path != "/search":
                self.send_response(404); self.end_headers(); return
            qs = parse_qs(u.query)
            query = (qs.get("q") or [""])[0]
            k = int((qs.get("k") or ["8"])[0])
            body = "\n".join(search_core(query, k)).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *a):   # quiet
            pass

    def reaper():
        while True:
            _t.sleep(60)
            if _t.time() - last_hit[0] > IDLE_TTL:
                os._exit(0)

    try:
        srv = HTTPServer((HOST, PORT), H)
    except OSError:
        # port taken — a live server already exists, quietly exit (lazy-spawn race)
        os._exit(0)
    threading.Thread(target=reaper, daemon=True).start()
    print(f"memory-index warm server on {HOST}:{PORT} (TTL {IDLE_TTL//60} min)")
    srv.serve_forever()


def _try_server(query, k):
    """Knock on the warm server. None = no server."""
    import urllib.parse
    import urllib.request
    try:
        with urllib.request.urlopen(
                f"http://{HOST}:{PORT}/search?q={urllib.parse.quote(query)}&k={k}",
                timeout=15) as r:
            return r.read().decode()
    except Exception:
        return None


def _spawn_server():
    """Lazily bring up the server in the background (detached, log to state dir)."""
    import subprocess
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    log = open(INDEX_DIR / "server.log", "a")
    subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "serve"],
                     stdout=log, stderr=log, start_new_session=True)


def search(query, k=8):
    if not NPZ.exists():
        print("no index — first run: python scripts/memory_index.py build", file=sys.stderr)
        return
    warm = _try_server(query, k)
    if warm is not None:
        print(warm)
        return
    _spawn_server()                       # warm for next time
    print("\n".join(search_core(query, k)))   # this time — cold


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("build", "update", "search", "serve", "dupes"):
        print(__doc__)
        return
    cmd = sys.argv[1]
    if cmd == "build":
        build()
    elif cmd == "update":
        update()
    elif cmd == "serve":
        serve()
    elif cmd == "dupes":
        dupes(float(sys.argv[2]) if len(sys.argv) > 2 else 0.85)
    else:
        search(" ".join(sys.argv[2:]))


if __name__ == "__main__":
    main()
