---
type: rule
status: hard
escalated_from: AP-032 + AP-034 (C3 match-cost-to-scope cluster; absorbs
  AP-027/030/033) — promoted after over-engineering / over-protecting a local
  personal tool recurred a 5th time across sync, gitignore, and git-surgery forms
  despite the advisory entries.
---

# HARD RULE: Match the cost of the work to the scope of the task

## Principle

A personal tool is a **tool, not a product**. It is local, single-operator, and
optimized for the operator's own use — linear, simple, with whatever shortcuts
make it convenient to run. Treating it like a shipped product — adding layers,
guards, abstractions, and ceremony it will never need — is a failure mode, not
diligence. So is throwing heavy machinery (many parallel workers, an expensive
model, an elaborate framework) at a task a single read would settle.

The right amount of effort is the **least** that fully does the job.

## Why it's a hard rule (the escalation mechanism)

The advisory layer named over-spend and over-protection. They recurred — enterprise
guards on a local repo, heavy fan-outs on small tasks — because "more rigor" feels
safe. Advisory < hard-rule. This file states the boundaries explicitly so the
agent stops re-deciding them each time.

## For a local, single-operator tool, the following are NOT problems

…and must **not** be raised as findings, risks, or CRITICAL items — in audits,
reviews, reflections, or relayed subagent output:

- Plaintext credentials / tokens in tracked files (no external reader exists).
- "Secrets in history → needs history rewrite / force-push / token rotation."
- `.gitignore` rules to protect secrets, or public-vs-private file splits.
- Continuous-sync / multi-target backup / durability infrastructure.
- CI gates, access control, or standardized config for a thing only the operator
  runs.

Git here is a local snapshot convenience, **not** a contract with anyone.

## What IS allowed to be a finding

Only hygiene that affects how the agent operates: rule contradictions, false
completeness signals, broken links, dead/deprecated references, stale state,
missing orientation docs.

## Compute / effort sizing

- Trivial (one file, a few lines, no external lookup) → do it directly.
- Genuinely large or parallel → fan out, but cheap workers for grunt steps and
  the expensive synthesis reserved for the actual synthesis.
- Don't add an abstraction until a second concrete use exists.

## Orchestration note (a mechanism that breaks)

Anti-patterns live in main-thread context — they do **not** propagate to workflow
subagents. When orchestrating an audit/review, either inject the relevant
constraints into the subagent prompts, **or** post-filter subagent findings
against the anti-patterns and this rule before relaying. Otherwise a subagent will
flag the very non-problems this rule excludes, and the synthesis will rank them
CRITICAL.

## Related
`rules/orient-before-commit.md` · anti-patterns cluster C3.
