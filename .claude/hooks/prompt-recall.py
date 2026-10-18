#!/usr/bin/env python3
"""UserPromptSubmit hook: memory for each message.

For every message the person sends in this folder, attach up to 3 nearest nodes of the
semantic index (state/memory-index/nodes.npz) — path, section, snippet — as context, so
the assistant sees related notes before it answers. Left to itself an agent rarely goes
to memory; a hook on every message does. Measured on one real vault (60 real messages):
a hit >= 0.50 for 40% of messages vs 7.6% for grep; at 0.55 — 17%.

Same warm server as semantic-recall.py (this folder's port, X-Vault-Root check), same
0.50 threshold. Prints nothing when:
  - search by meaning is not installed here (no index);
  - the message is a slash command or a harness notification;
  - the person's own words (pastes, tags and links removed) are under 20 characters —
    a CJK character counts as 3 — then the pasted text, if any, is the query;
  - the query is mostly code or a log (under 30% letters);
  - nothing scores >= 0.50 outside daily/ and inbox/ (raw stream and drop-box, not
    curated memory), or every hit was already shown this session
    (state/memory-index/seen/<session>.json, files older than 7 days are cleared);
  - the server is cold or belongs to another folder — then this folder's server is
    spawned in the background for the next message.
Never blocks a message: any error = silent exit 0. Log: state/memory-index/hook.log
(lengths and paths only, never the text of the message).
Vault root: $CLAUDE_PROJECT_DIR, else two levels up from this file.
Layer doc: knowledge/concepts/memory-embedding-layer.md
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import zlib
from pathlib import Path

MIN_QUERY = 20       # "yes", "go on", "ok" — no search
MAX_QUERY = 400      # the query = the start of the message
MIN_SCORE = 0.50     # as for greps (relevant hits score 0.59+)
MIN_SCORE_CJK = 0.40 # Chinese/Japanese queries score lower: in a live onboarding run (2026-10-19)
                     # the right card topped the list at 0.44 while unrelated files sat at 0.38-0.39
TOP_K_CJK = 2        # lower bar -> fewer hits, so noise stays small
TOP_K = 3
FETCH_K = 12         # with a margin: the filters below drop some paths
SKIP_PREFIX = ("daily/", "inbox/")
SKIP_PART = ("/inbox/",)
HEADER = ("Related notes from this folder's memory (semantic index, best matches for the "
          "message; open what is relevant before answering — check here before building "
          "something new):")


def vault_root():
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and os.path.isdir(env):
        return Path(env).resolve()
    return Path(__file__).resolve().parents[2]   # .claude/hooks/<this> → vault root


def server_port(root):
    """This folder's warm-server port — same formula as scripts/memory_index.py (keep in sync)."""
    return 8800 + zlib.crc32(str(root).encode()) % 200


def _log(root, msg):
    try:
        from datetime import datetime
        with open(root / "state" / "memory-index" / "hook.log", "a") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')} prompt-recall {msg}\n")
    except Exception:
        pass


def own_text(prompt):
    """The person's own words without pastes, tags and links; the paste is the fallback query."""
    pasted = " ".join(re.findall(r"<pasted_content[^>]*>(.*?)</pasted_content[^>]*>",
                                 prompt, flags=re.S))
    t = re.sub(r"<pasted_content[^>]*>.*?</pasted_content[^>]*>", " ", prompt, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"https?://\S+", " ", t)
    return " ".join(t.split()), " ".join(pasted.split())


def weight(s):
    """Length with a CJK character counted as 3 — one carries about as much as three Latin
    letters, so a short Chinese question is not dismissed as 'too short'."""
    return len(s) + 2 * sum(1 for ch in s if "\u3040" <= ch <= "\u9fff" or "\uac00" <= ch <= "\ud7af")


def _seen_path(root, sid):
    safe = re.sub(r"[^A-Za-z0-9_-]", "", sid)[:64] or "nosid"
    return root / "state" / "memory-index" / "seen" / f"{safe}.json"


def seen_load(root, sid):
    try:
        return set(json.loads(_seen_path(root, sid).read_text()))
    except Exception:
        return set()


