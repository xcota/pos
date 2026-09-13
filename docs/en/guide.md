# Camomile guide: every word, and what is inside the folder

_Version 2 · September 2026_

> **Before you begin.** This guide assumes you have already downloaded Camomile, unzipped it and opened it in Claude Code — the program by Anthropic that reads this folder. If you haven't, the README has the click-by-click steps.
>
> **If anything ever goes wrong, just describe what you see on screen — it reads its own folder and fixes most things itself.**

**What it costs.** Camomile itself is free. Claude Code needs a paid Claude plan from Anthropic — Pro is the cheaper one and is enough; the current price is on Anthropic's site. That is the only money involved.

**Two words used throughout.**

- **Opening the folder** means starting Claude Code in it — the two lines from the README: `cd` with your folder, then `claude`. Not double-clicking the folder on your desktop.
- **A card** is what it shows you about one area of your life: a few numbered lines of what it heard, for you to read and correct. Nothing to fill in.

**How to stop.** Press `Esc` to interrupt an answer running too long. Type `/exit` to close the program. Everything you have already told it is already saved — type `/start` next time and it carries on from the same place.

You never have to type a command. Camomile works if you only write to it in ordinary words — it reads its own notes when a conversation starts and writes them down when it ends. Everything below can also be said in normal words; the four short words just save typing. If you never learn one, nothing is lost.

This page is for the other mood: when you want to know exactly what each word does and what is in the folder.

## Part 1. The words you type

Four are worth knowing. You type them into the same chat box where you write everything else, then press Enter. If you spell one wrong, nothing breaks — say the same thing in ordinary words instead ("save this conversation") and you get the same result.

### `/start`

**When.** Once, on a folder you have just unzipped — and again if you broke off part-way, to carry on from the same place.

**What you type.** `/start` (a bare `start` works too).

**What happens, step by step.**

1. It greets you, asks what to call you, and says what is coming: three stories, about fifteen minutes, one card per area of life for you to correct, then it builds your folder. The seven areas are Self-development (learning and growth), Vitality (body and energy), Surroundings (people and place), Wealth (what "enough" means to you), Rest, Work, and Assets (money and property). You can stop any time, and it never asks you to score yourself.
2. It takes its manner from your first reply — language, how you addressed it, length, lists or prose.
3. One yes/no question: should it be able to find your notes by what they mean, not only by the exact words you typed? (Ask "where did I write about being tired" and it finds a note that says "wrecked every morning".) The cost comes first: about 300 megabytes downloaded once, and about a gigabyte of space — roughly two hundred photos. Say no now, and say "turn on search by meaning" any time later.
4. Without asking, it starts keeping a copy of every earlier version of your notes, so nothing you write can be lost, and makes a folder called `inbox` for files you want it to read.
5. Three stories, one at a time — it asks, you answer, then it asks the next: yesterday from waking to sleep; the last month; what you learned this year. Each is saved word for word.
6. Then one card per area, corrected by number: "3 is wrong, what actually happened is…". If you just say "yes", only the lines that are your own words count as confirmed; anything it worked out itself stays a guess until you reply with the line number. If you told it enough about an area it may put its own number at the end of that card, with how sure it is — its reading, never a mark you give yourself.
7. Once you have corrected the first two cards, it builds your folder. Then it asks you to close it and open it again — the only thing in the setup you do by hand. Type `/exit`; then the two lines from the README: `cd`, a space, your folder dragged into the window with the mouse, Enter — then `claude`, Enter. The remaining five cards come after that.

**What you see.** An ordinary conversation: no technical text, no file locations, no error messages. A card looks like this:

> **Work**
> 1. You said: "the shop eats my mornings — I'm behind the till by seven."
> 2. You said: "I took the packaging supplier on myself, nobody else was going to chase them."
> 3. I saw in your files: Friday is your deadline with that supplier.
> 4. I think: the ordering, the till and the books are all on you, with nobody to hand them to.
>
> I don't know: whether you want the shop bigger, or just easier.
>
> I heard the evenings are worse than the mornings — right?
>
> How this area reads to me: a one-person business at full stretch, holding up, no slack in it. Fairly sure — it came up in all three stories.

