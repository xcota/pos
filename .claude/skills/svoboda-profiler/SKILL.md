---
name: svoboda-profiler
version: 3.2
user_invocable: true
description: "Use when asked to profile someone, unpack a person, build a psychological portrait, run a Svoboda session, or map life state. Triggers on profile someone, unpack a person, psychological portrait, point A, life-state map, svoboda session."
---

# Svoboda Profiler v3.2

Build (1) a **causal psychological profile** AND (2) a **living life-state document** through structured conversation. Not a personality test, not a balance wheel — a guided unpacking that reveals *why* someone operates the way they do AND maps where they are now → where they're going.

**Approach:** Fixed Point A (current state), not aspirational targets. Re-cut on accrual; annual refresh as the floor.

**Output triple:**
1. Narrative profile (`profile.md`) — psychological portrait with tags, origins, predictive model
2. Machine-readable profile (`profile.yaml`) — feeds downstream `vault-scaffolder`. **Canonical schema is defined once, below in Phase 4, and the scaffolder reads that exact shape.**
3. Operational layer (`pp.md` + `plan-fact.md` template + `plans.md`) — living life-state document

## The 7 domains

The `key` column is the identifier used in files, folders and `profile.yaml` — it never changes and
is never translated. The name and the gloss in brackets are what you say out loud, translated into
the language of the conversation.

| Key | Domain (say it with the gloss) | Focus |
|-----|-------------------------------|-------|
| `samorazvitie` | Self-development (learning and growth) | learning, education, skills, content consumption, personal growth |
| `vitalnost` | Vitality (body and energy) | health, body, energy, mental state, appetite for life — NOT just physical |
| `okruzhenie` | Surroundings (people and place) | environment, place of living, people, networking, communication channels |
| `bogatstvo` | Wealth (what "enough" means to you) | philosophical relationship with wealth — what "rich" means to them, what they hold above money |
| `otdyh` | Rest (what restores you) | rest, recovery, travel, entertainment, hobbies as recovery (NOT skill-building) |
| `delo` | Work (what you do) | work, business, projects, profession, what they DO |
| `aktivy` | Assets (money and property) | financial assets, income sources, asset management, liabilities |

Chinese: 自我成长（学习与成长）· 活力（身体与精力）· 环境（身边的人和住的地方）· 财富（对你来说什么是够）·
休息（什么让你恢复）· 事业（你在做什么）· 资产（钱和财产）.

**Critical distinction:** Wealth (`bogatstvo`, philosophical) ≠ Assets (`aktivy`, operational).
Wealth is "what does wealth mean to you / you can be rich and stingy or poor and generous". Assets
is "what do you actually own and how do you manage it".

## Invocation

- `/svoboda-profiler {subject_id}` — start new or resume existing session
- `/svoboda-profiler {subject_id} status` — current phase, blocks_completed, ETA
- `/svoboda-profiler {subject_id} synthesize` — force Phase 4 with collected data
- `/svoboda-profiler {subject_id} scaffold` — Phase 5 hand-off to vault-scaffolder
- `/svoboda-profiler {subject_id} update {domain}` — re-cut a single domain (annual refresh)
- `/svoboda-profiler {subject_id} delta "{fact}"` — log ONE drift fact between sessions (living profile, v3.1) — no session needed
- `/svoboda-profiler {subject_id} resynthesize` — re-run Phase 4 against accrued deltas → **versioned diff**, not a from-scratch rewrite (v3.1)

## Session State (multi-phase, resume-able)

Persisted as `memory/svoboda/{subject_id}/session.yaml` (the schema below). A resume reads it back by that name.

```yaml
subject_id: {id}
started: {iso_date}
last_updated: {iso_date}
phase: 1
domains_completed: []   # subset of [samorazvitie, vitalnost, okruzhenie, bogatstvo, otdyh, delo, aktivy]
cards_confirmed: []     # domains whose card was shown AND confirmed/corrected by the person
self_scoring: not_asked # not_asked|volunteered — we NEVER ask the person for a number
interface_draft: {channel: text, reply_len: "", language: "", profanity: "", address: "", lists: "", avoid: []}
                        # shape of the conversation; copied into profile.yaml at Phase 4
layers_completed: []    # subset of [granularity, motivation, losses, loneliness, anger, irreversibility, attachment, attribution, rumination, boundary, temporal, strengths, load_mode]
parents_done: false
synthesized: false
operational_layer_done: false   # NEW v3: dashboard + plan-vs-fact + plans generated
scaffolded: false
profile_version: 0              # v3.1: bumps on each (re)synthesis
last_delta: null                # v3.1: iso_date of last logged drift fact
delta_count_since_synthesis: 0  # v3.1: staleness trigger — re-cut a domain when this crosses threshold
data_path: memory/svoboda/{subject_id}/
channel: {text|voice}   # how the person answers
language: {en|zh|ru|…}  # the language the person writes in — everything you say goes in it
```

