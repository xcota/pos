---
name: recall
version: 2.1
user_invocable: true
description: Search the person's own notes — by meaning if the semantic index is installed, by exact words otherwise. Never fails in front of the person.
---

# /recall — search the person's own notes

`/recall {query}` — find one of their old notes. Two modes, and the person never switches between
them: you check yourself what is installed.

## Step 0 — which search exists here (DO THIS FIRST)

```bash
ls .memory_venv/bin/python state/memory-index/nodes.npz
```

(`ls` is pre-allowed in `.claude/settings.json`, so the person sees no "allow this?" window.)

- Both files present → step 1 (search by meaning).
- Either one missing → **do not launch the engine at all** (the person would see an error full of
  paths). Search by exact words and answer with the result:

  ```bash
  grep -rin "$QUERY" knowledge/ daily/ memory/ inbox/ state/ reports/ 2>/dev/null | head -40
  ```

  A word from the query may not match literally — try 2–3 forms ("tired", "tiredness",
  "worn out") before saying nothing was found.

  To the person — one plain line, once per conversation, in their language:
  > Search by meaning isn't installed here — I'm searching by exact words. Say the word if you want
  > it on.

  Not one line to the person about venvs, models, gigabytes or installation. If they ask about
  search by meaning themselves → then you may offer to install it (`bash scripts/bootstrap.sh`,
  a one-off ~300 MB download) and only on their "yes".
- The engine was there but fell over (any error, empty output) → go quietly into the same `words`
  branch. Onboarding and the conversation never stop because of search.

## Mechanism
`scripts/memory_index.py` — EmbeddingGemma q8 ONNX, nodes chunked by header, one `.npz` sidecar (`state/memory-index/`), brute-force cosine. Zero DB, zero external APIs. A warm server on 127.0.0.1:8765 (lazy, 30 min TTL): the first query is ~7s, then ~65 ms. Architecture: `knowledge/concepts/memory-embedding-layer.md`.

Indexed: `knowledge/ daily/ context/ reports/ state/ memory/ inbox/ projects/` — which includes
the person's verbatim stories (`memory/svoboda/{id}/stories/`) and whatever they drop into `inbox/`.

**Setup (once, only when the person asks):** the engine lives in a venv. Installed by
`bash scripts/bootstrap.sh` (which calls `scripts/memory_index_setup.sh` and builds the index).
A ~309 MB model is downloaded once; the build takes seconds on a small folder. By hand:
`.memory_venv/bin/python scripts/memory_index.py build` (the venv python, not the system `python3`
— the dependencies live in the venv).

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
   then fall back to the `words` branch of Step 0 before saying "found nothing".
5. Do NOT synthesize — that's the caller's job.

## When to call
- Main thread doesn't remember context; "did we already discuss this?"
- A meaning-level question with no exact term (jargon, paraphrase)
- A subagent needs historical context

## When NOT to call
- Exact lookup of a known file → Read
- Exact term/name → Glob/grep (faster; semantics get appended by the hook if it's enabled)
