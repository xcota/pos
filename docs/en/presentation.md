# Camomile: what it is, how it works, how to use it

_Version 2 · September 2026_

_**This page** explains what it is and how it works. **The guide** explains every word, with examples, and what is inside the folder: `docs/en/guide.md` in your folder, or online at https://xcota.github.io/pos/en/guide.html._

**What it does on its own:** at every start it reads its own notes (who you are, where you stopped). Every few days it offers to tidy its memory and, separately, to go over its own misses — both only after your yes. Nothing else happens without you.

## What it is

Camomile is a folder on your computer plus an AI assistant that reads and writes that folder. The assistant itself lives in Claude Code — a program by Anthropic that opens in a command window — not in the folder. This same text is online, if you would rather read before downloading anything: https://xcota.github.io/pos/ (English · 中文 · Русский).

In an ordinary AI chat you start from zero every time: who you are, what you are doing, what you already decided. Here all of that sits in files on your own disk. The assistant looks into them at the start of a conversation and adds to them at the end. The longer you use it, the better it hits the mark — not because it "gets smarter", but because more is written down about you, in your own words.

**Who this is for.** Anyone who has used ChatGPT and wants more from AI than one-off answers. You do not write a single line of code, at any point.

What that looks like on an ordinary Tuesday: you talk over which supplier to drop and why — six months later you ask "why did I drop them", and the answer is your own note, not a guess. Or you come back after a fortnight away and ask "where did I stop with the new till system" — and it tells you, together with the reason you stopped there.

It only does anything while that window is open and you are typing in it. Close the window and nothing of it is working on your files — you can shut the computer down, and nothing happens until you open it again.

The name comes from the picture — think of a daisy: you in the middle, seven petals around you — Self-development (learning and growth), Vitality (body and energy), Surroundings (people and place), Wealth (what "enough" means to you — the feeling, not the figure), Rest (what restores you), Work (what you do), Assets (the money itself: income, savings, property, equipment, debts). Life is not one petal, so notes are kept on all seven, and over time you can see which ones are full and which ones you simply never talked about.

## What happens, step by step

### Day one: getting it on your computer

Four steps, four short things to type in all — the wait is however long the downloads take. The conversation that follows, where it gets to know you, is about fifteen minutes on top.

1. **Install Claude Code** — a program by Anthropic that opens in the window where computer commands are typed. On a Mac: press Command and the space bar together — a search box appears in the middle of the screen — type "Terminal" and press Enter. On Linux: that window is usually called Terminal too; open it from your applications list, or press Ctrl, Alt and T together. Then open Anthropic's page, https://code.claude.com/docs/en/setup, find the install line for your kind of computer, select it and copy it. Click into the command window, paste it (Command together with V, or Ctrl together with Shift and V on Linux), press Enter, and wait until text stops scrolling — a minute or two. You only ever do this once. It needs a paid Claude plan from Anthropic: Pro is the cheaper one and is enough to start.
2. **Download this folder.** https://github.com/xcota/pos → green "Code" button → "Download ZIP". The page is called "pos" — that is the right place, it is the older name of the same thing. If that page does not open where you live (in China, for example), the same folder is at https://gitee.com/cotya/pos-starter → "克隆/下载" → "下载 ZIP". Double-click the archive and a folder appears next to it, called `pos-main` or `pos-starter-master` — that is the one, the odd name is normal. Move it into your Documents, rename it "Camomile" if you like.
3. **Point the window at the folder.** Open your Documents folder so you can see it next to the command window. In the command window type `cd`, then a space, then drag the Camomile folder itself onto the window — the folder, not the zip file you downloaded — and press Enter. `cd` means "go to"; the long line with slashes that appears by itself is the folder's address — do not edit it. Then type `claude` and press Enter. The very first time, it opens your browser so you can sign in to your Claude account — sign in with the account your paid plan is on, then come back to the command window. It may also ask you to pick light or dark; either is fine. Then it asks whether you trust the files in this folder: answer Yes, it is your own folder. If it says `command not found`, close this window, open a new one the same way, and type `claude` again — a window opened before the install finished does not know about it yet. If it still says that, the install did not finish: redo step 1.
4. **Type `/start`** (with the slash) and press Enter. The last thing you need to know.

It worked if the window clears, a greeting appears, and there is a line at the bottom to type into. From there it is plain writing back and forth.