Continue from `phase` + next uncompleted block. Never restart completed blocks. Every exchange writes raw data + updates session YAML atomically.

## Protocol

### Phase 0: Onboarding — stories instead of a questionnaire

**Language first. Speak the language the person writes in; if you are unsure, ask once, in one
line, and then stay in the language they answer in.** Their own words are never translated when
you quote them back. Card labels come from the table in "Card labels (EN / ZH / RU)" below. File
names, folder names, domain keys and commands stay ASCII/English in every language.

**The person is never asked to rate themselves with a number — this is the only place such a
question is mentioned at all, and it is mentioned as a ban.** "Rate this area of your life from 1
to 10" and every variant of it is not asked: the person has no reason to know what the number is,
and what comes back is a self-image instead of facts. The number for each area is set by the agent
— out of what the person told you — and shown for checking as the last line of the card.

**Empty folder (the normal case — the person has just arrived).** There is no corpus; onboarding
runs from their first answer. Three anchor stories, one per turn, in your own words, not as a list:

1. "Tell me about yesterday like you'd tell a friend, from waking up to going to sleep" → Work,
   Rest, Vitality, Surroundings.
2. "Over the last month: what you bought, what you regret, what you're glad about" → Assets, Wealth.
3. "What you learned this year and from whom" → Self-development, Surroundings.

No forced choice between two options. Text is the normal channel; voice only if the person has
something to transcribe with (they drop the transcript into `inbox/`; the package ships no
transcription of its own).

**Every story is saved verbatim** to `memory/svoboda/{subject_id}/stories/<area>.md` (on the first
turn, `mkdir -p memory/svoboda/{subject_id}/stories`), with the date in the heading. It is the only
source of "you said" lines and the only thing the quote check runs against. Do not paraphrase into
that file — put in exactly what the person wrote.

