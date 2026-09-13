# Camomile guide: every word, and what is inside the folder

_Version 2 · September 2026_

You never need commands. Camomile works if you only write to it in ordinary words — it reads its own notes when a conversation starts and writes them down when it ends.

This page is for the other mood: when you want to know exactly what each word does and what is in the folder.

Read the part you need and close it.

## Part 1. The words you type

Four are worth knowing. Type them exactly as written, slash included.

### `/start`

**When.** Once, on a folder you have just unpacked — and again if you broke off part-way, to carry on from the same place.

**What you type.** `/start` (a bare `start` works too).

**What happens, step by step.**

1. It greets you, asks what to call you, and says what is coming: three stories, about fifteen minutes, a card per area of life to correct, then it builds your folder. You can stop any time, and it never asks you to score yourself.
2. It takes its manner from your very first reply — language, how you addressed it, length, lists or prose.
3. One yes/no question: set up search by meaning? The cost comes first — about 300 megabytes downloaded once, about a gigabyte on disk. Say no and it searches exact words.
4. Silently it starts keeping earlier versions of your notes and makes an `inbox` folder.
5. Three stories, one per turn: yesterday; the last month; what you learned this year — each saved word for word.
6. Then a card per area, corrected by number: "3 is wrong, what actually happened is…". A plain "yes" confirms only your own words; its conclusions stay guesses until you answer by number. After two cards it builds your folder, then asks you once to close it and open it again — the only thing you do by hand.

**What you see.** Plain conversation: no program output, no paths, no errors. Cards come as numbered lines, then "I don't know", then "I heard X — right?", its reading of the area last.

**What it writes.** Your file "who I am", your words and its guesses kept apart · your goals · your front page with the seven areas · its table of contents for memory · the area cards · your stories verbatim.

**Example.**

> **You:** `/start`
> **It:** Hello. What should I call you?
> **You:** Marta.
> **It:** Next is three stories, then a card per area of life to correct — I'll never ask you to score yourself. First, one yes/no: set up search by meaning? About 300 MB, once.
> **You:** yes
> **It:** Installing. Tell me about yesterday, from waking to sleep.


### `/session-save`

**When.** At the end of a conversation worth keeping, or when it has got heavy — its rules set the working ceiling at 100K and tell it to save there.

**What you type.** `/session-save`, optionally with a name for the checkpoint.

**What happens, step by step.**

1. First it re-reads the conversation as evidence about itself: where you corrected it, what you valued, where it missed.
2. If you corrected *how* it talks to you, it offers one or two candidate lines for the "How to work with me" section of your own file, and keeps only what you agree to. Silence is not agreement.
3. If something new about one of the seven areas came up, your exact phrase goes into your stories and one line onto that area's card — without re-scoring the area or showing the card again.
4. It summarises everything unwritten since the last save, hunting for work that exists only in the conversation; new knowledge gets a page.
5. It updates "where we stopped", adds two or three lines to today's note, and writes a checkpoint under 500 words: done, still to do, key files, where to continue.
6. It saves a new version into the folder's history, then offers the tidy-up or the misses review if either was due — running it only on your yes.

**What you see.** A short report of what was saved, plus those one or two lines awaiting your yes or no.

**What it writes.** Your file "who I am" (that section) · your stories · one area card · today's note · "where we stopped" · new pages · its lessons and mistakes · a checkpoint.

**Example.**

> **You:** save this conversation
> **It:** Saved: the supplier decision and why, the two prices, Friday as the deadline. Where-we-stopped says you're waiting on their reply.
> **It:** One for your yes or no — you twice told me to stop asking follow-ups. Write down "no follow-ups unless I ask for options"?
> **You:** yes
> **It:** Written. Also: my memory is due a tidying — now or later?


### `/recall`

**When.** You want something you wrote before and no longer remember the words you wrote it in.

**What you type.** `/recall` and your question in your own words.

**What happens, step by step.**

1. Quietly it checks whether search by meaning is installed here — that check is pre-approved, so you never see an "allow this?" window.
2. If it is, it searches by meaning: a ranked shortlist, each candidate with the section that matched and a snippet.
3. If not — or if the engine falls over — it searches exact words, trying two or three forms first, and says so once per conversation in one plain line: search by meaning isn't installed here, say the word if you want it on. You never see an error full of paths.
4. What comes back is candidates, not an answer — so it opens the best one to three and reads you the section.

**What it writes.** Nothing. This one only reads.

**Example.**

