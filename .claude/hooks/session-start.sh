#!/bin/bash
# SessionStart hook — pours the folder's state into the assistant's context at every launch.
#
# Lives INSIDE the folder (.claude/hooks) so it travels with it. Registered in .claude/settings.json.
# Fault-tolerant by design: no `set -e`, no `pipefail`. A hook must never break a session —
# a failing section prints its reason and leaves the neighbours alone. Everything it prints is
# addressed to the assistant (English, the engine language); the assistant speaks to the person
# in the person's language and never shows them command names.
#
# Sections: State · Priorities · Today · Checkpoints · sensors (boot size, search-index drift) ·
# gates (💤 memory tidy-up = /dream, 🔍 reflection = /reflect).
# Before onboarding (context/identity.md still has {{ }} placeholders) it prints ONE line and exits.

# Drain the harness JSON on stdin, but never block (a manual run may have an open, empty stdin).
if [ ! -t 0 ] && read -t 0 -r _ 2>/dev/null; then cat >/dev/null 2>&1; fi

WS="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." 2>/dev/null && pwd)}"
[ -d "$WS" ] || exit 0
IDENTITY="$WS/context/identity.md"

# ─── Not set up yet → one line, nothing else ─────────────────────────────────
if [ ! -f "$IDENTITY" ] || grep -q '{{' "$IDENTITY" 2>/dev/null; then
    echo "--- Camomile: this folder is NOT set up yet (context/identity.md still has placeholders). If the person's first message is \"start\" or \"/start\", run the start skill (it also resumes an interrupted first session). Otherwise answer with ONE plain line, in their language: \"This folder isn't set up yet — just type /start and I'll do the rest.\" Never say \"vault\" to the person. ---"
    exit 0
fi

# ─── Session counter FIRST, before any printing (a failing section must not stop the count) ──
COUNTER="$WS/state/session_count_since_dream.txt"
mkdir -p "$WS/state" 2>/dev/null
COUNT=$(cat "$COUNTER" 2>/dev/null || echo 0)
case "$COUNT" in ''|*[!0-9]*) COUNT=0 ;; esac
COUNT=$((COUNT + 1))
echo "$COUNT" > "$COUNTER" 2>/dev/null || true

# ─── Helpers ────────────────────────────────────────────────────────────────
strip_frontmatter() {   # drop a leading --- ... --- block
    awk 'NR==1 && $0=="---" {fm=1; next} fm && $0=="---" {fm=0; next} !fm' "$1" 2>/dev/null
}
mtime() {               # file modification time, epoch seconds (mac / linux)
    stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null || echo 0
}
stamp_epoch() {         # read a stamp file: epoch digits, or an ISO date (python3 if present) → epoch; else 0
    local f="$1" s
    [ -f "$f" ] || { echo 0; return 0; }
    s=$(tr -d '[:space:]' < "$f" 2>/dev/null)
    case "$s" in
        '') echo 0 ;;
        *[!0-9]*)
            if command -v python3 >/dev/null 2>&1; then
                python3 - "$s" <<'PY' 2>/dev/null || echo 0
import datetime, sys
try:
    print(int(datetime.datetime.fromisoformat(sys.argv[1].replace("Z", "+00:00")).timestamp()))
except Exception:
    print(0)
PY
            else
                echo 0
            fi ;;
        *) echo "$s" ;;
    esac
}

# ─── Sections ───────────────────────────────────────────────────────────────
section_state() {
    local f="$WS/state/current.md" body
    echo "--- State ---"
    if [ ! -f "$f" ]; then echo "(no state/current.md yet — the first /session-save creates it)"; echo "---"; return 0; fi
    body=$(strip_frontmatter "$f" | grep -v '^[[:space:]]*$' | head -40 | cut -c1-400)
    if [ -n "$body" ]; then printf '%s\n' "$body"; else echo "(state/current.md is empty)"; fi
    echo "---"
}

