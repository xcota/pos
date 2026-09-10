#!/usr/bin/env python3
"""Проверка цитат в карточке сферы.

Каждая строка карточки, которая начинается с «ты сказал:» или «вы сказали:»
(обращение — то же, каким идёт разговор), должна дословно находиться в рассказах
человека (папка stories/ рядом с карточкой). Если цитаты там нет — строка не факт,
а моё предположение: скрипт печатает её номер и переписывает её в
«я услышал: … — так?».

Поправки человека тоже должны лежать в stories/ (например stories/popravki.md) —
иначе его же свежая поправка не найдётся и уедет обратно в вопрос.

Запуск:
    python3 scripts/check_quotes.py memory/svoboda/{id}/domains/delo.md
    python3 scripts/check_quotes.py <карточка> --dry-run      # только показать
    python3 scripts/check_quotes.py <карточка> --stories <папка>

Коды выхода: 0 — все цитаты нашлись; 1 — были непроверенные строки (они
помечены); 2 — карточку или рассказы не удалось прочитать, либо в карточке нет
ни одной строки-цитаты (проверять нечего — показывать такую карточку нельзя).

Только стандартная библиотека. Ничего никуда не отправляет.
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

QUOTE_MARKS = '«»""„“”\'"'
SAID_RE = re.compile(
    r"^(\s*(?:\d+[.)]\s*)?)(ты сказал(?:а)?|вы сказали)\s*:\s*(.+?)\s*$",
    re.IGNORECASE,
)
QUOTED_RE = re.compile(r"[«\"„](.+?)[»\"“”]", re.DOTALL)


def normalize(text: str) -> str:
    """Сравниваем без регистра, пунктуации, ё и лишних пробелов."""
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
    """Что именно проверять в строке «ты сказал: …»."""
    match = SAID_RE.match(line)
    if not match:
        return []
    payload = match.group(3)
    quoted = [q for q in QUOTED_RE.findall(payload) if normalize(q)]
    if quoted:
        return quoted
    # кавычек нет — проверяем всю строку, отрезав пометку канала в скобках
    payload = re.sub(r"\((?:[^()]*)\)\s*$", "", payload).strip()
    return [payload] if normalize(payload) else []


def rewrite(line: str) -> str:
    """Строка становится вопросом. Ссылку на рассказ отрезаем — цитаты там нет."""
    match = SAID_RE.match(line)
    prefix, payload = match.group(1), match.group(3)
    quoted = QUOTED_RE.findall(payload)
    if quoted:
        payload = " ".join(f"«{q.strip()}»" for q in quoted)
    payload = payload.rstrip()
    if payload.endswith("?"):
        return f"{prefix}я услышал: {payload}"
    return f"{prefix}я услышал: {payload} — так?"


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверить цитаты в карточке сферы")
    parser.add_argument("card", help="файл карточки")
    parser.add_argument("--stories", help="папка с рассказами (по умолчанию — рядом с карточкой)")
    parser.add_argument("--dry-run", action="store_true", help="не править файл, только показать")
    args = parser.parse_args()

    card = Path(args.card)
    if not card.is_file():
        print(f"нет карточки: {card}")
        return 2

    stories_dir = find_stories_dir(card, args.stories)
    if stories_dir is None:
        print("не нашёл папку stories/ с рассказами — проверять не по чему")
        return 2

    corpus = load_stories(stories_dir)
    if not corpus:
        print(f"в {stories_dir} пусто — проверять не по чему")
        return 2

    lines = card.read_text(encoding="utf-8").splitlines()
    total = sum(1 for line in lines if claims(line))
    if not total:
        print(
            "в карточке нет ни одной строки «ты сказал» / «вы сказали» — проверять нечего; "
            "либо цитат нет, либо они написаны другими словами. Карточку не показывать."
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
        print(f"цитаты сходятся: {total} из {total} (рассказы: {stories_dir})")
        return 0

    for number, original, missing in bad:
        print(f"строка {number}: в рассказах нет — {missing[0].strip()}")
        print(f"  было:  {original}")
        print(f"  стало: {lines[number - 1].strip()}")
    if not args.dry_run:
        card.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"помечено строк: {len(bad)}. Карточка поправлена — показывать можно после чистого прогона.")
    else:
        print(f"помечено бы строк: {len(bad)} (--dry-run, файл не тронут)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