After their first answer, fill `session.yaml.interface_draft` (see "Working profile and
adaptation") and from your next turn speak in their shape.

**The folder is already alive (a repeat pass, there is accumulated material).** Before asking
anything, read what the person has already said and done: their saved stories `stories/*.md` and
notes in `inbox/`, their dated corrections, your own `daily/` for the last two weeks (that is your
retelling, not their words — label it that way), `git log --since=30.days --format=%s` as a trace
of behaviour. If there is a lot of raw material (>20K tokens), that is a separate agent's job, not
the main window's: it returns `memory/svoboda/{subject_id}/prefill.md` ≤15K with draft cards and
gaps, and the main window reads only that.
Do NOT read: the old `profile.md` in full (except the "How to work with me" section),
`context/identity.md` except its "Withdrawn" (what already turned out to be wrong) and "How to work
with me" sections, `knowledge/people/{subject_id}.md` — otherwise you are working over your own old
labels instead of the person.

## Card labels (EN / ZH / RU)

Pick the row set for the language of the conversation. The kind of line IS its tier — see Phase 1
Step C.

| Kind of line | EN | ZH | RU |
|---|---|---|---|
| their exact words | `you said:` | `你说：` | `ты сказал(а): / вы сказали:` |
| seen in their files | `I saw in your files:` | `我在你的文件里看到：` | `видел в файлах:` |
| my inference | `I think:` | `我觉得：` | `я думаю:` |
| a gap | `I don't know:` | `我不知道：` | `не знаю:` |
| heard, unconfirmed | `I heard «…» — right?` | `我听到的是「…」——对吗？` | `я услышал «…» — так?` |
| closing read | `As I see it:` | `我的看法：` | `как вижу:` |

`scripts/check_quotes.py` recognises the "you said" label in all three languages, so a card written
in any of them is checked the same way.

### Phase 1: the 7 domains — story → card → correction

For EACH domain, in order:

**Step A′ — Prompt.** One pass: ask them to tell you about the area however they like, plus no more
than three concrete gaps left over from earlier stories. A live conversation = one question per
turn. Never ask for a number in any form. Before sending, run your prompt against this person's
`avoid[]` (from `interface_draft`): a hit means rephrase, not send. The stop-phrasing list belongs
to the specific person; the skill holds no constants.

**Step B — Probes** for the domain (below) + `references/domain_probes.md` — sub-questions used to
count coverage. Probes are never read out as a list; they exist so you can measure coverage.

**Step C — The card** `memory/svoboda/{subject_id}/domains/{domain}.md`. Write it straight away in
the words it will be shown in — no internal codes or tags in it, only the source marker at the end
of a line (that tail is not read out when you show it). **Labels come from the card-label table in
the language of the conversation, and the form of address is the one the conversation uses.** The
quote check understands all three label sets, so there is no need to rewrite the card before
showing it (the example below is in English):

```
# Work — {subject_id}
stories: stories/yesterday.md, stories/year-of-learning.md

## Lines
1. you said: «spent the morning fixing a client's site» — stories/yesterday.md
2. you said: «call with my partner» — stories/yesterday.md
3. I saw in your files: edits in three projects this month, nothing closed — git status
4. I think: the bottleneck is the flow of clients, not the choice of project — from 1 and 3
5. I heard: «Figma» — right?

## I don't know
- whether the site is the main income or one of several; whether the partner is money or craft
## Closed by them (do not ask again)
- (empty)
## Coverage: 4 of 7 sub-questions → medium confidence
## As I see it: the hands-on work is there, client flow is the jam. 6 out of 10, medium confidence.
## Corrections
- (after it is shown)
```

Four kinds of line, and the kind of line IS its tier:
- **«you said: «…»»** — only a verbatim quote from their story + the story file at the end of the
  line. A paraphrase never goes here: that is already "I think".
- **«I saw in your files: …»** — behaviour visible in the folder (files, `git status`), with its
  source.
- **«I think: …»** — your inference, with the numbers of the lines it was drawn from.
- **«I heard: … — right?»** — a name, a number, a city, a word you half-caught: until the person
  confirms it, it feeds neither conclusions nor the number.
- Third-party statements — «second-hand: …», without the names of outside people.

Rules:
- Something skipped (you asked, they didn't touch it) = a gap in the data, not a diagnosis. What
  they closed in words → "Closed by them", never asked again unless they raise it.
- **Coverage** = sub-questions touched / all of them per `references/domain_probes.md`. Under 40% →
  `observed: null`, and in the showing "no number — you didn't talk about this", not a zero and not
  "a weak area".
- Confidence (low / medium / high) — from coverage, not from the number of lines.
- About speech, write only "named / never named the X family" (`granularity_instrument.md`). The
  words "suppression", "defence", "trauma" never enter a card.
- Nothing resembling passwords, keys or card numbers goes into a card, even if they dictated it.

**Step D — Quote check (mandatory, before showing).**

```bash
python3 scripts/check_quotes.py memory/svoboda/{subject_id}/domains/{domain}.md
```

The script takes every "you said" line (in any of the three label languages) and looks for it
verbatim in that person's saved stories (`stories/` — including `stories/corrections.md`, where
their corrections land, see Step F). Not found → it prints the line number and rewrites the line as
"I heard: … — right?": meaning it was your wording, not their words. A red run (exit code 1) = **do
not show the card**: deal with the flagged lines and run it again, until a clean run in the same
session. Exit code 2 = there is nothing to check (no stories, or no quote line in the card) — that
is also "do not show": first save the story into `stories/`, then build the card. No Python → drop
the "you said" lines from the showing entirely, leaving "I saw in your files", "I think" and "I
don't know": what is unverified is not passed off as their words.

**How to name the areas out loud.** Always with the gloss in brackets, so the person isn't left
guessing: Self-development (learning and growth) · Vitality (body and energy) · Surroundings
(people and place) · Wealth (what "enough" means to you) · Rest (what restores you) · Work (what
you do) · Assets (money and property). In Chinese: 自我成长（学习与成长）· 活力（身体与精力）·
环境（身边的人和住的地方）· 财富（对你来说什么是够）· 休息（什么让你恢复）· 事业（你在做什么）·
资产（钱和财产）.

**Step E — Showing.** You read the card to the person as it is, minus the source tails and the
internal headings, strictly in this order:

1. The numbered lines: "you said: …" / "I saw in your files: …" / "I think: …".
2. "I don't know: …".
3. "I heard X — right?".
4. As the last line: "As I see Work: {one phrase in their words}. N out of 10, medium confidence" —
   or "I'm not putting a number on it, you didn't talk about this" when coverage is thin.

Never open with the number and never ask about it. Example of a showing:

> Work — here's what I understood, correct me by number:
> 1. you said: you spent the morning fixing a client's site
> 2. you said: a call with your partner
> 3. I saw in your files: edits in three projects this month, nothing closed
> 4. I think: the bottleneck is the flow of clients, not the choice of project
> I don't know: whether the site is your main income or one of several; whether the partner is
> money or craft.
> I heard «Figma» — right?
> As I see Work: the hands-on work is there, client flow is the jam. 6 out of 10, medium confidence.

**Step F — Correction.** Their correction is **first appended verbatim** to
`memory/svoboda/{subject_id}/stories/corrections.md` (heading `## {YYYY-MM-DD} — {area}`, their
phrase as-is underneath), and only then do you edit the card and re-run the quote check. Otherwise
the script won't find their fresh words in the stories and will push them back into "I heard: … —
right?" — and the person gets asked about the very thing they just corrected.

A one-word "yes" confirms only the "you said" lines. "I think" lines stay guesses until the person
answers by number. "Not like that: …" → their wording becomes a "you said" line on top of the old
one, and the old one moves to "Corrections" + `delta_log {source: correction}`. An "I saw in your
files" line is never erased under an interpretation — the fact stays, their words go next to it.
Silence ≠ confirmation: no answer → the card stays a draft, and neither synthesis nor the folder
build starts. A domain confirmed/corrected → add it to `session.yaml.cards_confirmed`. If the
person names a number **themselves**, record it in `score_divergence` as volunteered and set
`self_scoring: volunteered`; asking is not allowed.

**Gate:** while `cards_confirmed` is under two — do not run Phase 4 and do not start the folder
build.

**Step B — domain probes:**

1. **Self-development** (`samorazvitie`) — NOT diplomas, but *how* they learn. Burst-mode?
   Conformist? What they rejected matters more. Skills (existing + wanted), content consumed, which
   books changed their life.

2. **Vitality** (`vitalnost`) — body relationship + mental state + appetite for life. Substances
   history if any. How they monitor/optimize. Interoception level. What they think about on waking.
   What inspires them.

3. **Surroundings** (`okruzhenie`) — physical environment (place of living, atmosphere), people
   network, communication channels. Who they want around them (the wish) vs who is actually there
   (the fact). Networking strategies. **Includes parents/family if the person doesn't separate
   Phase 3.**

4. **Wealth** (`bogatstvo`) — *philosophical*. "What is wealth to you? How will you know it has
   arrived?" What they put above money — in their own words, with no esoterica (no tarot, no
   "energies", no spiritual practices). Relationship with abundance/scarcity. What they would do
   with unlimited resources.

