---
name: session-start
description: "Use when starting a new working session or when context needs fresh boot."
version: 1.0
user_invocable: true
---
# /session-start — Boot Camomile Context

Boot context for a new working session. Progressive loading: minimal at start, expand by task.

## Steps

0. **Check what the start hook already poured in.** `.claude/hooks/session-start.sh` runs at every launch and prints a `--- State ---` block (state, priorities, today's note, checkpoints, sensors and the 💤/🔍 gates). If that block is in context, skip steps 1, 2, 4 and 5 — those files are already read, re-reading them wastes the boot budget. No block (a subagent, another entry point, or the hook failed) → do the steps by hand. If the block says the folder is not set up yet, follow its line and stop.

1. If `state/current.md` exists, read it — what's happening across all contexts right now. If it's absent (or `context/identity.md` still has `{{ }}` placeholders), the folder isn't set up yet — don't fabricate state. Say it to the person in ONE plain line, in the language they write in, and stop:

   > This folder isn't set up yet — just type `/start` and I'll do the rest. No commands or steps needed from you.

   Say it in the language the person writes in. Never write the word "vault" to the person — it is a folder.
2. Read `context/priorities.md` — current focus and active work
3. Read `context/anti-patterns-index.md` → load the **LIVE watch-list** (active failure modes). Full `context/anti-patterns.md` is reference — pull by AP-ID when a task touches that domain.
4. Check if `daily/{today's date}.md` exists — read last 20 lines for today's events
5. Scan `state/sessions/` — any active checkpoints to continue?
6. If the task is system architecture, agent runtime, or sync — read `context/agent-runtime.md`

## Output

Display a compact dashboard:

In plain words, in the language the person writes in, with no paths and no jargon:

```
=== Camomile ===
In focus now: {top priorities from priorities.md}
Where we stopped: {active contexts from current.md}
What I remember not to repeat: {top 3 anti-patterns}
Today: {key events if daily note exists}
Can be continued: {available session checkpoint, if any}
===
```

Drop an empty line entirely — shorter is better than a row of dashes.

## Rules

- Total context after boot should be 15-25K tokens, not more
- Do NOT load all of knowledge/ — only load specific files when the task demands it
- Do NOT load project context unless working on that project
- If user wants to continue a session: read the checkpoint, load its context
- After displaying dashboard, ask "What are we working on?" if not obvious
