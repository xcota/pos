#!/usr/bin/env python3
"""Quote check for a domain card.

Every card line that starts with a "you said" label — `you said:` in English,
`你说：` in Chinese, `ты сказал(а):` / `вы сказали:` in Russian (the form of
address is the one the conversation uses) — must be found word for word in the
person's stories (the `stories/` folder next to the card). If the quote isn't
there, the line is not a fact but my own assumption: the script prints its number
and rewrites it as "I heard: … — right?" in the same language.

The person's corrections must also live in stories/ (for example
stories/corrections.md) — otherwise their own fresh correction is not found and
travels straight back into a question.

Usage:
    python3 scripts/check_quotes.py memory/svoboda/{id}/domains/delo.md
    python3 scripts/check_quotes.py <card> --dry-run      # show only
    python3 scripts/check_quotes.py <card> --stories <folder>

Exit codes: 0 — every quote checked out; 1 — there were unverified lines (they
are now flagged); 2 — the card or the stories could not be read, or the card has
no quote line at all (nothing to check — such a card must not be shown).

Standard library only. Sends nothing anywhere.
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

# "you said" in the three card-label languages (see the label table in
# .claude/skills/start/SKILL.md). Add a language here and the check follows.
SAID_RE = re.compile(
    r"^(\s*(?:\d+[.)]\s*)?)(you said|你说|ты сказал(?:а)?|вы сказали)\s*[:：]\s*(.+?)\s*$",
    re.IGNORECASE,
)
HEARD = {
    "en": ("I heard: {payload}", "I heard: {payload} — right?"),
    "zh": ("我听到的是：{payload}", "我听到的是：{payload}——对吗？"),
    "ru": ("я услышал: {payload}", "я услышал: {payload} — так?"),
}
QUOTED_RE = re.compile(r"[«\"„「『](.+?)[»\"“”」』]", re.DOTALL)


def label_language(label: str) -> str:
    """Which language's label set this line was written in."""
    low = label.lower()
    if low.startswith("you said"):
        return "en"
    if label.startswith("你说"):
        return "zh"
    return "ru"


def normalize(text: str) -> str:
    """Compare without case, punctuation, Russian ё, or extra spaces."""
    text = unicodedata.normalize("NFKC", text).lower().replace("ё", "е")
    text = "".join(ch if ch.isalnum() else " " for ch in text)
    return " ".join(text.split())


def find_stories_dir(card: Path, override: str | None) -> Path | None:
    if override:
        path = Path(override)
        return path if path.is_dir() else None
    here = card.resolve().parent
    for candidate in [here, *here.parents][:4]:
        stories = candidate / "stories"
        if stories.is_dir():
            return stories
    return None


def load_stories(stories: Path) -> str:
    chunks = []
    for path in sorted(stories.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".txt", ""}:
            try:
                chunks.append(path.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                continue
    return normalize("\n".join(chunks))


def claims(line: str) -> list[str]:
    """What exactly to check in a "you said: …" line."""
    match = SAID_RE.match(line)
    if not match:
        return []
    payload = match.group(3)
    quoted = [q for q in QUOTED_RE.findall(payload) if normalize(q)]
    if quoted:
        return quoted
    # no quotation marks — check the whole line, minus a trailing source marker
    payload = re.sub(r"\((?:[^()]*)\)\s*$", "", payload).strip()
    return [payload] if normalize(payload) else []


def rewrite(line: str) -> str:
    """The line becomes a question. The story reference is cut — the quote isn't there."""
    match = SAID_RE.match(line)
    prefix, payload = match.group(1), match.group(3)
    lang = label_language(match.group(2))
    quoted = QUOTED_RE.findall(payload)
    if quoted:
        marks = ("「", "」") if lang == "zh" else ("«", "»")
        payload = " ".join(f"{marks[0]}{q.strip()}{marks[1]}" for q in quoted)
    payload = payload.rstrip()
    plain, question = HEARD[lang]
    if payload.endswith(("?", "？")):
        return prefix + plain.format(payload=payload)
    return prefix + question.format(payload=payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the quotes in a domain card")
    parser.add_argument("card", help="the card file")
    parser.add_argument("--stories", help="folder with the stories (default: next to the card)")
    parser.add_argument("--dry-run", action="store_true", help="don't edit the file, only show")
    args = parser.parse_args()

    card = Path(args.card)
    if not card.is_file():
        print(f"no such card: {card}")
        return 2

    stories_dir = find_stories_dir(card, args.stories)
    if stories_dir is None:
        print("couldn't find a stories/ folder with the stories — nothing to check against")
        return 2

    corpus = load_stories(stories_dir)
    if not corpus:
        print(f"{stories_dir} is empty — nothing to check against")
        return 2

    lines = card.read_text(encoding="utf-8").splitlines()
    total = sum(1 for line in lines if claims(line))
    if not total:
        print(
            "the card has no \"you said\" line in any of the label languages — nothing to check; "
            "either there are no quotes, or they are written in other words. Do not show this card."
        )
        return 2

    bad = []
    for i, line in enumerate(lines):
        parts = claims(line)
        if not parts:
            continue
        missing = [p for p in parts if normalize(p) not in corpus]
        if missing:
            bad.append((i + 1, line.strip(), missing))
            lines[i] = rewrite(line)

    if not bad:
        print(f"quotes check out: {total} of {total} (stories: {stories_dir})")
        return 0

    for number, original, missing in bad:
        print(f"line {number}: not in the stories — {missing[0].strip()}")
        print(f"  was:  {original}")
        print(f"  now:  {lines[number - 1].strip()}")
    if not args.dry_run:
        card.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"lines flagged: {len(bad)}. Card corrected — it may be shown after a clean run.")
    else:
        print(f"lines that would be flagged: {len(bad)} (--dry-run, file untouched)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
