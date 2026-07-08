---
type: context
tags: [rules, quality, scoring]
updated: 2026-06-14
---

# Scoring Gate Protocol

Every research/analysis output from a subagent gets scored 0-100 before it is accepted.

## When to Apply
- Research reports
- Strategy proposals
- Content extraction (transcripts → insights)
- Any output that will be stored in `knowledge/` or `reports/`

## Scoring Criteria

| Criterion | Weight | What to check |
|-----------|--------|---------------|
| Accuracy | 30% | Facts verifiable, no hallucinations |
| Actionability | 25% | Can the owner act on this immediately? |
| Completeness | 20% | Nothing obvious missing? |
| Signal density | 15% | No filler, every sentence carries info |
| Connection | 10% | Links to existing knowledge-graph entities |

## Rules
- Score ≥ 80 → accept
- Score 60-79 → iterate with specific feedback
- Score < 60 → reject and redo
- Log scores in the daily note for tracking over time

## Model Routing

Route by capability and speed. Under subscription-based access (no per-token billing), tier selection is a quality/speed tradeoff, not a cost calculation.

| Task type | Model tier | Why |
|-----------|-----------|-----|
| File search, grep, counts, parsing | Fast | Sufficient, quick |
| Code, text generation, extraction, bulk research | Mid | Balance of quality and speed |
| Architecture, strategy, quality gate, scoring, short high-stakes tasks | Top | Highest quality, verification |
| Bulk reading / large-file passes | Mid (not Top) | Top tier wasted on mechanical reading; Mid handles it |

> Routing stays quality/speed-first. Don't default everything to Top — reserve it for synthesis, judgment, and gate decisions.
