---
name: session-save
description: "Use when saving session state before closing or when context exceeds 150K tokens."
version: 1.0
user_invocable: true
---
# /session-save — Save Session State

Save current session state before closing or when context gets heavy (>150K tokens).

## Arguments
- `[name]` — optional checkpoint name. Auto-generated if not provided.

## Steps

0. **Analyze this session as a self-improvement signal:** before summarizing, walk back through this session and read it as friction data (like `/reflect` Step 1b, but over the CURRENT dialogue): how the user responded (tone, corrections, what they valued, what frustrated them), and where the agent missed, substituted, failed to orient, or added noise. → new anti-pattern / learned / identity refinements, tagged with a source-tier. Don't bulk-load the transcript — reflect over what is already in context.

   **Поправки формы → `context/identity.md` § «Как со мной работать».** Если человек за эту сессию
   поправил, КАК с ним говорить («короче», «не спрашивай про это», «на ты», «не списком») — это
   данные об интерфейсе, а не выводы о нём: 0–2 строки в тот раздел, каждая с датой и его словами.
   Второго списка в другом файле не заводить. Покажи кандидатов одной строкой и запиши только то,
   с чем он согласился; молчание — не согласие. Выводы о человеке (карточки сфер, профиль) сюда
   не попадают, и наоборот.

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

## Rules
- Keep checkpoint files under 500 words
- Don't save trivial sessions (quick questions, lookups)
- Always update state/current.md — other contexts depend on it
- Scope = un-persisted work since last commit, not just the latest task
