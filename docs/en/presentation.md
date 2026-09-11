# Camomile: what it is, how it works, and how to use it

## What it is

Camomile is a folder on your computer plus an AI assistant that reads and writes that folder.

In an ordinary AI chat you start from zero every time: who you are, what you are doing, what you already decided. Here all of that sits in files on your disk. The assistant looks into them at the start of a conversation and adds to them at the end. The longer you use it, the better it hits the mark — not because it "gets smarter", but because more is written down about you, in your own words.

The name comes from the picture. You are in the middle, seven petals around you, and each petal is one area of life:

- **Self-development** — what you are learning and where you are growing
- **Vitality** — body, sleep, energy, how you feel
- **Surroundings** — the people close to you: family, friends, partners; and the place where you live
- **Wealth** — what "enough" means to you and how you will know it has arrived
- **Rest** — how you recover and what you enjoy
- **Work** — your job, your projects, whatever you are seriously busy with
- **Assets** — money and property: income, savings, housing, equipment, debts

Inside the files these seven keep their original Russian names (`samorazvitie`, `vitalnost`, `okruzhenie`, `bogatstvo`, `otdyh`, `delo`, `aktivy`) — they are internal labels, nothing you have to read or type; in the original their first letters spell the word for "freedom".

The point of the daisy is simple: life is not one petal. The assistant keeps notes on all seven, and over time it becomes visible which ones are dense and which ones you simply never talked about.

## How it works

Three things make up the whole system.

### 1. Memory — it remembers you between conversations

Mechanics, no miracles. The folder holds ordinary text files: "who I am", "what I am doing now", "my goals", notes by day, cards about people and projects. At the start of every conversation the assistant reads those files — that takes it seconds. At the end, when you say `/session-save` (or just "save this conversation"), it writes down what was done and decided.

That is all. No magic and no database: open a file in a text editor and you see ordinary text that you can edit yourself.

There is also **search by meaning** — when you ask "where did I talk about being tired in the mornings" and the note says "wrecked after getting up", and it still finds it. Nobody installs it silently: right at the start of the first session the assistant asks one yes/no question and says honestly what it costs — about one gigabyte of disk space and five to ten minutes to download. Say no and nothing is downloaded, search works by exact words, everything else works as usual. If the install fails (it happens), nothing breaks either — it says so in one line and moves on.

### 2. Your work — it keeps your projects and decisions

The assistant gives each of your things its own page and links the pages to each other — something like a small personal encyclopedia of your life. A person, a project, a decision, notes on something you read: each gets its own card.

When you make a hard decision, you can ask for it to be written down separately: what you decided and why. Six months later the question "why did I do that back then" has an answer instead of a guess.

### 3. The mirror — it notices your corrections and adjusts

This is the part an ordinary chat does not have. When you correct the assistant — "too long", "don't ask two questions at once", "use my first name" — the correction goes into the "How to work with me" section of your "who I am" file, and it re-reads that file every time it starts. So the manner is not lost when you close the window and open a new one the next day.

It does not do this silently: when you say "save" at the end of a conversation, it shows one or two candidate lines for that section and writes down only what you agreed to. Stay quiet and nothing is written. And the other way round: a correction about how to talk to you stays a correction about how to talk to you — it never turns into a conclusion about you as a person.

Every few days you can type `/reflect`, and it goes over the recent days of work and pulls out lessons.

To be honest about it: the folder already contains more than forty common mistakes taken apart, plus a set of rules — not about you, but about how AI assistants usually get things wrong (start building instead of asking, write in a clever-sounding way, claim work they did not do). So the assistant arrives already trained, and from there you finish the job.

## Getting started

What you will see on screen, step by step. The same four steps as in the README — there are no others.

**Step 1. Install Claude Code.** Claude Code is a program made by Anthropic: it starts in a command window, and inside that same window you write back and forth with the assistant, just like an ordinary chat. Inside it, the assistant is allowed to read and write files in your folder. A paid Claude plan (Pro or Max) is required — you pay Anthropic for it. Instructions: https://code.claude.com/docs/en/setup — there is one command there that you paste into a command window (step 3). You install it once.

**Step 2. Download the folder and unpack it** — into your Documents, for example. The page: https://github.com/xcota/pos (green "Code" button → "Download ZIP"); if GitHub does not open, the same folder is at https://gitee.com/cotya/pos-starter (button "克隆/下载" → "下载 ZIP"). After unpacking, the folder is called `pos-main` or `pos-starter-master` — you can rename it to "Camomile".

