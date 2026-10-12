#!/usr/bin/env python3
"""Vault sensors: four read-only checks on the state of the vault.

  1. SIZE        - files over the size limit, with a cut plan by section.
  2. INDEXES     - IDs found in the entry files (`context/learned.md`,
                   `context/anti-patterns.md`) that no line of the curated index
                   (`*-index.md`) resolves; counters hardcoded in an index header.
                   A range such as `L-001..L-007` covers every ID inside it; the
                   archive `context/anti-patterns-archive.md` is optional.
  3. CANDIDATES  - entries in `context/skill-candidates.md` marked "ready for gate" in
                   the heading that lack "Verified by" or "What didn't work".
  4. SKILLS      - `.claude/skills/*/SKILL.md` and `modules/*/SKILL.md`: frontmatter
                   present, name = directory name, description present and <= 1024
                   chars, file <= 500 lines.
  (3-4: a skill is written down only when it says what verified it and what did not work.)

The line these sensors do not cross: they report, they never act. A curated index is
human judgment (clusters, recurrence chains, the watch-list); a generator does not
reproduce it, and generating it destroys the curation and bloats boot. Cutting a big
file is a human call too: a byte limit cannot tell dense useful text from bloat.
Candidates and skills are not edited - the sensors only name what is wrong.

Usage:
    python3 scripts/vault_sensors.py [--ids]
        --ids   full lists (uncovered IDs, candidates and skills with remarks);
                by default the first 15 of each

Exit code is 0 whatever is found. Standard library only; writes nothing, sends nothing.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIPPED = []  # checks that could not run (a file is missing): the closing line must not say "clean" then


def read(p):
    return Path(p).read_text(encoding="utf-8", errors="ignore")


# (label, file with the entries, curated index file(s), ID prefix). The anti-pattern index
# may have an archive companion (notes moved out of boot); every index file is optional,
# but at least one must exist for the pair to be checked.
PAIRS = [
    ("lessons", "context/learned.md", ("context/learned-index.md",), "L"),
    ("anti-patterns", "context/anti-patterns.md",
     ("context/anti-patterns-index.md", "context/anti-patterns-archive.md"), "AP"),
]


def ids(files, prefix, ranges=False):
    """Every `PREFIX-NNN` mentioned in the given files that exist; None if none exists.
    ranges=True also expands "L-001..L-007" into each ID between the ends: that is how an
    index lists a whole theme or cluster in one line."""
    out = None
    one = re.compile(rf"\b{prefix}-\d{{3,4}}\b")
    # "L-001..L-007", "L-001..007", "L-001...L-007", "L-001…L-007"; with a dash only when
    # both ends carry the prefix ("L-001 - L-007"), so "L-012 - 2026" is not a range.
    span = re.compile(rf"\b{prefix}-(\d{{3,4}})(?:\s*(?:\.\.\.?|…)\s*(?:{prefix}-)?|\s*[–—-]\s*{prefix}-)(\d{{3,4}})\b")
    for name in files:
        p = ROOT / name
        if not p.is_file():
            continue
        text = read(p)
        found = set(one.findall(text))
        if ranges:
            for m in span.finditer(text):
                lo, hi, width = int(m.group(1)), int(m.group(2)), len(m.group(1))
                if lo <= hi < lo + 1000:
                    found.update(f"{prefix}-{n:0{width}d}" for n in range(lo, hi + 1))
        out = (out or set()) | found
    return out


def header_claims(path):
    """Counters hardcoded in an index header (first 15 lines): they go stale."""
    p = ROOT / path
    if not p.is_file():
        return []
    # Quote lines (`> ...`) are skipped: they explain WHY counters should not be there and
    # quote old wrong numbers as examples. A sensor that fires on its own documentation
    # is useless.
    lines = [ln for ln in read(p).split("\n")[:15] if not ln.lstrip().startswith(">")]
    head = "\n".join(lines)
    out = []
    m = re.search(r"(\d+)\s+unique\s+(?:AP|L)-ID", head)
    if m:
        out.append(("claimed unique IDs", int(m.group(1))))
    m = re.search(r"max\s+((?:AP|L)-\d{3,4})", head)
    if m:
        out.append(("claimed max", m.group(1)))
    m = re.search(r"\((?:AP|L)-\d{3,4}\.\.((?:AP|L)-\d{3,4})\)", head)
    if m:
        out.append(("claimed range up to", m.group(1)))
    return out


# The limit is a guideline, not a law: legitimate dense notes exist. 40 KB is about where a
# file stops being readable in one pass. Watched: the files the agent loads at boot.
SIZE_LIMIT = 40 * 1024
WATCHED = ["context/*.md", "state/current.md", "MEMORY.md", "CLAUDE.md"]


def sensor_size():
    """Files over the limit + a cut plan by top-level (##) section."""
    seen, over = set(), []
    for pat in WATCHED:
        for p in sorted(ROOT.glob(pat)):
            if p in seen or not p.is_file():
                continue
            seen.add(p)
            sz = p.stat().st_size
            if sz > SIZE_LIMIT:
                over.append((p, sz))
    if not over:
        print(f"── size: no files over the {SIZE_LIMIT // 1024} KB limit\n")
        return 0
    print(f"── size  ⚠  (limit {SIZE_LIMIT // 1024} KB)")
    for p, sz in sorted(over, key=lambda x: -x[1]):
        rel = p.relative_to(ROOT)
        # top-level sections -> a ready cut plan (bytes, like the file size above)
        secs = []
        cur, cnt = None, 0
        for ln in read(p).split("\n"):
            if re.match(r"^##\s+\S", ln):
                if cur:
                    secs.append((cur, cnt))
                cur, cnt = ln[3:].strip()[:44], 0
            cnt += len(ln.encode("utf-8")) + 1
        if cur:
            secs.append((cur, cnt))
        print(f"   {sz/1024:7.0f} KB  {rel}   x{sz/SIZE_LIMIT:.1f} of the limit, sections: {len(secs)}")
        for name, c in sorted(secs, key=lambda x: -x[1])[:3]:
            print(f"            └ {c/1024:5.0f} KB  \"{name}\"")
    print("   verdict: split along section boundaries, do not trim the tail.\n")
    return len(over)


# ── sensors 3-4: skill candidates and skill formatting ─────────────────────────
CAND_FILE = "context/skill-candidates.md"
CAND_FIELDS = (("Verified by", r"Verified\s+by"), ("What didn't work", r"What\s+didn['’]t\s+work"))
# Readiness is marked in the HEADING of the entry: "### CAND-017 - ... · status: candidate
# - ready for gate". The two fields are mandatory only for marked entries: a raw candidate
# must not carry them yet.
READY_RE = re.compile(r"ready\s+(?:for|to)\s+(?:the\s+)?(?:gate|promot\w*)|gate[-\s]ready", re.I)
DONE_RE = re.compile(r"status:\s*(?:promoted|rejected)", re.I)  # gate already passed or closed

SKILL_TREES = [".claude/skills", "modules"]  # installed skills + modules (installed by /enable-modules)
DESC_MAX, SKILL_LINES_MAX = 1024, 500


def cut(items, show_all):
    """First 15 (all with --ids) + a tail "... and N more"."""
    if show_all or len(items) <= 15:
        return items, ""
    return items[:15], f"   … and {len(items) - 15} more"


def cand_entries(text):
    """Candidate entries: [(heading, line number, [body lines])].
    An entry = a ## or ### heading with the word CAND; it ends at the next heading of level 1-3.
    The content of ``` blocks is skipped: the format template itself starts with "### CAND-NNN"."""
    out, cur, fence = [], None, False
    for no, ln in enumerate(text.split("\n"), 1):
        if ln.lstrip().startswith(("```", "~~~")):
            fence = not fence
        elif not fence and re.match(r"#{1,3}\s", ln):
            cur = (ln, no, []) if re.match(r"#{2,3}\s+CAND\b", ln) else None
            if cur:
                out.append(cur)
            continue
        if cur:
            cur[2].append(ln)
    return out


def field_filled(body, label_re):
    """The field "label:" is in the entry body and something is written in it: not empty and
    not the template's "{...}". The value is on the same line or on the indented lines right below."""
    pat = re.compile(r"(?:^|[\s(;—])" + label_re + r"\s*:(.*)$", re.I)
    for i, ln in enumerate(body):
        m = pat.search(ln.replace("*", "").replace("`", ""))
        if not m:
            continue
        val, j = m.group(1), i + 1
        while not val.strip() and j < len(body) and body[j].startswith((" ", "\t")):
            val, j = val + body[j], j + 1
        if re.search(r"\w", re.sub(r"\{[^}]*\}", "", val)):
            return True
    return False


def sensor_candidates(show_all):
    """Candidates marked "ready for gate" that lack a mandatory field."""
    p = ROOT / CAND_FILE
    if not p.is_file():
        print("── candidates: file not found, skipped\n")
        SKIPPED.append("candidates")
        return 0
    ready, bad = 0, []
    for head, no, body in cand_entries(read(p)):
        if not READY_RE.search(head) or DONE_RE.search(head):
            continue
        ready += 1
        miss = [name for name, rx in CAND_FIELDS if not field_filled(body, rx)]
        if miss:
            bad.append((head, no, miss))
    if not bad:
        what = (f"{ready} marked \"ready for gate\", all have \"Verified by\" and \"What didn't work\""
                if ready else "none marked \"ready for gate\"")
        print(f"── candidates: {what}\n")
        return 0
    print(f"── candidates  ⚠  (marked \"ready for gate\": {ready}, missing a mandatory field: {len(bad)})")
    shown, tail = cut(bad, show_all)
    for head, no, miss in shown:
        m = re.match(r"#+\s+(CAND(?:-\d+)?)\s*[—–:·-]*\s*(.*)", head)
        cid, title = (m.group(1), re.split(r"\s+[·(]", m.group(2))[0][:80]) if m else ("CAND", head[:80])
        print(f"   {cid:8}  line {no}: missing " + ", ".join(f"\"{f}\"" for f in miss))
        print(f"             {title}")
    if tail:
        print(tail)
    print("   verdict: do not bring to the gate until both fields are filled (format: top of the "
          "file); the sensor does not edit the entry.\n")
    return len(bad)


def fm_scalar(first, cont):
    """A frontmatter value -> a string, the way YAML would read it (scalars only)."""
    if first[:1] in (">", "|"):                   # block scalar: strip the common indent
        ind = min((len(c) - len(c.lstrip()) for c in cont if c.strip()), default=0)
        rows = [c[ind:].rstrip() for c in cont]
        if first[0] == "|":
            return "\n".join(rows).strip()
        paras = "\n".join(rows).strip().split("\n\n")  # '>' - lines are joined with a space
        return "\n".join(" ".join(p.split("\n")) for p in paras)
    s = " ".join(x for x in [first] + [c.strip() for c in cont] if x)
    m = re.match(r'"((?:[^"\\]|\\.)*)"', s)
    if m:                                         # "...": escapes as in JSON; exotic ones (\e, \x) not handled
        try:
            return json.loads('"' + m.group(1) + '"')
        except ValueError:
            return m.group(1)
    m = re.match(r"'((?:[^']|'')*)'", s)
    if m:
        return m.group(1).replace("''", "'")
    return re.sub(r"(?:^|\s+)#.*$", "", s).strip()  # plain: " # comment" is not part of the value


def parse_frontmatter(text):
    """Frontmatter without PyYAML (the sensors live on the stdlib): ({key: string}, None) or
    (None, reason). Reads scalars: plain (also multi-line), '...', "...", block > and |.
    Lists and nesting stay raw text - enough for name and description."""
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].rstrip() != "---":
        return None, "no frontmatter"
    end = next((i for i in range(1, len(lines)) if lines[i].rstrip() == "---"), None)
    if end is None:
        return None, "frontmatter not closed"
    groups = []                                   # [key, value on the key's line, [continuation lines]]
    for ln in lines[1:end]:
        m = re.match(r"([A-Za-z_][\w.-]*)\s*:(?:\s+(.*))?$", ln)
        if m:
            groups.append([m.group(1), (m.group(2) or "").strip(), []])
        elif groups and not ln.startswith("#"):
            groups[-1][2].append(ln)
    return {k: fm_scalar(v, cont) for k, v, cont in groups}, None


