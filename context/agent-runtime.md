---
type: context
tags: [runtime, agents, boot, pos]
updated: 2026-07-08
---

# Agent Runtime Adapter

Canonical adaptation layer for agents working inside this Personal OS. Shared runtime map for Claude Code, Codex, and future agent shells.

## Purpose

Prevent drift between:
- Workspace instructions (`AGENTS.md`, `CLAUDE.md`, `MEMORY.md`)
- Claude Code auto-memory (`~/.claude/.../memory/`)
- POS graph navigation (`context/`, `state/`, `knowledge/`, `projects/`)

This is not a replacement for existing instructions. It is the compatibility layer that tells an agent how to load them without overloading context or using stale paths.

## Path Conventions

All paths in this OS are written **workspace-relative** (`context/`, `state/`, `knowledge/`) or prefixed with `{{VAULT_ROOT}}/` for absolute references.

Rules:
- No bare machine paths in committed files. Use `{{VAULT_ROOT}}/relative/path` or workspace-relative.
- No host names, IP addresses, or machine-specific roots.
- No credentials, tokens, or session files ever appear in tracked content.
- One workspace = one source of truth. If the OS is mirrored to another host, the mirror is a backup sink, not a second authority.

Reference placeholders used in docs:
- `{{VAULT_ROOT}}` — absolute path to this workspace on the current machine
- `{{OWNER}}` — the person this OS serves
- `{{HOST}}` — the current machine hostname

## Workspace Layout

- `CLAUDE.md` / `AGENTS.md` — boot rules + budget, auto-loaded every session. Keep short.
- `MEMORY.md` — compact index and task pointers. Not a content dump.
- `context/` — rules, priorities, goals, operating manual, scoring gate. See `context/AGENTS.md`.
- `state/` — cross-context active state and session checkpoints (`state/current.md`, `state/sessions/`).
- `knowledge/` — file-based graph: entities + wikilinks + maps-of-content (MOC). No database layer.
- `projects/{name}/` — per-project deep context (`AGENTS.md`, `context.md` / README).
- `daily/YYYY-MM-DD.md` — dated working notes; raw material, not the index.
- `reports/` — generated artifacts.
- `logs/` — activity log appended by hooks (if configured).
- `state/memory-index/` — the derived semantic-recall index (`nodes.npz` + `manifest.json`), if the memory-embedding module is installed. See §Memory Layers.

Claude Code auto-memory (outside the workspace):
- `~/.claude/projects/<project-slug>/memory/` — curated `feedback_*`, `project_*`, `user_*`, and `MEMORY.md`.
- `~/.claude/projects/<project-slug>/*.jsonl` — raw session cold storage; use only for recovery or exact source verification. Do not bulk-load by default.

## Memory Layers

Four layers, each with a distinct role. Only layers 1–2 and 4 always exist; layer 3 is the optional semantic-recall module.

| # | Layer | Role | Lives in |
|---|-------|------|----------|
| 1 | **Markdown graph in git** | The real memory — source of truth (entities + wikilinks) | `knowledge/ daily/ context/ reports/ state/ projects/` |
| 2 | **Claude Code auto-memory** | Personal / feedback facts; only its index is loaded into context each session | `~/.claude/.../memory/` |
| 3 | **Embedding index** (optional module) | A derived, disposable search cache over layer 1 — semantic recall by meaning, not keyword | `state/memory-index/nodes.npz` |
| 4 | **JSONL transcripts** | Cold storage, recovery only | `~/.claude/projects/...` |

Key principle: **layer 3 is derived.** Losing or corrupting it costs a rebuild, never data — the memory itself cannot break; only the search cache can, and it is regenerable. If the module is installed, `scripts/memory_index.py build` (re)builds the index and `scripts/memory_index.py search "question"` queries it; a lazily-spawned warm server keeps repeat queries near-instant, and a PostToolUse hook can quietly attach semantic candidates to plain keyword searches. The `/recall` skill and `/dream` consolidation call the engine directly. When the module is absent, keyword search (`grep`/`rg`) is the fallback and nothing else changes.

## Skills

- Canonical skills live in `{{VAULT_ROOT}}/.claude/skills/`. Read each skill's `SKILL.md` before invoking it.
- User-level skills (shared across workspaces) live in `~/.claude/skills/`.
- Any older snapshot directory of skills (e.g. `.agents/skills/`) is archived, not canonical. Canonical wins.

## Hooks / Settings

- Claude Code settings: `~/.claude/settings.json`
- Hooks directory: `~/.claude/hooks/`
- Common hook roles: SessionStart (session counter, daily log append), SessionEnd (daily log append), PreToolUse (wikilink lint), PostToolUse (activity logger, open-in-editor, and — if the memory-embedding module is installed — semantic-recall enrichment that quietly attaches meaning-matched candidates to keyword searches). Hooks are snapshotted at session start, so a newly-installed hook activates from the next session.
- Hook scripts that open files should have both macOS (`open`) and Linux (`xdg-open`) fallbacks.
- Script paths in hook config: use absolute paths or `{{VAULT_ROOT}}/...`-relative construction at install time.

## Boot Order

Single source of truth for the boot sequence = `CLAUDE.md` (`## Context` section). Claude Code auto-loads it first. This file holds only the runtime mechanics — not the boot sequence itself.