### The first session: it gets to know you

It asks what to call you and reads one short paragraph of what comes next: three stories, about fifteen minutes, a card per area for you to correct, then it builds your folder — and you can stop at any moment. It never asks you for a score. On each area it writes its own reading — a figure out of ten with how sure it is — and only where you told it enough. That figure is a guess for you to correct or cross out, not a grade. If you name a number yourself ("I'd give work an eight"), it writes it down as yours and says if it sees things differently; it simply never asks you for one.

It takes the manner from your very first answer: a short answer gets short questions, one at a time; your language and your register, strong words included, if you use them; the way you addressed it, first name or not; lists if you write in lists.

One yes/no question comes early: search by meaning. The cost is on the table before you answer — about one gigabyte of disk space, downloaded once, five to ten minutes. Say no and everything works, it just searches by exact words. Nothing is downloaded quietly. While you answer, it also quietly sets up two things in the folder: keeping earlier versions of your notes, and an `inbox` folder where you can drop your own files later.

Then three stories instead of a questionnaire: yesterday, from waking up to going to sleep; the last month — what you bought, what you regret, what you are glad about; what you learned this year and from whom. Your words are stored word for word, and they are the only thing ever quoted back to you.

For each area you get a card to check: numbered lines "you said" (your own words, checked against your own stories before the card is shown), "I saw in your files", "I think", then "I don't know" and "I heard X — right?". Its own reading for the area comes last, with how sure it is. You correct by number: "3 is wrong, what actually happened is…". A plain "yes" confirms only the "you said" lines — its conclusions stay guesses until you answer them by number. Said little about an area? Then no number at all, only "you didn't talk about this" — not a zero, not a "weak area".

After five areas the questions go deeper: what really makes you angry, a loss you have not got over, how being lonely differs from being alone, what counts as irreversible for you, what charges you up and what drains you. Any of these you can pass on — say you would rather not and it moves to the next one. Parents and childhood are a separate part, and optional in the same way.

It starts building your folder only after you have confirmed or corrected at least two cards — and two is enough: there is no point waiting for all seven areas. Disagreeing is fine, a correction counts as an answer; it just wants your yes or your fix on at least two cards before it writes anything down. Otherwise its own guesses get read back as facts in every later conversation.

Then it writes your files: who you are, how to work with you, your goals, starting tasks, a cover page with the seven areas, a "where to invest" list — only the areas you yourself called a hole, in your own words — and the record of the conversation itself. The whole portrait is written down as preliminary. And nothing is planned off its own numbers: a low reading of its own stays inside that area's card as its reading, and you are free to disagree by number.

At the end it asks you once to close it and open it again: type `/exit` and press Enter (or just close the window), then do the two lines from step 3 again — `cd` with your folder dragged in, then `claude`. That restart is the only thing you do by hand in the whole session.

A quick pass is about fifteen minutes. Everything deeper is not a second session you have to book — it accrues in ordinary conversations as you talk. Stop anywhere: it is all written down, so you come back, type `/start` again, and it continues from the same place instead of starting over.

### Every conversation after that

You open the same window the same way; the up arrow on your keyboard brings back what you typed last time. You do not have to remind it of anything. Before answering, it reads its own notes — who you are and how you like to be talked to, where you stopped, what you saved today — and picks up from there.

At the end, say "save this conversation". It writes down what was done and decided, adds two or three lines to today's note, gives genuinely new things their own pages, and — if something new about one of the seven areas came up in passing — puts one line into that area's card, in your words. It does not re-score the area and does not show the card again; a full re-do of an area happens only if you ask for one. If you forget and simply close the window, nothing that was already in your files is lost — only today's conversation goes unwritten. Say it next time and carry on.

### Every few days

Two things it raises itself, each in one sentence, each waiting for your yes.

**A tidy-up of its memory.** Notes pile up, repeat, go out of date. Every few days it will say its memory needs a few minutes of tidying and ask whether to do it now; you answer yes or later. What it does is its own bookkeeping: it merges its own repeated notes into the right files instead of leaving near-copies, puts real dates in place of "yesterday", drops its own notes that you have since corrected, shortens its own list of contents so it finds things faster, and refreshes search by meaning so new notes are found too. Your own words — the stories you told it — are not touched, and earlier versions of the files are kept, so anything can be brought back. Afterwards it reports in a few lines what it changed.

