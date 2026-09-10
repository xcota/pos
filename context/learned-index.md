---
type: context
tags: [lessons, index, evolving]
updated: 2026-01-01
maps: context/learned.md
---

# Learned Index — theme map, statuses

**An additive layer over `context/learned.md`. References lesson IDs; the bodies
stay in the source. Never delete — only amend (status banner in place).**

This is the navigation layer for the lessons corpus. It groups lessons by theme
so the agent can load the relevant cluster instead of the whole file, marks the
handful of core lessons that should never be dropped under compaction, and tracks
non-LIVE statuses.

## Theme map (scaffolding)

Add each new lesson under the theme it belongs to, by ID. Themes are stable; the
membership grows. A one-line gloss per theme keeps the map self-describing.

- **A — Orchestration / Subagent discipline.** _Dispatch vs main-thread bloat;
  quality-gate before relay; anti-patterns don't reach subagents; match model cost
  to task tier; share-zero-state parallelism; checkpoint at phase transitions; be
  terse per step._ → L-001..L-007
- **B — Knowledge graph / Vault integrity.** _Corrections are durable priors;
  retrieve before generating; backlink at creation; record conflicts vs overwrite;
  verify integration; lint-driven write order; bulk cleanup by buckets; MOC is
  navigation._ → L-008..L-015
- **C — Communication / Trust / Frame-switching.** _Restate the frame on pushback;
  validate gaps when they converge; trust their domain expertise; deliver the
  artifact not a comment on their bets; shorthand → tooling; ask load-bearing
  context up front; regress upstream for "source"._ → L-016..L-022
- **D — Process discipline / Anti-procrastination.** _Lesson count isn't health;
  fix recurrence at the directive layer; "mechanical" steps skip the gate; growth
  edge is restraint not capability; build→verify can close a case; time-box
  warmups; research needs an execution deadline._ → L-023..L-029
- **E — Infrastructure / Reliability / Ops.** _Init files before jobs; heartbeats
  on anything automatic; managed units for daemons; failures by root cause; never
  rsync `.git`; hard-block media in gitignore; cheap proactive rot-checks;
  sandbox-blocked networking mimics outage; delivery is best-effort._ → L-030..L-038
- **F — Extraction / Reverse-engineering.** _Capture the reference first; identify
  the format before decompiling; the engine is the value not the UI; browser source
  bypasses shell-net; verify the speaker; keep match/not-found/error separate;
  trust strong signals over a dirty field; substring harvesting has FP classes._
  → L-039..L-046
- **G — Architecture philosophy.** _Guard the most-loaded file; steal patterns not
  infra; tight loops are the system; discoverability decides existence; UI from the
  machine outward; templates without application are decoration; closed lanes need
  a tombstone._ → L-047..L-053

## Core lessons (never dropped under compaction)

The small set that changes how the agent operates everywhere — must survive any
context compression. Keep it short; if everything is core, nothing is.

- **L-001** — the dispatcher doesn't do the work.
- **L-003** — anti-patterns don't propagate into subagents (inject / post-filter).
- **L-008** — a correction is a durable prior.
- **L-009** — orient by retrieval before generation.
- **L-016** — restate the frame on pushback.
- **L-024** — fix a recurrence at the directive layer, not the advisory one.
- **L-047** — guard the most-loaded file.

## Statuses (non-LIVE)

- **RETRACTED:** a lesson withdrawn as wrong; keep the tombstone, don't revive.
- **SUPERSEDED:** `L-old → L-new` when a later lesson absorbs or corrects it.
- **CLOSED-DOMAIN:** lessons from a finished line of work — IDs still resolve, but
  boot and reflection skip them.
- **Dup-merge:** when two lessons converge on one root, annotate the pair here —
  don't delete either.

*(None in the seed corpus — start clean. The real record that this was distilled
from did retract a lesson once: a "you must spend every Nth session on revenue"
heuristic that fabricated pressure the operator never asked for. The general
warning survives as L-024 + `rules/work-is-the-work.md` — when a "productivity"
lesson starts driving the agent to redirect away from the operator's chosen work,
that lesson is the bug.)*

## Arc (one line)

Track the agent's competence as a single updating sentence — a fast read on where
it's maturing and where it keeps regressing. Seed: _"naive → quality-gated →
frame-aware → directive-layer-fixed → calibration/restraint as the live edge."_