5. **Rest** (`otdyh`) — recovery patterns, travel, entertainment. Not hobby-projects (those go to
   Work / Self-development) — what actually *restores*. The effect of travel. Time in nature.

6. **Work** (`delo`) — what they build, how they work, what tools, what they refuse to do.
   Business / job / projects. Sources of professional income.

7. **Assets** (`aktivy`) — operational. Income sources (numbers if they give them), passive income,
   liquid/illiquid assets, liabilities, loans, financial literacy, past bad money decisions.

**Collection guidelines:**
- One domain per exchange. Brief question, no preamble.
- Text is the normal channel; a voice transcript the person supplies is welcome extra (speech patterns).
- Accept whatever format. The story goes verbatim into `stories/`, the read-out into the card —
  never the other way round.
- If they go off-script into another domain — let them, remap later.
- Off-script content → `data_path/freeform.md`, integrate in synthesis.
- One story usually closes several areas: split it across the cards yourself instead of asking the
  same thing seven times.

**Working profile and adaptation**

What adapts is the form, not the content: uncomfortable observations and gaps are still reported,
just in their register.

- **Where it lives.** The single source of truth is the "How to work with me" section in
  `context/identity.md` (every boot reads it). Fields: how to address them · length and pace ·
  language and register · what not to ask and not to offer (`avoid[]`) · what works · withdrawn
  (with a date). Every line carries a date and either their quote or a file reference. Do not start
  a second such list in another file.
- **During onboarding** the form lives in `session.yaml.interface_draft`: `channel: text|voice` ·
  `reply_len: short|medium|long` · `language` · `profanity: yes|no` · `address: informal|formal|name` ·
  `lists: yes|no` · `avoid: []`. Every field is executable: short → a prompt of ≤2 lines and one
  question; `lists: no` → don't answer with a list; `avoid` → grep your own turn before sending,
  and only your own lines (questions and prompts), never their quotes.
- A form correction ("don't ask it like that", "shorter") = interface data, not personality data →
  `interface_draft` + `delta_log {source: interface}`, never into conclusions about the person.
- At Phase 4, `interface_draft` and `self_scoring` are copied into `profile.yaml`; the scaffolder
  reads them from there and writes the "How to work with me" section of `context/identity.md`.
- **How it grows afterwards:** `/session-save` Step 0 — this session's corrections → 0–2 lines into
  the same section; the agent shows the candidates and the person nods or doesn't. That section is
  exempt from the "don't read the old profile" ban: form ≠ conclusions about the person.

### Phase 2: 13 Deep Layers (depth → causal map)

After 5+ domains collected, probe these. Read `references/deep_layers.md`. Layers 1–6 are the core; 7–13 (v3.2) add causal angles as MEASUREMENT, never therapy. Where a layer carries an academic typology (attachment type, attribution axes, mode-under-load), hold it as a **silent profiler yardstick** scored from speech — never read the labels to the subject.

