#!/usr/bin/env python3
"""session_usage.py: usage counter over Claude Code transcripts. READ-ONLY.

Use it to measure a change (a hook, the boot, a rule) as numbers before/after instead of by
eye. Source: <config>/projects/<this folder>/*.jsonl (main sessions) and, with --agents,
<session>/subagents/**/agent-*.jsonl (subagents and workflow agents). Standard library only,
nothing leaves the machine. Message text is read only to classify turns; only numbers and
ids are printed.

The line this script does not cross: it measures, it draws no conclusions. The runaway
threshold (RUNAWAY) and the list of service tags are constants at the top; change them there.

Which folder. Claude Code keeps a project's transcripts in <config>/projects/<slug>/, where
<config> is $CLAUDE_CONFIG_DIR or ~/.claude, and <slug> is the project's absolute path with
EVERY character outside [A-Za-z0-9] replaced by "-": slashes, dots, spaces, underscores,
hyphens, accented and non-Latin letters alike. Example: /path/to/my.vault_1 becomes
-path-to-my-vault-1; a hidden folder shows as a double dash (/a/.b -> -a--b). A path
whose slug passes 200 characters is cut there and gets a "-<hash>" suffix; this script finds
such a folder by its 200-character prefix. The rule was read from Claude Code's own code and
checked against real directories. If transcripts live somewhere else, pass --dir.

How it is counted (found on real files, not from documentation):
  answers = UNIQUE message.id. One model answer is written as several lines (one per block:
            thinking / text / tool_use) with the same usage, and after a compaction the tail
            of the history is sometimes written again (usage=0). Per id the maximum of each
            usage field is taken. Summing per line overstates usage 2.7-3.4 times; summed per
            id, sessions without subagents and forks matched the app's own cost counter to
            the token (both measured on the transcripts this was built against, 2026-10).
            Stub answers (model=<synthetic>: API errors) are not counted.
  human   = human replies. Not counted: tool results, isMeta, the compaction summary,
            task-notification, peer/plugin messages, local-command/bash output,
            "[Request interrupted...]". Counted: plain text, a slash-command prompt
            (<command-message>), a reply typed while the agent was working (queued_command
            / prompt). Duplicates of one record (by uuid) collapse.
  tools   = unique tool_use.id. Calls made before the first human reply are in the total
            but not in "max" and "15+" (there is nothing for them to belong to).
  max     = the most tool calls after a single human reply; 15+ = the number of human
            replies followed by >= 15 calls ("agent runaway"). Notifications from background
            agents do not start a reply: their calls count for the last human reply.
  compact = compact_boundary records (by uuid).
  cache%  = cache_read / (input + cache_read + cache_creation).

Forks and resumes. When a session is resumed or forked, the app starts a NEW file with a copy
of the whole history (uuids kept), so one message lives in several files and a sum over files
counts it twice (about 10% of messages in the transcripts this was built against). A message
is credited to the ancestor file (the one whose activity ended earlier; on a tie, the one
created earlier); in the descendant it goes to the "inherit" column and is not in the usage.
The total over all files equals the real usage without duplicates. Files with no model
answers of their own (pure copies) are left out of the table; their number is printed at the
bottom. --keep-inherited switches the subtraction off (each session as it is, the total is
overstated).

Subagents (--agents): under each session a separate row "└ agents xN" with the same numbers
over its transcripts (they have no human replies: "—"); at the bottom three totals:
sessions / agents / all. In usage, subagents are not smaller than the main session (in cache
tokens, and much more in the number of answers), so without --agents the picture is
incomplete. There are no duplicates between subagent files (checked), so the fork logic is
not applied to them.

What the transcripts do not contain (accuracy limits, data of 2026-10):
  - the app's own service requests (a small model: titles, classifiers): their usage is not
    written to the file. So input here is noticeably below the app's counter;
    cache_read/cache_create on the checked sessions without forks agree with it within 4%.
  - for unfinished answers (stop_reason empty in every line) output is a stream stub. In
    main sessions these are a fraction of a percent, in subagents about 15% of answers, and
    their output is understated (a lower bound). The number of such answers is printed at the
    bottom and is in the JSON (unfinished_replies).

Usage:  python3 scripts/session_usage.py                    # last 10 sessions + total
        python3 scripts/session_usage.py --last 5 --agents
        python3 scripts/session_usage.py --since 2026-10-05  # everything since this date
        python3 scripts/session_usage.py --since 2026-09-20 --until 2026-10-05 --json > before.json
        python3 scripts/session_usage.py --session 1a2b3c4d --agents
        --last N        the last N sessions by the end of their own activity
                        (default 10; with --since/--until/--session there is no limit)
        --since/--until a window over the time of the RECORDS, not the file date (a long
                        session is cut by day). Dates are local time; --until does not
                        include its date, so "before" and "after" one date do not overlap
        --agents        add subagents (a row under the session + three totals)
        --json          machine output for before/after comparison
        --keep-inherited  do not subtract the history inherited from forks
        --dir PATH      another transcripts directory (default: this folder's project)
"""
import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RUNAWAY = 15  # a reply with >= 15 tool calls after it = "agent runaway"
SLUG_MAX = 200  # Claude Code cuts a longer slug here and appends "-<hash>"
EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)
TOKENS = ("input", "output", "cache_read", "cache_creation")