You reply "4 is wrong, my sister does the books" — or just "yes".

**What it writes.** Your file "who I am", your words and its guesses kept apart · your goals · your front page with the seven areas · its memory index · the area cards · your stories word for word · a page about you in your notes · its own instruction sheet, written for you · and its guesses about your blind spots, turned into rules it holds itself to.


### `/session-save`

**When.** At the end of a conversation worth keeping, or when it has got long — it watches that itself and suggests saving when the time comes.

**What you type.** `/session-save`, and you can add a name for it — "save this as the supplier conversation" — which makes it easier to find later.

**What happens, step by step.**

1. First it re-reads the conversation as evidence about itself: where you corrected it, what you valued, where it missed.
2. If you corrected *how* it talks to you, it suggests one or two sentences for the "How to work with me" part of your file "who I am" — you say yes or no to each. Say nothing and it writes nothing.
3. If something new about one of the seven areas came up, your exact phrase goes into your stories and one line onto that area's card — without redoing the area or showing you the card again.
4. It summarises everything unwritten since the last save, hunting for work that exists only in the conversation; new knowledge gets a page.
5. It updates "where we stopped", adds two or three lines to today's note, and writes a hand-over note under 500 words: what is done, what is still to do, which files matter, where to continue.
6. It saves a new version into the folder's history. Then, if enough time has passed, it offers one of two things in one sentence: a tidy-up of its memory, or a look back at the mistakes it has made. Both happen only if you say yes.

**What you see.** A short report of what was saved, plus those one or two sentences awaiting your yes or no.

**What it writes.** Your file "who I am" (that one section) · your stories · one area card · today's note · "where we stopped" · new pages · its lessons and its list of mistakes · a hand-over note.

**Example.**

> **You:** save this conversation
> **It:** Saved: the supplier decision and why, the two prices, Friday as the deadline. Where-we-stopped says you're waiting on their reply.
> **It:** One for your yes or no — you twice told me to stop asking follow-ups. Write down "no follow-ups unless I ask for options"?
> **You:** yes
> **It:** Written. Also: my memory is due a tidying — now or later?


### `/recall`

**When.** You want something you wrote before and no longer remember the words you used.

**What you type.** `/recall` and your question, in your own words.

**What happens, step by step.**

1. It checks whether search by meaning is set up here — quietly, in the background; it won't interrupt you to ask permission.
2. If it is, it searches by meaning: back comes a shortlist of likely notes, each with the section that matched and a few words of it.
3. If it isn't set up, it looks for the exact words instead and says so once per conversation in one plain line: search by meaning isn't set up here, say the word if you want it on. If it is set up but falls over, it switches to exact words without saying anything — you never see an error full of file locations.
4. A shortlist is not an answer — so it opens the two or three most likely and reads you the relevant bit.

**What it writes.** Nothing of yours — it only reads your notes. (Search by meaning keeps its own scratch log next to its dictionary.)

**Example.**

> **You:** `/recall` where did I write about being wrecked in the mornings
> **It:** Closest is your story about yesterday: "woke at six, felt like I'd been hit by a bus." There's also a line in your Vitality card from July — mornings are the worst part of the day, and you'd stopped eating after nine that month.


### `/reflect`

**When.** About every three days. It measures that itself, offers it in one sentence, and runs only on your yes. You can also ask any time.

**What you type.** `/reflect`.

**What happens, step by step.**

1. It gathers the last three to five daily notes, recent decisions, its lessons, the recent saves, and its list of mistakes — the running list of ones it caught itself making, kept so it stops repeating them.
2. Mostly it re-reads the conversations themselves — what you said, what it answered, and the places where the two of you got stuck.
3. About you: what you valued or disliked, what you needed and didn't say — each becomes a suggested line for your file "who I am". About itself: where it went off and did something you hadn't asked for, started building before it understood the question, gave you far more than you wanted, or kept you waiting — each becomes an entry on its list of mistakes.
4. It draws out lessons, proposes changes, checks whether your goals still hold, and files a short report.
5. Then it reads back to you, in your language, three to five plain lines: what it understands about how you like to be talked to, what it still doesn't know about that, and the one or two misses it won't repeat. It asks you nothing — a mirror, not a questionnaire.

