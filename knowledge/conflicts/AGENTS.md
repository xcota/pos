---
type: meta
tags: [graph, conflicts, epistemic, convention]
updated: YYYY-MM-DD
---

# knowledge/conflicts/ — Conflict-as-Record + Epistemic Taxonomy

The epistemic layer of the graph. File-based: markdown + wikilinks, **no SQL, no MCP**. All fields are **optional and lazy** — their absence means "legacy / not yet annotated", not an error. Only the ingest / graph-add path and conflict events write these fields. An index generator that only reads `type` / `domain` / `updated` will not break when new fields appear.

## Epistemic frontmatter (optional, added to any `knowledge/*.md`)

```yaml
modality: observation            # WHAT KIND of statement (12-enum below)
epistemic_status: sourced_claim  # CONFIDENCE LADDER (13-enum below)
confidence: 0.82                 # scalar 0.0–1.0 (a single number, not a vector)
confidence_sources: 1            # optional: N independent confirmations
last_verified: YYYY-MM-DD        # enables a stale-check during lint
conflicts: []                    # wikilinks to conflict records; non-empty ⇒ promotion blocked
```

**`modality` (12):** `factual_claim | observation | assumption | hypothesis | decision | policy | preference | requirement | risk | capability | definition | deprecation`

**`epistemic_status` (13):**
- Promotion ladder (ascending): `mention → extracted_candidate → sourced_claim → corroborated_claim → reviewed_claim → accepted_knowledge → canonical_knowledge`
- Degradation / dispute (orthogonal, not rungs): `disputed | deprecated | superseded | forbidden_for_use` (plus `assumption`, `hypothesis` as terminal states).

## Confidence tiers (a simple reconciliation)

If you also tag claims by where they came from, map it to the ladder rather than inventing a second vocabulary:

| Source tier | confidence | typical epistemic_status |
|---|---|---|
| Stated directly by a trusted primary source | 0.9–1.0 | reviewed_claim / accepted_knowledge |
| Inferred from observed behavior | 0.6–0.8 | corroborated_claim |
| Model/AI inference | 0.3–0.5 | hypothesis (+ modality: hypothesis) |
| Third-party opinion | 0.4–0.6 | sourced_claim (+ modality: observation) |

Rule: never move `epistemic_status` up the ladder without a corroborating source or direct confirmation.

## Conflict-as-Record (3 writes, 0 overwrites)

**Trigger:** ingest or graph-add produces a claim whose normalized subject matches an existing note, but the assertion **differs**.

**Action:**

1. **Create** `knowledge/conflicts/<slug>-conflict-YYYYMMDD.md`:
   ```yaml
   type: conflict_record
   epistemic_status: disputed
   conflicting_with: ["[[original-note]]"]
   conflict_markers:                 # string[]
     - "source A asserts X — ref: knowledge/research/src-a.md"
     - "source B asserts Y — ref: knowledge/raw/src-b.md"
   confidence_a: 0.82
   confidence_b: 0.55
   promotion_blocked: true
   resolution: null
   ```
   Body: both claims verbatim + provenance. Do not delete either until resolved.
2. **Downgrade the original** (frontmatter only, body untouched): set `epistemic_status: disputed` and `conflicts: ["[[<slug>-conflict>]]"]`.
3. **Backlink** from the conflict record to both nodes (no floating nodes).

**Invariants:** both claims survive; promotion to any rung is **blocked** while `resolution: null`; resolution is **manual, human-in-the-loop**. On resolution: loser → `superseded` + `superseded_by: [[winner]]`; winner clears `conflicts: []`; the record sets `resolution: <date + reason>`.

The principle: a contradiction is a **new record plus a promotion block, not an overwrite** of old by new. This is what prevents a naive "newer beats older" ingest rule from silently destroying a contested fact.

## What to adopt vs skip

**Adopt:** modality × status enums · conflict-as-record · `conflict_markers: string[]` · `promotion_blocked` · scalar confidence.
**Skip:** a confidence *vector* (a single scalar is enough); any nightly autonomous overwrite of canonical notes; a third "lifecycle" axis (a single-user graph doesn't need it).