**A look at its own misses.** About every three days it offers to go back over the last days — where it misread you, where it produced too much, where it made you wait — and to write the lessons down so the same thing does not repeat.

### Whenever you need

Ask for something old in your own words: "where did I write about being tired in the mornings". With search by meaning it finds the note that says "wrecked after getting up"; without it, it searches exact words and tells you so plainly, once.

Ask why you decided something months ago and the answer is the note, not a guess. Hand it your day — thoughts, links, files — in words; or, for files, there is a folder called `inbox` inside your own folder: put them there and then tell it "take a look in inbox" — it does not go looking by itself. And correct it whenever it grates: "shorter", "don't ask me about that", "use my first name". Corrections like that are kept as rules about talking to you, never as conclusions about you; at the end it shows one or two lines it would like to write down, and keeps only what you agreed with. Silence is not agreement.

### What never happens

It never writes to you first, never reminds you, never runs on a schedule, never watches you. It does not ask you to score yourself. It does not install anything quietly. It does not praise you for answering, and does not explain things as if to a ten-year-old. It does not pass its own wording off as your words: a quote it cannot find in your stories turns into "I heard … — right?". It never copies a password, PIN, key, card number, code or recovery phrase into any file, even if you dictate one and ask it to. It never restores a line you crossed out or rewrites one you fixed by hand. And it never starts the tidy-up or the review of misses without your yes.

## Three things inside

**Memory — it remembers you between conversations.** Ordinary text files: who you are, what you are doing now, your goals, notes by day, pages about people and projects. It reads them at the start on its own; you say "save" at the end. No magic and no database: open a file in a text editor and you see ordinary text that you can edit yourself.

**Your work — it keeps your projects and decisions.** Each of your things gets its own page, and the pages link to one another — something like a small personal encyclopedia of your life. A person, a project, a decision, notes on something you read. Ask for a hard decision to be written down separately, with the reason, and six months later "why did I do that back then" has an answer instead of a guess.

**How it adapts to you — it keeps your corrections and stops repeating what you told it not to do.** This is the part an ordinary chat does not have. Your corrections about how to talk to you go into a "How to work with me" section of your own file, and that file is re-read at every start — so the manner is not lost when you close the window and open a new one the next day. What changes is the **form**, not the content: it still names the inconvenient facts and the gaps, only in the manner you showed it. The folder also arrives with more than forty common mistakes already taken apart: not about you, but about how AI assistants usually get things wrong — building instead of asking, writing in a clever-sounding way, claiming work they did not do. Those are written down in the folder in plain text, and it reads the ones that apply to what you are doing. On top of them it keeps your own corrections as you make them — nothing for you to fill in.

## What you type

Once at the very beginning: `/start` — and again if you broke off part-way through that first session; it carries on from the same place instead of starting over.

Three short words worth remembering afterwards. Type them exactly as they appear here, slash included:

| Word | What it does |
|---|---|
| `/session-save` | save this conversation into memory |
| `/recall` | find an old note |
| `/reflect` | go over the misses of the last few days — and, once you have a few conversations behind you, show what it has understood about your manner and what it still does not know |

Everything else is plain words: "save this conversation", "find where I wrote about…", "write down why I decided this", "shorter answers from now on". Both the tidy-up of its memory and the review of its misses it offers by itself — you only say yes or later. If you want to start the review yourself, the word for it is `/reflect`.

How each word works, step by step and with examples, and what is inside the folder: the guide — `docs/en/guide.md` in your folder, or online at https://xcota.github.io/pos/en/guide.html.

## Your data

Everything sits on your own disk, in that one folder, as ordinary text files — even a basic text editor opens them. There is no storage program and no server of ours on the internet. We do not register you anywhere: we have no accounts and there is nowhere to create one. The only thing that ever runs in the background is the local search, if you turned it on — it wakes for your question and goes back to sleep after half an hour, on your machine.

Your notes live only in that folder: copy it and all of them have moved to another computer. Separately, Claude Code keeps a record of the conversations themselves outside your folder, in its own service area — deleting your folder does not delete those; they go with Claude Code's own files.

