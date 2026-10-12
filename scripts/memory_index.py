#!/usr/bin/env python3
"""memory_index.py — node-level semantic index for the vault (Path A).

Design decisions (all measured, not guessed):
  - granularity = one node per markdown section + baked-in header-path. On a capped
    corpus (540 files, 25 questions) the node pipeline scored MRR .773 vs .422 for
    file-level embedding — but chunking, header-path, collapse-to-file and long-file
    truncation changed at once, so "chunking matters more than model choice" is a
    strong hint, NOT a proof. A live replay on a full vault: MRR .593.
  - model = EmbeddingGemma-300m q8 ONNX (ungated), 768d — quality in the BGE-M3 tier
    (hit@5 ~0.92) at ~15x less weight (309 MB vs 4.5 GB). q8 quantises the model
    WEIGHTS; the vectors on disk are float32 (VEC_DTYPE).
  - storage = ONE .npz sidecar (gitignored — a rebuildable cache, never the memory itself), brute-force numpy cosine, NO index / DB
    → nothing to corrupt (an embedded vector store under concurrent read+write
    once blew up to 100+ GB; a single flat file has no such failure mode).
  - ONLY full-write + atomic replace. NEVER an incremental upsert into the store.
  - format 2: strings without padding (one UTF-8 buffer + offsets; paths = a file table
    + a file_id per node) and the meta (model, dim, git_head, built_at, counters) INSIDE
    the npz — vectors, strings and meta change in ONE atomic replace. manifest.json is
    only a mirror for the start hook and for people. Format 1 (fixed-width string
    arrays, meta only in manifest.json) is still read; the next `update` rewrites it.

Usage:
  python scripts/memory_index.py build            # rebuild sidecar (full vault)
  python scripts/memory_index.py update           # re-embed ONLY changed files (for /dream)
  python scripts/memory_index.py search "question"  # top-K path + header + snippet
  python scripts/memory_index.py serve            # warm server (lazy, TTL suicide)
  python scripts/memory_index.py dupes [0.85]     # semantic duplicate nodes (graph upkeep)

Latency: a cold query is ~7s (model load). So `search` first knocks on a warm
server (ms), and if absent searches cold AND spawns the server in the background
for next time. The server dies on its own after 30 min idle — not a daemon, a cache
with a TTL. It is read-only over the .npz, and re-reads the file when its mtime changes.
One server per folder: it listens on 127.0.0.1:PORT, PORT = 8800 + crc32(root) % 200,
and stamps every /search answer with X-Vault-Root (this folder's absolute path,
percent-encoded). A client that gets another folder's stamp treats the server as
cold — two folders on one machine never answer each other's searches.
Architecture note: knowledge/concepts/memory-embedding-layer.md
"""
import json
import os
import re
import subprocess
import sys
import urllib.parse
import zlib
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
# Match = substring of the path wrapped in slashes ("/" + relpath + "/"), so a file
# suffix is written with a trailing slash (e.g. ".generated.md/").
EXCLUDE = (
    "/node_modules/", "/.venv/", "/.memory_venv/", "/build/", "/.git/", "/memory-index/",
    "/site-packages/",   # third-party library files under ANY env name ("/.venv/" misses e.g. "/.venv-tools/")
)

# --- storage ---
INDEX_DIR = ROOT / "state/memory-index"
NPZ = INDEX_DIR / "nodes.npz"
MANIFEST = INDEX_DIR / "manifest.json"
FORMAT = 2               # strings without padding + meta inside the npz
VEC_DTYPE = np.float32   # vector dtype ON DISK (always loaded as float32). float16 would cut the
                         # vectors in half but reorders near-ties (measured: 5 of 25 top-10 lists)


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


def is_excluded(rel):
    """rel = "/" + relpath + "/". One filter for build, update and the stale sweep."""
    return any(x in rel for x in EXCLUDE)


def walk_nodes():
    """Walk the graph → list of (relpath, header_path, body, embed_text)."""
    out = []
    for wing in WINGS:
        wing_dir = ROOT / wing
        if not wing_dir.is_dir():
            continue
        for p in wing_dir.rglob("*.md"):
            rel = "/" + str(p.relative_to(ROOT)) + "/"
            if is_excluded(rel):
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
    if not texts:                       # an empty folder must not crash the build
        return np.zeros((0, DIM or 768), dtype=np.float32)
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


