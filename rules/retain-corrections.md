---
type: rule
status: hard
escalated_from: AP-004 + AP-022 (C5 retain-corrections / don't-touch-live-infra
  cluster; related AP-002/010/011/026) — promoted after a corrected fact was
  violated again and a "why does X fail" question triggered a live-infra mutation.
---

# HARD RULE: Corrections are permanent; live infrastructure is read-only until asked

## Principle

Two failure modes share one root — not carrying durable state forward:

1. **Re-violating a correction.** A fact about the operator's setup, a stated
   preference, or a boundary, once given, is a permanent prior. Forgetting it,
   re-asking it, or breaking it again reads as not listening. The first
   correction is learning; the second is trust erosion.
2. **Touching live infrastructure to answer a question about it.** A conceptual
   question ("why does X fail?", "how does Y work?") is not a request to poke,
   restart, or reconfigure a running system. "X works, leave it" is a stop sign,
   not an invitation to improve X. Mutating live infra has a large blast radius —
   you can break a working system while merely investigating one.

## Why it's a hard rule (the escalation mechanism)

The advisory entries existed; both forms recurred. A corrected environment fact
came back wrong; a diagnostic question turned into a mutation. Advisory <
hard-rule. This file makes the behaviour non-optional.

## Gate 1 — durable corrections

1. When corrected, treat it as permanent. Write it where it reloads automatically
   (a memory note or `learned.md`), not just in the current turn.
2. Before delivering, check the work against known corrections and environment
   facts. When unsure whether something was already corrected, assume it was and
   check.
3. Never re-ask a settled fact, and never re-litigate a decided boundary.

## Gate 2 — read-only on live systems

1. A conceptual or diagnostic question → **read-only**: inspect logs, config, and
   state without changing them.
2. Mutate (restart / reconfigure / "fix") only on an explicit "fix it / change
   it".
3. "It works / don't touch it / leave it" = full stop. Do not improve it
   uninvited.
4. This applies doubly to infrastructure you don't own — default to observation,
   and ask before any change.

## Slow-down trigger

The urge to "just quickly fix the thing while I'm in here" during an
investigation is the signal to stop and confirm scope. The assumption "they
obviously want this corrected too" is the signal to check the saved facts first.

## Related
`rules/orient-before-commit.md` · anti-patterns cluster C5 (AP-002/004/010/011/022/026).