> **You:** `/recall` where did I write about being wrecked in the mornings
> **It:** Closest is your story about yesterday: "woke at six, felt like I'd been hit by a bus." There's also a line in your Vitality card from July.
> **You:** the July one
> **It:** Opened it: mornings are the worst part of the day. It also notes you'd stopped eating after nine that month.


### `/reflect`

**When.** About every three days. It measures that itself, offers it in one sentence, and runs only on your yes. You can also ask any time.

**What you type.** `/reflect`.

**What happens, step by step.**

1. It gathers the last three to five daily notes, recent decisions, its watch-list of mistakes, its lessons and the recent saves.
2. The main material is the conversations themselves — read narrowly: only your turns, its replies and the friction points.
3. About you: what you valued or disliked, what you needed and didn't say — each becomes a candidate line for your own file. About itself: where it swapped your goal for its own, failed to orient, over-produced or made you wait — each becomes an entry on its watch-list.
4. It extracts lessons, proposes changes, checks whether your goals still hold, and files a short report.
5. Then it reads back to you, in your language, three to five plain lines with no paths: what it has understood about how you like to be talked to, what it still doesn't know about that, and the one or two misses it will not repeat. It asks you nothing — a mirror, not a questionnaire.

**What you see.** A compact, unflattering report, then those few lines. Its own instruction: be honest, don't sugarcoat failures.

**What it writes.** Its lessons · its list of mistakes — one that turns up three times or more is promoted into the folder's rules, where it becomes binding · your goals if horizons moved · a dated report · a stamp.

**Example.**

> **You:** `/reflect`
> **It:** Two misses in three days: Tuesday I built a table when you asked for one number; Wednesday I asked three questions before answering yours.
> **It:** What I think I know: short answers first, no tables unless asked, and you'd rather hear something is missing than get a guess.
> **It:** What I don't know yet: whether you want me to push back when I disagree.
> **It:** The two I won't repeat: no unrequested tables, and answer before I ask.


### What it offers by itself

Two things, each in one sentence, each waiting for your yes. Never more than one offer per start.

**A tidy-up of its memory.** Both conditions must be true first: a day has passed since the last one, *and* you have opened the folder about five times since. Then it says its memory needs a few minutes of tidying and asks whether to do it now.

Six plain steps: it reads what is already written before touching anything; gathers the last few days and the facts that have drifted; merges its repeated notes into the proper file instead of leaving near-copies, turns "yesterday" into real dates, deletes facts it has found to be wrong; shortens its own table of contents; refreshes search by meaning; then reports what changed.

It never touches your own words: your stories stay as you said them, and earlier versions are kept. Say "later" and nothing breaks — it asks once more when you save, and again next time you open the folder, until you say yes.

**A look at its own misses.** About every three days — the review under `/reflect`. It reads the last few days of notes and, mainly, the recent conversations; writes its lessons, its watch-list, a short report and a stamp; and ends by reading those three to five lines back to you.


### More words, if you ever want them

**`/ingest`** — *optional — you can ask for the same in plain words.* Turns a transcript, a chat export, notes or a YouTube link into pages in your notes. Video needs a helper called yt-dlp; with no subtitles it never invents a transcript — it asks you to paste one.

**`/query`** — *optional — you can ask for the same in plain words.* For a question needing several notes joined up. It answers directly, points each claim at its note, then files the answer as a page.

**`/graph-add`** — *optional — you can ask for the same in plain words.* Gives a person, project or decision a page of its own. If an existing note says otherwise it files both versions and stops to tell you.

**`/self-check`** — *optional — you can ask for the same in plain words.* The health of the folder, scored across nine things — your notes and how well they link, how fresh its state is, its three small helpers, its earlier versions. A total out of sixteen, then the gaps worst-first with a fix for each.

**`/lint`** — *optional — you can ask for the same in plain words.* The health of the notes: pages nothing links to, claims nobody has checked in a month, the same number stated two ways. It reports; it does not silently fix.

**`/enable-modules`** — *optional — you can ask for the same in plain words.* Switches on an add-on listed in `modules.yaml`, laying down starter files only where nothing exists, never over what you filled in.

**`/compress`** — *optional — you can ask for the same in plain words.* Shortens a heavy conversation into a hand-over note under two kilobytes, then checks every path, number and name survived it.


### Words it uses itself — you never type them

