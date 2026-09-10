---
name: ingest
description: "Use when a raw source file needs to be ingested into the knowledge graph."
version: 3.1
user_invocable: true
---
# /ingest — Structured Data Extraction

Extract structured knowledge from raw data sources into the knowledge graph.

## Arguments
- `[source_type]` — source kind: telegram | transcript | youtube | notes | bio | survey | audio
- `[path]` — path to the file or directory holding the data
- `[topic]` — optional topic/context to focus extraction

## Pipeline

### Phase 1: R2C (Raw → Characteristics)
1. Detect source type (auto-detect, or from the argument).
   - YouTube URL: create `inbox/youtube/{slug}_{video_id}/`, fetch auto-subs with `yt-dlp --skip-download --write-auto-subs --sub-langs "en.*,<primary>.*" --sub-format vtt` (use the subject's primary language from `context/identity.md` if profiled, else `en`; run `yt-dlp --list-subs <url>` first if unsure). Needs `yt-dlp` installed. **If no `.vtt` is produced** (yt-dlp exits 0 even when it finds nothing), do NOT fabricate a transcript — mark the source `unresolved` and ask the user to paste one. Otherwise normalize VTT into `transcript.md` + `transcript.txt`, then process as `transcript`.
2. Load the source-specific extraction prompt from `projects/ingest/prompts/{source_type}.md`.
   - If `projects/ingest/prompts/youtube.md` is missing, use `transcript.md` and add focus on: source metadata, chapter outline, reusable concepts, architecture deltas, action items.
3. Split input into chunks (~1500 tokens, with overlap).
4. Parallel subagents: each chunk × each dimension —
   - **bio** — biographical facts, events, chronology
   - **patterns** — patterns of behavior, decisions, thinking
   - **values** — values, beliefs, priorities
   - **connections** — people, relationships, social graph
   - **insights** — insights, unique ideas, non-obvious observations
5. Output format per chunk:
   ```
   date/period – dimension – fact/observation – "evidence quote" – confidence (0-1)
   ```

### Phase 2: C2F (Characteristics → Final)
1. Collect all Phase 1 results.
2. Deduplicate: merge identical facts, raise confidence.
3. Consolidate: group by topic/entity.
4. Create/update files in `knowledge/`:
   - New entity → `knowledge/{type}/{entity-name}.md` with frontmatter + `[[wikilinks]]`.
   - Existing entity → append/merge new facts.
   - Wikilink validation: every `[[link]]` must point at a file that exists.

### Phase 3: Output
1. Summary: how many entities created/updated, key findings.
2. Update `state/current.md` with the ingest result.
3. Append to `daily/{today}.md`.

## Rules
- Confidence < 0.5 → mark as uncertain, do not create an entity.
- Don't duplicate already-known facts (check `knowledge/` before writing).
- One entity = one file. Don't smear a single entity across multiple files.
- Filenames: `[a-z0-9_-]` only (hard rule from CLAUDE.md).
- Don't create entities for small everyday trivia.
- For architectural sources: a single summary is not enough. Fold the delta into the relevant `context/`, `knowledge/concepts/`, MOC, or skill files.
- **On conflict** (a new claim contradicts an existing one about the same subject): use **conflict-as-record**, do NOT overwrite. Create `knowledge/conflicts/<slug>-conflict-{date}.md` (both claims + provenance + `promotion_blocked: true`), downgrade the original (frontmatter `epistemic_status: disputed` + `conflicts: [...]`), backlink, and ask the user. Protocol: `knowledge/conflicts/AGENTS.md`. "Fresh > old" applies ONLY to undisputed updates from the SAME source.
- **Epistemic frontmatter** (Phase 2): write `modality` / `epistemic_status` / `confidence` (from the per-chunk confidence 0-1 already in the pipeline) per entity. `confidence < 0.5` → `epistemic_status: extracted_candidate` (do not promote). Enums: `knowledge/conflicts/AGENTS.md`.
- **Coverage gate** (Phase 3): every processed source → one line `{covered | omitted_boilerplate | redacted | unresolved}` + reason. Any `unresolved` blocks ingest completion. Put the table in the summary + `daily/{today}`.
