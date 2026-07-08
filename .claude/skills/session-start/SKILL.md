---
name: session-start
description: "Use when starting a new working session or when context needs fresh boot."
version: 1.0
user_invocable: true
---
# /session-start — Boot Personal OS Context

Boot context for a new working session. Progressive loading: minimal at start, expand by task.

## Steps

1. If `state/current.md` exists, read it — what's happening across all contexts right now. If it's absent (or `context/identity.md` still has `{{ }}` placeholders), the vault isn't set up yet — don't fabricate state. Warmly tell the user, in one line: *"This vault isn't set up yet — just say `start` and I'll do it with you (no commands, no steps)."* Then stop and let them.
2. Read `context/priorities.md` — current focus and active work
3. Read `context/anti-patterns-index.md` → load the **LIVE watch-list** (active failure modes). Full `context/anti-patterns.md` is reference — pull by AP-ID when a task touches that domain.
4. Check if `daily/{today's date}.md` exists — read last 20 lines for today's events
5. Scan `state/sessions/` — any active checkpoints to continue?
6. If the task is system architecture, agent runtime, or sync — read `context/agent-runtime.md`

## Output

Display a compact dashboard:

```
=== Personal OS ===
Focus: {top priorities from priorities.md}
State: {active contexts from current.md}
Watch: {top 3 anti-patterns to remember}
Today: {key events if daily note exists}
Checkpoint: {available session to continue, if any}
===
```

## Rules

- Total context after boot should be 15-25K tokens, not more
- Do NOT load all of knowledge/ — only load specific files when the task demands it
- Do NOT load project context unless working on that project
- If user wants to continue a session: read the checkpoint, load its context
- After displaying dashboard, ask "What are we working on?" if not obvious
