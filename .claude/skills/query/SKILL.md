---
name: query
description: "Use when a non-trivial question needs a researched answer that should persist in the knowledge graph."
version: 1.0
user_invocable: true
---
# /query — Ask, Synthesize, File-Back

LLM-wiki pattern: every non-trivial query produces a new synthesis page. The wiki compounds.

## Usage
`/query {question}` — ask and file
`/query --ephemeral {question}` — answer without filing (for trivial lookups)

## When to Use
- Any question requiring synthesis across 2+ entities
- Strategic decisions ("should we X?")
- Comparative analysis ("difference between X and Y")
- How-to that combines multiple sources
- Anything you'd want to NOT re-derive next time

## When NOT to Use
- Factual lookups ("what's X's email") — use grep
- Trivial questions ("how many entities")
- Clarifications within the current session

## Pipeline

### Step 1: Search Existing
```bash
grep -rl "{keywords}" knowledge/
```
Check whether the question (or a close variant) was already filed. If yes:
- Read the existing synthesis.
- Decide: augment, supersede, or refer.

### Step 2: Gather Sources
Find relevant entities:
- **Always check your domain hubs first** — if your graph has a MOC or hub note for the question's domain (e.g. `knowledge/moc/{domain}.md`), start there.
- By tag: `grep -rl "domain/{X}" knowledge/`
- By concept: `grep -rl "concept-name" knowledge/`
- By person: check `knowledge/people/`
- Relevant transcripts/sources: check `reports/`

List sources explicitly — every claim needs a source.

### Step 3: Synthesize
Produce an answer with:
- Direct answer first (results-first).
- Reasoning backed by evidence from sources.
- Each claim cites `[[source-entity]]`.
- Contradictions flagged explicitly.
- Uncertainty quantified.

### Step 4: Score
Apply the `context/scoring-gate.md` criteria (≥80/100). If below: iterate.

### Step 5: File Back
Create a new entity at `knowledge/concepts/query_{slug}_{date}.md`:
```yaml
---
type: synthesis
tags: [domain/{X}, type/synthesis, query]
updated: {today}
question: "{original question}"
sources: [[entity1]], [[entity2]], ...
score: {0-100}
---
# {Question}

## Answer
{direct synthesis}

## Evidence
- From [[entity1]]: {quote/paraphrase}
- From [[entity2]]: {quote/paraphrase}

## Caveats
{what's uncertain, what's missing}

## Connections
- [[related-entity]]
```

### Step 6: Backlinks
Update each source to mention this synthesis in its Related section (avoids floating nodes).

### Step 7: Log
```
[{YYYY-MM-DD HH:MM}] [query] "{question}" → {new-entity-path} | score: {N}/100, {N} sources
```

## Rules
- **File-back is mandatory** for non-ephemeral queries — otherwise the synthesis is lost.
- **Cite everything** — no synthesis without a source.
- **Flag contradictions** — don't hide disagreement between sources.
- **Next query starts from this one** — write as if future-you will read it.

## Example
```
/query "should we ship the new onboarding flow before or after the next release?"
```
→ Searches: `knowledge/concepts/onboarding-funnel.md`, `knowledge/decisions/2026-01-10-release-cadence.md`, relevant retro notes in `reports/`.
→ Synthesizes: "Ship after. The release-cadence decision caps in-flight changes per cycle, and the onboarding-funnel note shows the metric lift only registers with a clean A/B window — bundling both into one release confounds attribution."
→ Files: `knowledge/concepts/query_onboarding_ship_timing_2026-01-12.md`.
→ Next time a similar question comes up: it starts from this file, not from zero.
