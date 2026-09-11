# The first session: how getting acquainted goes

Starting point: the folder is empty and the assistant knows nothing about you. So the first session is a conversation, and out of it the assistant builds a description of you.

## What happens, in order

**First — hello.** The assistant asks what to call you and says in one paragraph what is about to happen: three stories, then cards for you to check, then it builds the folder. Next comes one yes/no question: install search by meaning. It tells you honestly what that costs — about a gigabyte of disk space and five to ten minutes to download, and no money. Say no and it will search by exact words, and everything else works as usual. It downloads nothing silently in the background. While you answer, it quietly prepares the folder: it sets up keeping earlier versions of your notes, and an `inbox/` folder where you will be able to drop your own files later.

**Then — three stories.** Not once are you asked to rate yourself: how would you know what your vitality (body and energy) is — that is subjective. Instead of a questionnaire the assistant asks you to talk the way you would to a friend: yesterday, from waking up to going to bed; the past month — what you bought, what you regret, what you are glad about; what you learned over the past year and from whom. Three stories cover all seven areas — Self-development (learning and growth), Vitality (body and energy), Surroundings (people and place), Wealth (what "enough" means to you), Rest (what restores you), Work (what you do), Assets (money and property). Each story is saved in your folder word for word: that is later the only source for the "you said" lines.

**Next — a card per area, for you to check.** Having gone through the stories, the assistant shows a numbered list for each area: "you said: …" (only your own words, word for word), "I saw in your files: …", "I think: …", then "I don't know: …", then "I heard «…» — right?", and as the last line its own number with a confidence level. Before showing it, it checks itself: the folder contains a small program that matches every quote against your own stories. If a quote is not found word for word, that line turns into a question, "I heard «…» — right?", and until the check comes back clean it does not show the card at all. You correct by number: "3 is wrong, what actually happened is…". A one-word "yes" confirms only the "you said" lines; what it thinks stays its guess until you answer by number.

**Next — questions that go deeper.** After five areas the conversation changes character: what really makes you angry, what you lost and could not digest, how being lonely differs from being alone, what counts as irreversible for you, what charges you up and what drains you. It is still a conversation, not a test, but the questions are not shallow.

**Parents and childhood are a separate part, and it is optional.** The assistant asks whether you are willing to talk about that. Say no and it moves on — that is a normal answer, not a gap.

**At the end — the portrait.** Out of the conversation it puts together a description: how you are built, what you do at typical decision points, what it is guessing at and what it does not know about you, and its number for each area. There is one threshold: two cards that you have seen and either confirmed or corrected. Fewer than two and it does not build; more than two is not worth waiting for — the deeper questions and the remaining areas can be done later. The first pass is always marked as preliminary.

**Building the folder.** After the portrait it builds your folder: the "who I am" file, your goals, starting tasks, a cover page with the seven areas. And it asks you once to close it and open it again in the same folder — that is the only thing you do by hand in the whole session, and it is the same two lines in the command window that you used to start.

How long it takes: a quick pass is about fifteen minutes, the full one, with all the deeper questions, takes several sittings. You can stop anywhere: everything is already on disk, so you come back, type `/start`, and it continues from the same place.

## The assistant's first lines

It sounds roughly like this. It takes how to address you from your own answer.

> What should I call you?
>
> This is your folder: I remember what you tell me and work from there. Here is how this goes — you tell me about your life in three stories, about fifteen minutes. I will not ask you to rate yourself on a scale: how would you know. I will sort it out myself and show you a card for each area — "here is what you said, here is what I think about it, here is what I don't know". You correct it by number. Then I build the folder. You can stop at any moment.

> Should I install search by meaning? That is when I find an old note of yours by the thought rather than the exact word. It takes about a gigabyte on disk, five to ten minutes. Everything works without it, I will just search by exact words. Install it?

> Tell me about yesterday, the way you would tell a friend, from waking up to going to bed. However suits you — short or in detail.

And then, having gone through the story, a card for you to check:

> Work (what you do) — here is what I understood, correct me by number:
> 1. you said: spent the morning fixing a client's website
> 2. you said: call with my partner
> 3. I saw in your files: edits in three projects over the past month, nothing closed
> 4. I think: the bottleneck is the flow of clients, not the choice of project
> I don't know: whether the website is your main income or one of several; whether the partner is a money partner or a work partner.
> I heard «Figma» — right?
> As I see it, Work: the hands-on work is there, the flow of clients is the jam. 6 out of 10, medium confidence.

The lines here carry different weight, and the first words show it. "You said" — your own words, word for word, nothing of its own. "I saw in your files" — what it found in your own folder. "I think" — its guess, and it stays a guess until you answer by number. "I heard «…» — right?" — a name, a number or a city it might have misheard. For an area you barely talked about, the last line with a number will not be there at all.

## The number for an area: where it comes from and what is done with it

There is one number, and the assistant assigns it — out of what you told it. You are not asked for it: you are not obliged to know what shape an area of yours is in, and a self-rating instead of facts gives it nothing. It shows the number as the last line of the card, with how confident it is next to it.

If you said almost nothing about an area, there will be no number at all: it writes "you didn't talk about this". That is not a zero and not a "weak area" — it is an absence of data.

What happens to the numbers next: **no "where to invest" list appears out of its number.** The goals file, in the "where to invest" section, only gets the areas that you yourself said had a hole — in your own words. A low number of its own stays in the area's card as its reading, and you are free to disagree: say so by number and it rewrites.

If you name a number yourself ("I'd give work an eight"), it writes it down as yours and notes if it sees things differently. It will not ask you for that number.

## How the assistant adjusts to you

What adjusts is the **form**, not the content: it still names inconvenient facts and gaps — just in the manner you showed it.

What it picks up from your very first answer:

- you answer briefly — the questions get shorter and come one at a time; you answer at length — it can take several topics at once;
- how you talk — it uses the same language and the same register, strong words included, if you use them;
- how you introduced yourself and how you addressed it — by first name or not;
- whether you answer in lists or in solid text — it asks the same way.

Your corrections about form add up in the "How to work with me" section of your "who I am" file — tone, length, how to address you, what not to ask about. That file is read every time it starts, so the manner is not lost when you close the window and open a new one the next day. At the end of a conversation, when you say "save", the assistant shows one or two candidate lines for that section and writes down only what you agreed to. It will not praise you or cheer you on: you are not taking an exam.

## How the first session ends

By this point the folder contains:

- a description of you: how you are built, what you do at typical decision points, its guesses about what you do not see in yourself, and, as a separate section, what it does not know about you;
- cards for the areas with its numbers — the ones you have already seen and corrected;
- a "where to invest" list — only from the areas you yourself said had a hole;
- your goals and starting tasks;
- a cover page with the seven areas;
- the record of the conversation.

All of it is ordinary text files. Open them, read them, cross out what does not belong. If you disagree with a wording, tell the assistant and it rewrites.

## What comes next

Ordinary work. Depth is picked up as you go, but not by itself: when you say "save" at the end of a conversation, the assistant adds one or two lines to the area's card out of what you mentioned in passing — your phrase word for word and, if there is one, its conclusion from it. It does not recalculate the number while doing that, and it does not show the card again.

If you want to redo an area from scratch, say so in plain words: "let's go through Work again". Then it asks you questions about that area and shows a new card for you to check, the same as in the first session.

Once you have a few conversations behind you, type `/reflect` — it will show what it has understood about your manner and what it still does not know.