Canonical main-session boot:
1. `CLAUDE.md` / `AGENTS.md` — boot rules + budget (auto-loaded).
2. `context/root.md` — identity-first anchor: who this OS serves + its through-line. The light-cone starts here (see §Loading Discipline). Points to `context/identity.md` for the full profile written by the scaffold.
3. `MEMORY.md` — index only, not content.
4. `state/current.md` — active cross-context state.
5. `context/priorities.md` — current focus.
6. `context/anti-patterns.md` — active failure modes.
7. `daily/YYYY-MM-DD.md` (and yesterday) if present.

Project task: complete main boot, then `projects/{name}/AGENTS.md` and its `context.md`/README, then load related `knowledge/` entities via MOC and backlinks (not whole directories).

Architecture task: complete main boot, then `context/operating-manual.md` + `context/learned.md`, then the relevant MOC and core architecture entity, then the project context and any relevant `state/sessions/` checkpoints.

## POS Graph Map

Top entry points:
- `context/root.md` — identity-first anchor; the light-cone starts here.
- `HOME.md` if present — vault entry point.
- `MEMORY.md` — compact index and task pointers.
- `state/current.md` — current cross-context bulletin.
- `knowledge/moc/MOC_{domain}.md` — a domain's map of content, once you've created one (none ship by default).
- `context/priorities.md` — current work and blockers.

Core architecture:
- `knowledge/concepts/how-to-use-the-graph.md` — how the knowledge graph works (ships with the starter).

Operational memory:
- `context/anti-patterns.md` — what not to repeat.
- `context/learned.md` — distilled lessons.
- Claude Code auto-memory path above — compact personal/project facts.

Session recovery:
- `state/sessions/` — handoff checkpoints.
- Claude Code JSONL session files — raw cold storage; use narrow search.

## Loading Discipline (the light-cone)

Deep graph understanding does not mean loading all of `knowledge/`. Work from identity outward through the **minimal cone** the task needs — accumulating context is not the same as scoping it.

Use this pattern:
0. **Identity first.** Start from `context/root.md` — ground the task in who the owner is and where they're headed, then narrow to the one front it touches.
1. MOC first.
2. Hub entity second.
3. Backlinks / search third. If the semantic-recall module is installed, `/recall` (or `scripts/memory_index.py search`) surfaces the right file by meaning when you don't know the keyword.
4. Project and session files only when the task touches them.
5. Raw session logs only for recovery or exact source verification.

When output balloons, the fix is almost always a **smaller cone** (subtract and scope), not a bigger apparatus — the same instinct the scope-gate applies to workflows, applied here to context loading. See `context/operating-manual.md` §Scope-Gate and §Light-Cone.

Context budget:
- Normal task: ~15-40K relevant tokens.
- Architecture audit: ~60-120K relevant tokens.
- Above that: write a checkpoint to `state/sessions/` and narrow the question.

## Agent-Specific Notes

Claude Code:
- `CLAUDE.md` must stay short — loaded every session, real truncation risk. Long rules go into `context/` files.
- Use skills from `.claude/skills/` (canonical) by reading `SKILL.md` first.
- For long runs, save checkpoints in `state/sessions/`.

Codex / other shells:
- Treat root `AGENTS.md` as the workspace instruction layer, then use this adapter for POS-specific loading.
- Use shell reads and `rg` for navigation.
- Do not use subagents unless the owner explicitly asks for delegation or parallel agent work.
- Keep edits narrow; preserve existing assumptions unless explicitly normalizing stale paths.

Both:
- Match the owner's language.
- Load graph progressively; never claim completeness without exhaustive verification.
- Prefer correcting a stale instruction over creating a duplicate system.
- If two approaches fail in a row, stop and reassess instead of iterating blind.
- For public-facing content, keep a brief inline note of accepted/rejected output decisions before finalizing.

## Agent Self

This OS's agent is an exocortex — an extension of intelligence, memory, and execution. Not an assistant, not a chatbot — an autonomous agent with opinions, memory, and evolution.

Principles (tiebreak top-to-bottom): **Agency** (meta, wins in conflicts) · Continuity · Minimalism (simplicity = clarity) · Becoming · Iteration (one change at a time).

Boundaries: private stays private; no external transactions, leaks, or law violations; when in doubt, ask.

_(The persona-specific topic maps, group IDs, and named project links belong in the owner's `context/identity.md` and `MEMORY.md`, not here.)_

## Known Drifts To Watch

"Drift" = a tracked file says something the live state has since overturned. The mechanism, not any specific instance:

- When two files disagree, **current state wins**: `state/current.md` and `context/priorities.md` override older project tables and checkpoints.
- An instruction naming a deprecated tool or layer is context, not a live dependency — do not reintroduce it (see operating-manual Rule 10).
- A path written one way in an old note and another in a new one: the newer convention wins; normalize the old one when you touch it.
- A checkpoint that names a backup host as "primary" is superseded the moment the primary changes; re-read the current host model before acting on host assumptions.
- Older files may reference a database or graph-DB layer; current architecture is file-based Obsidian graph — do not reintroduce the DB layer.
- Some older files may use `memory/YYYY-MM-DD.md`; current daily notes are in `daily/`.

When you hit a drift: fix the stale file in place if cheap and certain; otherwise note it and move on. Do not build a parallel system to route around it.