# ---------- storage: format 2 (strings without padding, meta inside) ----------
def _pack(strs):
    """Strings → (one UTF-8 buffer as uint8, int64 offsets).
    Format 1 stored fixed-width <U arrays: the longest string (one header of 839 chars)
    stretched every row — on one real vault 62% of the file was padding."""
    bs = [str(s).encode("utf-8") for s in strs]
    off = np.zeros(len(bs) + 1, dtype=np.int64)
    if bs:
        off[1:] = np.cumsum([len(b) for b in bs])
    return np.frombuffer(b"".join(bs), dtype=np.uint8), off


def _unpack(buf, off):
    raw = buf.tobytes()
    out = np.empty(len(off) - 1, dtype=object)
    for i in range(len(out)):
        out[i] = raw[off[i]:off[i + 1]].decode("utf-8")
    return out


def _git_head():
    try:
        return subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"


def _load_index():
    """→ (vecs float32, relpaths, headers, snippets, meta). Reads format 2 and format 1.
    Strings come back as object arrays (no padding in memory; nothing is pickled to disk)."""
    d = np.load(NPZ, allow_pickle=False)
    if "meta" in d.files:
        meta = json.loads(d["meta"].tobytes().decode("utf-8"))
        relpaths = _unpack(d["files_buf"], d["files_off"])[d["file_id"]]
        headers = _unpack(d["headers_buf"], d["headers_off"])
        snippets = _unpack(d["snippets_buf"], d["snippets_off"])
    else:   # format 1: fixed-width <U arrays, meta only in manifest.json
        try:
            meta = json.loads(MANIFEST.read_text())
        except Exception:
            meta = {}
        meta["format"] = 1   # the version comes from the file itself, not from the manifest
        relpaths, headers, snippets = (d[k].astype(object) for k in ("relpaths", "headers", "snippets"))
    return d["vecs"].astype(np.float32, copy=False), relpaths, headers, snippets, meta


def _meta():
    """Config + watermarks of the index. The truth is the meta inside the npz (read without
    loading the vectors: npz is lazy); fallback = manifest.json (format 1 or a broken file)."""
    try:
        d = np.load(NPZ, allow_pickle=False)
        if "meta" in d.files:
            return json.loads(d["meta"].tobytes().decode("utf-8"))
    except Exception:
        pass
    try:
        return json.loads(MANIFEST.read_text())
    except Exception:
        return {}


def _save(vecs, relpaths, headers, snippets):
    """Full write + ONE atomic replace: vectors, strings and meta travel together."""
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    relpaths = np.asarray(relpaths, dtype=object)
    files, file_id = np.unique(relpaths, return_inverse=True)
    meta = {
        "format": FORMAT, "model": REPO, "onnx": ONNX_FILE, "dim": DIM,
        "vec_dtype": np.dtype(VEC_DTYPE).name,
        "n_nodes": int(len(relpaths)), "n_files": int(len(files)),
        "built_at": datetime.now().isoformat(timespec="seconds"),
        "git_head": _git_head(),
    }
    fb, fo = _pack(files)
    hb, ho = _pack(headers)
    sb, so = _pack(snippets)
    # tmp name MUST end in .npz — otherwise np.savez appends the suffix itself
    tmp = INDEX_DIR / "nodes.tmp.npz"
    np.savez(tmp, vecs=np.asarray(vecs).astype(VEC_DTYPE), file_id=file_id.astype(np.uint32),
             files_buf=fb, files_off=fo, headers_buf=hb, headers_off=ho,
             snippets_buf=sb, snippets_off=so,
             meta=np.frombuffer(json.dumps(meta, ensure_ascii=False).encode("utf-8"), dtype=np.uint8))
    os.replace(tmp, NPZ)   # atomic replace — never an upsert
    # mirror for the start hook / people; if this write fails, the truth is already in the npz
    MANIFEST.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"OK → {NPZ.relative_to(ROOT)} ({NPZ.stat().st_size/1e6:.1f} MB, "
          f"{meta['n_nodes']} nodes, {meta['n_files']} files)")


