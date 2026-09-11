---
type: context
tags: [identity, profile]
updated: ""
profile_version: ""
sourced_from: memory/svoboda/{subject_id}/profile.yaml
---

# Who you are: {{name}}

> **This file is about you, and it is yours.** The assistant fills it in from your own stories
> after onboarding and re-reads it on every start — this is where it knows how to talk to you from.
>
> **Edit it by hand as much as you like.** Cross a line out and it does not come back: on a rebuild
> the assistant reads this file and keeps everything you corrected or added. If you disagree with a
> wording, say so in words and it will rewrite it.
>
> **How to read the lines.** Each one shows where it came from: _your words_ (you said it, word for
> word) · _seen in your files_ (it found this in your folder) · _my guess_ (its inference, not a
> fact — arguable). It must not write guesses without a source. There are no diagnoses here and
> there cannot be: this is a description, not medicine. Anything that turned out to be wrong moves
> down into "Withdrawn" and is never deleted silently.
>
> **Language.** This file is written in the language you write in. Section headings are translated
> along with the rest; file names and keys stay as they are.

## In short

| What | How |
|-------|-------|
| Name | _{{what you're called}}_ |
| Age | _{{how old}}_ |
| What you do | _{{work, occupation}}_ |
| Languages | _{{which ones you speak}}_ |
| Time zone | _{{where you are in time}}_ |

---

## How to work with me

_This is about the form of the conversation, not conclusions about the person. Filled from
`profile.yaml.interface_draft` at build time and extended by `/session-save` whenever the person
corrects the form. Every line carries a date and their own words. Don't invent lines: no correction
from them, no line._

| What | How | Date | Source |
|---|---|---|---|
| Form of address | _first name / formal / informal_ | | |
| Answer length | _short / medium / full_ | | |
| Pace | _one question at a time / several is fine_ | | |
| Language and register | _language, strong words yes/no_ | | |
| Lists | _as a list / as prose_ | | |
| What not to ask | _your stop-topics and stop-phrasings_ | | |
| What works | _what you answer readily_ | | |
| Withdrawn | _what stopped applying, with a date_ | | |

---

## What you said about yourself

_Your words, verbatim, with dates. Everything else in this file grows out of them._

- _«…» — {{date}}_

---

## How you think and learn

_How you get to grips with something new: going deep or skimming the surface, in bursts or a little
every day. One or two lines, each with a reference to your words or to what is visible in the
files._

---

## What charges you and what drains you

_What gives you energy and what eats it — out of your own stories. No "and that's why you are like
this" conclusions._

---

## What makes you angry

_What genuinely sets you off: a broken agreement, waffle instead of an answer, the same question
asked again. The assistant doesn't do those things and doesn't step on them._

---

## How you respond under load

_What is visible when a lot lands at once: shorter messages, faster pace, time of day. Observations
with a source only — no labels and no diagnoses._

---

## What you usually do in typical situations

_The assistant's guess: in a situation like this you will most likely do that. It exists so it
doesn't have to re-ask the obvious. Wrong — say so and the line changes._

| Situation | What you'll most likely do |
|-----------|-------------------|
| _…_ | _…_ |

---

## My guesses about what you don't see about yourself

_This is the most arguable part of the file, and it is marked as a guess. Not a diagnosis and not a
verdict — just what the assistant watches more closely. Each line: what exactly, why it thinks so,
what would change its mind. Disagree — cross it out, it won't come back._

1. _…_
2. _…_
3. _…_

---

## What I don't know about you

_The gaps. What you haven't talked about, and what the assistant never asked. Honestly empty here
rather than invented._

- _…_

---

## Withdrawn

_What turned out to be wrong moves here: the old wording, the date, and what replaced it. Nothing
is deleted silently — otherwise the same thing comes back on the next pass._

_(empty for now)_

---

## What the assistant does here

Not a chat that forgets. Four things:

1. **Remembers** — between conversations, in full, in your words.
2. **Does** — takes a task to the end instead of handing out advice.
3. **Reflects** — shows you the repeats and what you yourself said earlier.
4. **Works on its own** — within the limits you agreed.

You decide. It works things out, does them, and shows you what it sees. It doesn't give unasked-for
advice.