def module_skill_names():
    """`skill:` names declared in modules.yaml. A module's SKILL.md is installed under that name
    (usually the same as the module folder), so it may be the valid `name` of the file."""
    p = ROOT / "modules.yaml"
    return set(re.findall(r"^\s*skill:\s*['\"]?([\w.-]+)", read(p), re.M)) if p.is_file() else set()


def skill_problems(dirname, text, also_ok=()):
    """What is wrong in one SKILL.md's formatting -> a list of remarks (empty = fine)."""
    out = []
    fm, why = parse_frontmatter(text)
    if fm is None:
        out.append(why)
    else:
        name, desc = fm.get("name", ""), fm.get("description", "")
        if not name:
            out.append("no name")
        elif name != dirname and name not in also_ok:
            out.append(f"name \"{name}\" != directory \"{dirname}\"")
        if not desc:
            out.append("no description")
        elif len(desc) > DESC_MAX:
            out.append(f"description {len(desc)} chars > {DESC_MAX}")
    n = len(text.splitlines())
    if n > SKILL_LINES_MAX:
        out.append(f"{n} lines > {SKILL_LINES_MAX}")
    return out


def skill_dir_verdict(name, files):
    """A directory WITHOUT SKILL.md -> None (not a skill, skip) or what is wrong with it.
    files = {name: text} for the top-level *.md. Not a skill: a name starting with "_" or "."
    (archive, hidden) and a directory with no .md that has frontmatter name+description (data,
    assets, reference). If such an .md exists (skill.md, Skill.md) it is a skill with a wrong file
    name: macOS ignores case and would load it, a case-sensitive filesystem (Linux) would not."""
    if name[:1] in "_.":
        return None
    for fn, text in sorted(files.items()):
        fm, _ = parse_frontmatter(text)
        if fm and fm.get("name") and fm.get("description"):
            return f"no SKILL.md, but {fn} has name+description - the skill will not load on Linux"
    return None


