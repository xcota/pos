#!/usr/bin/env python3
"""
PreToolUse hook for Claude Code.

Validates [[wikilinks]] in any Write/Edit that targets <vault>/knowledge/**/*.md.

Rules:
  - [[folder/file]]   -> BLOCK (path-style)
  - [[file.md]]       -> BLOCK (extension)
  - [[nonexistent]]   -> BLOCK (target missing)
  - the same file blocked twice in a row -> warn once, then let the write through
  - [[name|alias]]    -> check `name` only
  - Inside ``` fences ``` or `inline code` -> skipped

Path-agnostic: the knowledge root is resolved from the write target itself
(the nearest `knowledge/` ancestor of the file being written), falling back to
$CLAUDE_PROJECT_DIR / two-levels-up from this hook. No hardcoded absolute path.

On any parsing failure: exit 0 (fail-open).
"""

import json
import os
import re
import sys
from pathlib import Path

# Two levels up from this file: .claude/hooks/<this> → vault root.
_SELF_ROOT = Path(__file__).resolve().parent.parent.parent


def fail_open(_msg=""):
    sys.exit(0)


def knowledge_root_for(file_path: str) -> str | None:
    """Return the knowledge/ root the target lives under, or None if not in one."""
    p = Path(file_path).resolve()
    for parent in p.parents:
        if parent.name == "knowledge":
            return str(parent)
    # Fallbacks: env-provided project dir, then relative-to-self.
    for base in (os.environ.get("CLAUDE_PROJECT_DIR"), str(_SELF_ROOT)):
        if base:
            kr = Path(base) / "knowledge"
            if kr.is_dir():
                try:
                    p.relative_to(kr)
                    return str(kr)
                except ValueError:
                    pass
    return None


def strip_code(text: str) -> str:
    """Remove fenced code blocks and inline code so their contents are ignored."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def load_existing_entities(knowledge_root: str) -> set:
    """Walk knowledge/ once and return set of basenames (without .md)."""
    names = set()
    for root, _dirs, files in os.walk(knowledge_root):
        for f in files:
            if f.endswith(".md"):
                names.add(f[:-3])
    return names


WIKILINK_RE = re.compile(r"\[\[([^\[\]\n]+?)\]\]")


def validate(content: str, existing: set) -> list:
    """Return list of error message strings (empty = ok)."""
    errors = []
    cleaned = strip_code(content)
    for m in WIKILINK_RE.finditer(cleaned):
        raw = m.group(1).strip()
        if not raw:
            continue
        target = raw.split("|", 1)[0].strip()
        target_no_anchor = target.split("#", 1)[0].strip()
        if not target_no_anchor:
            continue

        if "/" in target_no_anchor:
            errors.append(
                f"wikilink contains a path: [[{target}]] — use a plain name "
                f"[[{os.path.basename(target_no_anchor)}]] (no folders)"
            )
            continue

        if target_no_anchor.lower().endswith(".md"):
            stripped = target_no_anchor[:-3]
            errors.append(
                f"wikilink contains .md: [[{target}]] — use [[{stripped}]]"
            )
            continue

        if target_no_anchor not in existing:
            errors.append(
                f"wikilink does not exist: [[{target_no_anchor}]] — "
                f"create knowledge/.../{target_no_anchor}.md or remove the link"
            )
    return errors


MAX_BLOCKS = 2   # after this many blocks on the same file, warn and let the write through


def _attempts_file(knowledge_root: str) -> Path:
    """state/.lint-attempts.json next to the knowledge/ root (fallback: this repo)."""
    base = Path(knowledge_root).parent if knowledge_root else _SELF_ROOT
    return base / "state" / ".lint-attempts.json"


def _load_attempts(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def _save_attempts(path: Path, data: dict) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data))
    except Exception:
        pass


def bump_attempts(knowledge_root: str, file_path: str) -> int:
    """Count how many times in a row this file was blocked. Returns the new count."""
    ap = _attempts_file(knowledge_root)
    data = _load_attempts(ap)
    n = int(data.get(file_path, 0)) + 1
    data[file_path] = n
    _save_attempts(ap, data)
    return n


def clear_attempts(knowledge_root: str, file_path: str) -> None:
    ap = _attempts_file(knowledge_root)
    data = _load_attempts(ap)
    if data.pop(file_path, None) is not None:
        _save_attempts(ap, data)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        fail_open()

    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path") or ""

    if not file_path.endswith(".md"):
        sys.exit(0)

    knowledge_root = knowledge_root_for(file_path)
    if not knowledge_root:
        sys.exit(0)   # not a knowledge/ write — nothing to lint

    # Write -> content; Edit -> new_string; MultiEdit -> edits[].new_string
    chunks = []
    if "content" in tool_input and isinstance(tool_input["content"], str):
        chunks.append(tool_input["content"])
    if "new_string" in tool_input and isinstance(tool_input["new_string"], str):
        chunks.append(tool_input["new_string"])
    edits = tool_input.get("edits")
    if isinstance(edits, list):
        for e in edits:
            if isinstance(e, dict) and isinstance(e.get("new_string"), str):
                chunks.append(e["new_string"])

    if not chunks:
        sys.exit(0)

    try:
        existing = load_existing_entities(knowledge_root)
    except Exception:
        fail_open()

    all_errors = []
    for c in chunks:
        all_errors.extend(validate(c, existing))

    if not all_errors:
        clear_attempts(knowledge_root, file_path)
        sys.exit(0)

    seen = set()
    uniq = []
    for e in all_errors:
        if e not in seen:
            seen.add(e)
            uniq.append(e)

    tries = bump_attempts(knowledge_root, file_path)
    if tries > MAX_BLOCKS:
        # Two blocks were enough to say it. A third would start a repair loop in
        # front of the user — let the write through with a note instead.
        clear_attempts(knowledge_root, file_path)
        sys.stderr.write(
            "NOTE: wikilink lint still unhappy about " + file_path +
            " after " + str(MAX_BLOCKS) + " tries — writing anyway. "
            "Fix the links later, do NOT retry now.\n"
        )
        for e in uniq:
            sys.stderr.write("  - " + e + "\n")
        sys.exit(0)

    sys.stderr.write("BLOCK: wikilink lint failed for " + file_path + "\n")
    for e in uniq:
        sys.stderr.write("  - " + e + "\n")
    sys.stderr.write(
        "Rule: [[entity-name]] — plain filename, no paths, no .md, "
        "and the file must exist in knowledge/.\n"
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
