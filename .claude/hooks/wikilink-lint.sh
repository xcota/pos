#!/usr/bin/env bash
# PreToolUse hook: validate [[wikilinks]] in knowledge/ writes.
# Delegates to python3 for robust JSON + regex handling.
# Path-agnostic: the python resolves its own dir from BASH_SOURCE, no absolute path.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$HERE/wikilink-lint.py"
