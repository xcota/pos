#!/usr/bin/env bash
# PreToolUse hook: validate [[wikilinks]] in knowledge/ writes.
# Delegates to python3 for robust JSON + regex handling.
# Path-agnostic: the python resolves its own dir from BASH_SOURCE, no absolute path.
#
# No python3 on this machine? Then this check simply does not exist: consume the
# payload, exit 0, say nothing. A missing optional checker must never surface as
# an error on the user's screen, and must never block a write.
command -v python3 >/dev/null 2>&1 || { cat >/dev/null 2>&1; exit 0; }
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$HERE/wikilink-lint.py"