1. **Emotional granularity** — feel with high resolution or process emotions as data? **(v3.1: score against the coverage map in `references/granularity_instrument.md` — which emotion families + body-signal channels they spontaneously reach vs systematically never name.)**
2. **Motivation of the instrument** — *why* do they want what they say they want?
3. **Losses** — wounds (not lessons). What they lost and couldn't convert.
4. **Loneliness** — distinguish solitude from loneliness?
5. **Anger** — what triggers real anger? Most diagnostic suppressed emotion.
6. **Irreversibility** — what do they consider irreversible?
7. **Attachment** (v3.2) — when someone close pulls away, what fires first? Type as causal pattern + genesis. → Section V.
8. **Attribution** (v3.2) — where the cause flies on failure vs who gets credit on success. Asymmetry = predictive lever. → Section VI + XIII.
9. **Rumination vs reflection** (v3.2) — does the thought loop in place or turn a new side? Resolves "no off-switch."
10. **Boundary under pressure** (v3.2) — self-erasure (yield to keep the bond) vs system-integrity (hold + anger), and the switch-point.
11. **Time perspective** (v3.2) — which time they decide from; future-as-plan vs future-as-deferral.
12. **Strengths vs skills** (v3.2) — what charges vs what drains; causal to burnout / role-fit. Deepens Work.
13. **Cognitive mode under load** (v3.2) — does analytic mode hold or flip under stress; where it goes rigid. Strictest non-therapy watch.

Layer 1 + Layer 3 most diagnostic — prioritize these. Layer 7 (attachment) + Layer 10 (boundary) feed Section V; Layer 13 predicts crisis behavior.

### Phase 3: Parents/Origin (optional, high-value)

If open to it, read `references/parents_brief.md`. Genesis of patterns from Phases 1-2. Without it, profile describes but doesn't explain.

**v3.2 — memory-availability map (lens, not a new phase):** across the session (esp. here) notice the DENSITY of access by period — which years come with emotion and detail, which only as dry fact, which get skipped. The distribution itself is suppression data, independent of content (e.g. a vivid window around one parent vs a functional/compressed account of a painful stretch points at where the pattern-generator hides). Probe gently and optionally ("that stretch — what do you remember alive, not facts?"). **Map the distribution, do NOT excavate or "process" the repressed** — this is a pointer for attention, not trauma work (Principle 8). Fold the narrative-coherence signal in here too: a self-version discarded without integration (an earlier self spoken of as a closed, disowned chapter) = the same fragmentation signal, one line, not a separate construct. Record to `memory_access` in profile.yaml.

### Phase 4: Synthesis

**The threshold depends on the run — one rule, repeated in `start` ③ and in `vault-scaffolder`:**

| Run | Threshold | What is written |
|---|---|---|
| First (`run_type: fresh`, folder not built yet) | **≥2 confirmed cards** (`cards_confirmed`) | `profile.yaml` + a short `profile.md` with `depth: provisional`; empty fields stay empty, nothing invented |
| Full pass (`rerun`, depth) | 5 domains from Phase 1 + 3 layers from Phase 2 | the full `profile.md` per template, `depth: confirmed` |

The first run does **not** wait for five domains and three layers: otherwise fifteen minutes in,
the person has neither a portrait nor a built folder, and `context/identity.md` is still full of
`{{ }}`. Two confirmed cards ARE the minimum of a first run; the rest accrues as you go.

Read `references/synthesis_template.md` (on a first run — only the sections there is data for; a
section with no data is simply absent from the file).

**Two artifacts in same turn:**

1. **Narrative profile** → `memory/svoboda/{subject_id}/profile.md` — full document per template (13 sections, tags, predictive model, blind spots, corrections log).

2. **Machine-readable profile** → `memory/svoboda/{subject_id}/profile.yaml`.

#### CANONICAL profile.yaml schema (v3.2) — single source of truth

`vault-scaffolder` reads THIS exact shape. Key names and nesting are a contract — do not flatten or rename. Fields the scaffolder consumes are marked `[scaffolder]`.

