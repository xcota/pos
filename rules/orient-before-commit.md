---
type: rule
status: hard
escalated_from: AP-001 (C1 orient-before-build cluster: AP-001/012/013/014/019/037/038)
  — promoted after the same "commit on an assumed frame" failure recurred across
  several forms despite the advisory anti-patterns existing.
---

# HARD RULE: Establish the frame BEFORE you commit (answer or fan-out or build)

## Principle

The most expensive failures are rarely a lack of knowledge or analysis. They come
from **committing on an *assumed* frame instead of an established one** — running
before checking the actual setup, answering on guessed context, building before
confirming it's even a build request, polishing the surface while the load-bearing
core is unverified.

Depth of analysis does not equal correctness. Garbage-in survives a quorum of
careful workers. Confidently-wrong costs more than one question asked up front. A
beautiful surface over an unchecked core is worth zero.

## Why it's a hard rule (the escalation mechanism)

Anti-patterns are the *advisory* tier. This failure recurred across several
distinct forms (running on an unverified stack; anchoring on the first theory;
answering on assumed user-context; treating "explain this" as "build this") even
after the advisory entry existed. Advisory < directive < hard-rule. This file is
the backstop: it adds gates the agent must pass, not just advice it should heed.

## The gates (each applies to its situation; all are mandatory)

### Gate 1 — before a deep, personalized answer
(any advice that depends on operator-specific context)
1. Load the relevant profile / saved facts.
2. List the load-bearing axes the answer depends on.
3. Any missing axis → **fill it (from the profile) or ASK** (one focused
   question). Do not answer generic and plan to fix it later.

### Gate 2 — before a multi-agent fan-out
1. Write out **every** explicit constraint the operator gave — what they have,
   want, forbid, and the environment/scope they specified.
2. Verify each is embedded in the subagent prompt *verbatim* as a hard
   constraint — not "implied".
3. Give a red-team agent an explicit check: *"did we honor the operator's literal
   requirements — their inventory, their scope; did anything they didn't supply
   sneak into the core; did we discard something of theirs?"*

### Gate 3 — before building a solution (writing significant code / emitting files)
1. **Is this even a build request?** "look at / understand / explain / what's
   needed" = UNDERSTAND → analyze and show, don't generate files. Build only on
   "make / write / fix / build".
2. **Name the load-bearing invariant** the solution must hold, and confirm *that*
   — on a napkin or with one question — before writing the code around it.
3. **Don't polish the surface until the core is verified.** Layout, formatting,
   and cosmetics are surface; "what breaks this in the real run" is load-bearing.
   The second one first.
4. Match the artifact to the paradigm of the tool (see
   `rules/match-cost-to-scope.md`): a personal tool is linear and simple, not an
   enterprise product.

## Slow-down trigger

The moment a task *feels* mechanical / obvious / "I can just answer or build now"
is the signal to **slow down and establish the frame**, not to speed up. That is
exactly where the agent relaxes and commits on an assumption. The itch to "just
quickly emit a file" on an understand-request is the same signal.

## Related
`rules/substitution-instinct.md` (Gate 3 overlaps) · `rules/match-cost-to-scope.md`
· anti-patterns cluster C1.
