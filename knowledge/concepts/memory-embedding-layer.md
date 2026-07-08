---
type: concept
aliases: [recall, semantic-recall, embedding-layer, memory-index]
tags: [domain/meta, type/concept, memory, retrieval, embedding]
updated: YYYY-MM-DD
status: engine component (optional — the vault works without it; this adds semantic recall on top)
---
# Node-level Memory Embedding Layer (Path A)

Semantic search across the whole vault: **one `.npz` file of vectors + brute-force cosine**. It sits on top of the plain-Markdown graph — the graph is the memory; this is a rebuildable search cache over it. Every design decision below was measured, not chosen by taste.

## Where it sits in the memory stack

Four layers of memory, each with its own role:

| # | Layer | Role | Lives in |
|---|-------|------|----------|
| 1 | **Markdown graph in git** | the REAL memory, source of truth (one `.md` per entity, `[[wikilinks]]`) | `knowledge/ daily/ context/ reports/ state/ projects/` |
| 2 | **Agent auto-memory** | durable personal/feedback facts; only a thin index enters context | the agent's own memory store |
| 3 | **Embedding index (THIS layer)** | a derived search cache over layer 1. Disposable, rebuildable | `state/memory-index/nodes.npz` |
| 4 | **Session transcripts** | cold storage, recovery only | the agent's projects directory |

Key principle: layer 3 is **derived**. Losing or corrupting it = a ~35-min rebuild, zero lost data. The memory can't break; only the search cache can — and it's disposable.

## Why the layer helps (all measured on one real vault of ~1080 files / ~12.7K nodes; 25 Q&A)

| method | MRR | hit@1 | hit@5 | hit@10 |
|---|---|---|---|---|
| grep / BM25 (file) | 0.151 | 0.04 | 0.32 | 0.40 |
| English-only MiniLM (control) | 0.008 | 0 | 0 | 0 |
| multilingual MiniLM | 0.312 | 0.28 | 0.36 | 0.40 |
| e5-small / e5-base | 0.405 / 0.384 | — | — | — |
| BGE-M3 **file-level** | 0.318 | 0.24 | 0.44 | 0.52 |
| BGE-M3 **nodes** | 0.663 | 0.52 | 0.84 | 0.88 |
| **EmbeddingGemma-300m q8 [chosen]** | **0.620** | 0.40 | **0.92** | **0.92** |

Facts the design stands on:
1. **Granularity is the main lever.** Same model: file-level 0.318 → nodes 0.663 (**~2.1x**). Chunking by header decides more than picking a model.
2. **grep degrades as the vault grows; embedding barely does.** At ~540 files the gap was ~2.3x; at ~1080 files, ~4.4x. The bigger the memory, the more the layer earns its keep.
3. **Multilinguality is a threshold, not a bonus.** An English-centric model on a non-English vault is dead (0.008) even with perfect chunking. If your vault is not English, pick a multilingual embedding model.
4. **Real quality is above raw MRR.** Manual inspection of the "misses": most are rank 2–3, where a *legitimately co-relevant* file sits above the ground-truth (often a better answer). The operational metric is hit@5 = **0.92**: the right file is in the top five 92% of the time.
5. **RRF/fusion hurts** (0.773 → 0.511 on a capped corpus): a strong dense arm shouldn't be diluted with a weak grep arm. Don't build fusion.

## Model: EmbeddingGemma-300m, q8 ONNX, 768d

- Repo: `onnx-community/embeddinggemma-300m-ONNX` — **ungated** (the Google original is gated; this ONNX re-upload downloads without a token).
- **q8 = the quant sweet spot:** MRR 0.620, bit-for-bit with fp32, weight **309 MB** (fp16 is 618 MB for the same quality; q4 is 197 MB but ~9% lower MRR). Versus BGE-M3: ~6% lower MRR, but **+9% hit@5 and 15x lighter** (309 MB vs 4.5 GB). Selection criterion: quality + weight; speed doesn't matter here.
- Take the model's **`sentence_embedding`** output (pooled + projection head), NOT `last_hidden_state` (a manual mean-pool bypasses the head = not a real Gemma embedding).
- Prompts are required: query `task: search result | query: {q}`, document `title: none | text: {d}`.
- **Matryoshka (MRL) in reserve:** the vector's dimensions are ordered by importance → a finished 768d vector is truncated to the first 256 + renormalized, WITHOUT re-embedding. At 256d hit@5 holds 0.92 and the vectors shrink 3x. Toggled by the `DIM` constant.
- Everything on CPU (`CPUExecutionProvider`).

## Build pipeline (`scripts/memory_index.py build`, ~35 min CPU)

```
walk 6 wings (knowledge daily context reports state projects)
  minus /node_modules/ /.venv/ /build/ /.git/ /memory-index/
→ chunk each file by ## / ### headers
    node = (header-path, section body); a file with no headers = 1 node
    header-path = "file-stem > H2 > H3" — BAKED INTO the embedding text
→ D_PROMPT + header-path + body[:2000] → EmbeddingGemma q8 → L2-normalize
→ np.savez(nodes.tmp.npz): vecs[N×768 f32] + relpaths[N] + headers[N] + snippets[N]
→ os.replace(tmp → nodes.npz)          ← ATOMIC; a partial write does not exist
→ manifest.json: model, dim, counters, git HEAD, build date
```

