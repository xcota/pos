# AGENTS.md — Workspace Boot Rules

This folder is home. Treat it as the canonical Personal OS workspace. (Boot file for Codex / non–Claude-Code agents; Claude Code reads `CLAUDE.md`.)

## Session Boot
Before doing task work:

1. Read `CLAUDE.md` (operating rules + orchestration).
2. Read `context/identity.md` — your profile. If it still contains `{{ }}` placeholders or an empty `profile_version:`, the vault is not personalized yet: read `.claude/skills/start/SKILL.md` and run it — `start` is the entry point that sets everything up (it orchestrates `/svoboda-profiler` + `/vault-scaffolder` for you). Tell the user they only need to say `start`.
3. Read `daily/YYYY-MM-DD.md` for today and yesterday.
4. In a main/direct session, read `MEMORY.md`.
5. For project work, read `projects/{project}/AGENTS.md` and/or `projects/{project}/context.md` if present.

Don't ask permission for this boot context. Just load it.

## Memory
- Daily notes: `daily/YYYY-MM-DD.md` — chronological source of recent state.
- Long-term index: `MEMORY.md` — loaded in direct/main sessions, not shared/group contexts.
- Durable lessons: `context/learned.md`.
- Mistakes to avoid: `context/anti-patterns.md`.
- Current cross-context state: `state/current.md`.
- Significant decisions: `state/decisions/`.

Write down decisions, durable context, corrections, and lessons. "Mental notes" do not survive session restarts.

## Safety
- Do not exfiltrate private data.
- Do not send emails, posts, or external messages without explicit user intent.
- Do not run destructive commands without asking.
- Prefer recoverable operations; `trash` beats permanent delete.
- Preserve user changes. Never revert unrelated dirty worktree files.

## Language
Always respond in the language of the most recent user message. Language mismatch breaks trust.

## Tools And Skills
- Skills live under `.claude/skills/`. If a skill is invoked or clearly applies, read its `SKILL.md`.
- Optional modules ship under `modules/` — flip `enabled: true` in `modules.yaml`, then run `/enable-modules` to activate one (it creates dirs and seeds routes).
- For browser/local UI work, prefer configured browser/computer-use tools over ad hoc shell shortcuts.
- For repo edits, keep changes scoped and commit meaningful work.

## Communication
- Concise and high-signal. Results first; process only when useful.
- In group chats, respond only when directly asked or when adding real value.

## Extended Manual
Detailed conventions that aren't boot-critical live in `context/operating-manual.md`, `context/anti-patterns.md`, and `context/learned.md`. Keep this file under 3500 bytes; move overflow into context files and link them here.