- **`/session-start`** — the ordinary start. A small helper already does this whenever you open the folder.
- **`/dream`** — the tidy-up of its memory. You answer yes to the offer; you never need the word.
- **`/svoboda-profiler`** — the engine under your first conversation; "let's go through Work again" reaches it too.
- **`/vault-scaffolder`** — the part that builds your folder. `/start` calls it for you.

### Saying it in plain words

| What you want | What to say |
|---|---|
| Save this conversation | "save this conversation" |
| Find an old note | "find where I wrote about being tired in the mornings" |
| Remember a person | "write a page about my supplier Anna" |
| Record a decision and why | "write down that I dropped that supplier, and why" |
| Read files you dropped in | "take a look in inbox" |
| Shorter answers | "shorter" / "answer first, explain if I ask" |
| Stop asking about something | "don't ask me about that" |
| Redo one area of life | "let's go through Work again" |
| Tidy its memory now | "tidy your memory now" |
| An earlier version of a file | "bring back yesterday's version of my goals file" |
| How healthy the folder is | "is anything broken in this folder?" |
| Erase something about you | "remove this line about me" |
| Take a transcript into your notes | "read this transcript into my notes" |

## Part 2. What is inside the folder

All ordinary text files — open any of them in whatever text editor your computer came with.

| Name | What it holds | Yours to edit? |
|---|---|---|
| `HOME.md` | Your front page: where you're heading, the seven areas, what you're doing. | yes |
| `CLAUDE.md` | The assistant's instruction sheet, read at every start. | carefully |
| `MEMORY.md` | The table of contents for memory — pointers, never content. | carefully |
| `README.md`, `README.zh.md` | The front door for a newcomer, English and Chinese. | yes |
| `AGENTS.md` | The same instruction sheet for other AI programs. | carefully |
| `LICENSE` | The legal text (AGPL v3): free to use and change. | leave it |
| `context/` | Your own file "who I am" — thirteen sections, including "How to work with me" and "Withdrawn" — plus your goals, your priorities, its lessons and its mistakes. | carefully — your own file and goals are yours; cross a line out and it stays out |
| `knowledge/` | Your notes, linked to each other, on thirteen shelves: people, projects, concepts, decisions, research, tools, business, health, psychology, courses, overview pages, disagreements, memory pointers. | yes |
| `daily/` | One file per day. Ships empty. | yes |
| `state/` | "Where we stopped", a checkpoint per save, decisions, its search dictionary, two stamps for the tidy-up and the misses review. | carefully — not for hand-editing |
| `memory/svoboda/` | One blank form; your material goes in a subfolder named after you. | carefully |
| `inbox/` | *appears later.* Your drop-box for thoughts, links and files. Never opened unasked. | yes — that's the point of it |
| `reports/` | Finished things it wrote as separate files, including every misses review. | yes |
| `rules/` | Eleven hard rules plus a map of them. | carefully |
| `.claude/` | The machinery: settings that pre-approve ordinary operations, the three small helpers, the fifteen words it knows. | leave it |
| `scripts/` | Five small programs, including the search engine and the quote check. | leave it — safe to run again |
| `_templates/` | Eight blank forms: a day, a decision, a person, a project, a meeting, a plan, research, a claim ledger. | yes |
| `modules/`, `modules.yaml` | Optional add-ons and which are on. All off by default. | yes — you flip `enabled:` by hand |
| `assets/` | The logo files. | yes |
| `docs/` | The presentation in three languages, this guide, a page for builders. | yes |
| `state/current.md` | *appears later.* Where we stopped; its first forty lines are read out at every start. | carefully |
| `state/sessions/` | *appears later.* One checkpoint per saved conversation; the three newest are named at every start. | yes |
| `daily/YYYY-MM-DD.md` | *appears later.* Today's note; its last eight lines are read out at every start. | yes |
| `memory/svoboda/<you>/` | *appears later.* Your stories word for word plus your corrections — the only source of "you said" lines — the seven area cards and your profile. | carefully — the stories must stay verbatim |
| `.memory_venv/` | *appears later, only with search by meaning.* About a gigabyte of hidden helper files. Not your notes. | leave it |
| `pp.md`, `plan-fact.md`, `plans.md` | *appear later, only if you ask.* A dashboard you keep yourself, a plan-versus-fact journal, a roadmap. | yes |
| `projects/{name}/` | *appears later, when you make one.* For a project with real operational detail. | yes |


## Part 3. What happens under the hood

### At every start

A small helper runs by itself the moment you open the folder and pours in a short block before you type: up to forty lines of "where we stopped", the first section of your priorities, the last eight lines of today's note, and the three newest checkpoints by name. Before printing anything it bumps a counter of how often you have opened the folder, so a later failure can't lose the count.

