#!/bin/bash
# SessionEnd hook — one line per session in today's daily note: "- [HH:MM] <first real message>".
#
# Lives INSIDE the folder (.claude/hooks) so it travels with it. Registered in .claude/settings.json.
# The line = the person's first substantive message of the session: not a slash command, not a
# harness caveat / notification / tool result, not a bare "continue"; collapsed to one line,
# cut at a word boundary near 80 characters. Nothing is written when:
#   - this session already has its line (session ids in state/.session_end_logged, gitignored —
#     a resumed or re-ended session does not log twice);
#   - the thread's first message is older than 36 h (a resume of an old thread — its line exists);
#   - the whole session is one short probe (a single message under 30 characters; CJK counts x3);
#   - the line would carry a password, code, key or card number (rules/secrets-never-in-notes.md);
#   - there is no python3 — then this hook simply does not exist.
# A missing daily note is created from _templates/daily_template.md; the line is appended under a
# "## Sessions" heading at the end — append-only, like every other writer of daily/.
# Fault-tolerant: prints nothing, always exits 0 — a hook must never spoil the end of a session.

INPUT=$(cat 2>/dev/null || true)
command -v python3 >/dev/null 2>&1 || exit 0
WS="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." 2>/dev/null && pwd)}"
[ -d "$WS" ] || exit 0

HOOK_INPUT="$INPUT" python3 - "$WS" <<'PY' >/dev/null 2>&1
import datetime, json, os, re, sys

ws = sys.argv[1]
try:
    payload = json.loads(os.environ.get("HOOK_INPUT") or "{}")
except Exception:
    sys.exit(0)
transcript = payload.get("transcript_path") or ""
if not os.path.isfile(transcript):
    sys.exit(0)
sid = str(payload.get("session_id") or os.path.splitext(os.path.basename(transcript))[0])
mark = os.path.join(ws, "state", ".session_end_logged")
try:
    with open(mark, encoding="utf-8") as f:
        logged = f.read().split()
except OSError:
    logged = []
if sid in logged:
    sys.exit(0)

# Not the person's words: harness tags, notices, commands, skill bodies, compaction summaries.
SKIP = ("<", "[", "/", "Caveat:", "This session is being continued", "Base directory for this skill",
        "# /", "Command:", "command-", '@"')
CONTINUE = re.compile(r"^(?:please\s+)?(?:continue|go on)\b|^продолж(?:ай|и)\b|^继续", re.I)


def text_of(m):
    c = (m.get("message") or {}).get("content", "")
    if isinstance(c, str):
        return c.strip()
    if isinstance(c, list):
        for b in c:
            if isinstance(b, dict) and b.get("type") == "text":
                return (b.get("text") or "").strip()
    return ""


def weight(s):
    """Length with a CJK character counted as 3 (as in prompt-recall.py): a short Chinese
    sentence is a real request, not a probe."""
    return len(s) + 2 * sum(1 for ch in s if "\u3040" <= ch <= "\u9fff" or "\uac00" <= ch <= "\ud7af")


first, first_ts, n = None, None, 0
with open(transcript, encoding="utf-8", errors="replace") as f:
    for line in f:
        if '"user"' not in line:          # cheap pre-filter: only user entries get parsed
            continue
        try:
            m = json.loads(line)
        except Exception:
            continue
        if m.get("type") != "user" or m.get("isMeta") or m.get("isSidechain"):
            continue
        t = text_of(m)
        if not t or t.startswith(SKIP) or CONTINUE.match(t):
            continue
        n += 1
        if first is None:
            first, first_ts = " ".join(t.split()), m.get("timestamp")
        else:
            break                           # two real messages = not a probe; enough to know
if first is None:
    sys.exit(0)
if first_ts:
    try:
        ts = datetime.datetime.fromisoformat(first_ts.replace("Z", "+00:00"))
        if (datetime.datetime.now(datetime.timezone.utc) - ts).total_seconds() > 36 * 3600:
            sys.exit(0)                     # resume of an old thread — its line was written then
    except Exception:
        pass
