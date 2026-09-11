![Camomile](assets/logo/camomile-wordmark.png)

English · [中文](README.zh.md) · [Русский](docs/ru/README.md)

# Camomile

**A folder on your computer where an AI assistant remembers you: what you are doing, what you decided, and how you want to be talked to.**

An ordinary AI chat forgets everything the moment you close the window. Every time you explain again who you are, what you are working on, what you agreed last time. Here the assistant writes all of that into files on your own disk and re-reads them at the start of every conversation.

**Who this is for.** Anyone who has heard of ChatGPT and wants more from AI than one-off answers. You do not need to write a single line of code.

## What you get

- **You stop introducing yourself.** You open a conversation and the assistant already knows what you are working on, what you decided last Tuesday, and why.
- **Nothing gets dropped.** Put something aside for a month, come back, ask "where did I stop" — the answer is there, together with the reason you put it aside.
- **Old decisions can be found again.** "Where did I write down why I turned down that apartment" — it finds it, even if you wrote it in completely different words back then. That is search by meaning: right at the start the assistant asks one yes/no question about whether to install it, and tells you honestly how much disk space and time it costs. Say no and search works by exact words instead — records phrased differently will not be found.
- **Your rules for the conversation stick.** "Don't write so much", "don't ask two questions at once", "use my first name" — these go into a "How to work with me" section of your "who I am" file, and the assistant re-reads that file every time it starts. When you say "save" at the end of a conversation, it shows you one or two candidate lines for that section and writes down only what you agreed to.
- **No rating yourself on a scale.** Nobody asks you to give yourself a score for "health" or "money". You just talk, the way you would to a friend — the assistant does the sorting and shows you its reading so you can check it.
- **You can see how life is going as a whole.** Seven areas: Self-development (learning and growth), Vitality (body and energy), Surroundings (people and place), Wealth (what "enough" means to you), Rest (what restores you), Work (what you do), Assets (money and property). Each area has a card: you can see what you told it and what you never talked about. When you say "save" at the end of a conversation, what is new goes into the right card as a line.

## What you need

- **A Mac or a Linux computer.** Windows is not supported yet — there is no version for it, you would waste an evening.
- **The Claude Code program and a paid Claude plan** (Pro or Max, from Anthropic). Claude Code is a program made by Anthropic: you start it in a command window, and inside that same window you write back and forth with the assistant, just like an ordinary chat. The assistant lives there, not in this folder. The plan is paid to Anthropic — that is the only payment involved.
- **Two small helper programs, both free: Python and Git.** The first lets the assistant search your notes and check its own quotes; the second keeps earlier versions of your notes. On a Mac they are usually already there. If Python is missing, nothing breaks and no errors appear on screen — you simply get no search by meaning and no quote self-check; the assistant will say so in plain words and tell you what to install.
- **This folder**, downloaded and unpacked wherever is convenient for you.
- **About fifteen minutes** for the first session, and an internet connection the whole time you are talking to the assistant.

## Getting started: four steps

1. **Install Claude Code.** Anthropic's instructions: https://code.claude.com/docs/en/setup — there is one command there that you paste into a command window. On a Mac that window is called Terminal: press Command (⌘) together with the space bar, type "Terminal" and press Enter. You install it once. A paid Claude plan — Pro or Max — is required.
2. **Download the folder.** Open https://github.com/xcota/pos, press the green "Code" button and choose "Download ZIP". If GitHub does not open for you (in China, for example), the same folder is at https://gitee.com/cotya/pos-starter — button "克隆/下载" → "下载 ZIP". Double-clicking the downloaded archive creates a folder next to it (it will be called `pos-main` or `pos-starter-master`) — move it into your Documents. You can rename it to "Camomile", nothing breaks.
3. **Open the folder in Claude Code.** In that same command window (if you closed it, open it again the same way) type `cd`, then a space, then drag the folder into the window with your mouse and press Enter. `cd` means "go to": you are telling the window which folder to work with from now on. When you drag the folder in, a long line with slashes appears by itself — that is the folder's address, it is supposed to look like that, do not edit it. Then type `claude` and press Enter. If the answer is `command not found`, the program is not installed — go back to step 1.
4. **Type `/start`.** From here the assistant leads: it asks you about yourself and builds your folder for you. You can stop anywhere — come back, type `/start` again, and it continues from the same place instead of starting over.

**How to tell it worked.** After `claude` the window clears, the program's greeting appears, and at the bottom there is a line you can type into. That is the success: from here on everything happens right there, as ordinary writing back and forth — you type a sentence, press Enter, read the answer. Apart from the few words in the cheat sheet below, there is nothing else to learn.

## What the first session looks like

Briefly, so there are no surprises:

- The assistant asks what to call you and explains in one paragraph what is about to happen.
- One yes/no question: install search by meaning or not.
- **Three stories instead of a questionnaire**: yesterday, from waking up to going to bed; the past month — what you bought, what you regret, what you are glad about; what you learned over the past year and from whom. Not once are you asked to rate yourself on a scale.
- **A card to check** for each area: numbered lines "you said" (your own words, word for word), "I saw in your files", "I think", then "I don't know" and "I heard X — right?". You correct by number: "3 is wrong, what actually happened is…".
- **A number for the area** — only as the last line of the card, and only if you told it enough about that area. The assistant is the one who assigns it, and says next to it how confident it is. If you said little, there is no number at all: "you didn't talk about this".
- It only starts building your folder after you have confirmed or corrected at least two cards.
- Right at the end it asks you once to close it and open it again in the same folder. Those are the same two lines from step 3. That is the only thing you do by hand in the whole session.

More detail: [what this is and how it works](docs/en/presentation.md) · [what the first session looks like](docs/en/onboarding-flow.md)

## Coming back tomorrow

The same two lines in the same command window: first `cd` with your folder, then `claude`. In a command window the up arrow on your keyboard brings back what you typed last time — that is quicker.

## Where your data is

Everything sits on your own disk as ordinary text files — even a basic text editor opens them. There is no separate storage program and no server of ours. We do not register you anywhere: we have no accounts and there is nowhere to create one. The only subscription is with Anthropic, for the Claude Code program itself. Copy the folder and you have moved all your notes; delete the folder and the notes are gone.

You do not need to give the assistant passwords, keys or card numbers, and it does not copy them into your files even if you mention them in conversation — that is written into its rules.

About disk space: if you agreed to search by meaning, its dictionary is kept outside the folder, in a service area of your system — about one gigabyte. It is not your notes, but it does take up space; the assistant can tell you how to remove it.

An honest note about the internet: for the assistant to answer you, pieces of your notes are sent to Claude — the same as any text you type into an AI chat. Storage is on your side, thinking happens on Anthropic's servers. That is why you need an internet connection.

## Cheat sheet: three words

Type them in Latin letters, with the slash in front, right in the conversation line:

| Word | What it does |
|---|---|
| `/session-save` | save this conversation into memory |
| `/recall` | find an old note |
| `/reflect` | go over the misses of the last few days |

`/start` is only needed the very first time (and to continue an interrupted first session). All of the same things can be asked for in plain words: "save this conversation", "find where I wrote about…".

## License

AGPL v3: using and changing it is free; if you build a service for other people on top of it, open up your changes too. Full text in the LICENSE file.
