---
type: rule
status: hard
escalated_from: a preservation / local-only anti-pattern cluster (C3) — promoted
  after over-engineering security and durability guards for a private local repo
  recurred despite advisory entries that already named both "over-engineering
  data-leak guards for a local-only repo" and "match preservation cost to scope".
---

# HARD RULE: The engine assumes a LOCAL-ONLY repo

## Design assumption

This vault is **local-first**. By design it assumes: no shared
remote, no external reader, no CI, no auditor; git is a **local snapshot
convenience, not a contract with anyone**; and it runs on the operator's own
compute with no paid external APIs required to function. The whole engine is built
around a single operator on their own machine.

Because of that, for this vault and any personal local-only tool, the following are
**NOT problems and must NOT be raised as findings, risks, or CRITICAL items** — in
audits, reviews, reflections, or relayed subagent output:

- Plaintext credentials / API tokens / passwords in tracked files. No external
  reader exists to leak them to.
- Secrets in git history; "needs a history rewrite / force-push / token rotation".
- `.gitignore` rules to protect secrets, or sensitive-vs-public file splits.
- Binaries in git framed as a *security / leak* concern (a disk-size note is fine,
  but don't act on it without an explicit ask — history is convenience, not a
  contract).
- Continuous-sync / multi-target backup / durability infrastructure for a personal
  tool.

## What IS allowed to be a finding

Only hygiene that affects how an agent operates: rule contradictions, false
completeness signals, broken wikilinks, dead or deprecated references, stale state,
missing orientation docs.

## Note if you ship the engine outward

If a copy of this engine is ever published or shared, that copy has a different
threat model — treat secret-scrubbing and access questions as real *there*. This
rule is about the **private local instance the operator runs**, not a public fork.

## Orchestration note (the mechanism that broke)

Anti-patterns live in main-thread context — they do **not** propagate to workflow
subagents. When orchestrating an audit/review, either inject the relevant
constraints into the subagent prompts, **or** post-filter subagent findings against
this rule and the anti-patterns before relaying. Otherwise a git-hygiene subagent
flags plaintext secrets, the synthesis ranks them CRITICAL, and the main thread
relays it raw. Sibling: `match-cost-to-scope.md`.
