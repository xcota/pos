---
name: vault-scaffolder
version: 3.0
user_invocable: true
description: "Use when a completed svoboda profile.yaml exists and a fresh Camomile folder needs to be personalized in the current workspace."
---

# /vault-scaffolder — Personalize Camomile (in-place)

Takes a completed svoboda `profile.yaml` (v3.2 schema) and personalizes Camomile **in the current workspace**. Overwrites the blank onboarding `CLAUDE.md`, writes `context/identity.md`, `context/goals.md`, the self-entity, and the operational layer, and **appends** profile-specific anti-patterns to the shipped corpus.

**Assumes the engine is already present.** Skills (`.claude/skills/`), templates (`_templates/`), `context/scoring-gate.md`, AND the shipped engine corpus — `context/anti-patterns.md`, `anti-patterns-index.md`, `context/learned.md`, `learned-index.md`, `rules/*.md` — all ship with the starter repo. The scaffolder personalizes content; it does NOT re-scaffold skills, templates, or the AP/L corpus. **It NEVER regenerates `anti-patterns.md` or `learned.md` — it appends to them.**

**Reads the v3.2 nested schema directly** (see contract below). It does not require the profiler to flatten anything.

## Invocation

```
/vault-scaffolder {subject_id}
```

## Input

1. **Required:** `{subject_id}` argument
2. Read `memory/svoboda/{subject_id}/profile.yaml`
3. No file → **don't show the person a raw error and don't ask them to type a second command.**
   On a first run the profile is written right now: go back into `svoboda-profiler` Phase 4 and
   synthesize by the first-run rule — **≥2 confirmed cards → `profile.yaml` with
   `depth: provisional`** (five domains and three layers are only needed for a full pass). Fewer
   than two cards → show the next card, and tell the person in one line: "It's early to build yet —
   let's go through one more area."

## Gate — two confirmed cards (check BEFORE step one)

Read `memory/svoboda/{subject_id}/session.yaml` → `cards_confirmed`. Fewer than two areas that the
person has seen and confirmed or corrected — **do not build the folder**. Say so in ordinary words,
in their language:

> It's early to build: I've shown you {N} card out of seven. Let's do one more and then I'll build.

A folder built from unverified conclusions is a set of labels that then loads on every boot. The
gate is not bypassed by an argument or by "just build it" — show the next card instead.

**Two cards are the whole threshold of a first run.** On `run_type: fresh` there is no need to wait
for five domains and three deep layers: with `depth: provisional` the folder is built in full (who
you are, goals, area cards, front page), and depth accrues afterwards. The same rule is written in
`svoboda-profiler` Phase 4 and in `start` ③.

## profile.yaml — schema contract (v3.2, must match svoboda-profiler)

This is the SAME canonical schema defined in `svoboda-profiler/SKILL.md` Phase 4. Read these exact keys. Nesting matters.

```yaml
subject_id: str                                   # kebab-case, == folder name
profile_version: str                              # top-level (e.g. "2.0")
synthesized: str                                  # YYYY-MM-DD

identity:                                         # NESTED map
  name: str
  age: int
  role: str
  languages: [str, ...]                           # languages[0] = primary
  timezone: str                                   # IANA tz

svoboda_scores:                                   # NESTED map, agent's OBSERVED read per domain (int, or null = "you didn't talk about this")
  samorazvitie: int
  vitalnost: int
  okruzhenie: int
  bogatstvo: int
  otdyh: int
  delo: int
  aktivy: int

score_confidence: {domain: low|med|high}          # confidence per domain (coverage-based)
growth_edges_named: [str, ...]                    # domains where the person NAMED a gap themselves — ONLY these go into "where to invest" and into 🟡 (Step 5b, Step 6). My own low number does not: it stays in the domain card as my reading
cards_confirmed: [str, ...]                       # confirmed cards (duplicated from session.yaml)
depth: provisional|confirmed                      # a first run is always provisional
interface_draft: {channel, reply_len, language, profanity, address, lists, avoid: []}
                                                  # shape of the conversation → context/identity.md § "How to work with me"
self_scoring: not_asked|volunteered               # the person is never asked for a number

domains_active: [str, ...]                        # FLAT list
north_star: str                                   # 1-2 sentences, verbatim into goals.md
style: direct|explanatory|mixed
cognitive_style: scanning|deep-dive|burst|gradual
triggers: [str, ...]                              # FLAT list, 3-5 items
blind_spots: [str, ...]                           # FLAT list
predictive_model: [{situation: str, behavior: str}, ...]   # list of rows

tags:                                             # NESTED map (NOT a flat list)
  core_confirmed: [str, ...]
  refined: [str, ...]
  retired_from_baseline: [str, ...]

synthesis_constraint: str                         # optional free-text guardrail

# Optional / advisory (read if present, otherwise skip — do NOT fail):
score_divergence: [...]
granularity_coverage: {...}
cadence: {chronotype, reflection}
# plus v3.2 deep-layer fields (attachment, attribution, ...) — NOT consumed here.
```

