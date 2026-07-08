---
type: context
tags: [anti-patterns, index, evolving]
updated: 2026-01-01
maps: context/anti-patterns.md
---

# Anti-Patterns Index — clusters, statuses, watch-list

**An additive layer over `context/anti-patterns.md`. References AP IDs; never
duplicates their bodies. Zero renumber — each `AP-NNN` resolves in the source
file. IDs are citation keys, so this index only ever points at them.**

This file exists so the agent doesn't have to load the entire anti-pattern
corpus at boot. It groups entries into a few **root clusters** (a recurrence is
one root firing again, not a brand-new failure), tracks each entry's **status**,
and maintains a small **watch-list** of the ones worth carrying in working
memory.

## Legend

- **status:**
  - `LIVE` — an active failure mode with no hard backstop yet.
  - `ESCALATED` — promoted into a `rules/*.md` hard rule via `escalated_from`.
  - `SOLVED` — a structural fix removed the trigger; the entry stays for history.
  - `RETRACTED` — withdrawn (was wrong, or no longer applies). Keep the tombstone;
    don't re-arm it.
- **boot:**
  - `WATCH` — carried in the session-start watch-list (small, cross-domain).
  - `archive` — read by ID only when its domain is touched; not loaded at boot.

## Root clusters (scaffolding)

A new anti-pattern usually belongs to one of these. Recurrence = the cluster's
root firing again. When a cluster accumulates a 3rd recurrence with no hard rule,
that's the promotion signal (see the rules in `rules/`).

| #  | Cluster | Theme | Members | Hard-rule backstop |
|----|---------|-------|---------|--------------------|
| **C1** | ORIENT-BEFORE-BUILD | Check what exists / take the cheapest path / internal-first before build, guess, or external lookup. | AP-001, AP-012, AP-013, AP-014, AP-019, AP-037, AP-038 | `rules/orient-before-commit.md` |
| **C2** | ANSWER-THE-ACTUAL-QUESTION | Render the literal spec / read the named source / no convenient substitute / honor literal scope. | AP-007, AP-009, AP-015, AP-025, AP-028, AP-035, AP-040, AP-041 | `rules/substitution-instinct.md` |
| **C3** | MATCH-COST-TO-SCOPE | No enterprise theater, no heavy machinery / over-protection on a small personal-tool task. | AP-027, AP-030, AP-032, AP-033, AP-034 | `rules/match-cost-to-scope.md` |
| **C4** | VERIFY-BEFORE-SHOW | No public trial-and-error; confirm before claiming; verify integration not just creation; don't fake completeness; probe the real thing. | AP-008, AP-016, AP-017, AP-018, AP-020, AP-021, AP-023, AP-024, AP-036, AP-039 | none yet (promote on 3rd recurrence) |
| **C5** | RETAIN-CORRECTIONS / DON'T-TOUCH-LIVE-INFRA | Durable priors; respect env/account facts; read-only on live/others' systems; don't pathologize. | AP-002, AP-004, AP-005, AP-006, AP-010, AP-011, AP-022, AP-026, AP-029, AP-031, AP-042, AP-043 | `rules/retain-corrections.md` (corrections + read-only); naming via `rules/naming-convention.md`; work-frame via `rules/work-is-the-work.md` |

Note: AP-003 (no filler) is a baseline communication rule cited across clusters;
keep it on the watch-list. Each new AP should be filed under exactly one cluster.

## LIVE watch-list (carried at boot)

Keep this list short — only the cross-domain failure modes most likely to fire in
an arbitrary session. `session-start` loads *this list*, not the whole AP file
(the rest is fetched by ID when its domain comes up).

- **C1:** AP-012 (don't claim false absence), AP-037 (orient covers tooling),
  AP-038 (graph before web).
- **C2:** AP-009 (answer the asked question), AP-035 (literal spec — ESCALATED),
  AP-040 (given list = exact scope).
- **C3:** AP-032 / AP-034 (over-protect / over-spend — ESCALATED).
- **C4:** AP-008 (don't claim unfinished work), AP-036 (verify before "look").
- **C5:** AP-002 / AP-004 (stale facts / repeat corrections), AP-031 (don't
  pathologize), AP-003 (no filler).

> Mechanism note: anti-patterns live in main-thread context and do **not**
> propagate into spawned subagents. When orchestrating a workflow, either inject
> the relevant AP text into the subagent prompt, or post-filter subagent findings
> against this file before relaying. A subagent doesn't know your anti-patterns.

## ESCALATED → rules/

Only entries with a *real* `escalated_from` citation in a rules file. When you
promote an AP, add it here and flip its status to `ESCALATED`.

- → `rules/orient-before-commit.md` — `escalated_from: AP-001` (C1 frame-before-commit cluster).
- → `rules/substitution-instinct.md` — `escalated_from: AP-035` (C2 meta; absorbs AP-007/009/015/025/028/040/041).
- → `rules/match-cost-to-scope.md` — `escalated_from: AP-032 + AP-034` (C3 meta; absorbs AP-027/030/033).
- → `rules/retain-corrections.md` — `escalated_from: AP-004 + AP-022` (C5 corrections + read-only/live-infra).
- → `rules/naming-convention.md` — filename-hygiene (a C5 durable-convention member).
- → `rules/work-is-the-work.md` — `escalated_from: AP-006`-class work-frame (the primary work is the work; not a revenue/output redirect).

## RETRACTED

Tombstones go here. A retracted AP must not sit on a live recurrence chain — if a
later cycle tries to revive it, the tombstone is the record that it was already
withdrawn. *(None in the seed corpus — start clean.)*

## Promotion candidates (pre-staged)

Track failure modes that have fired twice and have a high blast radius, so the
3rd fire is an obvious promote rather than a fresh debate. Note the target rule
filename and the trigger phrasing here before it earns its hard rule.

- **C4 (VERIFY-BEFORE-SHOW)** is the largest cluster with *no* hard backstop —
  AP-008/017/018/020/021/036/039 all live here. If a verify-before-claiming
  failure recurs a 3rd time, promote to `rules/verify-before-show.md`.

## Notes

- Don't infer `ESCALATED` from an AP merely *referencing* a rule. Status flips
  only when a rule's frontmatter actually carries `escalated_from: AP-NNN`.
- `SOLVED` requires a real structural guard that removed the trigger. Keep the
  status even when unused — a future fix flips the flag without editing the AP.
- A cluster grouping ≠ a numbering guarantee. APs keep their append-order IDs;
  the cluster column is the only place membership is recorded.