```yaml
subject_id: {id}                    # [scaffolder] kebab-case, matches folder name
profile_version: {N.N}              # [scaffolder] top-level; bumps each (re)synthesis
synthesized: {iso_date}             # YYYY-MM-DD
run_type: fresh|rerun|patched
supersedes: ""                      # prior profile_version replaced, or ""

identity:                           # [scaffolder] nested map
  name: {...}
  age: {...}
  role: {...}
  languages: [...]                  # languages[0] = primary
  timezone: {...}                   # IANA tz

svoboda_scores:                     # [scaffolder] nested map, OBSERVED score (1..10) the profiler derived
  samorazvitie: {N or null}         # null = thin coverage, "you didn't talk about this" (NOT a zero)
  vitalnost: {N or null}
  okruzhenie: {N or null}
  bogatstvo: {N or null}
  otdyh: {N or null}
  delo: {N or null}
  aktivy: {N or null}

score_confidence:                   # low|med|high per domain — from sub-question coverage, not from the number of lines
  {domain}: low|med|high

self_scoring: not_asked             # not_asked|volunteered — we never ask the person for a number
score_divergence:                   # ONLY when the person named a number themselves, unasked
  - {domain: delo, self: 8 (volunteered), observed: 4, note: "named it unasked; the story has three stalled projects"}

interface_draft: {channel, reply_len, language, profanity, address, lists, avoid: []}
                                    # [scaffolder] shape of the conversation, from session.yaml; → the "How to work with me" section

domains_active: [...]               # [scaffolder] subset of svoboda where person actually operates
growth_edges_named: [...]           # [scaffolder] ONLY domains where the person named a gap in their own words
depth: provisional|confirmed        # a first run is always provisional
cards_confirmed: [...]              # domains whose card the person saw and confirmed/corrected

north_star: >                       # [scaffolder] 1-2 sentences; verbatim into context/goals.md.
  ...                               # Separate the telos (what they want) from the means (how they fund it).

style: direct|explanatory|mixed     # [scaffolder]
cognitive_style: scanning|deep-dive|burst|gradual   # [scaffolder]

triggers: [...]                     # [scaffolder] FLAT list, 3-5 instant-frustration. Note if reactivity is low/contextual.

granularity_coverage:               # v3.1: from references/granularity_instrument.md
  emotion_families_reached: [...]   # spontaneously named
  emotion_families_absent: [...]    # systematically never named — diagnostic (alias: emotion_families_thin)
  body_channels_reached: [...]
  note: >

cadence:
  chronotype: {...}
  reflection: daily|weekly|biweekly|monthly|annual

blind_spots: [...]                  # [scaffolder] FLAT list. Watch-items, NOT diagnoses. Each seeds AP-006+.

predictive_model:                   # [scaffolder] list of rows
  - {situation: {...}, behavior: {...}}

tags:                               # [scaffolder] NESTED map (v3.2). NOT a flat list — see scaffolder flatten rule.
  core_confirmed: [...]             # well-evidenced traits
  refined: [...]                    # nuanced / qualified traits
  retired_from_baseline: [...]      # tombstoned claims a prior run asserted (NOT applied to vault)

synthesis_constraint: ""            # [scaffolder] free-text guardrail, e.g. "don't reduce to buzzwords"

# ── v3.2 deep-layer outputs (yardstick labels are profiler-internal, never read to subject; NOT consumed by scaffolder) ──
attachment: {mechanics: "...", origin: "...", yardstick: anxious|avoidant|secure|disorganized}
attribution: {failure: internal|external, success: internal|external, note: "..."}
rumination: reflective|ruminative|mixed
boundary_map: {systems: hard|soft, intimacy: hard|soft, switch_point: "..."}
temporal_orientation: past|present|future-plan|future-deferral
strength_skill_map: [{activity: "...", energy: charges|drains}]
cognitive_load_mode: holds|switches
social_graph: [{person: "...", energy: gives|takes, attachment: "...", unresolved_loss: true|false}]
memory_access: [{period: "...", access: vivid|factual|amnesiac}]
value_conflicts: [{pair: "...", declared: "...", revealed: "...", note: "..."}]
session_state: {ns_buffer: low|normal|strained|overloaded}   # operational, NOT a trait

delta_log: []                       # v3.1: living profile, append-only [{date, source, domain, fact}]. Empty on fresh synthesis.
```

> **Schema contract note (v3.2):** `identity`, `svoboda_scores`, and `tags` are NESTED maps; `triggers`, `blind_spots`, `domains_active` are FLAT lists; `predictive_model` is a list of `{situation, behavior}` rows. The scaffolder flattens `tags` itself as `core_confirmed + refined` (retired tags are tombstoned, not applied). A blank template lives at `memory/svoboda/profile.template.yaml`.

**Synthesis rules:**
- Every pattern → tag (e.g., `#conflict_avoider`)
- Every tag → origin from a [FACT] quote of theirs, or `origin: not given` (no quote → the origin is not invented)
- Predictive model: 5-7 common decision points
- Blind spots: what they can't see
- Corrections log: where initial read was wrong

### Phase 4b: Scoring Gate (≥80 to accept)

Score the profile (the agent scores ITS OWN work, not the person scoring themselves) against `context/scoring-gate.md` AND the Profile Quality Checklist:
- Every tag has origin traced OR explicitly `not given` (+20)
- Predictive model evidence-based, not archetypal (+20)
- ≥2 corrections logged (+15)
- Non-obvious blind spots (+15)
- One "doesn't fit the system" finding (+15)
- Speech pattern analysis present if voice data (+10)
- Phase 1 ≥5/7 AND Phase 2 ≥3/6 (+5)

**Gate before the checklist:** fewer than two cards shown and confirmed (`cards_confirmed`) → do not synthesize at all. A first run is always `depth: provisional`. If there are ≥2 cards but the checklist is <65 — don't stop and don't write "too guarded": emit provisional and move on (a first run over text objectively cannot earn the +10 for speech and the +5 for coverage).

<80 → iterate the weakest section, re-probe (**max 2 cycles** — never loop a guarded subject indefinitely). 65–79 after 2 cycles → accept as **provisional**: emit the profile with a header caveat `Depth: provisional — re-cut when the subject is ready`, set `depth: provisional` in profile.yaml, and proceed (skip no downstream phase). <65 after 2 cycles: if `cards_confirmed` ≥ 2 — provisional anyway, move on; never tell the person the session was "too guarded" (they answered everything they were asked). If there are fewer than two cards — don't synthesize, go back and do the next card. ≥80 → Phase 4c.

