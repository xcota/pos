---
type: context
tags: [index, context-layer]
updated: 2026-06-14
---

# Context Layer Index

`context/` holds the stable rules, goals, and quality gates for this folder. These files change rarely. Load them deliberately — most are not part of the every-session boot.

Read this index to know which file answers which need.

## Files

| File | What it is | Read when |
|------|-----------|-----------|
| `root.md` | Identity core + the light-cone doctrine: the single source the task field-of-view is assembled from (persona blanks written by the profiler; §4 doctrine is portable) | Main boot; scoping any task's field-of-view |
| `identity.md` | Who this OS serves; agent-self principles (persona-specific, written by the profiler) | Main boot; any task needing the owner's profile |
| `agent-runtime.md` | Runtime adapter: path conventions (`{{VAULT_ROOT}}`), boot order, loading discipline, graph map, drift handling | Onboarding a new agent shell; resolving stale paths or conflicting instructions |
| `operating-manual.md` | The 10 working rules, 6 frustration triggers (FT-1..6), communication style, decision-making style, contextual behaviors | Any non-trivial task; before delivering work |
| `priorities.md` | Current focus and blockers | Main boot; deciding what to work on |
| `goals.md` | Longer-horizon goals (reference, not per-session) | Strategy and architecture work |
| `anti-patterns.md` | Active failure modes — what not to repeat (AP-NNN bodies) | Main boot; before delivery |
| `anti-patterns-index.md` | Navigation over the AP corpus: root clusters, statuses, boot watch-list, escalation→`rules/` map | Boot (load the watch-list, not the whole AP file); when promoting an AP to a hard rule |
| `learned.md` | Distilled lessons from past work (L-NNN bodies) | Architecture work; when a decision echoes a past one |
| `learned-index.md` | Navigation over the lessons corpus: theme map, core-lessons-never-dropped, statuses | Boot (load core lessons); choosing which lesson cluster to load |
| `scoring-gate.md` | 0-100 quality gate + model routing for subagent research/analysis output | Before accepting anything bound for `knowledge/` or `reports/` |
| `skill-candidates.md` | Cold staging for distilled winning procedures awaiting a deliberate promotion gate (mechanism only; not in boot) | During `/reflect`, `/session-save`, or a review |

## Load Order

- Per session (light): `identity.md`, `priorities.md`, `anti-patterns.md`.
- On a real task: add `operating-manual.md`.
- Architecture / strategy: add `goals.md`, `learned.md`.
- Accepting subagent output: `scoring-gate.md`.
- Confused about paths, boot order, or a contradiction between files: `agent-runtime.md`.

## Conventions

- This index points; it does not duplicate content. To change a rule, edit its file, not this index.
- When state and a rule file disagree, current state (`state/current.md`, `priorities.md`) wins; fix the stale file.
- Keep these files free of credentials, host names, and absolute machine paths (use `{{VAULT_ROOT}}`-relative — see `agent-runtime.md`).
- `identity.md` is the only file here that is persona-specific. All others are portable engine layer.