def sensor_skills(show_all):
    """Skill formatting: frontmatter, name = directory, description <= 1024 chars, file <= 500 lines."""
    seen, bad, skipped = {}, [], []
    for tree in SKILL_TREES:
        base = ROOT / tree
        if not base.is_dir():
            continue
        also_ok = module_skill_names() if tree == "modules" else ()
        for d in sorted(x for x in base.iterdir() if x.is_dir()):
            if "SKILL.md" in os.listdir(d):       # exact name: macOS would find skill.md as well
                seen[tree] = seen.get(tree, 0) + 1
                probs = skill_problems(d.name, read(d / "SKILL.md"), also_ok)
                if probs:
                    bad.append((f"{tree}/{d.name}/SKILL.md", probs))
                continue
            why = skill_dir_verdict(d.name, {f.name: read(f) for f in d.glob("*.md")})
            if why:
                bad.append((f"{tree}/{d.name}/", [why]))
            else:
                skipped.append(f"{tree}/{d.name}")
    if not seen and not bad:
        print("── skills: no directories with SKILL.md found, skipped\n")
        SKIPPED.append("skills")
        return 0
    total, parts = sum(seen.values()), " + ".join(f"{t} {n}" for t, n in seen.items())
    note = f" · skipped directories without SKILL.md (not skills): {len(skipped)}" if skipped else ""
    if not bad:
        print(f"── skills: {total} SKILL.md ({parts}) - frontmatter, name = directory, "
              f"description <= {DESC_MAX} chars, <= {SKILL_LINES_MAX} lines: OK{note}\n")
        return 0
    print(f"── skills  ⚠  (checked {total} SKILL.md{': ' + parts if parts else ''}; "
          f"with remarks: {len(bad)}{note})")
    shown, tail = cut(bad, show_all)
    for path, probs in shown:
        print(f"   {path}: " + " · ".join(probs))
    if tail:
        print(tail)
    print("   verdict: the skill's owner fixes it; the sensor does not.\n")
    return len(bad)


