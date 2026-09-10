# research/

Research notes, paper summaries, frameworks, and findings you want to keep and link against. A research node captures *what you learned* from an external source and *what it changes* for you — not raw transcript, not a permanent verdict.

## What goes here

- Summaries of papers, articles, talks
- Findings from experiments or investigations
- Frameworks adopted from external sources
- Comparisons and evaluations

## Node anatomy

```yaml
---
type: research
tags: [domain/<domain>, type/research]
updated: YYYY-MM-DD
source:        # url / citation / where it came from
---
```

Body shape (mirrors `_templates/research_template.md`):

```markdown
# <Title>

## Compiled Truth
**Question:** what were you trying to learn?
**Answer:** 1-3 sentence conclusion.

## Key Findings
1. Finding — explanation

## What This Changes
- Updates [[entity]] — how
- Contradicts [[entity]] — why

## Open Questions
- Question → what data would answer it

## Evidence Timeline
_Append-only. Never edit past entries._
- YYYY-MM-DD: initiated — source
```

## How entities link

- Research nodes validate or contradict [[concept]] nodes.
- They motivate [[decision]] nodes (cite the research as rationale).
- They inform [[project]] nodes (a finding changes how you build).

## When to read

- When evaluating a new approach and you want to know if you already studied something relevant.
- When a decision needs evidence behind it.
- Before re-reading a source — check if you already summarized it.