**What you see.** A compact, unflattering report, then those few lines. Its own instruction: be honest, don't sugarcoat failures.

**What it writes.** Its lessons · its list of mistakes, where one that turns up three times or more gets written into the folder's rules so it can't happen again · your goals, if your timescales changed · a dated report · the date it ran, so it knows when to do this next.

**Example.**

> **You:** `/reflect`
> **It:** Two misses in three days: Tuesday I built a table when you asked for one number; Wednesday I asked three questions before answering yours.
> **It:** What I think I know: short answers first, no tables unless asked, and you'd rather hear something is missing than get a guess. What I don't know yet: whether you want me to push back when I disagree.
> **It:** The two I won't repeat: no tables you didn't ask for, and answer before I ask.


### What it offers by itself

Two things, each in one sentence, each waiting for your yes. Never more than one offer each time you open the folder.

**A tidy-up of its memory.** Both conditions must be true: a day has passed since the last one, *and* you have opened the folder about five times since. Then it says its memory needs a few minutes of tidying and asks whether to do it now. Six steps:

1. It reads what is already written before touching anything.
2. It gathers the last few days and the facts that have drifted out of date.
3. It merges its repeated notes into the proper file instead of leaving near-copies, turns "yesterday" into real dates, and deletes facts it has found wrong.
4. It shortens its own memory index.
5. It refreshes search by meaning.
6. It reports what changed.

It never touches your own words — your stories and the "you said" lines on the cards are off-limits to it by its own rules; it tidies only what it wrote itself, and earlier versions are kept. Say "later" and nothing breaks — it asks again when you save, and next time you open the folder. If you never want it to ask at all, say "stop offering to tidy up" (or "never ask me that"): it writes that down in your file "who I am", and from then on it tidies only when you ask.

**A look at its own misses.** About every three days — the review under `/reflect` above, offered the same way: one sentence, and only on your yes.


### More words, if you ever want them

None of these seven are needed — you can ask for any of them in plain words.

**`/ingest`** — turns a transcript, a chat export, notes or a YouTube link into pages in your notes. Video needs a small free program called yt-dlp: ask "do I have yt-dlp?" and it checks and walks you through installing it. With no subtitles it never invents a transcript — it asks you to paste one.

**`/query`** — for a question needing several notes joined up. It answers directly, says which note each claim came from, then files the answer as a page.

**`/graph-add`** — gives a person, project or decision a page of its own. If an existing note says otherwise, it files both versions and tells you.

**`/self-check`** — the health of the folder: eight things scored, a total out of sixteen — out of fourteen on a new folder, where "projects" doesn't count yet. It lists the problems worst first, with a fix for each.

**`/lint`** — the health of the notes: pages nothing links to, claims nobody has checked in a month, the same number stated two ways. It reports; it doesn't silently fix.

**`/enable-modules`** — switches on an add-on, laying down starter files only where nothing exists, never over what you filled in. You don't need the word: just say "turn on the fitness add-on".

**`/compress`** — squeezes a long conversation into about one page, then checks that no file name, number or person's name got lost on the way.


### Words it uses itself — you may see these names go by

You never type these; they just go by in its replies sometimes, so here is what they are.

- **`/session-start`** — the ordinary start. One of the three background scripts does this by itself whenever you open the folder.
- **`/dream`** — the tidy-up of its memory. You answer yes to the offer; you never need the word.
- **`/svoboda-profiler`** — the part that runs your first conversation, the one that asks for your three stories. (*Svoboda* is Russian for freedom; it is just a name.) "Let's go through Work again" reaches it too.
- **`/vault-scaffolder`** — the part that builds your folder. `/start` calls it for you.

### Saying it in plain words