### tags normalization (THE fix — read carefully)

`tags` is a **nested map** in v3.2, not a flat list. Earlier scaffolder versions expected `tags: [str, ...]` and broke on this shape. Normalize ONCE at the top of generation, then use the flat form everywhere downstream:

```
tags_all     = tags.core_confirmed + tags.refined      # applied to the vault
tags_retired = tags.retired_from_baseline              # tombstoned — recorded once, NOT applied
```

Whenever a step below says "tags", it means `tags_all`. Never apply `tags_retired` as live traits.

If a legacy `profile.yaml` provides `tags` as a flat list, treat the whole list as `tags_all` and `tags_retired = []` (backward compatible).

### Other tolerant reads

- `granularity_coverage.emotion_families_absent` may appear as `emotion_families_thin` in some profiles — accept either.
- Any optional field absent → skip the dependent line, do not error.

## Generation Steps

All paths relative to workspace root (`.`).

> **Fill-in-place, don't flatten.** Several targets SHIP as richer templates than the inline blocks below: `context/identity.md` (full skeleton), `MEMORY.md` (index taxonomy), `HOME.md`, `context/goals.md`. For those, **Read the shipped file first, then fill its sections in place** — replace `{{ }}` / `_placeholder_` text, keep every section, table, and frontmatter tag. The inline blocks here are the *fields to populate*, not a replacement file. Only `CLAUDE.md` (Step 2) is a true OVERWRITE (it ships as a blank onboarding stub). The Write tool also refuses to overwrite a file it hasn't read, so Read-before-write is required regardless.
> **Re-run safety.** On a re-run against an already-personalized vault, user-filled content must survive: Steps 6 and 11 preserve user sections, Step 7 de-dups, Step 12 skips existing files — see each step.

### Step 0 — Load + normalize

Read `profile.yaml`. Compute `tags_all` and `tags_retired` per the rule above. Resolve `today` (synthesis date or current date). All later steps use these.

**Slugify `subject_id`.** Enforce the package naming rule (`rules/naming-convention.md`: `[a-z0-9_-]` only). If `subject_id` (or the `/svoboda-profiler` arg) has spaces, uppercase, or non-ASCII (e.g. `李明`, `José Núñez`, `John Smith`), transliterate/slugify it (`li-ming`, `jose-nunez`, `john-smith`) and use the slug for ALL filenames, `[[wikilinks]]` (Steps 9–10) and the `memory/svoboda/{subject_id}/` folder. Preserve the original display name as `title: "..."` in the Step 9 person-entity frontmatter. Warn, don't hard-fail.

### Step 1 — Ensure directory structure

```bash
mkdir -p context knowledge/people knowledge/concepts knowledge/moc state daily reports scripts
```

Skills and templates already exist from the starter repo. If `_templates/` or `.claude/skills/` are missing, warn but continue — do NOT generate them.

