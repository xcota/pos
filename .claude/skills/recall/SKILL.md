---
name: recall
version: 2.0
user_invocable: true
description: Semantic search across the whole vault via the node-level embedding index.
---

# /recall — Semantic Memory Search

`/recall {query}` — top relevant nodes (file + section + snippet) from the node-level index.

## Mechanism
`scripts/memory_index.py` — EmbeddingGemma q8 ONNX, nodes chunked by header, one `.npz` sidecar (`state/memory-index/`), brute-force cosine. Zero DB, zero external APIs. A warm server on 127.0.0.1:8765 (lazy, 30 min TTL): the first query is ~7s, then ~65 ms. Architecture: `knowledge/concepts/memory-embedding-layer.md`.

**Setup (once):** the engine runs in a venv. If `search` errors with a missing module, run `bash scripts/memory_index_setup.sh`, then `.memory_venv/bin/python scripts/memory_index.py build` (use the venv python, NOT system `python3` — the deps live in the venv). First run downloads a ~309 MB model; build is seconds on a small vault, up to ~35 min on a large one.

## Steps
1. Run the search from the vault root:
   ```bash
   .memory_venv/bin/python scripts/memory_index.py search "$QUERY"
   ```
   (It knocks on the warm server itself; no server → a cold search + a lazy background spawn. If you named the venv differently, use that path — e.g. `bge_test_venv/bin/python`.)
2. Result format: `rank. [score] relpath` + `§ header-path` + snippet.
   Score ≥0.5 = usually an exact hit; 0.4–0.5 = eyeball it.
3. The result is a set of Read candidates, NOT the answer. Open the top 1–3 files and read the section.
4. No sensible results → rephrase the query (semantics prefer a question, not a keyword stub).
5. Do NOT synthesize — that's the caller's job.

## When to call
- Main thread doesn't remember context; "did we already discuss this?"
- A meaning-level question with no exact term (jargon, paraphrase)
- A subagent needs historical context

## When NOT to call
- Exact lookup of a known file → Read
- Exact term/name → Glob/grep (faster; semantics get appended by the hook if it's enabled)
