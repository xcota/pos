#!/bin/bash
# PostToolUse gate on Bash: cheaply lets everything through EXCEPT grep/rg commands.
# In this environment Claude Code has no Grep tool — search goes through `grep`/`rg`
# inside the Bash tool, so we weave semantics in here. Python only starts on a real grep.
#
# Path-agnostic: the hook dir is resolved from this script's own location, so the
# same wiring works from any clone regardless of where the vault lives.
INPUT=$(cat 2>/dev/null || true)
echo "$INPUT" | grep -qE '"command":.*\b(grep|egrep|fgrep|rg)\b' || exit 0
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "$INPUT" | python3 "$HERE/semantic-recall.py"
exit 0