## Search pipeline (`scripts/memory_index.py search "question"`)

```
Q_PROMPT + question → embed the query
→ sims = vecs @ q              (brute-force cosine, single-digit ms over ~12.7K nodes)
→ collapse: best node per file → top-K files
→ output: score · relpath · § header-path · 160-char snippet
```

It returns **path + section + snippet, not the full chunk** — the reading agent decides what to open with Read; context stays clean.

## Warm server (lazy, TTL suicide) — removes the cold start

`memory_index.py serve` — HTTP on `127.0.0.1:8765` (stdlib), model + vectors held in RAM (~500 MB). **Not a daemon:** `search` brings it up lazily (the first query is cold and spawns it in the background), and it dies on its own after 30 min idle. Read-only over the `.npz`, re-reads the file by mtime after a rebuild.

| mode | latency (measured) |
|---|---|
| cold query (first one, brings up the server) | ~7s |
| warm via CLI `search` | **0.15s** |
| warm raw HTTP (`GET /search?q=...`) | **0.065s** |

~65 ms per semantic query over ~12.7K nodes → weaving it into every grep call costs effectively nothing.

## Invariants (each one is a learned scar, not a preference)

| Invariant | Why |
|---|---|
| One `.npz`, zero DB, zero HNSW | an embedded vector store under concurrent write+read once ballooned to 100+ GB. Brute force over ~12.7K vectors needs no index — and what isn't there can't corrupt |
| Only full-write + `os.replace`, never upsert | the same scar; the tmp name MUST end in `.npz`, else `np.savez` appends the suffix itself and the atomic swap misses |
| No fusion/RRF with grep | measured: it sinks the strong arm |
| No daemon/crons | the model loads on call; the price is a ~7s cold start |
| No MCP / external APIs / $0 | fully local; the model is a one-time ~309 MB download |
| Model/dim are constants in the head of `memory_index.py` | changing the model or the MRL truncation = editing constants, not rewriting the engine |
| The venv and every `.npz` are gitignored — a blank clone ships without vectors | both are regenerable: `bash scripts/memory_index_setup.sh` rebuilds the venv (~1 GB), `memory_index.py build` rebuilds the sidecar on first run |

## Integration — a hook on **Bash** (this environment has no Grep tool)

In this Claude Code there is no `Grep` tool — search (in the main thread and in sub-agents) goes through `grep`/`rg` inside the **Bash tool**. So the hook hangs on the `Bash` matcher:
- `.claude/hooks/semantic-recall.sh` — a cheap gate: python starts ONLY if the command contains `grep`/`rg` (non-greps are dropped in ~0.02s).
- `.claude/hooks/semantic-recall.py` — extracts the pattern from the grep command (shlex; handles quotes and pipes) → knocks on the warm server → dense candidates are appended as `additionalContext`.
- Registered in `.claude/settings.json` under the PostToolUse `Bash` matcher. **Active from the next session** (hooks are snapshotted at start). No server → a quiet plain grep + a lazy spawn; it NEVER blocks the search.

`/recall` and `/dream` call the engine directly (they don't depend on the hook).

## Runtime fragility: the venv is gitignored and can vanish

The engine runs in a venv (`onnxruntime` + `transformers` + `numpy`, ~1 GB, gitignored). If it's deleted (a cleanup, a python upgrade), the data is fine (`nodes.npz` + the model cache under `~/.cache/huggingface`); only the runtime is gone. Recreate it: `bash scripts/memory_index_setup.sh` (the model self-downloads on the first build/search). The hook and server fail quietly when the venv is absent — they never block.

`/dream` update: git-diff from `manifest.git_head` → re-embed only the nodes of changed files → assemble a **new full** array in memory → atomic replace. Only the re-compute is incremental; the write is always full.

## Graph-upkeep operations the layer opens up (that grep couldn't)

Node vectors are not only for search. A pairwise cosine over the nodes gives the lint/dream passes semantic tools:
1. **Duplicate detector:** node pairs with cos > ~0.9 from DIFFERENT files = merge candidates (one event described twice). Previously only caught by eye.
2. **Link suggester:** for a file, the top-K semantic neighbors it has NO wikilink to = candidate edges. Upgrades the "missing cross-references" check from name-grep to meaning.
3. **Orphan re-filing:** an orphan file's nearest neighbors = where to backlink it.
4. All of this is numpy over the ready `.npz`, seconds, no LLM.

## File registry

| File | What |
|---|---|
| `scripts/memory_index.py` | the engine: build + update + search + serve + dupes, self-contained |
| `scripts/memory_index_setup.sh` | venv bootstrap (regenerable runtime) |
| `state/memory-index/nodes.npz` | sidecar: vecs + relpaths + headers + snippets (built locally on first `build`, gitignored) |
| `state/memory-index/manifest.json` | model/dim/counters/git HEAD/build date |
| `.claude/hooks/semantic-recall.sh` / `.py` | PostToolUse Bash hook that appends semantic hits to a grep |

## Related

- [[wikilink-conventions]] — the linking rules the graph (layer 1) is built on
- [[how-to-use-the-graph]] — the workflow this recall layer accelerates
