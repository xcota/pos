---
type: rule
status: hard
escalated_from: a filename-hygiene anti-pattern (C5 durable-conventions) —
  promoted after non-conforming names (spaces, mixed case, non-ASCII) caused
  cross-platform sync noise and case-collisions more than once.
---

# HARD RULE: File naming convention

## Principle

Filenames are interface, not decoration. Consistent, machine-friendly names keep
the workspace navigable, keep sync between machines quiet, and let the agent
predict where things live. Inconsistent names produce duplicates,
case-collisions, and unicode-normalization noise that no later cleanup fully
removes.

## The character rule (hard)

Filenames use **`[a-z0-9_-]` only**. No spaces, no uppercase, no non-ASCII, no
special characters. The only exceptions are a few all-caps system files
(`MEMORY.md`, `README.md`, `AGENTS.md`, `SHIP.md`) and the generated
map-of-content prefix `MOC_<name>.md`. A source name that breaks this gets
slugified on ingest; preserve the original in frontmatter (`title: "..."`).

Rationale: case-insensitive filesystems plus unicode NFD/NFC normalization plus
cross-machine sync turn "pretty" names into silent breakage.

## Document formula

```
{project}_{type}_description_YYYY-MM-DD.md
```

- lowercase, digits, underscores; date always at the **end**.
- max ~80 chars; max two codes before the description (project + type).
- type is encoded in the filename, not in a folder hierarchy.

Examples:
```
proj_research_topic_overview_2026-01-05.md
proj_report_audit_results_2026-01-05.md
self_retro_week_review_2026-01-05.md
```

## What gets which scheme

- **Documents** (reports, research, transcripts) → the full dated formula.
- **Entity files** (knowledge-graph nodes — people, concepts, tools) →
  `entity-name.md`, lowercase-hyphenated, **no date** (they're permanent nodes,
  not temporal documents).
- **Daily notes** → `YYYY-MM-DD.md` in `daily/`.
- **Project context** → `context.md` + `AGENTS.md` under `projects/{name}/`.
- New files with no clear home → `inbox/`.

## Generic codes (customize per workspace)

Project codes are 2–8 chars and workspace-specific; define them in a small table
and keep it short. Content types are a fixed small set:

| Type | For |
|------|-----|
| `research` | analysis, investigations |
| `plan` | roadmaps, strategies |
| `guide` | how-to, instructions |
| `rule` | standards, conventions |
| `report` | generated reports, audits |
| `summary` | digests, meeting notes |
| `template` | reusable templates |
| `daily` | daily notes |
| `retro` | retrospectives |

## Frontmatter

Every document file carries at least:
```yaml
---
type: research
tags: [project/<code>, topic/<topic>]
date: 2026-01-05
---
```
Tag namespaces: `project/`, `type/`, `topic/`, `status/`.

## Related
anti-patterns cluster C5 (durable conventions are corrections that must persist).
