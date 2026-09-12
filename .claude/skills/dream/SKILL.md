---
name: dream
version: 1.0
user_invocable: true
description: "Use when 24h+ since last dream AND 5+ sessions elapsed, or when explicitly asked to consolidate memory."
source: Adapted from the Claude Code autoDream protocol.
trigger: dual-gate — 24h since last dream AND 5+ sessions since last dream
---

# /dream — Memory Consolidation

You are performing a dream — a reflective pass over your memory files. Synthesize what you've learned recently into durable, well-organized memories so that future sessions can orient quickly.

**Memory directories:**
- `knowledge/` — entity files (people, business, concepts, tools, projects) + MOC
- `context/` — priorities, anti-patterns, learned, goals
- `state/` — current.md, decisions, sessions

**Index file:** `MEMORY.md` (workspace root) — also `knowledge/INDEX.md` if present
**Index limits:** 200 lines AND 25KB
**Daily logs:** `daily/YYYY-MM-DD.md`

**Session transcripts:** Claude Code stores per-session JSONL transcripts under its projects directory (e.g. `~/.claude/projects/<slug>/*.jsonl`, where `<slug>` is derived from the vault path). These are large — grep narrowly, never read whole files.

**Sister tool:** the node-level embedding index — semantic search across the whole vault. Use it in Phase 1 to fetch existing facts before synthesizing, and in Phase 2 to surface contradictions.

```bash
.memory_venv/bin/python scripts/memory_index.py search "QUERY"
# warm server (ms): curl -s "http://127.0.0.1:8765/search?q=QUERY&k=8"
```
Architecture: `knowledge/concepts/memory-embedding-layer.md`.

---

## Phase 1 — Orient (CRITICAL — this is the fix for hallucination)

**Synthesis without prior reading = hallucination factory.** Before writing anything:

- `ls knowledge/ context/ state/` to see what already exists
- Read `MEMORY.md` and `knowledge/INDEX.md` (if it exists) to understand the current index
- Read `state/current.md` for cross-context state
- Skim existing topic files in the area you're about to touch — improve them, don't create duplicates
- Review `state/sessions/` for recent checkpoints
- Use `memory_index.py search "{topic}"` (node index) to surface related nodes before deciding what's new

**If you skip Phase 1, abort the dream.** Do not write to memory without knowing what's already there.

## Phase 2 — Gather recent signal

Sources in priority order:

1. **Daily logs** — `daily/{last 3-7 days}.md` (append-only stream of what happened)
2. **Drifted facts** — memories that contradict current code/state. Cross-check entity files against `git log --oneline -30` and recent edits.
3. **Anti-patterns triggered** — `context/anti-patterns.md` recent entries → are there new patterns to extract?
4. **Reflection reports** — `reports/reflection-*.md` if any since the last dream
5. **Transcript search** — only for things you already suspect matter:
   ```bash
   grep -rn "<narrow term>" ~/.claude/projects/ --include="*.jsonl" | tail -50
   ```
6. **Semantic contradictions** — `memory_index.py search "{drifted topic}"` to see if the graph has conflicting facts

**Don't exhaustively read transcripts.** Look only for things you already suspect matter.

## Phase 3 — Consolidate

For each thing worth remembering, write or update a file in the appropriate directory:

- **Entities** (people, businesses, concepts, tools, projects) → `knowledge/{type}/{kebab-name}.md` with `[[wikilinks]]`
- **Lessons / insights** → append to `context/learned.md`
- **Anti-patterns** → append to `context/anti-patterns.md`
- **Cross-context state** → update `state/current.md`
- **Decisions** → `state/decisions/{date}-{topic}.md`

Rules:
- **Merge into existing topic files** rather than creating near-duplicates. If a `knowledge/people/<name>.md` exists, update it — don't write `<name>-2.md`.
- **Convert relative dates** ("yesterday", "last week") to absolute dates (`2026-04-09`) so they stay interpretable.
- **Delete contradicted facts** — if today's investigation disproves an old memory, fix it at the source. Don't leave both versions.
- **Wikilinks must resolve** — the PreToolUse hook rejects a Write to `knowledge/` if any `[[link]]` doesn't exist. Either create the stub first or remove the link.
- **Naming:** kebab-case, no caps, no extensions in links (`[[some-entity]]`, not `[[Some Entity.md]]`)