### Phase 4c: Entity Creation (knowledge graph integration)

1. Create/update `knowledge/people/{subject_id}.md` with YAML frontmatter (type, tags from profile, profile_version, dates). Body = condensed profile (no link to a separate profile file — none is generated, so don't emit a dangling wikilink).
2. Add `[[{subject_id}]]` backlink in `knowledge/moc/MOC_people.md` (if it doesn't exist yet — it ships with only AGENTS.md — create it with a `# People` header first, matching vault-scaffolder Step 10).
3. For each `#tag`: link to or stub `knowledge/concepts/{tag}.md`.
4. Log to `memory/svoboda/{subject_id}/log.md`: `[date] [svoboda] {id} synthesized → score={N}, phases={...}, tags={N}`
5. Update session YAML: `synthesized: true, synthesis_score: {N}`.

### Phase 4d: Operational Layer (NEW v3)

Three operational artifacts that turn the profile from snapshot → living document.

**Created only when the person explicitly asks for them.** Nothing is pre-filled with numbers: the
agent's observed numbers live in the domain cards and in `profile.yaml`; they do not migrate into
the journal or the dashboard. Write each of these in the language the person writes in.

1. **`memory/svoboda/{subject_id}/pp.md`** — the dashboard. Only if the person wants to track
   numbers month by month themselves; the month row stays empty — your observed numbers do not go
   in here:
   ```markdown
   # Dashboard — {subject_id}

   You keep this yourself, if you want to see movement month by month. The trajectory matters, not
   the absolute value.

   | Month | Self-development | Vitality | Surroundings | Wealth | Rest | Work | Assets | Notes |
   |-------|---|---|---|---|---|---|---|-------|
   | {YYYY-MM} |  |  |  |  |  |  |  |  |
   ```

2. **`memory/svoboda/{subject_id}/plan-fact.md`** — daily journal template:
   ```markdown
   # PLAN vs FACT — {subject_id}

   ## {YYYY-MM-DD}
   **Plan:** {what was planned}
   **Fact:** {what was done}
   **Reflection:**
   1. What was today like? (2-3 adjectives)
   2. Who or what am I grateful to?
   3. The main lesson?

   **Nervous-system buffer (last 2 weeks):** depleted / normal / at the limit
   ```
   v3.2: the **NS buffer** line is a session-state modifier, NOT a domain and NOT a trait. Svoboda records it so the same reaction reads correctly (a flare in `overloaded` = physiology; in `normal` = a stable pattern) and it **modifies interpretation, it does not trigger an intervention**.

3. **`memory/svoboda/{subject_id}/plans.md`** — Point A → B → C → G roadmap:
   ```markdown
   # PLANS — {subject_id}

   ## Key metric
   {measurable, e.g. "personal income per month"}

   ## Point A (now)
   {value} — {date}

   ## Point B (in 3 months)
   {target} — {date}
   **Why:** {motivation}
   **How:** {steps}

   ## Point C (in 6 months)
   {target}

   ## Point G (strategic)
   {long-term north star — derived from profile.north_star}
   ```
   Pre-fill Point G from `profile.yaml.north_star`.

After generation: `operational_layer_done: true` in session YAML.

### Phase 5: Scaffold Hand-off (optional)

`/svoboda-profiler {subject_id} scaffold` AND `synthesized: true`:
1. Read `memory/svoboda/{subject_id}/profile.yaml` — verify exists
2. Run `/vault-scaffolder {subject_id}` — personalizes the folder **in the current workspace** (skills + templates already ship here)
3. Verify CLAUDE.md / context files were written in place
4. Update session YAML: `scaffolded: true`
5. Tell user: `"Vault personalized — restart Claude Code here to activate."`

## Living Profile — delta accrual (v3.1)

The pre-3.1 weakness: `profile.yaml` is a one-shot snapshot dated `synthesized`, re-cut "annually" — so it silently decays. People change between birthdays; the profile lags reality for months. v3.1 closes this with a **delta layer between full re-cuts** (auto-accrued facts + pattern reports regenerated on accumulation).

**How it works:**

1. **Log drift, don't wait for the annual cut.** `/svoboda-profiler {id} delta "{fact}"` appends one entry to `profile.yaml.delta_log` and bumps `delta_count_since_synthesis`:
   ```yaml
   - {date: 2026-06-12, source: session|note|observed, domain: delo, fact: "dropped project X, north_star drifted"}
   ```
   A delta is a **fact that contradicts or extends the synthesized baseline** — a changed north_star, a domain that moved, a trigger that appeared/dissolved. Not a daily mood. The profiler (or any other skill that learns something durable — e.g. a `/reflect` consolidation pass) writes these. Deltas are **candidates**, never silent rewrites of the causal core.

2. **Staleness trigger.** When `delta_count_since_synthesis` crosses ~3, OR a delta lands on a domain whose meaning materially changed → flag that domain for re-cut (`update {domain}`). Cheap, surgical, keeps the snapshot honest without forcing a full annual session early.

3. **Resynthesize = versioned diff, not rewrite.** `/svoboda-profiler {id} resynthesize` re-runs Phase 4 reading the prior `profile.yaml` + `profile.md` + accrued `delta_log` + operational-layer journal, and emits **what changed since `profile_version` N**: moved scores, new/retired tags, predictive-model updates. Bump `profile_version`, reset `delta_count_since_synthesis: 0`, fold resolved deltas into the body, keep an entry in the corrections log. **The causal core (Phase 3 genesis, origin-traced tags) is sticky** — deltas update facts and active domains, not the childhood etiology, unless a genuine new origin surfaces.

This makes the profile a true living document (Principle 3) operationally, not just aspirationally.

## Measurement vs intervention boundary

This is a **diagnostic** instrument. Adopt the measurement engine; reject the therapy engine. Recorded here so the boundary stays explicit on future edits.

**In scope (measurement / freshness):**
- Living profile / delta accrual + version diff.
- Granularity coverage map — a **diagnostic yardstick** (`references/granularity_instrument.md`), NOT a daily logger.
- Volunteered-score vs observed — only when the person named a number unasked.
- v3.2 deep layers 7–13 — conversational MEASUREMENT scored from speech, each rendered flat (no clinical labels to the subject), each with a non-therapy boundary baked into its probe.
- Social graph (refines Surroundings) + memory-availability map (lens in Phase 3) — diagnostic refinements, not new domains.
- NS-buffer session-state — an interpretation modifier only, NOT wired to regulation routing.

**Out of scope (intervention / retention):**
- Guided paths / CBT worksheets, "regulation tasks" → diagnose, do not intervene. If intervention is ever wanted, it lives in a SEPARATE skill that *reads* `profile.yaml` as context and never writes judgments into it. Keep the diagnostic↔intervention boundary at the file level.
- Symptom-screening telos (rate distress → route to a treatment track) → contradicts fixed Point A, non-judgmental scoring.
- Streaks / mascot / proactive nudges / gamification → retention apparatus, noise for a personal tool.
- Subject-facing daily mood log → the taxonomy is the profiler's instrument, not a logging burden on the subject.

## Key Principles

1. **Causality > description.** "He's analytical" = worthless. "She rehearses every decision in advance because a volatile parent made surprises unsafe in childhood" = profile.
2. **Point A ≠ the goal.** This is about FIXING current state, not aspirational. Don't push subject toward "10s everywhere" — record where they actually are.
3. **Living document, not snapshot.** v3 added the operational layer; v3.1 adds the delta layer. Log drift as it happens, resynthesize on accrual, re-cut domains annually as the floor.
4. **Colour/number as a signal, not a verdict.** A low OBSERVED score with confidence ≥ med = where attention is needed, not judgment. Low confidence = "you didn't talk about this", not a weak spot. The agent sets the number and shows it for checking — the person is never asked to rate themselves.
5. **Corrections > projections.** If subject corrects you — log it. The correction IS the data.
6. **Speech = data.** How they speak matters as much as what. Voice preferred for that reason.
7. **A skip = a gap in the data.** What they skip is a gap to fill or a boundary they closed — not a diagnosis.
8. **Not therapy.** Profiling, not healing. No "you should work on this." Just the map.

## Voice — an optional extra input

The normal input is text: the package ships no transcription, and there is no reason to make the
person install anything for onboarding. If they already have something to transcribe a recording
with, let them drop the text of the transcript into `inbox/`, and from there it reads as an
ordinary story (saved into `stories/`). A transcript additionally shows HOW the person speaks:
jumps, self-corrections, the density of emotional words. Names, numbers and cities you half-caught
are always `[?]` until confirmed.

## References

- `references/domain_probes.md` — per-domain sub-questions used to count coverage (Phase 1 Step B)
- `references/svoboda_questions.md` — a fallback questions bank for blank-page syndrome, when the
  person doesn't know what to say about an area. Not a questionnaire and never read straight
  through — you take one or two and ask them in your own words. There are no self-rating questions
  in it, and there must never be.
- `scripts/check_quotes.py` — checks a card's quotes against the person's stories (Phase 1 Step D, mandatory before showing)
- `references/deep_layers.md` — Phase 2 questioning framework
- `references/granularity_instrument.md` — v3.1: emotion-family + body-signal coverage map (Layer 1 diagnostic yardstick)
- `references/parents_brief.md` — Phase 3 family system brief
- `references/synthesis_template.md` — Phase 4 narrative output structure + Quality Checklist
- `memory/svoboda/profile.template.yaml` — blank canonical profile.yaml to copy and fill