Passwords, PINs, keys, card numbers, security codes, text-message codes, recovery phrases, passport numbers: you never need to give them, and a rule in the folder forbids writing any of them into any file — even if you dictate one yourself and ask for it to be saved. Only the fact without the secret ("has access to the bank"). If one is already sitting in a file, it tells you instead of quietly rewriting it.

An honest note about the internet: for the assistant to answer you, pieces of your notes are sent to Claude — the same as any text you type into an AI chat. Storage is on your side, the thinking happens on Anthropic's servers, and that is why you need a connection while you are talking. Nothing goes anywhere else: the search and the quote check run on your own machine. The tidy-up is done by the assistant itself, so those notes go to Claude like anything else you write to it.

Disk space, and only if you said yes to search by meaning: about one gigabyte in total, downloaded once. It sits partly in your folder and partly in your system's hidden downloads area — the assistant can show you both and delete them. Neither one is your notes, and both can be rebuilt later without losing a single note.

## Questions and answers

**What does it cost?** A Claude plan from Anthropic — that is where the assistant runs. Pro is the cheaper one and is enough to start; you buy it on Anthropic's own site. Plans come with a limit on how much you can use in a stretch: if you reach it, the assistant pauses for a few hours and then works again. No other payments, and nothing paid to us.

**Can I use it on a phone?** No. You need a computer: Mac or Linux. Windows is not supported yet — there is no version for it, you would waste an evening.

**What if I delete the folder?** Your notes are gone and nothing about you is remembered any more; there is no second copy of them. Two things live outside the folder and are not affected: the record of the conversations themselves, which Claude Code keeps in its own service area (that goes when Claude Code's own files go), and the downloaded dictionary for search by meaning, if you agreed to it — not your notes, but it takes up space.

**Can I write in English or Chinese?** Yes — it speaks the language you write in. If it cannot tell which one you want, it asks once.

**Do I have to go through the whole first session?** No. The first pass gives you a working basis and the rest is picked up as you go, in ordinary conversations. You can stop at any question, and parents and childhood can be skipped entirely.

**What does it write down about me, and how do I erase it?** What you told it, plus its own conclusions, marked as guesses. All of it is files you can open, read, edit and delete by hand — or just tell it: remove this. A line you fix or cross out yourself stays fixed.

**Does it diagnose me?** It builds a portrait: repeating reactions — how you behave when someone close pulls away, where you put the blame for a failure, what overload does to you — and where that came from, family included, if you talk about it. It is not therapy: no exercises, no homework, no "you should work on this". The portrait is yours to read and edit. Say you do not want it and it does not dig.

**Do I have to keep its memory in order myself?** No. It reads its own notes at every start; you say "save" at the end. The tidy-up and the review of misses it offers itself, and both wait for your yes. Say no and nothing breaks. It will ask once more when you save the conversation, and again the next time you open it, until you say yes.

**And if something breaks?** Tell it in plain words what you see on the screen. It reads the same folder and fixes things itself. Worst case: move your old folder aside — your notes stay in it — unpack a fresh copy, and the assistant can bring your notes across.

## What you need: the honest list

- A Mac or a Linux computer. Windows is not supported yet — there is no version for it, you would waste an evening.
- A paid Claude plan from Anthropic, Pro or Max — the only payment involved. Pro is enough to start.
- The Claude Code program, installed once.
- Two small helper programs, both free: Python and Git. You do not check this yourself: at the first start the assistant says in plain words whether anything is missing and gives you one line to paste — that is all it takes. Without Python you lose search by meaning and the check that the words it puts in your mouth are really yours (so those lines are left out of a card rather than guessed at), plus the check that the links between your notes still work; without Git you lose the safety net of earlier versions of your notes. Nothing else changes, nothing breaks, and no errors appear on your screen.
- This folder, downloaded and unpacked wherever suits you.
- Typing two lines into a command window once, and repeating them each time you come back.
- An internet connection the whole time you are talking to the assistant.
- About fifteen minutes for the first session; everything deeper accrues in ordinary conversations afterwards.
- **One yes/no question:** search by meaning — about one gigabyte of disk space, downloaded once, five to ten minutes. It finds your notes by the sense of your question instead of the exact words. Say no and nothing is downloaded; everything else works.

What you do **not** need: to program, to keep an account anywhere else, to run a server of your own.

## License

AGPL v3: using and changing it is free; if you build a service for other people on top of it, open up your changes too. Full text in the LICENSE file.