## Phase 4 — Prune and index

Update `MEMORY.md` (and `knowledge/INDEX.md` if present) so each stays **under 200 lines AND under 25KB**.

It's an **index**, not a dump. Each entry = one line under ~150 characters:
```
- [Title](path/to/file.md) — one-line hook
```

Never write memory content directly into the index.

- **Remove** pointers to memories that are stale, wrong, or superseded
- **Demote verbose entries** — if an index line is over ~200 chars, the content belongs in the topic file. Shorten the line, move the detail.
- **Add** pointers to newly important memories
- **Resolve contradictions** — if two files disagree, fix the wrong one (don't index both)

After pruning: `wc -l MEMORY.md` — must be ≤200. If over, prune harder.

## Phase 5 — Update the node-level embedding index

Only if `.memory_venv/bin/python` exists (the person said yes to search by meaning). If it does not, skip this phase without a word. Otherwise recompute the semantic index — ONLY the changed files (git-diff from `manifest.git_head`, seconds, not the ~35-min full build):

```bash
.memory_venv/bin/python scripts/memory_index.py update
```

Layer architecture: `knowledge/concepts/memory-embedding-layer.md` (EmbeddingGemma q8 ONNX, nodes chunked by header, one `.npz` sidecar, brute-force cosine).

**Invariants:** `update`/`build` write ONLY a full-write + atomic `os.replace` — never an incremental upsert into the store. The warm server (127.0.0.1:8765) is read-only and re-reads the `.npz` by mtime on its own — no need to kill or restart it. Don't run two `update`/`build` in parallel (the last one wins — it won't corrupt anything, but it burns CPU for nothing).

**Optional (graph hygiene):** `memory_index.py dupes 0.9` — semantic duplicate nodes from different files = merge candidates; interpret by class (translations / boilerplate "Related" sections are not rot).

## Phase 6 — Report

Return a **brief** summary (≤15 lines):
- Files updated / created / deleted (counts)
- Top 3 facts merged or contradictions resolved
- Index size before → after
- Anything notable surfaced from semantic recall (node index)

If nothing changed (memories are already tight), say so in one line.

Either way, close the gate first (the two commands under *Trigger gate* below), then report.

---

## Trigger gate (when to actually run)

Dual-gate, both must be true:
1. **≥24h** since the last dream — `state/last_dream.txt` (epoch seconds, written by this skill)
2. **≥5 sessions** since the last dream — `state/session_count_since_dream.txt` (counted by the start hook)

You don't compute this yourself: `.claude/hooks/session-start.sh` checks both at every launch and prints `💤 Memory tidy-up is due` when the gate is open. Then you offer it to the person in ONE sentence, in their language ("My memory needs a few minutes of tidying — do it now?") and run only on a yes. The person never needs to know the word "dream".

**After a successful run — mandatory, this is what closes the gate** (skip it and the offer repeats at every start):
```bash
date +%s > state/last_dream.txt
echo 0 > state/session_count_since_dream.txt
```

Manual override: the person asks for it directly (in any words) → ignore the gate, still close it afterwards.

## Anti-patterns (do NOT)

- ❌ Skip Phase 1 — synthesizing without orienting is the exact hallucination loop this protocol exists to prevent
- ❌ Read full JSONL transcripts — always grep narrowly
- ❌ Create near-duplicate entity files — merge into existing
- ❌ Leave contradicted facts both intact
- ❌ Dump content into MEMORY.md — it's an index, not a memory
- ❌ Use external APIs — local only (node embedding index + grep + file ops)

## Why this structure

Naive consolidation synthesizes without grounding → it hallucinates schemas and entity facts that don't exist. This protocol fixes that structurally:

1. **Phase 1 orient is mandatory** — no synthesis without reading existing state
2. **"Merge into existing topics rather than creating near-duplicates"** — kills the duplication loop
3. **Hard 200-line index cap** — prevents the index bloating into a memory dump
4. **Dual-gate trigger** (24h AND 5 sessions) — replaces a noisy daily cron

Pair this with `/reflect` as the data-collection layer: periodic reflection reports feed Phase 2.