| What you want | What to say |
|---|---|
| Save this conversation | "save this conversation" |
| Find an old note | "find where I wrote about being tired in the mornings" |
| Remember a person | "write a page about my supplier Anna" |
| Read files you dropped in | "take a look in inbox" |
| Shorter answers | "shorter" / "answer first, explain if I ask" |
| Stop asking about something | "don't ask me about that" |
| Stop the tidy-up offers for good | "stop offering to tidy up" |
| Redo one area of life | "let's go through Work again" |
| Tidy its memory now | "tidy your memory now" |
| An earlier version of a file | "bring back yesterday's version of my goals file" |
| Turn on search by meaning later | "turn on search by meaning" |
| Turn on an add-on | "turn on the fitness add-on" |
| How healthy the folder is | "is anything broken in this folder?" |
| Erase something about you | "remove this line about me" |

## Part 2. What is inside the folder

All ordinary text files — open any of them in whatever text editor your computer came with.

| Name | What it holds | Yours to edit? |
|---|---|---|
| `HOME.md` | Your front page: where you're heading, the seven areas, what you're doing. | yes |
| `CLAUDE.md` | The assistant's instruction sheet, read every time you open the folder. | leave it — rewritten from scratch when the folder is rebuilt |
| `MEMORY.md` | An index of its memory — one line per topic saying where the real note lives, like the index at the back of a book. The writing itself is in the other files. | carefully |
| `README.md`, `README.zh.md` | The front door for a newcomer, English and Chinese. | yes |
| `AGENTS.md` | A second, parallel instruction sheet for AI programs other than Claude Code — kept in step with `CLAUDE.md` by hand. | carefully |
| `LICENSE` | The legal text (AGPL v3): free to use and change. | leave it |
| `context/` | Your file "who I am" — twelve sections, including "How to work with me" and "Withdrawn" — plus your goals, your priorities, its lessons and its list of mistakes. | carefully — your file and goals are yours; cross a line out and it stays out |
| `knowledge/` | Your notes, linked to each other, on thirteen shelves: people, projects, concepts, decisions, research, tools, business, health, psychology, courses, overview pages, disagreements, index entries. | yes |
| `daily/` | One file per day, named by the date — `daily/2026-09-13.md`. Starts empty; the last eight lines of today's are read back every time you open the folder. | yes |
| `state/` | "Where we stopped" — its first forty lines are read back every time you open the folder — one hand-over note per saved conversation, decisions, its search dictionary, and the dates of the last tidy-up and misses review. | no — Camomile keeps these for itself, leave them alone |
| `memory/svoboda/` | A blank form, and a subfolder named after you: your stories word for word plus your corrections (the only source of "you said" lines), the seven area cards and your profile. | carefully — the stories must stay as you said them |
| `inbox/` | *appears later.* Your drop-box for thoughts, links and files. It won't work through what you drop there until you ask — but a search does look inside it. | yes — that's the point of it |
| `reports/` | Finished things it wrote as separate files, including every misses review. | yes |
| `rules/` | Eleven hard rules plus a map of them. | carefully |
| `.claude/` | The working parts: its settings, the three background scripts, and all fifteen words from Part 1. Nothing here is meant for you. | leave it |
| `scripts/` | Four small programs for you — search by meaning, the part that installs it, and the quote check — plus one the makers use to publish the project, which does nothing useful in your copy. | leave it — Camomile runs the four itself when it needs them |
| `_templates/` | Eight blank forms: a day, a decision, a person, a project, a meeting, a plan, research, and a list of things you've claimed are true with the evidence for each. | yes |
| `modules/`, `modules.yaml` | Optional add-ons and which are on. All off to begin with. | just ask: "turn on the fitness add-on" |
| `assets/` | The logo files. | yes |
| `docs/` | The presentation in three languages, this guide, a builders' page. | yes |
| `.memory_venv/` | *appears later, only with search by meaning.* About a gigabyte of hidden helper files. Not your notes. | leave it |
| `pp.md`, `plan-fact.md`, `plans.md` | A one-page overview of what you're tracking, a journal of plan against outcome, and a list of what's coming next — laid down blank when it builds your folder. Fill them in or delete them. | yes |
| `projects/{name}/` | *appears later, if you ask for one.* For a project with real detail. | yes |

Nothing you type into a file can break Camomile permanently: every earlier version is kept, and you can always say "bring back yesterday's version of this file". "Carefully" just means these are read as instructions, so an edit that confuses you will confuse it too.