### Step 2 — Generate CLAUDE.md (OVERWRITE blank onboarding version)

**CRITICAL FILE.** Must be < 3500 bytes. This OVERWRITE replaces the blank onboarding stub, but it MUST carry the SAME methodology the blank `CLAUDE.md` ships with — just personalized. Do **not** flatten to a generic "## Context" boot: the personalized file has to keep the identity-first Boot (pointing at `context/root.md`), the Scope-gate, the three Orchestration tiers, and the Memory pointer, or scaffolding destroys the doctrine. The blank onboarding stub ships at 3617B (it carries the multilingual welcome line, which the personalized file drops), so the sections below lean on pointers to `context/` docs to stay under budget once name/triggers/style are added. Fill `{placeholders}` from the normalized profile:

```markdown
# {identity.name} — Camomile

{identity.name}, {identity.age}. {identity.role}. Agent = memory + execution + mirror.

## Rules
1. Results first. Explanation if asked.
2. Direct. No filler. No hedging.
3. Initiative + instant correction.
4. Don't repeat mistakes → `context/anti-patterns.md`
5. Match the energy.
6. Don't claim unfinished work.
7. Parallelism via subagents.
8. Optimize, don't rebuild.
9. Mechanics > surface (HOW > WHAT).
10. Screwed up → fix, don't excuse.

## Boot (identity-first, minimal cone — load only what the task needs)
1. This file — boot rules + budget (auto-loaded).
2. `context/root.md` — who you serve + the through-line; the light-cone starts here.
3. `context/identity.md` — full profile. `MEMORY.md` — index, not content. `state/current.md` — cross-context state.
4. Then by task: `context/` (goals, anti-patterns, learned) · `knowledge/` (`[[wikilinks]]`).

Load boot context — don't ask. Expand the cone only as far as the task reaches.

## Scope-gate (FIRST, before any multi-file build or agent workflow)
Name the user's verb → the smallest artifact that closes it → deliver THAT first. A narrow verb (check / find / make-a-file / short) = a narrow artifact + the right tool, **not** an apparatus (swarm / treatise / site / strategy). Apparatus only if explicitly asked OR impossible without it. Depth of reasoning ≠ size of apparatus.

## Orchestration (main thread = dispatcher, not worker)
- **Tier 1 — Direct:** 1 file, <50 lines, no web, no multi-step. Inline.
- **Tier 2 — Single agent:** Explore / Plan / general-purpose. 2+ tasks → parallel.
- **Tier 3 — Dynamic workflow:** fan-out / adversarial-verify / judge. **Agent count ≠ quality.** Full doctrine: `context/workflow-doctrine.md`.

## Memory
Real memory = the Markdown graph in git. Optional **semantic-recall module** (`scripts/memory_index.py` + warm server + PostToolUse hook) lets `/recall` find by meaning; `grep`/`rg` is the fallback.

## Triggers (instant frustration)
{triggers joined with ` | `}

## Budget
Working-set 60K target · 100K ceiling → `/session-save` → `/compact`. Boot ~15–25K.

## Hard rules
1. Binary question → 1–3 lines.
2. `knowledge/` uses `[[wikilinks]]` — every `[[` must resolve.
3. Git local. Make files when a task needs them; never multiply for their own sake.
4. Filenames `[a-z0-9_-]` only.

## Style
{style} communication. {cognitive_style} learner. Speak the language the person writes in; theirs is {identity.languages[0]}.
{synthesis_constraint, if present, as one line: "Constraint: {...}"}
```

Use only the `triggers` that exist (join with ` | `; do not pad to 5).

**After writing:** `wc -c CLAUDE.md` — MUST be < 3500. If over, trim in this order: (1) the **Style** section (drop `cognitive_style` / the `Constraint:` line first, then collapse to one line); (2) the **Memory** line (shorten to `Real memory = the git Markdown graph; optional semantic-recall via /recall, grep is fallback.`). Never trim Boot, Scope-gate, or Orchestration — those ARE the methodology. A realistic sample fill of this template measures ~2500B, so there is ~1000B of headroom for longer names/roles/triggers.

### Step 3 — Generate MEMORY.md

```markdown
- [Identity](context/identity.md) — psychological profile, triggers, blind spots
- [Goals](context/goals.md) — north star and current objectives
- [Anti-patterns](context/anti-patterns.md) — what NOT to do (engine corpus + your appended ones)
- [Learned](context/learned.md) — durable operating lessons (engine corpus)
- [Scoring gate](context/scoring-gate.md) — quality threshold for outputs
- [Self](knowledge/people/{subject_id}.md) — self-entity in knowledge graph
```

### Step 4 — Fill HOME.md (in place)

The entry page the owner opens. It SHIPS already structured — **read it, then fill it in place.
Write it in the language the person writes in, keep every section and the plain-word glosses.**
What to fill:
- Title: `# {identity.name} — Home`
- Drop the "This page is still empty" line — it is only true before onboarding
- The mindmap: keep the 7 domains and their plain-word glosses as shipped; add the value from
  `svoboda_scores` ONLY for a domain the interview actually covered. A domain with thin coverage
  keeps the words `you didn't talk about this` instead of a number — never invent one
- Quick links: leave as shipped
- North-star line: replace `{{from north_star}}` with `north_star`, verbatim, in the owner's words
- `## How to use me`: keep as shipped — the four words, the two offers, the guide link — translated into the person's language; keep the code spans, and point the guide link at `docs/<lang>/guide.md` for their language (en / zh / ru)

### Step 5 — Fill context/identity.md (in place, IN THE PERSON'S LANGUAGE, preserve hand edits)

`context/identity.md` ships as a template in plain words — read it first and fill it in place,
keeping every section and its wording. **Write it in the language the person writes in, in ordinary
everyday words.** No labels, no English jargon and no internal codes (`#tags`, `profile.yaml` field
names) in this file: it is opened and edited by the person, not only by the agent. Section
headings are translated along with the rest; file names and keys stay as they are.

**The person's edits survive.** Before writing, read the current file and compare: a line the
person added, corrected or struck out is **never restored and never rewritten**. Update only what
came from the fresh profile and was written by you in the first place. That is promised in the
file's own header ("edit it by hand — your edits survive a rebuild") and in the README.

What goes where:

| Section of the file | From what |
|---|---|
| Header + `## In short` | `identity.name/age/role/languages/timezone`, `updated: {today}`, `profile_version` |
| `## How to work with me` | `interface_draft` (address, length, pace, language and register, lists, `avoid[]`). Every line with a date. An empty field stays empty. **Not overwritten on a re-run:** `/session-save` grows it from live corrections; keep the existing lines, add only new ones |
| `## What you said about yourself` | verbatim quotes from `stories/` with dates — their words only |
| `## How you think and learn` | `cognitive_style` + `style`, unpacked into ordinary words (not "scanning" but "skims the surface and comes back") |
| `## What charges you and what drains you` | `strength_skill_map`, if present; if not, the section stays empty |
| `## What makes you angry` | `triggers[]`, in their own phrasing |
| `## How you respond under load` | observations with a source + `cadence.chronotype`; no labels, no diagnoses |
| `## What you usually do in typical situations` | `predictive_model[]` → a "situation → what they'll do" table |
| `## My guesses about what you don't see` | `blind_spots[]`, each as a guess with its grounds (the same ones seed the profile anti-patterns in Step 7) |
| `## What I don't know about you` | domains and sub-questions with no coverage (`svoboda_scores: null`, low confidence) — honestly, rather than blank |
| `## Withdrawn` | `tags.retired_from_baseline` + earlier wordings the person corrected. Nothing is deleted silently |

Filling rules:

- No list of tags goes into this file: each meaningful tag is unfolded into a line of ordinary
  words in the section it belongs to. The internal tag list lives in
  `knowledge/people/{subject_id}.md` (Step 9), where only the agent reads it.
- Never write a label without their quote: attachment type, "Big Five", a one-word "stress
  reaction" — no quote, no line.
- Domain numbers are not copied into this file: they live in the cards
  `memory/svoboda/{id}/domains/` and in `profile.yaml`. Here — words only, and only what the person
  has seen.
- A first run = `depth: provisional`: sections with no data stay empty with their italic hint. An
  empty section is more honest than an invented one.

### Step 5b — Fill context/root.md (identity anchor — CLAUDE.md boots it every session)

`context/root.md` ships as a fill-in template with `{{ }}` placeholders in §1 and §3 and two illustrative EXAMPLE blockquotes. CLAUDE.md's Boot step 2 loads it as the light-cone anchor, and README + docs/methodology.md promise the scaffolder fills it — so an unfilled root.md is a broken boot. **Read `context/root.md` first** (Write requires read-before-write; it is also fill-in-place — §2 and §4 are portable doctrine that must survive verbatim). Then:

1. **§1 WHO** (the `_{{from identity…}}_` block, ~line 32): write the identity core from `identity.name` + `identity.age` + 4–6 core `tags_all` rendered as `#hashtag`-style descriptors (each a one-clause "how they decode/engage the world" note), + the integrity/anger trigger drawn from `triggers[]` if one exists (frame as `Anger trigger: #… — …`), + agreeableness / neuroticism markers if derivable from tags/style. Match the shape shown in the §1 EXAMPLE blockquote, then **DELETE that EXAMPLE blockquote** (lines ~39–44).
2. **North Star** (the `- **North Star:**` line, ~line 36): fill **verbatim** from `north_star`.
3. **§3 REAL DOMAINS** (the `_{{from svoboda_scores…}}_` block, ~line 64): one line per real life-domain from `domains_active`, grouped (e.g. **WORK / GROWTH / SYSTEM**). Each line: `domain — [where the material lives] · status-emoji`. Set the emoji: a domain from `growth_edges_named` (the person NAMED the gap themselves) → 🟡; empty (`null`) or low confidence → ⚪ labelled "you didn't talk about this" (never a zero and never 🟡); everything else → 🟢. **My own low number does not by itself earn a 🟡** — it stays in the domain card as my reading; the "where to invest" label comes only from their own words (the same rule in the schema above, in Step 6 and in `docs/en/onboarding-flow.md`). Mark off-repo material explicitly (that boundary is the "OS only sees part of my life" blind spot). Then **DELETE the §3 EXAMPLE blockquote** (lines ~68–80).
4. **Top note** (the blockquote at ~lines 10–16): after fill it is no longer a blank template — replace the "Until then this boots as a template" sentence with a one-line `Personalized {today}.` marker. **Keep** the "single source the field-of-view (the 'cone') is assembled from" sentence.
5. **Leave §2 (the four functions) and §4 (THE CONE RULE) EXACTLY as shipped** — portable engine doctrine, do NOT personalize.
6. Set the frontmatter `updated: {today}`.

**Re-run safety.** §1 / North Star / §3 are profile-derived — **refresh them every run** from the current profile (consistent with how Step 6 refreshes North Star + Domains to Develop). §2 and §4 are never touched.

### Step 6 — Fill context/goals.md (PRESERVE user goals on re-run)

`goals.md` ships as a fill-in template. Read it first, then:
- YAML frontmatter: `type: context`, `tags: [goals, strategy]`
- `## North Star` — verbatim from `north_star` (refresh every run — profile-derived)
- `## Domains to Develop` ("where to invest") — **only domains from `growth_edges_named[]`, where the person named the gap in their own words.** My own low number never goes here at any confidence: it stays in the domain card as my reading, and the person may disagree with it. An empty number (`null`) is even less of a reason. One rule, word for word in the schema, in Step 5b and in `docs/en/onboarding-flow.md`. Refresh every run — profile-derived
- `## Active Goals` — **user-owned.** FRESH vault: leave header-only empty tables (strip the `_e.g. …{{thing}}…_` example rows so no placeholder shows). RE-RUN (goals.md already has user rows): **preserve the existing Active Goals block verbatim** — never wipe a returning user's goals. Only North Star + Domains to Develop refresh.

### Step 7 — APPEND profile anti-patterns (PRESERVE the shipped corpus, de-dup on re-run)

The starter already ships `context/anti-patterns.md` with the universal engine corpus (AP-001..NNN) + the 3-tier escalation mechanism, plus `anti-patterns-index.md`, `context/learned.md`, and `learned-index.md`. **These are the kept baseline — do NOT regenerate or overwrite them. Append only.** (Append-only / never-renumber is the corpus's own contract — see the `anti-patterns.md` header.)

Profile APs live in ONE delimited block so a re-run replaces them instead of duplicating:

1. **De-dup first.** If `context/anti-patterns.md` already contains a `<!-- profile-aps:start -->` … `<!-- profile-aps:end -->` block, you are RE-RUNNING — **replace that whole block in place**, do NOT append a second copy. (No markers = fresh vault → append a new block at the end.)
2. Read `context/anti-patterns.md`; find the highest existing `AP-NNN` outside the profile block. Profile APs number sequentially from the next free ID (never renumber existing ones).
3. For each `blind_spots[]` item, write one AP (Trigger / Why / Do-instead) inside the `<!-- profile-aps:start/end -->` block. Cross-reference the matching `predictive_model[]` row where one exists.
4. **Index** (`context/anti-patterns-index.md` is a CLUSTER table C1–C5 + watch-list, NOT a per-AP status list): maintain ONE cluster row, id `profile` — Theme = "personal growth edges from the profile", Members = the comma-separated profile AP IDs, Hard-rule = "none". On a re-run, update that single row's Members; never add a second `profile` row.
5. Leave `context/learned.md` and both `*-index.md` corpus bodies intact (the boot files generated in Steps 2–3 already link them).

### Step 8 — Verify context/scoring-gate.md exists

Ships with the starter repo. If missing, generate a minimal version:
```markdown
---
type: context
---
# Scoring Gate
Score every deliverable 0-100 before accepting. Below 80 → iterate with specific feedback.
```

### Step 9 — Generate knowledge/people/{subject_id}.md

Self-entity file:
- YAML frontmatter: `type: person`, `tags: {tags_all}`, `created: {today}`, `profile_version: {profile_version}`
- Role, age, key characteristics
- The 7 domain scores inline
- North-star reference
- Do NOT add wikilinks to files that don't exist in the vault

### Step 10 — Generate knowledge/moc/MOC_people.md

```markdown
# People
- [[{subject_id}]]
```

### Step 11 — Generate state/current.md (only if absent — never clobber user state)

**Skip this step if `state/current.md` already exists.** It holds a returning user's cross-context state (Active Context, open threads, in-vault AP citations) written by `/session-save`, `/ingest`, `/session-start` — a re-profile must not wipe it. Generate only on a fresh vault:

```markdown
---
type: state
updated: {today}
---
# Current State

Vault personalized: {today}
Profile version: {profile_version}
Source: svoboda-profiler

## Active Context
Fresh vault — no active work yet.
```

### Step 12 — Copy operational layer

From `memory/svoboda/{subject_id}/`, copy each **only if the destination does not already exist** (never clobber user-filled data on a re-run):
- `pp.md` → `./pp.md`
- `plan-fact.md` → `./plan-fact.md`
- `plans.md` → `./plans.md`

If a source file is missing, generate a stub from profile data (see `svoboda-profiler` Phase 4d for format; pre-fill Point G from `north_star`). If the destination already exists, skip it.

## Verification (mandatory)

After all steps:

1. `wc -c CLAUDE.md` — **must be < 3500 bytes**. Also confirm it still carries the Boot (with `context/root.md`), Scope-gate, three Orchestration tiers, and Memory sections — not a flat "## Context" boot.
2. `find . -maxdepth 1 -name "*.md" | sort` — verify key files at root
3. `ls context/ knowledge/people/ state/` — verify generated dirs
4. `context/root.md` — **no `{{ }}` placeholders and no EXAMPLE blockquotes remain**; §1 WHO, North Star, and §3 domains are filled from the profile; §2 and §4 are untouched.
5. Verify all `[[wikilinks]]` resolve to actual files in the vault
6. Confirm `tags` was read as a nested map and `tags_retired` was NOT applied as live traits
7. `context/identity.md` — in the person's language, every section in place, the "How to work with
   me" section filled from `interface_draft` (or empty, if there was no data); no labels without a
   source; lines the person added or corrected are preserved
8. The gate held: `session.yaml.cards_confirmed` had ≥2 domains before the build started

## Output

```
Folder personalized — {N} files written.
CLAUDE.md: {bytes} bytes (< 3500 ✓)
context/root.md: identity anchor filled (§1 WHO · North Star · §3 domains) ✓
Domains: samorazvitie:{s} vitalnost:{v} okruzhenie:{o} bogatstvo:{b} otdyh:{o2} delo:{d} aktivy:{a}
Tags applied: {len(tags_all)} (retired/skipped: {len(tags_retired)})

Restart Claude Code in this directory to activate the personalized agent.
```

(`{N}` counts `context/root.md` among the written files.)

## Anti-patterns

- Do NOT treat `tags` as a flat list — it is a nested map (`core_confirmed`/`refined`/`retired_from_baseline`). Flatten via the Step 0 rule.
- Do NOT apply `tags.retired_from_baseline` — those are tombstoned claims a prior run withdrew.
- Do NOT re-scaffold skills or templates — they ship with the starter; this step only personalizes content.
- Do NOT exceed 3500 bytes on CLAUDE.md — Claude Code truncates at ~4000 silently.
- Do NOT flatten Step 2's CLAUDE.md to a generic "## Context" boot — the personalized file MUST carry the same methodology as the blank one (identity-first Boot → `context/root.md`, Scope-gate, three Orchestration tiers, Memory pointer). Scaffolding a vault must not strip the doctrine.
- Do NOT leave `context/root.md` unfilled (Step 5b) — CLAUDE.md boots it every session as the identity anchor. Fill §1 WHO / North Star / §3 domains from the profile and delete both EXAMPLE blockquotes; a vault shipped with `{{ }}` placeholders in root.md is a broken boot.
- Do NOT personalize §2 or §4 of `context/root.md` — they are portable engine doctrine (the four functions + the cone rule); fill only §1, North Star, and §3.
- Do NOT create `[[wikilinks]]` to nonexistent files.
- Do NOT include content from another subject's profile — every vault is unique to its subject.
- Do NOT fail on optional v3.2 fields being absent — skip the dependent line.
- Do NOT wipe user data on a re-run — preserve Active Goals (Step 6), skip existing `state/current.md` (Step 11), de-dup profile APs into the delimited block (Step 7), skip existing operational files (Step 12).
- Do NOT overwrite the richer shipped templates (`identity.md`, `MEMORY.md`, `HOME.md`, `goals.md`) with the thin inline blocks — fill them in place (see the Generation Steps preamble).
- Do NOT write a non-`[a-z0-9_-]` `subject_id` into a filename — slugify in Step 0.
- Do NOT build the folder until the person has confirmed at least two cards (`cards_confirmed` ≥ 2).
- Do NOT overwrite the "How to work with me" section on a re-run — it grows out of the person's own corrections.
- Do NOT wipe the person's edits in `context/identity.md`, and do NOT write that file in a language they don't write in — they open and edit it by hand.
- Do NOT hand out a 🟡 / "where to invest" on your own low number — only for domains in `growth_edges_named` (Step 5b, Step 6).
- Do NOT write a label into the profile without their quote (attachment type, traits, "stress reaction").
- Do NOT write outside the workspace.