def _stale_reason(rp):
    """Why a node must drop out: its file is gone from disk or now falls under EXCLUDE."""
    rel = "/" + rp + "/"
    if is_excluded(rel):
        return next((x for x in EXCLUDE if x in rel), "excluded")
    if not (ROOT / rp).exists():
        return "file deleted"
    return None


def _stale_mask(relpaths):
    cache = {}
    out = np.zeros(len(relpaths), dtype=bool)
    for i, rp in enumerate(relpaths):
        if rp not in cache:
            cache[rp] = _stale_reason(rp)
        out[i] = cache[rp] is not None
    return out, cache


# ---------- build ----------
def build():
    print("walk graph → nodes...")
    quads = walk_nodes()
    n_files = len({r for r, _, _, _ in quads})
    print(f"nodes: {len(quads)} from {n_files} files")

    embed_texts = [D_PROMPT.format(et) for _, _, _, et in quads]
    print("embedding (EmbeddingGemma q8 ONNX)... ~35 min on CPU for a big vault, under a minute for a small one")
    vecs = embed(embed_texts)

    relpaths = [r for r, _, _, _ in quads]
    headers = [hp for _, hp, _, _ in quads]
    snippets = [body[:300].replace("\n", " ") for _, _, body, _ in quads]
    _save(vecs, relpaths, headers, snippets)


# ---------- update (incremental RE-COMPUTE, full atomic write) ----------
def _git_changed(head_then):
    """Paths changed since head_then: committed (diff) + worktree (status).
    -z = paths verbatim: without it git quotes non-ASCII names ("\\320\\274...") and such
    files would never be re-embedded. --untracked-files=all: otherwise a new untracked
    folder comes as one "dir/" line and its .md files are missed."""
    git = ["git", "-C", str(ROOT)]
    out = set()
    diff = subprocess.check_output(git + ["diff", "--name-only", "-z", head_then, "HEAD"],
                                   stderr=subprocess.DEVNULL)
    out.update(p for p in diff.decode("utf-8", "replace").split("\0") if p)
    porc = subprocess.check_output(git + ["status", "--porcelain", "-z", "--untracked-files=all"],
                                   stderr=subprocess.DEVNULL).decode("utf-8", "replace")
    fields = porc.split("\0")
    i = 0
    while i < len(fields):
        f = fields[i]
        if len(f) > 3:
            out.add(f[3:])
            if f[0] in "RC":   # rename/copy: the original path follows as its own field
                i += 1
                if i < len(fields) and fields[i]:
                    out.add(fields[i])
        i += 1
    return out