def seen_save(root, sid, seen):
    try:
        p = _seen_path(root, sid)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(sorted(seen)))
        cutoff = time.time() - 7 * 86400          # old sessions — gone
        for old in p.parent.iterdir():
            if old.stat().st_mtime < cutoff:
                old.unlink()
    except Exception:
        pass


def ask_server(root, q, k, timeout=1.5):
    """Body of this folder's server answer; None = no server, or another folder's server."""
    url = f"http://127.0.0.1:{server_port(root)}/search?q={urllib.parse.quote(q)}&k={k}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            if r.headers.get("X-Vault-Root") != urllib.parse.quote(str(root)):
                return None
            return r.read().decode("utf-8", "replace")
    except Exception:
        return None


def spawn_server(root):
    py = root / ".memory_venv" / "bin" / "python"
    if not py.exists():
        return
    try:
        subprocess.Popen([str(py), str(root / "scripts" / "memory_index.py"), "serve"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)
    except Exception:
        pass


def recall(root, prompt, sid):
    head = prompt.lstrip()[:300]
    if head.startswith("/"):                      # skills and commands run on their own
        return []
    if (head.startswith(("<task-notification", "<system-reminder"))
            or "[SYSTEM NOTIFICATION" in head):   # notifications are not the person's words
        return []
    q, pasted = own_text(prompt)
    if weight(q) < MIN_QUERY and pasted:
        q = (q + " " + pasted[:300]).strip()
    if weight(q) < MIN_QUERY:
        return []
    letters = sum(ch.isalpha() for ch in q)
    if letters < 0.3 * len(q):                   # pasted code or a log, not a question
        _log(root, f"len={len(q)} mostly non-letters → skipped")
        return []
    q = q[:MAX_QUERY]
    body = ask_server(root, q, FETCH_K)
    if body is None:
        spawn_server(root)
        _log(root, f"len={len(q)} server cold or another folder's → spawned, skipped")
        return []

    seen = seen_load(root, sid)
    cjk = any("\u3040" <= ch <= "\u30ff" or "\u4e00" <= ch <= "\u9fff" for ch in q)
    min_score, top_k = (MIN_SCORE_CJK, TOP_K_CJK) if cjk else (MIN_SCORE, TOP_K)
    blocks, lines, i = [], body.splitlines(), 0
    while i < len(lines):
        ln = lines[i]
        block = [ln]
        j = i + 1
        while j < len(lines) and lines[j].startswith("     "):
            block.append(lines[j]); j += 1
        i = j
        m = re.match(r"\d+\. \[([0-9.]+)\] (.+)$", ln)
        if not m:
            continue
        score, path = float(m.group(1)), m.group(2).strip()
        if score < min_score or path in seen:
            continue
        if path.startswith(SKIP_PREFIX) or any(s in path for s in SKIP_PART):
            continue
        blocks.append((path, block))
        if len(blocks) >= top_k:
            break
    if not blocks:
        _log(root, f"len={len(q)} no hits above threshold")
        return []
    seen.update(p for p, _ in blocks)
    seen_save(root, sid, seen)
    out = []
    for n, (_, block) in enumerate(blocks, 1):
        out.append(re.sub(r"^\d+\.", f"{n}.", block[0]))
        out.extend(block[1:])
    _log(root, f"len={len(q)} emitted {len(blocks)}: " + ", ".join(p for p, _ in blocks))
    return out


def main():
    try:
        payload = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace") or "{}")
    except Exception:
        return
    root = vault_root()
    if not (root / "state" / "memory-index" / "nodes.npz").exists():
        return                                   # search by meaning is not installed here
    cwd = os.path.realpath(str(payload.get("cwd") or root))
    if cwd != str(root) and not cwd.startswith(str(root) + os.sep):
        return                                   # a session outside this folder
    prompt = payload.get("prompt") or ""
    sid = str(payload.get("session_id") or "nosid")
    try:
        hits = recall(root, prompt, sid)
    except Exception as e:
        _log(root, f"error {type(e).__name__}")
        hits = []
    if hits:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": HEADER + "\n" + "\n".join(hits)}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
