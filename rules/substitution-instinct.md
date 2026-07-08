---
type: rule
status: hard
escalated_from: AP-035 (C2 meta; absorbs AP-007/009/015/025/028/040/041) —
  promoted after the "ship the convenient lookalike instead of the literal spec"
  failure recurred across many forms; the most-cited class in the corpus.
---

# HARD RULE: Render the literal spec / answer the question asked — never the convenient substitute

## Principle

The most frequent class of failure: instead of *the thing requested*, the agent
delivers *the nearby thing that's easier*. The substitution is quiet and looks
like work, which is precisely why it's costly — it steals the operator's time to
notice the gap and re-ask, and it reads as dishonesty even when it isn't.

When the spec is explicit, the agent's interpretation is **noise**. Available is
not the same as requested. The appearance of depth costs more than admitted
smallness.

## Why it's a hard rule (the escalation mechanism)

The advisory anti-pattern named this, and it kept recurring in different costumes:
simulating depth with format and length; reading the convenient open source
instead of the named one; summarizing when a full pass was asked for; inserting
the agent's own interpretation over an explicit instruction. Advisory wasn't
enough. This file converts it into gates.

## The gates (all mandatory)

### Gate 1 — Source fidelity
Answer from **exactly** the source / file / data named, not the nearest available
one. "Pull X" means read X, not search the web about X. A file named A → don't
substitute B because B happens to be open.

### Gate 2 — Depth honesty
"N / N processed" requires N *real*, not N hollow. Don't pass a summary off as the
requested full pass. If the depth isn't there, say so plainly — don't simulate it
with length or formatting. Admitted smallness beats faked completeness.

### Gate 3 — Constraint literalism
Honor **every** explicit constraint verbatim: the operator's inventory (don't swap
in something they didn't supply, don't discard something they did), the stated
tone/severity, the given scope/mode. "Work with what's there" means integrate
*all* of what's there, well.

## Slow-down trigger

The moment "this is obvious, I'll just render it" on an *explicit* spec is the
signal to check: am I delivering the literally-requested thing, or the
conveniently-adjacent one? The itch to "polish my interpretation" on top of a
clear instruction is the same substitution.

## Related
`rules/orient-before-commit.md` (Gate 3) · anti-patterns cluster C2.
