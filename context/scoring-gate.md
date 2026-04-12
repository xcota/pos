---
type: context
tags: [rules, quality]
---
# Scoring Gate

Every analysis output gets scored 0-100 before accepting.

## Criteria
| Criterion | Weight | Check |
|-----------|--------|-------|
| Accuracy | 30% | Facts verifiable, no hallucinations |
| Actionability | 25% | Can the user act on this? |
| Completeness | 20% | Nothing obvious missing? |
| Signal density | 15% | No filler, every sentence carries info |
| Connection | 10% | Links to existing knowledge |

## Rules
- Score >= 80 → accept
- Score 60-79 → iterate with specific feedback
- Score < 60 → reject and redo