## Part 3. For the curious: what it does behind the scenes

### Every time you open the folder

Before you have typed a word it has already read a short block about you: where you stopped, the top of your priorities, the last lines of today's note, the three newest hand-over notes. That is why it never asks who you are. On a folder that isn't set up yet it prints one line instead: type `/start`.

It also checks two things about timing: whether a tidy-up is due (a day since the last one, and about five openings of the folder since) and whether a look at its mistakes is due (about three days). If one is, you get one sentence asking whether to do it now — at most one offer, the tidy-up first, nothing without your yes. If you have told it never to ask, it doesn't offer at all and waits for you to ask.


### When you save

You see a short report of what went into the notes, and one or two sentences waiting for your yes or no; on disk, the files listed under `/session-save` plus a new version in the folder's history. Those "How to work with me" lines only ever record how you like to be spoken to — short answers, no tables, use my first name. They never record opinions about you as a person; those go on the area cards.


### The tidy-up in detail

You see one sentence asking, and at the end a report of at most fifteen lines. In between, the six steps from Part 1 — with three things worth knowing. It reads what is already written before it writes anything: summarising without reading first is how a program starts making things up, so if it can't read first it stops instead. A line whose link would lead to a note that doesn't exist isn't saved at all. And refreshing search by meaning re-reads only the files that changed, a few seconds — building it from scratch takes much longer, but that happens only when you first switch it on, and runs in the background while you carry on. Your own words are never touched: your stories and the "you said" lines on the cards are outside the sweep by its own rules — it tidies only what it wrote itself.


### Search by meaning

Your notes are cut into sections, each carrying the heading it sits under, so a question matches the *sense* of a passage rather than its exact words. It covers your notes, your days, reports, your own stories and anything in `inbox`. It all lives in one extra file on your own disk, and nothing is sent anywhere. The space it takes — about a gigabyte of hidden helper files inside the folder, plus the 300-megabyte download kept outside it — is not your notes, and both parts can be deleted and rebuilt.

It isn't running all the time: it wakes when you ask something, stays ready for half an hour so the next question is instant, then sleeps. It can't be reached from outside your own computer.


### The quote check

Before a card is shown to you, every line on it that claims to be your words is checked word for word against your own stories; capitals and punctuation are ignored. If the words aren't there it was the assistant's phrasing, so the line becomes "I heard … — right?" instead. If anything can't be checked, the card is **not** shown until it is fixed.

It sends nothing anywhere, and works in English, Chinese and Russian. It uses Python, which most computers already have — ask "do I have Python?" and it will check. Without Python those "you said" lines are dropped, leaving "I saw in your files", "I think" and "I don't know": what can't be verified is never passed off as your words.


### Earlier versions and getting things back

The folder keeps a history of every save on your own disk, using a standard free tool called git; a folder fresh from a download has none, so the first conversation quietly starts one. You get things back by asking in plain words: "bring back yesterday's version of my goals file" · "show me how this file looked a week ago". It has a written procedure for this: it finds the version by date, reads you the earlier text first so you can see what you would be getting, and only on your yes puts that one file back — never the whole folder, never a file you didn't name. The version you had is kept in the history too, so you can change your mind. If it hesitates, tell it: the folder keeps its own history (git) — use that. There is also a manual route that works even when nothing else does: the three steps are in Part 4, under "Something broke".

### Copying, moving, resetting

Copy the folder and everything moves with it: every note, story and card, and the earlier versions. Delete it and your notes are gone; there is no second copy. You can put the folder anywhere on any computer and it still works. Two things live outside it and don't travel: Claude Code's own record of the conversations, and the download for search by meaning — neither is your notes, and both rebuild. Running the folder-builder again doesn't reset your content: goals are kept word for word, and crossed-out lines stay out. The one exception is the assistant's own instruction sheet, `CLAUDE.md` — that is rewritten from scratch every time, so keep anything you added to it somewhere else.


### What goes to the internet, what stays on your machine

**Goes out.** Your conversation, including the pieces of your notes it reads to answer you — the same as any text typed into an AI chat. Storage is on your side; the thinking happens on Anthropic's servers, which is why you need a connection while you talk. Only with search by meaning: that one 300-megabyte download, the cost stated before you answer.

