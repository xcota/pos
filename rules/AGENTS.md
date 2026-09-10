---
type: agents
directory: rules
---
# Rules

Hard rules for this workspace. A rule here is the **backstop tier** of the
3-tier discipline mechanism: advisory anti-patterns
(`context/anti-patterns.md`) → directive state (goals/priorities) →
**hard rule (this directory)**. A failure mode lands here only after the
advisory layer demonstrably failed to prevent its recurrence.

## When to read
- Before any non-trivial action, the agent should know these rules are in force.
- When a rule's domain is touched (building, answering a spec, sizing a task,
  recalling a correction, naming a file), read the matching rule.

## How a rule gets created
1. A failure recurs a 3rd time despite an advisory anti-pattern.
2. Promote it: write a `rules/<name>.md` with `status: hard` and
   `escalated_from: AP-NNN ...` in the frontmatter.
3. The rule must change what the agent is *allowed* to do — gates, not restated
   advice. Mark the source AP `ESCALATED` in `context/anti-patterns-index.md`.

## What's here
- `orient-before-commit.md` — establish the frame before answering / fanning out
  / building. (C1)
- `substitution-instinct.md` — render the literal spec; no convenient substitute.
  (C2)
- `match-cost-to-scope.md` — no enterprise theater or heavy machinery on a small
  personal-tool task. (C3)
- `retain-corrections.md` — corrections are permanent; live infra is read-only
  until asked. (C5)
- `work-is-the-work.md` — the operator's chosen primary work is the work; other
  lanes are opt-in; never redirect toward a generic "more valuable" goal. (C5)
- `honesty-register.md` — report facts, not a flattering frame: don't spin a weak
  result, don't dress up a failure, don't assert unverified absence. (C5)
- `plain-first.md` — lead with the plain "what this gives you" take; don't mirror
  the register of a jargon/academic source; apparatus after. (C2 axis)
- `perceive-before-ship.md` — perceive a sensory artifact through a real proxy
  (render / live click / read-back) before shipping; static assumptions are blind.
  (C4)
- `local-only-repo.md` — the engine assumes a local-only repo; don't raise
  secret-scrub / durability guards as findings for the private instance. (C3)
- `naming-convention.md` — `[a-z0-9_-]` filenames; dated document formula; entity
  vs document schemes.

## Conventions
- Frontmatter: every rule carries `type: rule`, `status: hard`, and
  `escalated_from:`.
- Rules cite the anti-pattern cluster they backstop, not specific incidents.
- AGENTS.md in every significant directory — explains what's here and when to
  read it.