if n == 1 and weight(first) < 30:
    sys.exit(0)                             # a lone short probe
topic = first if len(first) <= 80 else first[:80].rsplit(" ", 1)[0] + "…"   # no half-words

# The person's passwords and codes never land in their files (rules/secrets-never-in-notes.md).
SECRET_WORDS = re.compile(
    r"pass(?:word|wd|phrase|code)|\bpin\b|\bcvv\b|\bcvc\b|api[ _-]?key|secret[ _-]?key|private[ _-]?key"
    r"|\btokens?\b|seed[ _-]?phrase|mnemonic|one[- ]time code|\b2fa\b|card number|passport"
    r"|парол|пин[- ]?код|\bпин\b|токен|сид[- ]?фраз|мнемони|смс[- ]?код|код из смс|код подтвержд"
    r"|номер карты|паспорт|ключ(?:ом|и|а)? (?:api|апи|доступа|от кошелька)"
    r"|密码|口令|验证码|密钥|私钥|助记词|卡号|身份证|护照", re.I)
KEY_PREFIX = re.compile(r"(?:sk|pk|rk|ghp|gho|ghs|glpat|github_pat|xox[abprs])[-_][A-Za-z0-9]|AKIA[0-9A-Z]{12}|AIza[0-9A-Za-z_-]{20}")


def looks_secret(s):
    if SECRET_WORDS.search(s) or re.search(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)", s):
        return True                         # a keyword, or a card-like run of digits
    for tok in re.findall(r"[A-Za-z0-9_\-+=]{20,}", s):   # long opaque runs: keys, tokens, hashes
        core = tok.strip("_-")
        mixed = any(c.islower() for c in core) and any(c.isupper() for c in core) and any(c.isdigit() for c in core)
        if mixed or re.fullmatch(r"[0-9a-fA-F]{32,}", core) or KEY_PREFIX.match(core):
            return True
    return False


if looks_secret(topic):
    sys.exit(0)

now = datetime.datetime.now()
day = now.strftime("%Y-%m-%d")
daily = os.path.join(ws, "daily", day + ".md")


def from_template():
    """Today's note from the folder's own template ({{date:FORMAT}}, {{date}}, {{time}}, {{title}})."""
    try:
        with open(os.path.join(ws, "_templates", "daily_template.md"), encoding="utf-8") as f:
            t = f.read()
    except OSError:
        t = "---\ntype: daily\ntags: [daily]\nupdated: {{date:YYYY-MM-DD}}\n---\n\n# {{date:YYYY-MM-DD}} — {{date:dddd}}\n"
    fmt = {"YYYY": "%Y", "MM": "%m", "DD": "%d", "dddd": "%A", "ddd": "%a", "HH": "%H", "mm": "%M"}

    def date_spec(m):
        spec = m.group(1) or "YYYY-MM-DD"
        return now.strftime(re.sub(r"YYYY|dddd|ddd|MM|DD|HH|mm", lambda x: fmt[x.group(0)], spec))

    t = re.sub(r"\{\{date(?::([^}]*))?\}\}", date_spec, t)
    return t.replace("{{time}}", now.strftime("%H:%M")).replace("{{title}}", day)


os.makedirs(os.path.dirname(daily), exist_ok=True)
try:
    with open(daily, encoding="utf-8", errors="replace") as f:
        text, fresh = f.read(), ""
except OSError:
    text = fresh = from_template()
heads = [l.rstrip() for l in text.splitlines() if l.startswith("## ")]
chunk = "\n" if text and not text.endswith("\n") else ""
if not heads or heads[-1] != "## Sessions":
    chunk += "\n## Sessions\n"
chunk += f"- [{now.strftime('%H:%M')}] {topic}\n"
with open(daily, "a", encoding="utf-8") as f:
    f.write(fresh + chunk)

logged.append(sid)
os.makedirs(os.path.dirname(mark), exist_ok=True)
with open(mark, "w", encoding="utf-8") as f:
    f.write("\n".join(logged[-500:]) + "\n")
PY
exit 0