Then two gates. *Tidy-up due*: a day has passed and you've opened the folder about five times since. *Reflection due*: about three days, measured from when the folder was set up if there's no earlier stamp. Those notices are instructions to the assistant, not to you — offer it in one sentence, in your language, never show the command name, run it only on your yes. At most one offer per start, the tidy-up first.

Before your first conversation it prints one line and stops: if your first message is `/start` it runs the setup, otherwise it answers in one plain sentence — this folder isn't set up yet, just type `/start` and I'll do the rest.


### When you save

In order: it re-reads the conversation for friction; turns your corrections about *how* to talk to you into at most two dated candidate lines for the "How to work with me" section, writing only what you agreed to; puts anything new about one of the seven areas into your stories as your exact phrase, plus one line on that area's card; summarises **all** the work not yet written down since the last save; gives genuinely new knowledge a page; updates "where we stopped" and today's note; writes the checkpoint; and saves a new version into the folder's history.

Those "How to work with me" lines are the one channel for manner: interface data, not conclusions about you, and they live in one place only. Conclusions about you go on the area cards. Last step: if the tidy-up or the misses review was due, it offers it in one sentence and runs it only on your yes.


### The tidy-up in detail

1. **Look first.** It reads its table of contents and "where we stopped" before writing anything. Its own instruction is blunt: summarising without reading first is a hallucination factory, and skipping this aborts the run.
2. **Gather.** The last three to seven days of notes, facts that have drifted, mistakes triggered recently, and narrow searches through recent conversations — never whole ones.
3. **Consolidate.** Merge into the existing file on the topic instead of leaving a near-copy; turn "yesterday" into real dates; delete what today disproved. Every link must point at something real or the write is refused.
4. **Prune.** Its table of contents goes back under its size limit: stale pointers out, long lines demoted, contradictions settled.
5. **Refresh search by meaning.** Only the changed files are re-read — seconds, not the half-hour a full rebuild takes. Skipped silently if it was never installed.
6. **Report.** It closes the gate, then says in at most fifteen lines what changed.

Never touched: your own words. Also forbidden — skipping step one, reading whole conversations, making near-duplicates, leaving two contradictory facts standing, and using anything over the internet. The gate closes with two stamps: the time it ran, and the counter reset to zero.


### Search by meaning

Optional, answered with one yes/no during your first conversation.

Your notes are cut into sections, each carrying the heading it sits under, so a question matches the *sense* of a passage rather than its exact words. One file of numbers, no database, nothing over the internet. It covers your notes, days, reports, your own stories and anything in `inbox`, and returns a shortlist with the matching section and a snippet — candidates to open, not the answer.

The cost: about a gigabyte of helper files **inside** the folder, hidden, plus about 300 megabytes downloaded once and kept **outside** it, in your system's hidden downloads area. Neither is your notes; both rebuild.

It is not running all the time: it wakes for your question, keeps the dictionary in memory so the next one is instant, sleeps after half an hour, and listens only to your own machine. Without it everything works and it searches exact words, telling you so once per conversation in one plain line.


### The quote check

Every line on a card that claims to be your words is checked word for word against your own stories before the card is shown. The check ignores capitals, punctuation and extra spacing, and looks in your stories folder including the file where your corrections land first.

Not found means it was the assistant's phrasing, not yours — so the line becomes "I heard … — right?". If anything comes back unverified the card is **not** shown until it is fixed and re-checked in the same conversation.

It sends nothing anywhere — a small local program using only what comes with Python. Without Python those "you said" lines are dropped, leaving "I saw in your files", "I think" and "I don't know": what cannot be verified is never passed off as your words. It works in English, Chinese and Russian.


### Earlier versions and getting things back

The folder keeps a history of every save, on your own disk. One unpacked from a download arrives with no history, so the first conversation starts one quietly. Every save and every misses review adds a version with a one-line summary.

You get things back by asking in plain words: "bring back yesterday's version of my goals file" · "show me how this file looked a week ago". The assistant uses the folder's history to do it. If it hesitates, say: *use the folder's history (git)*.

There is also a manual route that always works: move your old folder aside — your notes stay in it — unpack a fresh copy, and ask the assistant to bring your notes across.

### Copying, moving, resetting

Copy the folder and everything moves with it: every note, story and card, and the history of earlier versions. Delete it and your notes are gone; there is no second copy.

