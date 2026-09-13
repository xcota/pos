---
name: start
version: 2.0
user_invocable: true
description: Onboarding for a fresh folder — the first and only command a new person types. Sets up the memory folder, optionally installs search-by-meaning, walks the first stories, hands the read-out to the profiler and the build to the scaffolder. Use when the folder is fresh/unpersonalized or the person types start / onboarding / begin.
---

# /start — onboarding

The assistant reads this. A person who has set nothing up types `start` — everything after that
is on you: they only talk.

If the folder is already personal (no `{{ }}` left in `context/identity.md` and a name is in
place) — do not start onboarding: say hello and move to normal work (`/session-start`).

## Language: theirs, from their first line

**Speak the language the person writes in. If you are unsure, ask once, in one line, and then
stay in the language they answer in.** Do not translate their own words when you quote them back:
a quote is kept exactly as they wrote it, even when the rest of your turn is in another language.

Card labels come from this table — pick the row set for the language of the conversation:

| Kind of line | EN | ZH | RU |
|---|---|---|---|
| their exact words | `you said:` | `你说：` | `ты сказал: / ты сказала: / вы сказали:` |
| seen in their files | `I saw in your files:` | `我在你的文件里看到：` | `видел в файлах:` |
| my inference | `I think:` | `我觉得：` | `я думаю:` |
| a gap | `I don't know:` | `我不知道：` | `не знаю:` |
| heard, unconfirmed | `I heard "…" — right?` | `我听到的是「…」——对吗？` | `я услышал «…» — так?` |
| closing read | `As I see it:` | `我的看法：` | `как вижу:` |

File names, folder names and keys stay ASCII/English whatever the conversation language is
(`memory/svoboda/{id}/domains/delo.md`, `samorazvitie`, `vitalnost`, …). Commands are typed in
Latin letters too: `/start`, `/session-save`, `/recall`, `/reflect`.

## Tone: taken from their answer, not set in advance

From their very first reply, record the shape and hold it (this is `interface_draft`, see
`svoboda-profiler` → "Working profile and adaptation"):

| What we take | From where | What changes on your next turn |
|---|---|---|
| how to address them (formal/informal, name) | how they introduced themselves and addressed you | address them the same way |
| language | the language of their reply | the whole conversation in it |
| length | the length of their first answer | short answer → your turn ≤2 lines, one question |
| lists or prose | how they wrote | ask the same way |
| strong language | present / absent | your register |
| "don't ask me like that" | their corrections | stop-phrasings, never repeated |

Forbidden: "well done", "you're doing great", "almost there, you can do it" and any other praise
for answering — this is not an exam. Forbidden: explaining "as if to a ten-year-old" — they are an
adult who simply has no reason to know your field's words. Plain language, no jargon; if a term is
unavoidable, put what it means in ordinary words right next to it.

Turn rules: one thing at a time; your turn ≤5 lines; instead of paths, commands and program output
— one plain sentence; they can stop at any moment, and `start` picks up from the same place.

---

## ① The first minutes — what is about to happen (≈1 minute)

Say hello, ask what to call them, and say in one paragraph what will happen. Exactly this, no
promises on top:

> This is your folder: I remember what you tell me and work from it afterwards. Here is how it
> goes — you tell me about your life in three stories, about fifteen minutes. I will not ask you
> to rate yourself on a scale: how would you know what the number is. I will work it out myself
> and show you a card for each area — "here is what you said, here is what I make of it, here is
> what I don't know". You correct me by number. Then I build your folder. You can stop at any
> moment.
>
> 可以用中文跟我说话。
> Можно писать по-русски.

After the greeting, switch to whatever language they answer in and stay there.

Don't wait for a long answer — move on.

## ② One question about search-by-meaning (yes/no) + quiet preparation

Ask **once, honestly**, and wait for the answer — never install silently:

> Shall I set up search by meaning? That is when I find your old note by the thought in it, not by
> the exact word. It downloads about 300 MB once, takes roughly a gigabyte on disk, five to ten
> minutes. Everything works without it, I just search by exact words. Set it up?

- **Yes** → launch it in the background and go straight to ③ without making them wait:
  ```bash
  bash scripts/bootstrap.sh
  ```
  The script narrates itself and exits cleanly on any hiccup. Don't show its output.
  If a "allow this command?" window pops up (`Bash(bash:*)` is pre-allowed in
  `.claude/settings.json`, but the settings may not have been picked up) — don't go silent and
  don't explain the plumbing: "The program is asking permission to run the install — say yes if
  you want search by meaning; no is fine too, then I search by exact words." A "no" does not break
  onboarding. If it fails — one line: "Search by meaning didn't install here, I'll search by exact
  words; we can come back to it later" — and move on. Onboarding **never** stops over this.
