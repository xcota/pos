---
name: session-save
description: "Use when saving session state before closing or when the working context passes the 100K ceiling set in CLAUDE.md."
version: 1.0
user_invocable: true
---
# /session-save — Save Session State

Save current session state before closing or when context gets heavy (past the 100K ceiling in CLAUDE.md).

## Arguments
- `[name]` — optional checkpoint name. Auto-generated if not provided.

## Steps

0. **Analyze this session as a self-improvement signal:** before summarizing, walk back through this session and read it as friction data (like `/reflect` Step 1b, but over the CURRENT dialogue): how the user responded (tone, corrections, what they valued, what frustrated them), and where the agent missed, substituted, failed to orient, or added noise. → new anti-pattern / learned / identity refinements, tagged with a source-tier. Don't bulk-load the transcript — reflect over what is already in context.

   **Form corrections → `context/identity.md` § "How to work with me".** If during this session the
   person corrected HOW you talk to them ("shorter", "don't ask me about that", "use my first
   name", "not as a list") — that is interface data, not a conclusion about them: 0–2 lines into
   that section, each with a date and their own words. Do not start a second such list in another
   file. Show the candidates in one line and write down only what they agreed with; silence is not
   agreement. Conclusions about the person (area cards, the profile) do not go here, and vice versa.

0b. **Something new about a life area → into that area's card (otherwise the portrait freezes at
   onboarding depth).** If in passing during this session the person told you something new about
   one of the seven areas (Self-development, Vitality, Surroundings, Wealth, Rest, Work, Assets)
   and the folder is already built (`memory/svoboda/{id}/` exists):

   1. The verbatim phrase → `memory/svoboda/{id}/stories/additions.md` under the heading
      `## {YYYY-MM-DD}` (without this the quote check will not find it).
   2. One line in `memory/svoboda/{id}/domains/{area}.md` under "Lines", in the same shape as
      during onboarding: `you said: «…» — from the conversation on {date}` or
      `I think: … — from 1 and 3`. Use the label set for the language of the conversation (see the
      table in `start` / `svoboda-profiler`). No more than two lines per session; a paraphrase
      instead of a quote is "I think", not "you said".
   3. An area got its first entries → note it in one line in `HOME.md` (in the seven-areas
      section), so it is visible where it is dense and where the person hasn't spoken.
   4. The number for the area is **not recalculated** here and not shown again. Rebuilding the
      whole card happens only on their word: "let's go through this area again" →
      `/svoboda-profiler {id} update {area}`.

1. **Summarize** what was done — scope = ALL un-persisted work since the last commit, NOT just the current salient task:
   - First **scan for orphans**: `git log --oneline -5` vs. substantive work that exists only in the transcript/compaction-summary. Anything analyzed-but-never-written-to-a-file → fixate it in this save. Work done before a `/compact` is the most likely orphan — explicitly verify it got persisted.
   - Key decisions made
   - Files created/modified
   - Insights discovered
   - What remains to be done

2. **Extract knowledge** — if any new entities, facts, or connections were discovered:
   - Create or update files in `knowledge/{type}/` with [[wikilinks]]
   - Only for genuinely new, reusable knowledge — not session-specific noise

3. **Update shared state:**
   - Update `state/current.md` with session results
   - Append to `daily/{today}.md` with session summary (2-3 lines)

4. **Track learnings:**
   - If any anti-patterns were triggered → append to `context/anti-patterns.md`
   - If any new lessons learned → append to `context/learned.md`

5. **Save checkpoint** to `state/sessions/{name}.md`:
   ```markdown
   ---
   type: session-checkpoint
   date: {today}
   ---
   # {name}

   ## Done
   {what was accomplished}

   ## Remaining
   {what still needs to be done}

   ## Key Files
   {files that were created or modified}

   ## Continue With
   {prompt to resume this work in a new session}
   ```

6. **Git commit** — but inspect before `git add -A`:
   - Check untracked weight: `git status --short` + `du -sh` suspicious inbox dirs. Cloned external repos (nested `.git`), heavy binaries, recon dumps → add to `.gitignore`, don't commit into the vault.
   - **Before gitignoring/cleaning any source data, confirm its analysis is already fixated in a durable note.** Don't make the source inaccessible AND drop the analysis in one move.
   ```bash
   # the vault is git-backed; init a repo on first use if one doesn't exist yet
   git rev-parse --is-inside-work-tree >/dev/null 2>&1 || git init -q
   git add -A && git commit -m "[session-save]: {brief summary}"
   ```

7. **Offer the tidy-up if it is due.** If this session's start block said `💤 Memory tidy-up is due` (or `🔍 Reflection is due`) and it hasn't been done yet, say it now in ONE sentence in the person's language and run `/dream` (or `/reflect`) only on a yes. Never run it unasked.

## Rules
- Keep checkpoint files under 500 words
- Don't save trivial sessions (quick questions, lookups)
- Always update state/current.md — other contexts depend on it
- Scope = un-persisted work since last commit, not just the latest task
