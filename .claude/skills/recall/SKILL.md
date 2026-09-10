---
name: recall
version: 2.1
user_invocable: true
description: Search the person's own notes — by meaning if the semantic index is installed, by exact words otherwise. Never fails in front of the person.
---

# /recall — поиск по записям человека

`/recall {query}` — найти его старую запись. Два режима, и переключение между ними
человек не настраивает: ты сам смотришь, что стоит.

## Шаг 0 — какой поиск здесь есть (ДЕЛАТЬ ПЕРВЫМ)

```bash
ls .memory_venv/bin/python state/memory-index/nodes.npz
```

(`ls` — из предразрешённых команд в `.claude/settings.json`, окна «разрешить?» человек не увидит.)

- Оба файла на месте → шаг 1 (поиск по смыслу).
- Хотя бы одного нет → **не запускай движок вообще** (человек увидит ошибку с путями).
  Ищи по точным словам и ответь результатом:

  ```bash
  grep -rin "$QUERY" knowledge/ daily/ memory/ inbox/ state/ reports/ 2>/dev/null | head -40
  ```

  Слово из запроса может не совпасть дословно — прогони 2–3 формы («усталость», «устал»,
  «разбит»), прежде чем сказать, что не нашлось.

  Человеку — одна плоская строка, один раз за разговор:
  > Поиск по смыслу здесь не стоит — ищу по точным словам. Захотите включить — скажите.

  Про venv, модель, гигабайты и установку человеку не пишем ни строки. Он спросил про
  поиск по смыслу сам → тогда можно предложить поставить (`bash scripts/bootstrap.sh`,
  разово ~300 МБ закачки) и только по его «да».
- Движок был, но упал (любая ошибка, пустой вывод) → молча уходи в ту же ветку `words`.
  Знакомство и разговор из-за поиска не останавливаются никогда.

## Mechanism
`scripts/memory_index.py` — EmbeddingGemma q8 ONNX, nodes chunked by header, one `.npz` sidecar (`state/memory-index/`), brute-force cosine. Zero DB, zero external APIs. A warm server on 127.0.0.1:8765 (lazy, 30 min TTL): the first query is ~7s, then ~65 ms. Architecture: `knowledge/concepts/memory-embedding-layer.md`.

Индексируются `knowledge/ daily/ context/ reports/ state/ memory/ inbox/ projects/` — то есть
и дословные рассказы человека (`memory/svoboda/{id}/stories/`), и то, что он кладёт в `inbox/`.

**Setup (once, только по просьбе человека):** движок живёт в venv. Ставится `bash scripts/bootstrap.sh`
(он же зовёт `scripts/memory_index_setup.sh` и собирает указатель). Разово качается модель ~309 МБ;
сборка — секунды на маленькой папке. Вручную: `.memory_venv/bin/python scripts/memory_index.py build`
(именно venv-питон, не системный `python3` — зависимости лежат в venv).

## Steps
1. Run the search from the vault root:
   ```bash
   .memory_venv/bin/python scripts/memory_index.py search "$QUERY"
   ```
   (It knocks on the warm server itself; no server → a cold search + a lazy background spawn.)
2. Result format: `rank. [score] relpath` + `§ header-path` + snippet.
   Score ≥0.5 = usually an exact hit; 0.4–0.5 = eyeball it.
3. The result is a set of Read candidates, NOT the answer. Open the top 1–3 files and read the section.
4. No sensible results → rephrase the query (semantics prefer a question, not a keyword stub),
   then fall back to the `words` branch of Step 0 before saying "не нашёл".
5. Do NOT synthesize — that's the caller's job.

## When to call
- Main thread doesn't remember context; "did we already discuss this?"
- A meaning-level question with no exact term (jargon, paraphrase)
- A subagent needs historical context

## When NOT to call
- Exact lookup of a known file → Read
- Exact term/name → Glob/grep (faster; semantics get appended by the hook if it's enabled)
