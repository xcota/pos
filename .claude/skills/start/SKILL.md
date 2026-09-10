---
name: start
version: 1.0
user_invocable: true
description: One-word self-unfolding onboarding. Sets up a fresh, unpersonalized vault end-to-end — installs the memory engine, runs the profile interview, scaffolds the vault, and teaches the user as it goes. The single front door.
---

# /start — set everything up (the only command a new user needs)

This runs when someone lands in a **fresh, unpersonalized** vault (or types `start`). Your job:
take them from a blank folder to a living, personalized Camomile folder **without them having to
know any commands, paths, or setup steps.** You drive; they just talk.

**Design target: a curious beginner — think "a smart 10-year-old with a short attention span."**
So:
- **One thing at a time.** Never dump a wall of text or a list of commands.
- **Plain words.** No jargon ("vault", "scaffold", "embedding") unless you immediately say what it
  means in kid-plain terms. Prefer "your notebook", "set it up", "search by meaning".
- **Do the work for them.** Run every shell command yourself, silently or with a one-line plain
  narration. The user should never see or type `pip`, `bash`, or a file path unless they ask.
- **Show progress + let them quit.** Say where they are ("① of ④"). They can stop anytime and
  come back by typing `start` — it resumes, never restarts from zero.
- **Teach by doing.** After each step, one sentence on *what they just got and how they'll use it*.
- **Be warm and short.** Encourage. Match their energy. This should feel like a friendly setup
  wizard, not a manual.

If the vault is ALREADY personalized (`context/identity.md` has no `{{ }}` placeholders and a real
name), don't re-onboard — greet them back and point to what they were doing (`/session-start`).

---

## The flow (four steps — you orchestrate all of them)

### ① Hello + the one-sentence what-is-this (~20 sec)
Greet by asking their name/handle to use. Say, in one sentence, what this is:
> "This is your own AI notebook-and-assistant that remembers everything and gets smarter about
> *you* over time. I'll set it up with you — takes about 15–20 minutes, and you can stop anytime."

Tell them the shape: "First I get to know you (a few questions), then I build your space, then
you're live." Then start step ②. Don't wait for a long answer — keep momentum.

### ② Turn on memory (runs in the background while you talk — don't make them wait)
First, silently make sure the vault is a **git repo** — the memory is git-backed (`/session-save`,
`/dream`, `/reflect` commit to it), so a clone works out of the box but an unzipped copy needs this
one-time init. Then kick off the semantic-memory engine **in the background** so it installs while
you do the interview. Run:
```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || git init -q   # git-backed memory; no-op if already a repo
bash scripts/bootstrap.sh
```
(Run it non-blocking / in the background if your harness supports it, e.g. append ` &`, or just
launch it and move straight into step ③ — it self-narrates and takes 1–2 min.)

Say it plainly, one line: *"Setting up your memory in the background — it lets me find things by
what you *mean*, not just exact words. Meanwhile, let's get to know you."*

Handle the two outcomes without alarming them:
- **No Python, or the script prints that it didn't manage** → that's fine, it exits cleanly. Say it
  in one plain line: *"Meaning-based search needs a free add-on I couldn't install here; everything
  else works and I'll search by exact words. We can come back to it later."* Then continue.
  **Never block onboarding on this, and never show the raw output.**
- **It succeeds** → mention it once at the end ("your memory is on"), don't interrupt the interview.

### ③ Get to know them → build their space (the core)
Run the profile interview by following **`.claude/skills/svoboda-profiler/SKILL.md`**, but wrap it
in this friendly frame:
- **One question at a time.** Ask, wait, react warmly, ask the next. Never paste the whole question
  set. The interview has natural sections — after each, say "that's section X done, Y to go — you're
  doing great" so they feel progress.
- **Let them go shallow or deep.** If they give short answers, that's OK — capture and move on.
  Remind them once: "you can stop after any section and pick up later by typing `start`."
- It's a normal conversation — no tools, no downloads, nothing for them to install. Just talking.

When the profiler has written `profile.yaml`, **immediately and silently build their vault** by
following **`.claude/skills/vault-scaffolder/SKILL.md`** — the user does NOT type a second command.
Narrate the result in plain words, not file paths:
> "Done — I just built your space. I set up who-you-are, your north star, your starting goals, and
> your memory notebook, all from what you told me."

### ④ You're live — teach the 3 things they'll actually use
Confirm memory finished (or note it's the plain-search fallback). Then teach ONLY these three, one
line each — this is the whole "how to use it" they need on day one:
1. **Just talk to me.** "Ask me anything, or tell me to do things. I remember across sessions."
2. **Dump your day.** "Drop notes, thoughts, links into me anytime — say them or put them in `daily/`."
3. **Say `save` when you want me to remember something important.** (i.e. `/session-save`.)

Then the finish line:
> "That's it — you're set up. Restart me in this folder and say hi. Your notes live here as plain
> files — you can open, edit or move them any time."

Optionally mention one power-up they can explore later, in one line: "When you're curious how the
brain works, ask me to explain `docs/methodology.md`."

---

## Rules
- **Never** show the user raw command output, pip logs, file paths, or errors unless they ask —
  translate everything into one plain sentence.
- **Never** make them run a second command. `start` (or the word "start") is the only thing they type.
- **Never** block or abort on the memory add-on failing — the core is pure Markdown and always works.
- Resumable: if `profile.yaml` or a partial `session.yaml` already exists, continue from there
  instead of restarting (the profiler handles resume — honor it).
- Keep each of your turns short. If you've written more than ~5 lines, you're dumping — trim.
- After onboarding completes, `start` should no longer re-onboard — it should greet + hand off to
  `/session-start`.

## What this skill orchestrates (so you don't reinvent it)
- `scripts/bootstrap.sh` → the memory engine (venv + model + index). Fire-and-forget, self-narrating.
- `.claude/skills/svoboda-profiler/SKILL.md` → the interview (writes `profile.yaml`).
- `.claude/skills/vault-scaffolder/SKILL.md` → builds the personalized vault from `profile.yaml`
  (fills CLAUDE.md, context/root.md, identity, goals, self-entity).
- `.claude/skills/session-start/SKILL.md` → the normal boot, for every session after onboarding.