**Stays here.** Search by meaning and the quote check never leave your machine. Your notes are plain files on your disk — no storage program, no server of ours, no account anywhere.

**Never written down.** A password, PIN, key, card number, security code, text-message code, recovery phrase or passport number never goes into any file, even if you dictate it and ask. That is a hard rule, not a promise. Only the fact without the secret — "has access to the bank".


### The rules it lives by

Eleven hard rules. Most were added only after the gentler version failed to stop that mistake coming back; one — no secrets in notes — was written straight in, to put a rule behind a promise the package had already made. The first three are always in force.

1. **Plain language first** — what a thing is and what it gives you, in ordinary words.
2. **Honest reporting** — the result, not a flattering frame around it.
3. **No secrets in notes** — no password, key, card number, code or recovery phrase in any file, even dictated.
4. **Answer the question asked** — never the convenient nearby substitute.
5. **Work out what is really being asked** — before answering or starting to build.
6. **Match the cost to the job** — a personal tool is a tool, not a product.
7. **Corrections are permanent** — once you correct it, it stays corrected, and it won't change what you're working on unless you ask.
8. **The work is the work** — what you called the main job *is* the job; other directions are yours to invite.
9. **Won't judge what it can't see or hear** — anything to be looked at or listened to comes back to you instead of being guessed at.
10. **This folder is local** — its earlier versions are a convenience for you, not a contract with anyone.
11. **Filenames are plain** — a housekeeping rule for its own files: lower-case letters, digits, dashes and underscores. Nothing for you to do.


### Optional add-ons

An add-on teaches Camomile one extra subject — fitness, say, or bookkeeping. They are all switched off to begin with, and it comes with none of its own: just one worked example, off, so you can turn it on, watch how it works, then replace it with your own. Ask "what add-ons are there?" for the list, and "turn on the … add-on" to switch one on.

## Part 4. Recipes

**Remember a person.**
1. "Write a page about Anna — she supplies the packaging, we met at the March fair."
2. It gives her a page, linked to something related, so she's findable later.
3. If a note already says otherwise, it shows you both versions instead of overwriting.

**Drop a file in.**
1. Put the file in the `inbox` folder.
2. Say "take a look in inbox" — it won't work through what's there until you ask, though a search does look inside.
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
1. Say "remove that line about me" and it moves the line into the "Withdrawn" part of your file with a date: it stops counting, but it is still written down. To have it gone altogether, delete the line yourself.
2. A crossed-out line is never put back; a line you rewrote is never rewritten over.
3. To see what's there: "read me what you have about me."

**I moved to a new computer.**
1. Copy the whole folder across — notes, stories, cards, earlier versions.
2. Install Claude Code there (Anthropic's instructions: https://code.claude.com/docs/en/setup), then open the folder the same way as at home: a command window, `cd` with the folder dragged in, then `claude`. If that means nothing to you, the README has the click-by-click version.
3. If you had search by meaning: "turn on search by meaning again" — no note is lost.

**Something broke.**
1. Tell it in plain words what you see on screen; it reads the same folder and fixes most things itself.
2. For a verdict: "is anything broken in this folder?"
3. Worst case, the manual route, which always works:
   1. Rename your old folder to `camomile-old`. Your notes stay in it, untouched.
   2. Download Camomile again: open https://github.com/xcota/pos, press the green "Code" button and choose "Download ZIP" (or https://gitee.com/cotya/pos-starter if GitHub doesn't open for you), and unzip it.
   3. Open the new folder and say: "my old folder is next to this one, called camomile-old — bring my notes across."

**I want to redo one area of the first session.**
1. Say "let's go through Work again".
2. It rewrites just that one card, starting from what it already had rather than from a blank page.
3. Your words go into your stories first, then the card is edited.

**I want a page for my project.**
1. "Make a page for the new till system" — plus the facts you have.
2. It links the page where it belongs and checks something links *to* it.
3. When the project grows real detail, ask for it — "put this project in its own folder with its own notes" — and it sets one up by hand, named the way the folder names things.

_For builders: `docs/methodology.md` (technical, English)._
