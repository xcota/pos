---
name: session-start
description: "Use when starting a new working session or when context needs fresh boot."
version: 1.0
user_invocable: true
---
# /session-start — Boot Camomile Context

Boot context for a new working session. Progressive loading: minimal at start, expand by task.

## Steps

1. If `state/current.md` exists, read it — what's happening across all contexts right now. If it's absent (or `context/identity.md` still has `{{ }}` placeholders), the folder isn't set up yet — don't fabricate state. Say it to the person in ONE plain line, in their language (Russian by default), and stop:

   > Папка ещё не настроена — просто напишите `start`, дальше всё сделаю я. Команд и шагов от вас не нужно.

   Слово «вейлт» / «vault» человеку не писать никогда — это папка.
2. Read `context/priorities.md` — current focus and active work
3. Read `context/anti-patterns-index.md` → load the **LIVE watch-list** (active failure modes). Full `context/anti-patterns.md` is reference — pull by AP-ID when a task touches that domain.
4. Check if `daily/{today's date}.md` exists — read last 20 lines for today's events
5. Scan `state/sessions/` — any active checkpoints to continue?
6. If the task is system architecture, agent runtime, or sync — read `context/agent-runtime.md`

## Output

Display a compact dashboard:

Плоским русским (или на языке человека), без путей и служебных слов:

```
=== Ромашка ===
Сейчас в фокусе: {top priorities from priorities.md}
На чём остановились: {active contexts from current.md}
О чём помню не повторять: {top 3 anti-patterns}
Сегодня: {key events if daily note exists}
Можно продолжить: {available session checkpoint, if any}
===
```

Пустую строку не показывать вовсе — лучше короче, чем с прочерками.

## Rules

- Total context after boot should be 15-25K tokens, not more
- Do NOT load all of knowledge/ — only load specific files when the task demands it
- Do NOT load project context unless working on that project
- If user wants to continue a session: read the checkpoint, load its context
- After displaying dashboard, ask "What are we working on?" if not obvious
