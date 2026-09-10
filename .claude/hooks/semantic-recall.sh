#!/bin/bash
# PostToolUse gate: cheaply lets everything through EXCEPT searches.
# Two search paths exist depending on the harness:
#   - a Grep tool call        → payload carries "tool_name":"Grep"
#   - grep/rg inside Bash     → payload carries the command line
# Both are forwarded; python only starts on a real search.
#
# Path-agnostic: the hook dir is resolved from this script's own location, so the
# same wiring works from any copy regardless of where the folder lives.
#
# No python3 on this machine? Swallow the payload and exit 0 — semantic memory is
# optional and its absence must never print anything to the user.
INPUT=$(cat 2>/dev/null || true)
command -v python3 >/dev/null 2>&1 || exit 0
if ! echo "$INPUT" | grep -qE '"tool_name"[[:space:]]*:[[:space:]]*"Grep"'; then
  echo "$INPUT" | grep -qE '"command":.*\b(grep|egrep|fgrep|rg)\b' || exit 0
fi
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "$INPUT" | python3 "$HERE/semantic-recall.py" 2>/dev/null
exit 0