section_priorities() {
    local f="$WS/context/priorities.md" body
    echo "--- Priorities ---"
    if [ ! -f "$f" ]; then echo "(no context/priorities.md)"; echo "---"; return 0; fi
    # first "## " section (any title — titles get renamed, a hard-coded one silently breaks)
    body=$(awk '/^## /{ if (flag) exit; flag=1; next } flag' "$f" 2>/dev/null | grep -v '^[[:space:]]*$' | head -8 | cut -c1-400)
    [ -z "$body" ] && body=$(strip_frontmatter "$f" | grep -v '^[[:space:]]*$' | head -8 | cut -c1-400)
    if [ -n "$body" ]; then printf '%s\n' "$body"; else echo "(context/priorities.md is empty)"; fi
    echo "---"
}

section_today() {
    local today daily
    today=$(date +%Y-%m-%d)
    daily="$WS/daily/$today.md"
    echo "--- Today ($today) ---"
    if [ ! -f "$daily" ]; then echo "(no daily note for today yet)"; echo "---"; return 0; fi
    tail -8 "$daily" 2>/dev/null | cut -c1-400 || echo "(could not read it)"
    echo "---"
}

section_checkpoints() {
    local d="$WS/state/sessions" list
    [ -d "$d" ] || return 0
    list=$(ls -t "$d" 2>/dev/null | grep '\.md$' | head -3 | sed 's/\.md$//' | tr '\n' ' ')
    [ -z "$list" ] && return 0
    echo "--- Checkpoints (state/sessions, newest first) ---"
    echo "$list"
    echo "---"
}

# Sensor: how far the search-by-meaning index lags behind git. Print only, never rebuilds.
section_index_drift() {
    local m="$WS/state/memory-index/manifest.json" head n
    [ -f "$m" ] || return 0
    head=$(sed -n 's/.*"git_head"[[:space:]]*:[[:space:]]*"\([0-9a-fA-F]*\)".*/\1/p' "$m" 2>/dev/null | head -1)
    [ -z "$head" ] && return 0
    n=$(git -C "$WS" rev-list --count "$head..HEAD" 2>/dev/null)
    case "$n" in ''|*[!0-9]*) return 0 ;; esac
    [ "$n" -gt 0 ] && echo "search index is $n commit(s) behind — /dream refreshes it"
    return 0
}

# Gate: memory tidy-up (/dream) — ≥24h since the last one AND ≥5 sessions since.
section_dream_gate() {
    local last now age
    last=$(stamp_epoch "$WS/state/last_dream.txt")
    case "$last" in ''|*[!0-9]*) last=0 ;; esac
    now=$(date +%s)
    if [ "$last" -gt 0 ]; then age=$(( (now - last) / 3600 )); else age=999; fi
    if [ "$age" -ge 24 ] && [ "$COUNT" -ge 5 ]; then
        echo "--- 💤 Memory tidy-up is due (${age}h since the last one, ${COUNT} sessions). Offer it to the person in ONE sentence, in their language (e.g. \"My memory needs a few minutes of tidying — do it now?\"); run /dream only on a yes. ---"
        return 0
    fi
    return 1
}

# Gate: reflection (/reflect) — ≥3 days since the last one (baseline: when the folder was set up).
section_reflect_gate() {
    local last now days
    last=$(stamp_epoch "$WS/state/last_reflect.txt")
    case "$last" in ''|*[!0-9]*) last=0 ;; esac
    [ "$last" -gt 0 ] || last=$(mtime "$IDENTITY")
    case "$last" in ''|*[!0-9]*) return 0 ;; esac
    now=$(date +%s)
    days=$(( (now - last) / 86400 ))
    if [ "$days" -ge 3 ]; then
        echo "--- 🔍 Reflection is due (${days} days since the last one). Offer it in ONE sentence (\"Shall I go over the misses of the last few days?\"); run /reflect only on a yes. ---"
    fi
    return 0
}

# ─── Assemble (into a variable, to measure its cost) ─────────────────────────
OUT=$(
    section_state
    section_priorities
    section_today
    section_checkpoints
)
printf '%s\n' "$OUT"

BYTES=$(printf '%s' "$OUT" | wc -c | tr -d ' ')
DRIFT=$(section_index_drift)
if [ -n "$DRIFT" ]; then echo "--- boot: ${BYTES} bytes · ${DRIFT} ---"; else echo "--- boot: ${BYTES} bytes ---"; fi

# One offer per start: tidy-up first; reflection only if no tidy-up was offered.
if ! section_dream_gate; then
    section_reflect_gate
fi
exit 0