Two things live outside and don't travel: Claude Code's own record of the conversations, and the download for search by meaning. Neither is your notes. Everything inside finds its own way around by looking at where it is, so the same wiring works from any copy.

The rebuildable parts are safe to delete: the hidden gigabyte of helper files and the search dictionary both recreate, losing no data. Running the folder-builder again doesn't reset your content either: your goals are kept word for word, and a line you crossed out is never restored.


### What goes to the internet, what stays on your machine

**Goes out.** Your conversation, including the pieces of your notes it reads to answer you — the same as any text typed into an AI chat. Storage is on your side; the thinking happens on Anthropic's servers, which is why you need a connection while talking. The tidy-up is the assistant's own work, so those notes travel like anything else you write. Only with search by meaning: one download of about 300 megabytes, the cost stated before you answer.

**Stays here.** The search engine and the quote check never leave your machine. Your notes are plain files on your disk — no storage program, no server of ours, no account to create anywhere.

**Never written down.** A password, PIN, key, card number, security code, text-message code, recovery phrase or passport number never goes into any file, even if you dictate it and ask. That is a hard rule, not a promise. Only the fact without the secret — "has access to the bank".


### The rules it lives by

Eleven hard rules, each added only after the gentler version failed to stop that mistake returning. Three are always in force: plain language, honest reporting, no secrets in notes.

1. **Plain language first** — what a thing is and what it gives you, in ordinary words. Added after a person disengaged: "too clever, I didn't understand any of it."
2. **Honest reporting** — the result, not a flattering frame around it.
3. **No secrets in notes** — no password, key, card number, code or recovery phrase in any file, even dictated.
4. **Answer the question actually asked** — never the convenient nearby substitute.
5. **Orient before committing** — establish what is really being asked before answering or building.
6. **Match the cost to the job** — a personal tool is a tool, not a product.
7. **Corrections are permanent** — a correction carries forward, and anything live stays read-only until you ask.
8. **The work is the work** — what you called the main job *is* the job; other directions are opt-in.
9. **Don't ship what it cannot perceive** — nothing judged by sight, sound or feel goes out unchecked.
10. **This folder is local** — its earlier versions are a convenience for you, not a contract with anyone.
11. **Filenames are plain** — lower-case letters, digits, dashes and underscores.


### Optional add-ons

An add-on is a folder with a word in it, listed in `modules.yaml` with a switch, the folders it needs and its starter files. Everything is off by default and it ships with none of its own — only one worked example, switched off, so you can turn it on, watch the mechanism work, then replace it with your own.

## Part 4. Recipes

**Remember a person.**
1. "Write a page about Anna — she supplies the packaging, we met at the March fair."
2. It gives her a page, linked to something related, so she's findable later.
3. If a note already says otherwise, it shows you both versions instead of overwriting.

**Drop a file in.**
1. Put the file in the `inbox` folder.
2. Say "take a look in inbox" — it doesn't go looking by itself.
3. For a transcript: "read this into my notes", and it becomes pages.

**"Why did I decide X?"**
1. Just ask: "why did I drop that supplier?"
2. It finds your own note and reads it back — your reason, not a guess.
3. To make it findable next time: "write this decision down with the reason."

**It talks too much.**
1. Say it in the moment: "shorter" · "no tables unless I ask".
2. At the end it shows one or two lines it wants to write down about that.
3. Say yes and the manner survives every future conversation. Silence is not agreement.

**Erase something about me.**
1. Say "remove that line about me", or delete the line yourself.
2. A crossed-out line is never put back; a line you rewrote is never rewritten over.
3. To see what's there at all: "read me what you have about me."

**I moved to a new computer.**
1. Copy the whole folder across — notes, stories, cards, earlier versions.
2. Install Claude Code there, point it at the folder, open it.
3. If you had search by meaning: "set up search by meaning again" — no note lost.

**Something broke.**
1. Tell it in plain words what you see on the screen; it reads the same folder and fixes things.
2. For a verdict: "is anything broken in this folder?"
3. Worst case: move the old folder aside, unpack a fresh copy, ask it to bring your notes over.

**I want to redo one area of the first session.**
1. Say "let's go through Work again".
2. It re-cuts that one area against the old version, never from nothing.
3. Your words go into your stories first, then the card is edited.

**I want a page for my project.**
1. "Make a page for the new till system" — plus the facts you have.
2. It links the page where it belongs and checks something links *to* it.
3. When the project grows real detail: "give this project its own folder".

_For builders: `docs/methodology.md` (technical, English)._