def update():
    """git-diff from the index's git_head + worktree → re-embed only the nodes of
    changed files → assemble a NEW full array → atomic replace.
    The re-compute is incremental; the write is ALWAYS full. Every run also drops the
    nodes of files that were deleted or fell under EXCLUDE (no model load for that)."""
    if not NPZ.exists():
        print("no index — full build")
        return build()
    meta = _meta()
    # vectors of different models in one array = garbage cosines without a single error
    if meta.get("model") != REPO or int(meta.get("dim") or 0) != DIM:
        print(f"index was built by another model/dim ({meta.get('model')}, {meta.get('dim')}) "
              f"≠ ({REPO}, {DIM}) — full build")
        return build()
    head_then = meta.get("git_head", "")
    if not head_then or head_then == "unknown":
        # built outside git or before the first commit (onboarding builds the index while the
        # folder may still have no history): nothing to diff from — a worktree-only update
        # would silently miss everything committed since
        print("index has no git watermark — full build")
        return build()
    try:
        changed = _git_changed(head_then)
    except (subprocess.CalledProcessError, OSError):
        print("git unavailable or the index's git_head does not resolve — full build")
        return build()

    def in_graph(rp):
        if not rp.endswith(".md"):
            return False
        if not any(rp.startswith(w + "/") for w in WINGS):
            return False
        return not is_excluded("/" + rp + "/")

    changed = {rp for rp in changed if in_graph(rp)}
    vecs, relpaths, headers, snippets, file_meta = _load_index()
    # self-cleaning: nodes of files that no longer exist (deleted, untracked and gone) or that
    # fell under EXCLUDE drop out on every update — before, they piled up until a full build
    stale, why = _stale_mask(relpaths)
    if not changed and not stale.any():
        if int(file_meta.get("format") or 1) < FORMAT:
            print(f"index is format {file_meta.get('format')} — rewriting as format {FORMAT} (no re-embedding)")
            return _save(vecs, relpaths, headers, snippets)
        print("no changed graph files — index is current")
        return
    if stale.any():
        dead = sorted({rp for rp, r in why.items() if r})
        print(f"dropping nodes of deleted/excluded files: {int(stale.sum())} ({len(dead)} files)")

    print(f"changed files: {len(changed)}")
    keep = np.array([rp not in changed for rp in relpaths], dtype=bool) & ~stale

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
        relpaths = list(relpaths[keep]) + [r for r, _, _, _ in new_quads]
        headers = list(headers[keep]) + [h for _, h, _, _ in new_quads]
        snippets = list(snippets[keep]) + [b[:300].replace("\n", " ") for _, _, b, _ in new_quads]
    else:
        vecs, relpaths = vecs[keep], relpaths[keep]
        headers, snippets = headers[keep], snippets[keep]

    _save(vecs, relpaths, headers, snippets)


# ---------- dupes (graph upkeep: semantic duplicate nodes) ----------
def dupes(threshold=0.85, top=40):
    """Pairs of nodes from DIFFERENT files with cos>threshold = merge candidates."""
    vecs, relpaths, headers, _, _ = _load_index()
    skip = np.array(["INDEX" in r or "AGENTS" in r or "MOC_" in r for r in relpaths])
    pairs = []
    step = 512   # block = step×N×4 bytes: 2000 took 175 MB at ~22K nodes, 512 takes 45 MB
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
        _NPZ_CACHE["data"] = _load_index()[:4]
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
HOST = "127.0.0.1"
# One port per folder (8800–8999), derived from its absolute path: two folders on one machine
# never share a server. The hooks compute the same formula without importing numpy —
# keep in sync with .claude/hooks/semantic-recall.py and .claude/hooks/prompt-recall.py.
PORT = 8800 + zlib.crc32(str(ROOT).encode()) % 200
# Whose index answered: this folder's absolute path. Percent-encoded because HTTP header
# values must be ASCII and a folder path may not be (a non-Latin user or folder name).
ROOT_STAMP = urllib.parse.quote(str(ROOT))
IDLE_TTL = 30 * 60   # 30 min idle → server dies on its own


def serve():
    import threading
    import time as _t
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.parse import urlparse, parse_qs

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
            self.send_header("X-Vault-Root", ROOT_STAMP)
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
        # bind BEFORE loading the model: a losing spawn (port taken) exits at once
        # instead of spending ~7s and ~500 MB on a model it will never serve
        srv = HTTPServer((HOST, PORT), H)
    except OSError:
        # port taken — a live server already exists, quietly exit (lazy-spawn race)
        os._exit(0)
    _load_model()      # warm the model once
    _load_npz()        # and the vectors
    last_hit[0] = _t.time()
    threading.Thread(target=reaper, daemon=True).start()
    print(f"memory-index warm server for {ROOT} on {HOST}:{PORT} (TTL {IDLE_TTL//60} min)", flush=True)
    srv.serve_forever()


def _try_server(query, k):
    """Knock on this folder's warm server. None = no server, or another folder's server."""
    import urllib.request
    try:
        with urllib.request.urlopen(
                f"http://{HOST}:{PORT}/search?q={urllib.parse.quote(query)}&k={k}",
                timeout=15) as r:
            if r.headers.get("X-Vault-Root") != ROOT_STAMP:
                return None   # someone else's index answered — same as no server
            return r.read().decode()
    except Exception:
        return None


def _spawn_server():
    """Lazily bring up the server in the background (detached, log to state dir)."""
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