# Line prefilter: JSON is parsed only for records of the needed types (the files hold many
# large tool_result entries and snapshots that the count does not need).
LINE_MAIN = re.compile(r'"type"\s*:\s*"(?:assistant|user|system|queued_command)"')
LINE_AGENT = re.compile(r'"type"\s*:\s*"assistant"')
TAG = re.compile(r"^\s*<([A-Za-z][A-Za-z0-9_-]{0,40})[\s>/]")
# Service insertions sit in user records but are not a human reply.
# Not in the list, so counted as a reply: command-message (slash prompt), pasted_content.
SERVICE_TAGS = {
    "local-command-caveat", "local-command-stdout", "local-command-stderr",
    "command-name",  # local commands (/model, /compact...): always preceded by a caveat
    "bash-input", "bash-stdout", "bash-stderr",
    "task-notification", "system-reminder", "cross-session-message",
}


def slug(path):
    """The folder name Claude Code gives a project: every character outside [A-Za-z0-9] -> "-",
    one dash per UTF-16 unit as in its JavaScript (so an emoji gives two)."""
    return "".join(c if c.isascii() and c.isalnum() else "-" * (len(c.encode("utf-16-le", "surrogatepass")) // 2)
                   for c in str(path))


def default_dir():
    cfg = os.environ.get("CLAUDE_CONFIG_DIR")
    projects = (Path(cfg).expanduser() if cfg else Path.home() / ".claude") / "projects"
    s = slug(ROOT)
    if len(s) > SLUG_MAX:  # the folder is "<first 200>-<hash>": find it by its prefix
        hits = sorted(projects.glob(s[:SLUG_MAX] + "-*"))
        if len(hits) == 1:
            return hits[0]
    return projects / s


# ───────────────────────── reading a transcript ─────────────────────────

def parse_ts(s):
    if not isinstance(s, str):
        return None
    try:
        d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def num(x):
    return int(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else 0


def usage_tuple(u):
    if not isinstance(u, dict):
        return (0, 0, 0, 0)
    return (num(u.get("input_tokens")), num(u.get("output_tokens")),
            num(u.get("cache_read_input_tokens")), num(u.get("cache_creation_input_tokens")))


def lead_tag(text):
    m = TAG.match(text) if isinstance(text, str) else None
    return m.group(1) if m else None


def human_origin(o):
    k = o.get("kind") if isinstance(o, dict) else o
    return k in (None, "human")  # None = old records without the origin field


def is_human_user(r):
    """A user record typed by a person (not a tool_result and not a service insertion)."""
    if r.get("isMeta") or r.get("isCompactSummary") or r.get("isVisibleInTranscriptOnly"):
        return False
    if not human_origin(r.get("origin")) or r.get("turnOrigin") not in (None, "human"):
        return False
    msg = r.get("message")
    c = msg.get("content") if isinstance(msg, dict) else None
    if isinstance(c, str):
        return bool(c.strip()) and lead_tag(c) not in SERVICE_TAGS
    if isinstance(c, list):
        blocks = [b for b in c if isinstance(b, dict)]
        if not blocks or any(b.get("type") == "tool_result" for b in blocks):
            return False
        texts = [b.get("text") or "" for b in blocks if b.get("type") == "text"]
        if not any(b.get("type") in ("image", "document") for b in blocks):
            if not texts or all(t.lstrip().startswith("[Request interrupted") for t in texts):
                return False
        return lead_tag(texts[0] if texts else None) not in SERVICE_TAGS
    return False


def is_human_queued(a):
    """A human reply typed while the agent was working (arrives as a queued_command attachment)."""
    p = a.get("prompt")
    return (a.get("commandMode") == "prompt" and not a.get("isMeta") and human_origin(a.get("origin"))
            and isinstance(p, str) and bool(p.strip()) and lead_tag(p) not in SERVICE_TAGS)


class Msg:
    """A model answer: the maximum of each usage field over all lines with this message.id."""
    __slots__ = ("model", "u", "tools", "done")

    def __init__(self, model, u):
        self.model, self.u, self.tools, self.done = model, list(u), set(), False

    def merge(self, u):
        for i in range(4):
            if u[i] > self.u[i]:
                self.u[i] = u[i]


class Scan:
    """One file. events, in order of first appearance:
       ("a", ts, mid) answer · ("t", ts, mid, tool_id) call · ("h", ts, uuid) human reply · ("c", ts, uuid) compaction."""
    __slots__ = ("msgs", "events", "last", "birth", "bad")

    def __init__(self):
        self.msgs, self.events, self.last, self.birth, self.bad = {}, [], None, 0.0, 0


def scan_file(path, agent=False):
    sc = Scan()
    rx = LINE_AGENT if agent else LINE_MAIN
    seen = set()  # uuids of replies/compactions: after a compaction the tail of the history is written again
    prev = None
    try:
        st = os.stat(path)
        sc.birth = getattr(st, "st_birthtime", st.st_mtime)
        f = open(path, encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"! could not read {path}: {e}", file=sys.stderr)
        return sc
    with f:
        for line in f:
            if not rx.search(line):
                continue
            try:
                r = json.loads(line)
            except ValueError:
                sc.bad += 1  # an unfinished last line of a live session is normal
                continue
            if not isinstance(r, dict):
                continue
            t = r.get("type")
            ts = parse_ts(r.get("timestamp")) or prev or EPOCH
            prev = ts
            kind = None
            if t == "assistant":
                m = r.get("message")
                if not isinstance(m, dict):
                    continue
                model, mid = m.get("model"), m.get("id")
                if not mid or not model or model == "<synthetic>":
                    continue
                u = usage_tuple(m.get("usage"))
                cur = sc.msgs.get(mid)
                if cur is None:
                    cur = sc.msgs[mid] = Msg(model, u)
                    sc.events.append(("a", ts, mid))
                    if sc.last is None or ts > sc.last:
                        sc.last = ts
                else:
                    cur.merge(u)
                if m.get("stop_reason"):
                    cur.done = True  # the final usage is written; for unfinished answers output is a stream stub
                c = m.get("content")
                if isinstance(c, list):
                    for b in c:
                        if isinstance(b, dict) and b.get("type") == "tool_use":
                            tid = b.get("id")
                            if tid and tid not in cur.tools:
                                cur.tools.add(tid)
                                sc.events.append(("t", ts, mid, tid))
                continue
            if agent:
                continue
            if t == "user" and is_human_user(r):
                kind = "h"
            elif t == "system" and r.get("subtype") == "compact_boundary":
                kind = "c"
            elif t == "attachment":
                a = r.get("attachment")
                if isinstance(a, dict) and a.get("type") == "queued_command" and is_human_queued(a):
                    kind = "h"
            if kind:
                uid = r.get("uuid")
                if uid and uid in seen:
                    continue
                seen.add(uid)
                sc.events.append((kind, ts, uid))
                if sc.last is None or ts > sc.last:
                    sc.last = ts
    return sc


# ───────────────────────── ownership across forks ─────────────────────────

def assign_owners(scans):
    """message.id and uuid -> the id of the owning session (see "Forks and resumes" in the header).
    An answer: first where the usage is recorded (a copy with usage=0 does not take someone
    else's), then the ancestor. Replies and compactions: the ancestor."""
    rank = {sid: (sc.last or EPOCH, sc.birth, sid) for sid, sc in scans.items()}
    own_msg, own_uid = {}, {}
    for sid, sc in scans.items():
        for mid, m in sc.msgs.items():
            key = (-sum(m.u), rank[sid])
            if mid not in own_msg or key < own_msg[mid][0]:
                own_msg[mid] = (key, sid)
        for ev in sc.events:
            if ev[0] in ("h", "c") and ev[2]:
                key = rank[sid]
                if ev[2] not in own_uid or key < own_uid[ev[2]][0]:
                    own_uid[ev[2]] = (key, sid)
    return ({k: v[1] for k, v in own_msg.items()}, {k: v[1] for k, v in own_uid.items()})


# ───────────────────────── counting ─────────────────────────

def blank():
    return {"start": None, "end": None, "models": Counter(), "human": 0, "replies": 0, "tools": 0,
            "max_tools": 0, "runaway": 0, "compactions": 0, "inherited": 0, "unfinished": 0,
            "tokens": dict.fromkeys(TOKENS, 0)}


def touch(d, ts):
    if d["start"] is None or ts < d["start"]:
        d["start"] = ts
    if d["end"] is None or ts > d["end"]:
        d["end"] = ts


def in_window(ts, lo, hi):
    return (lo is None or ts >= lo) and (hi is None or ts < hi)


def summarize(sid, sc, own_msg, own_uid, lo, hi, keep):
    d = blank()
    tools, turns = set(), [0]  # turns[0] - calls before the first human reply; turns[1:] - per reply
    for ev in sc.events:
        k, ts = ev[0], ev[1]
        if not in_window(ts, lo, hi):
            continue
        if k == "a":
            m = sc.msgs[ev[2]]
            if not keep and own_msg.get(ev[2], sid) != sid:
                d["inherited"] += 1
                continue
            d["replies"] += 1
            d["unfinished"] += not m.done
            d["models"][m.model] += 1
            for name, v in zip(TOKENS, m.u):
                d["tokens"][name] += v
            touch(d, ts)
        elif k == "t":
            if (not keep and own_msg.get(ev[2], sid) != sid) or ev[3] in tools:
                continue
            tools.add(ev[3])
            turns[-1] += 1
        else:  # "h" / "c"
            if not keep and ev[2] and own_uid.get(ev[2], sid) != sid:
                continue
            touch(d, ts)
            if k == "h":
                d["human"] += 1
                turns.append(0)
            else:
                d["compactions"] += 1
    d["tools"] = len(tools)
    d["max_tools"] = max(turns[1:], default=0)
    d["runaway"] = sum(1 for x in turns[1:] if x >= RUNAWAY)
    return d


def summarize_agents(sess_dir, lo, hi):
    """A session's subagents: unique message.id over all its agent-*.jsonl."""
    files = sorted(Path(sess_dir, "subagents").rglob("agent-*.jsonl")) if Path(sess_dir).is_dir() else []
    d = blank()
    d["files"] = 0
    msgs, tools, bad = {}, set(), 0
    for p in files:
        sc = scan_file(p, agent=True)
        bad += sc.bad
        active = False
        for ev in sc.events:
            if not in_window(ev[1], lo, hi):
                continue
            if ev[0] == "a":
                m = sc.msgs[ev[2]]
                if ev[2] in msgs:
                    msgs[ev[2]].merge(m.u)
                    continue
                msgs[ev[2]] = m
                d["models"][m.model] += 1
                touch(d, ev[1])
                active = True
            elif ev[3] not in tools:
                tools.add(ev[3])
        d["files"] += active
    for m in msgs.values():
        d["unfinished"] += not m.done
        for name, v in zip(TOKENS, m.u):
            d["tokens"][name] += v
    d["replies"], d["tools"] = len(msgs), len(tools)
    return d, bad


def add_into(total, d):
    total["models"].update(d["models"])
    for k in ("human", "replies", "tools", "runaway", "compactions", "inherited", "unfinished"):
        total[k] += d[k]
    for k in TOKENS:
        total["tokens"][k] += d["tokens"][k]
    total["max_tools"] = max(total["max_tools"], d["max_tools"])
    if d["start"] is not None:
        touch(total, d["start"])
        touch(total, d["end"])
    if "files" in d:
        total["files"] = total.get("files", 0) + d["files"]


def cache_share(t):
    den = t["input"] + t["cache_read"] + t["cache_creation"]
    return t["cache_read"] / den if den else None


# ───────────────────────── output ─────────────────────────

def fmt_n(n):
    if n < 10_000:
        return str(n)
    if n < 1_000_000:
        return f"{n / 1e3:.1f}k"
    if n < 1_000_000_000:
        return f"{n / 1e6:.1f}M"
    return f"{n / 1e9:.2f}B"


def short_model(m):
    return m[7:] if m.startswith("claude-") else m


def fmt_models(c, width=16):
    names = [short_model(m) for m, _ in c.most_common()]
    if not names:
        return "—"
    s = names[0]
    for i, n in enumerate(names[1:], 1):
        if len(s) + 1 + len(n) > width:
            return f"{s} +{len(names) - i}"
        s += "," + n
    return s


def fmt_dt(d):
    return d.astimezone().strftime("%Y-%m-%d %H:%M") if d else "—"


def iso(d):
    return d.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if d else None


def cells(label, d, human_cols=True):
    sh = cache_share(d["tokens"])
    dash = "—"
    return [label, fmt_dt(d["start"]), fmt_dt(d["end"]), fmt_models(d["models"]),
            str(d["human"]) if human_cols else dash, str(d["replies"]), str(d["tools"]),
            str(d["max_tools"]) if human_cols else dash, str(d["runaway"]) if human_cols else dash,
            str(d["compactions"]) if human_cols else dash, str(d["inherited"]) if human_cols else dash,
            fmt_n(d["tokens"]["input"]), fmt_n(d["tokens"]["output"]),
            fmt_n(d["tokens"]["cache_read"]), fmt_n(d["tokens"]["cache_creation"]),
            f"{sh * 100:.1f}" if sh is not None else dash]


HEAD = ["session", "start", "end", "models", "human", "answers", "tools", "max", "15+", "compact", "inherit",
        "input", "output", "cache_read", "cache_create", "cache%"]
LEFT = {0, 1, 2, 3}


def print_table(rows, sep_before):
    w = [max(len(HEAD[i]), *(len(r[i]) for r in rows)) for i in range(len(HEAD))]

    def line(r):
        return "  ".join(r[i].ljust(w[i]) if i in LEFT else r[i].rjust(w[i]) for i in range(len(r))).rstrip()

    print(line(HEAD))
    print("  ".join("─" * x for x in w))
    for n, r in enumerate(rows):
        if n in sep_before:
            print("  ".join("─" * x for x in w))
        print(line(r))


def to_json_block(d, with_human=True):
    out = {"start": iso(d["start"]), "end": iso(d["end"]),
           "models": dict(d["models"].most_common()),
           "model_replies": d["replies"], "tool_calls": d["tools"],
           "unfinished_replies": d["unfinished"],
           "tokens": dict(d["tokens"]), "cache_share": None}
    sh = cache_share(d["tokens"])
    out["cache_share"] = round(sh, 4) if sh is not None else None
    if with_human:
        out.update(human_replies=d["human"], max_tools_per_reply=d["max_tools"],
                   runaway_replies=d["runaway"], compactions=d["compactions"],
                   inherited_replies=d["inherited"])
    if "files" in d:
        out["agent_files"] = d["files"]
    return out


# ───────────────────────── main ─────────────────────────

def parse_date(s, ap):
    try:
        return datetime.strptime(s, "%Y-%m-%d").astimezone()  # midnight, local time
    except ValueError:
        ap.error(f"date must be YYYY-MM-DD, got: {s}")


def main():
    ap = argparse.ArgumentParser(prog="session_usage.py", add_help=True,
                                 description="Usage over Claude Code transcripts (read-only). "
                                             "Details are in the header of the file.")
    ap.add_argument("--last", type=int, metavar="N", help="the last N sessions (default 10)")
    ap.add_argument("--since", metavar="YYYY-MM-DD", help="only records from this date (local time)")
    ap.add_argument("--until", metavar="YYYY-MM-DD", help="only records BEFORE this date (not including it)")
    ap.add_argument("--session", metavar="PREFIX", help="a session by id prefix (several may match)")
    ap.add_argument("--agents", action="store_true", help="add subagents: a row under each session + totals")
    ap.add_argument("--json", action="store_true", help="machine output (JSON) instead of the table")
    ap.add_argument("--keep-inherited", action="store_true",
                    help="do not subtract the history inherited from forks (the total is overstated)")
    ap.add_argument("--dir", metavar="PATH", help="transcripts directory (default: this folder's project)")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # an old console codepage must not crash the report

    lo = parse_date(args.since, ap) if args.since else None
    hi = parse_date(args.until, ap) if args.until else None
    if args.last is not None and args.last < 1:
        ap.error("--last: need a number >= 1")
    base = Path(args.dir).expanduser() if args.dir else default_dir()
    if not base.is_dir():
        print(f"no transcripts directory: {base}\n"
              f"(Claude Code keeps a folder's sessions in a directory named after its path; "
              f"pass --dir if yours is elsewhere)", file=sys.stderr)
        return 2

    scans = {p.stem: scan_file(p) for p in sorted(base.glob("*.jsonl")) if p.stat().st_size}
    own_msg, own_uid = ({}, {}) if args.keep_inherited else assign_owners(scans)

    rows, hidden = [], [0, 0]  # hidden: files, human replies in them
    for sid, sc in scans.items():
        if args.session and not sid.startswith(args.session):
            continue
        d = summarize(sid, sc, own_msg, own_uid, lo, hi, args.keep_inherited)
        if d["start"] is None:
            continue
        if not d["replies"] and not args.session:  # a fork copy: nothing was spent in it
            hidden[0] += 1
            hidden[1] += d["human"]
            continue
        rows.append((sid, d))
    limit = args.last if args.last is not None else (None if (lo or hi or args.session) else 10)
    rows.sort(key=lambda x: x[1]["end"])
    if limit:
        rows = rows[-limit:]
    if not rows:
        print("no sessions match these conditions", file=sys.stderr)
        return 1

    bad = sum(sc.bad for sc in scans.values())
    tot = blank()
    tot_ag = blank()
    tot_ag["files"] = 0
    for sid, d in rows:
        if args.agents:
            d["agents"], b = summarize_agents(base / sid, lo, hi)
            bad += b
            add_into(tot_ag, d["agents"])
        add_into(tot, d)

    if args.json:
        res = {"dir": str(base), "generated": iso(datetime.now(timezone.utc)),
               "filters": {"last": limit, "since": args.since, "until": args.until, "session": args.session,
                           "agents": args.agents, "keep_inherited": args.keep_inherited, "runaway_threshold": RUNAWAY},
               "notes": {"hidden_files_without_replies": hidden[0], "hidden_human_replies": hidden[1],
                         "unreadable_json_lines": bad},
               "sessions": [], "total": to_json_block(tot)}
        for sid, d in rows:
            j = {"id": sid, "id8": sid[:8]}
            j.update(to_json_block(d))
            if args.agents:
                j["agents"] = to_json_block(d["agents"], with_human=False)
            res["sessions"].append(j)
        if args.agents:
            res["total_agents"] = to_json_block(tot_ag, with_human=False)
            allt = blank()
            add_into(allt, tot)
            add_into(allt, tot_ag)
            res["total_all"] = to_json_block(allt, with_human=False)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0

    table, seps = [], set()
    for sid, d in rows:
        table.append(cells(sid[:8], d))
        if args.agents and d["agents"]["replies"]:
            a = d["agents"]
            table.append(cells(f"  └ agents x{a['files']}", a, human_cols=False))
    seps.add(len(table))
    table.append(cells("TOTAL" if not args.agents else "TOTAL sessions", tot))
    if args.agents:
        table.append(cells("TOTAL agents", tot_ag, human_cols=False))
        allt = blank()
        add_into(allt, tot)
        add_into(allt, tot_ag)
        table.append(cells("TOTAL all", allt))
    span = f"{fmt_dt(tot['start'])} → {fmt_dt(tot['end'])}"
    print(f"session_usage · {base.name} · sessions {len(rows)} · {span}\n")
    print_table(table, seps)
    print()
    print(f"human — human replies · answers — model answers (unique message.id) · tools — tool calls · "
          f"max — most tool calls after one human reply · 15+ — human replies followed by >={RUNAWAY} calls · "
          f"compact — compactions")
    print("inherit — answers inherited from an ancestor (fork/resume), not counted in the usage · "
          "cache% = cache_read / (input + cache_read + cache_create)")
    notes = []
    if hidden[0]:
        notes.append(f"not shown: {hidden[0]} files without model answers of their own "
                     f"(fork copies; human replies in them: {hidden[1]})")
    if tot["unfinished"] or tot_ag["unfinished"]:
        parts = [f"sessions {tot['unfinished']}"] + ([f"agents {tot_ag['unfinished']}"] if args.agents else [])
        notes.append("answers without a final usage (their output is understated): " + ", ".join(parts))
    if bad:
        notes.append(f"unreadable JSON lines: {bad}")
    if args.keep_inherited:
        notes.append("--keep-inherited: forks counted together with the inherited history, the total is overstated")
    if notes:
        print("· " + " · ".join(notes))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # `| head` closed the pipe: not an error
        sys.exit(0)