**Step 3. Open the folder in Claude Code.** You need the window where commands are typed (on a Mac it is called Terminal; find it through the computer's search). Two lines go in there. The first: `cd`, a space, and the folder dragged in with your mouse — then Enter. `cd` means "go to": you are telling the window which folder to work with from now on. When you drag the folder in, a long line with slashes appears by itself — that is the folder's address, it is supposed to look like that, do not edit it. The second line: `claude` and Enter. If the answer is `command not found`, the program is not installed — go back to step 1.

**What success looks like.** The window clears, the program's greeting appears, and at the bottom there is a line you can type into. That is it — from here it is simply writing back and forth: you type a sentence, press Enter, read the answer.

**Step 4. Type `/start`.** One word. From here the assistant leads.

**Coming back tomorrow.** The same two lines in the same window: `cd` with your folder, then `claude`. The up arrow on your keyboard brings back what you typed last time. And one thing in advance: at the end of the first session the assistant asks you once to close it and open it again — those are the same two lines.

## The first session: getting acquainted

The assistant asks you about yourself — as an ordinary conversation, one question at a time, not a ten-page questionnaire.

How it goes today:

- **The start.** It asks what to call you and explains in one paragraph what is about to happen. Then one yes/no question: install search by meaning, and straight away what it costs (about a gigabyte of disk space, five to ten minutes). It downloads nothing silently.
- **Three stories instead of a questionnaire.** You are not asked to rate yourself: yesterday, from waking up to going to bed; the past month — what you bought, what you regret, what you are glad about; what you learned over the past year and from whom. That is enough to cover all seven areas. The stories are saved word for word.
- **A card per area, for you to check.** Numbered lines "you said" (your own words, word for word, checked against your own stories), "I saw in your files", "I think", then "I don't know" and "I heard '…' — right?", and as the last line its number with a confidence level. You correct by number. For an area you barely talked about there is no number at all — "you didn't talk about this".
- **Questions that go deeper.** After five areas the questions change character: what really makes you angry, what you lost and could not digest, how being lonely differs from being alone, what counts as irreversible for you. This is not a test — it is an ordinary conversation, just not a shallow one.
- **Parents and childhood** are a separate part, and it is **optional**. Say you would rather not, and the session moves on.
- **The portrait.** Out of all this it puts together a description: how you are built, where your strong spots and blind spots are, how you usually decide. It only starts building the folder after you have confirmed or corrected at least two cards — it does not build on unchecked conclusions.
- **Building the folder.** Then it builds your folder: the "who I am" file, your goals, starting tasks, a cover page with the seven areas. And it asks you once to close it and open it again.

How long it takes. A quick pass, enough to start working, is about fifteen minutes. The full thing, with all the deeper questions, takes noticeably longer — several sittings. You can stop anywhere: everything is already written down, so you come back and type `/start`.

## What changes as you use it

The more conversations you have saved, the less you have to re-tell yourself: the assistant already holds what you are working on, what you put aside and who is around you. Old decisions are one question away. The "How to work with me" section grows on your own corrections — and the conversation gets more accurate than it was on day one. We promise no timeline here: the speed depends only on how much you have said and saved.

What will **not** happen: the assistant will not write to you on its own, will not remind you about your tasks, and will do nothing without your word. It sets no schedules and does not watch you. Everything happens only when you open a conversation and ask for something. Three commands worth remembering (type them straight into the conversation, with a slash in front): `/session-save` — save the conversation into memory, `/recall` — find something old, `/reflect` — go over the misses of the last few days. You can also just ask in plain words: "save this conversation", "find where I wrote about…".

## Questions and answers

**Where is my data?** On your disk, in this folder, as ordinary text files. There is no separate storage and no server of ours. We do not register you anywhere: we have no accounts and there is nowhere to create one — the only subscription is with Anthropic, for the Claude Code program itself.

**What about passwords?** You do not need to give the assistant passwords, keys or card numbers, and it does not copy them into your files even if you mention them in conversation — that is written into its rules.

**Does anything go to the internet?** Yes, and it matters that you know it. For the assistant to answer, pieces of your notes are sent to Claude — as with any text you type into an AI chat. They go to no other service, but saying "everything stays on your computer" would not be true.

**What does it cost?** A paid Claude plan from Anthropic (Pro or Max) — that is where the assistant runs, and you pay Anthropic for it. No other payments, and nothing paid to us.

**Can I use it on a phone?** No. You need a computer: Mac or Linux. Windows is not supported yet.

**What if I delete the folder?** Your notes are gone: the assistant remembers nothing about you any more, and there is no copy anywhere. The only thing left outside the folder is the downloaded dictionary for search by meaning, if you agreed to it — about a gigabyte; that is not your data, but it takes up space. The flip side of the same thing: copy the folder and all your notes have moved to another computer.

**Can I use English or Chinese?** Yes — the assistant speaks the language you write in. If it is not sure which one you want, it asks once.

**Do I have to go through the whole first session?** No. The first pass gives you a working basis, the rest is picked up as you go. You can stop at any question, and the part about parents and childhood can be skipped entirely.

**What does it write down about me, and how do I erase it?** What you told it, plus its own conclusions. All of it is files you can open, read, edit and delete by hand. Or just tell it: remove this.

**Does it diagnose me?** It builds a psychological portrait: it notices repeating reactions — how you behave when someone close pulls away, where you put the blame for a failure, what overload does to you — and where that came from, including family, if you talk about it. It does not say labels out loud, but it does put its conclusions into your "who I am" file. The portrait is yours: you read it and you edit it. If you do not want this, tell it, and it will not dig.

**What does the assistant not do?** It does not write first, does not remind you, does not work on a schedule, does not go online on your behalf unasked, sends nothing to anyone, and does not claim work it did not do — if it did not do something, or is unsure, it says so.

**And if something breaks?** Tell it in plain words what you see on the screen. It reads the same folder and fixes things itself. Worst case: unpack the folder again and go through the first session once more.

## What you need: the honest list

- A Mac or a Linux computer. Windows is not supported yet.
- A paid Claude plan (Pro or Max) from Anthropic.
- The Claude Code program, installed.
- Two helper programs, both free: Python and Git. On a Mac they are usually already there. Without Python there is no search by meaning and no quote self-check (in that case it simply does not show the "you said" lines) — but nothing breaks and you will not see errors on screen.
- Being able to type two lines into a command window once — and to repeat them each time you come back.
- An internet connection the whole time you are talking to the assistant.
- About fifteen minutes for the first session. Going deeper takes several sittings.
- **One yes/no question:** search by meaning. The assistant asks right at the start and tells you what it costs: about a gigabyte of disk space, five to ten minutes. It lets you find your own notes by the sense of your question instead of the exact words. Say no and nothing is downloaded, everything else works.
- **Optional:** going through a YouTube video. That needs a separate free downloader program. Without it you can still work through chats, notes and summaries.

What you do **not** need: to program, to keep accounts anywhere else, to run a server.
