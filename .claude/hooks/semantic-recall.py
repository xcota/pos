#!/usr/bin/env python3
"""PostToolUse hook: append semantic candidates from the node-level embedding
index (state/memory-index/nodes.npz) to a search result.

In this environment Claude Code has NO Grep tool — search = `grep`/`rg` inside the
Bash tool. So the hook hangs on Bash (via the .sh gate) and extracts the pattern
from the command. A Grep tool, if it exists in another environment, is handled too.

Knocks on the warm memory_index server (127.0.0.1:8765, ~65ms). No server → lazy
background spawn + quiet exit (never blocks the search). Vault-scoped only.

Path-agnostic. The vault root is resolved, in order, from:
  1. $CLAUDE_PROJECT_DIR (exported by Claude Code)
  2. the hook payload's `cwd` / `project_dir`
  3. two levels up from this file (.claude/hooks/ → vault root)
The venv python is resolved relative to that root (.memory_venv, then bge_test_venv).
Layer doc: knowledge/concepts/memory-embedding-layer.md
"""
import json
import os
import re
import shlex
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

SERVER = "http://127.0.0.1:8765"
MIN_PATTERN = 6      # short/single-char patterns carry no semantics
MIN_SCORE = 0.50     # below this = polysemy noise (measured: relevant hits 0.59+)
TOP_K = 3
GREP_CMDS = {"grep", "egrep", "fgrep", "rg", " grep", "ack"}

# Two levels up from this file: .claude/hooks/<this> → vault root.
_SELF_ROOT = Path(__file__).resolve().parent.parent.parent


def resolve_vault(payload):
    """Vault root, path-agnostic. Env → payload → relative-to-self."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and Path(env).is_dir():
        return str(Path(env).resolve())
    for key in ("project_dir", "cwd"):
        v = payload.get(key)
        if v and Path(v).is_dir():
            return str(Path(v).resolve())
    return str(_SELF_ROOT)


def resolve_python(vault):
    """venv python relative to the vault root; system python3 as last resort."""
    for name in (".memory_venv", "bge_test_venv"):
        cand = Path(vault) / name / "bin" / "python"
        if cand.exists():
            return str(cand)
    return "python3"


def engine_path(vault):
    return str(Path(vault) / "scripts" / "memory_index.py")


def log_path(vault):
    return str(Path(vault) / "state" / "memory-index" / "hook.log")


def _log(vault, msg):
    try:
        from datetime import datetime
        lp = log_path(vault)
        os.makedirs(os.path.dirname(lp), exist_ok=True)
        with open(lp, "a") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')} {msg}\n")
    except Exception:
        pass


def pattern_from_grep(command):
    """Extract the search pattern from a grep/rg command. None = not a content grep."""
    # take the last pipe segment that runs grep/rg (e.g. after `| grep`)
    for seg in reversed(re.split(r"[|;]|&&", command)):
        try:
            toks = shlex.split(seg.strip())
        except ValueError:
            toks = seg.strip().split()
        if not toks:
            continue
        base = toks[0].rsplit("/", 1)[-1]
        if base not in ("grep", "egrep", "fgrep", "rg", "ack"):
            continue
        # first non-flag token AFTER grep = the pattern (for grep it comes before files)
        args = toks[1:]
        i = 0
        while i < len(args):
            a = args[i]
            if a == "--":
                i += 1
                break
            if a.startswith("-"):
                # flags that take a value (-e PATTERN, -m N, --include=…)
                if a in ("-e", "-m", "--include", "--exclude", "-A", "-B", "-C"):
                    if a == "-e" and i + 1 < len(args):
                        return args[i + 1]
                    i += 2
                    continue
                i += 1
                continue
            return a
        if i < len(args):
            return args[i]
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    vault = resolve_vault(payload)
    tool = payload.get("tool_name", "")
    cwd = payload.get("cwd", "")
    tin = payload.get("tool_input", {}) or {}

    if tool == "Grep":                      # in case of an env with a Grep tool
        scope = tin.get("path") or cwd
        pattern = (tin.get("pattern") or "").strip()
    elif tool == "Bash":                    # the real path in this environment
        scope = cwd
        cmd = tin.get("command", "") or ""
        pattern = (pattern_from_grep(cmd) or "").strip()
    else:
        return

    if not str(scope).startswith(vault):
        return
    if not pattern:
        return

    q = "".join(ch if ch.isalnum() or ch in " _-" else " " for ch in pattern).strip()
    if len(q) < MIN_PATTERN:
        return
    aid = payload.get("agent_id")   # present ONLY if the hook fired inside a subagent
    _log(vault, f"fired[{tool}]{'[agent '+aid+']' if aid else '[main]'} q={q[:60]!r}")

    try:
        with urllib.request.urlopen(
                f"{SERVER}/search?q={urllib.parse.quote(q)}&k={TOP_K}",
                timeout=0.8) as r:
            body = r.read().decode()
    except Exception:
        try:
            subprocess.Popen([resolve_python(vault), engine_path(vault), "serve"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True)
        except Exception:
            pass
        _log(vault, "server cold → spawned, skipped this call")
        return

    lines, keep = body.splitlines(), []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln[:1].isdigit() and "[" in ln:
            try:
                score = float(ln.split("[", 1)[1].split("]", 1)[0])
            except Exception:
                score = 0.0
            if score >= MIN_SCORE:
                keep.append(ln)
                j = i + 1
                while j < len(lines) and lines[j].startswith("     "):
                    keep.append(lines[j]); j += 1
        i += 1
    if not keep:
        _log(vault, "no hits above threshold")
        return
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                "Semantic memory (node index, for this search):\n"
                + "\n".join(keep)
            ),
        }
    }))
    _log(vault, f"emitted {len([k for k in keep if k[:1].isdigit()])} hits")


if __name__ == "__main__":
    main()