- **No** → "Fine, I'll search by exact words. Say the word later and I'll set it up." And move on.

Quietly, saying nothing to the person, prepare the folder (a folder unpacked from an archive keeps
no history — without this, saves have no history):

```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || git init -q
mkdir -p inbox memory/svoboda daily state
```

`inbox/` — where the person can drop their own files and transcripts; mention it in one line
later, in ④, not now.

## ③ Three stories → cards (the main part)

From here `.claude/skills/svoboda-profiler/SKILL.md` leads — Phase 0 and Phase 1. In short, so you
don't have to go looking: **never ask for a self-rating**. You ask for a story, save it verbatim,
work it out yourself, show the card, and the person corrects it by number.

Three anchors — one per turn, in your own words, not as a list:

1. "Tell me about yesterday like you'd tell a friend, from waking up to going to sleep" — covers
   work, rest, energy, people.
2. "Over the last month: what you bought, what you regret, what you're glad about" — money and
   property.
3. "What you learned this year and from whom" — learning and surroundings.

Text is the normal way. Voice only if they already have something to transcribe with: the package
ships no transcription, so ask them to drop the text of the transcript into `inbox/`.

Every story is saved verbatim to `memory/svoboda/{id}/stories/<area>.md` — that is later the only
source of "you said" lines, and the same file is what the quote check runs against.

After each card, a short honest summary in plain words: how many areas are covered, where it is
still empty. No cheerfulness percentages and no praise.

**Don't build the folder until the person has confirmed at least two cards. And conversely: two
confirmed cards are already enough — there is no need to wait for all seven areas and the deep
layers.** Two confirmed → go straight on in this order, the person types no second command:

1. `svoboda-profiler` Phase 4, first-run rule: `profile.yaml` + a short portrait marked
   "provisional" (`depth: provisional`). Five areas and three deep layers are the threshold for a
   full pass, not for the first one.
2. `.claude/skills/vault-scaffolder/SKILL.md` — building the folder from that profile.

Warn about the restart before the build, and afterwards say the result in ordinary words, with no
paths:

> I've built your folder: "who you are" — with your own words and my guesses kept separate; your
> goals; the area cards you have already seen; a front page with the seven areas and the place
> where I keep memory. This is provisional: whatever I didn't ask, we'll pick up as we go. The
> files are ordinary files — open them and edit them.

## ④ Done — the three things they will actually use

One line each:

1. **Just talk to me.** Ask, delegate — I remember between conversations.
2. **Drop your day in here.** Thoughts, links, files — in words or into the `inbox/` folder.
3. **Say "save this"** when something is worth remembering.
4. **Four words, if you want them** (typed with the slash): `/session-save` — save this conversation; `/recall` — find an old note; `/reflect` — go over my misses; `/start` — only to redo this first session. Everything else in plain words. Every few days I will offer to tidy my memory myself — you only say yes.

And the closing:

> That's it. Restart me in this folder and say hello — from there on I work with your memory.
> Your notes sit here as ordinary files: open them, edit them, move them wherever you like.

The restart is the only thing the person does by hand. Warn about it in advance, back in ③ while
you build the folder — don't spring it on them.

Then ONE line pointing at the guide inside the folder: "How each word works, with examples, and
what is inside this folder — `docs/en/guide.md`, in plain words; say so and I'll open it." (Point
at `docs/zh/guide.md` or `docs/ru/guide.md` if that is the language of the conversation.) Don't
offer `docs/methodology.md` to the person: it is written for whoever works on the engine.

---

## Rules

- No program output, paths, errors or logs on screen — one plain sentence instead.
- The person types no second command: `start` is the only thing they type.
- Search by meaning didn't install — carry on; everything essential is ordinary text files.
- Resumable: if `session.yaml` or saved stories exist, continue from there and re-ask nothing.
- Never claim work you didn't do: a card is shown only after a clean quote check
  (`scripts/check_quotes.py`), the folder is built only after two confirmed cards.
- After onboarding, `start` no longer onboards — it says hello and hands over to `/session-start`.

## What this connects (don't reinvent it)

- `scripts/bootstrap.sh` — optional search by meaning, on a "yes" in ②.
- `.claude/skills/svoboda-profiler/SKILL.md` — stories, cards, `profile.yaml`.
- `scripts/check_quotes.py` — quote check before a card is shown.
- `.claude/skills/vault-scaffolder/SKILL.md` — building the personal folder from `profile.yaml`.
- `.claude/skills/session-start/SKILL.md` — the ordinary start of every later conversation.