def main():
    ap = argparse.ArgumentParser(
        prog="vault_sensors.py",
        description="Read-only vault sensors: size, index coverage, skill candidates, skill formatting. "
                    "Details are in the header of the file.")
    ap.add_argument("--ids", action="store_true",
                    help="full lists (uncovered IDs, candidates, skills) instead of the first 15")
    show_all = ap.parse_args().ids
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # an old console codepage must not crash the report

    problems = sensor_size()
    for label, body_p, idx_p, prefix in PAIRS:
        body = ids((body_p,), prefix)
        idx = ids(idx_p, prefix, ranges=True)
        if body is None or idx is None:
            print(f"── {label}: file not found, skipped\n")
            SKIPPED.append(label)
            continue
        missing = sorted(body - idx)
        real_max = max(body, key=lambda x: int(x.split("-")[1])) if body else "-"
        cov = 100 * len(body & idx) // len(body) if body else 0
        flag = "" if not missing else "  ⚠"
        print(f"── {label}{flag}")
        print(f"   IDs in body: {len(body)}, max {real_max}   ·   covered by the index: {len(body & idx)} ({cov}%)")
        for claim, claimed in header_claims(idx_p[0]):
            actual = len(body) if "unique" in claim else real_max
            ok = str(claimed) == str(actual)
            print(f"   header: {claim} = {claimed}   ·   actual {actual}   {'matches' if ok else '⚠ MISMATCH'}")
            if not ok:
                problems += 1
        if missing:
            problems += 1
            shown, tail = cut(missing, show_all)
            print(f"   not resolved by any line of the index ({len(missing)}):")
            print(f"   {' '.join(shown)}{'  ' + tail.strip() if tail else ''}")
        print()
    problems += sensor_candidates(show_all)
    problems += sensor_skills(show_all)
    if problems:
        print(f"signals: {problems}. All of it is a manual work queue: indexes are curated by a person, "
              f"big files are cut along their sections, candidate fields and skill formatting are filled "
              f"in by hand. The sensors do not fix, they show.")
    elif SKIPPED:
        print(f"no signals from the checks that ran (skipped, file not found: {', '.join(SKIPPED)}).")
    else:
        print("clean: indexes match, no files over the limit, candidates and skills are in order.")


if __name__ == "__main__":
    main()
