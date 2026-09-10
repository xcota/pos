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
3. Файла нет → **не показывай человеку английскую ошибку и не проси его вводить вторую команду.**
   На первом заходе профиль пишется прямо сейчас: вернись в `svoboda-profiler` Phase 4 и
   синтезируй по правилу первого захода — **≥2 подтверждённых карточки → `profile.yaml` с
   `depth: provisional`** (пять сфер и три слоя нужны только для полного прохода). Карточек
   меньше двух → покажи следующую карточку, а человеку одной строкой: «Пока рано собирать —
   давайте пройдём ещё одну сферу».

## Gate — две подтверждённые карточки (проверить ДО первого шага)

Читай `memory/svoboda/{subject_id}/session.yaml` → `cards_confirmed`. Меньше двух сфер, которые
человек увидел и подтвердил или поправил, — **не собирать папку**. Сказать ему обычными словами:

> Пока рано собирать: я показал вам {N} карточку из семи. Давайте пройдём ещё одну, и я соберу.

Собранная из непроверенных выводов папка — это ярлыки, которые потом грузятся каждый запуск.
Гейт не обходится ни аргументом, ни просьбой «просто собери» — вместо этого покажи следующую
карточку.

**Две карточки — это и весь порог первого захода.** Ждать пяти сфер и трёх глубинных слоёв на
`run_type: fresh` не нужно: с `depth: provisional` папка собирается полностью (кто вы, цели,
карточки сфер, обложка), а глубина добирается дальше. Одно и то же правило записано в
`svoboda-profiler` Phase 4 и в `start` ③.

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

svoboda_scores:                                   # NESTED map, agent's OBSERVED read per domain (int, or null = «об этом не говорили»)
  samorazvitie: int
  vitalnost: int
  okruzhenie: int
  bogatstvo: int
  otdyh: int
  delo: int
  aktivy: int

score_confidence: {domain: low|med|high}          # confidence per domain (coverage-based)
growth_edges_named: [str, ...]                    # сферы, где человек САМ назвал дыру — ТОЛЬКО они идут в «куда вложиться» и в 🟡 (Step 5b, Step 6). Моя низкая цифра туда не попадает: она живёт в карточке сферы как моё прочтение
cards_confirmed: [str, ...]                       # подтверждённые карточки (дублируется из session.yaml)
depth: provisional|confirmed                      # первый проход всегда provisional
interface_draft: {channel, reply_len, language, profanity, address, lists, avoid: []}
                                                  # форма общения → context/identity.md § «Как со мной работать»
self_scoring: not_asked|volunteered               # у человека цифру не спрашивают

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

**Slugify `subject_id`.** Enforce the package naming rule (`rules/naming-convention.md`: `[a-z0-9_-]` only). If `subject_id` (or the `/svoboda-profiler` arg) has spaces, uppercase, or non-ASCII (e.g. `Иван Петров`, `John Smith`), transliterate/slugify it (`ivan-petrov`, `john-smith`) and use the slug for ALL filenames, `[[wikilinks]]` (Steps 9–10) and the `memory/svoboda/{subject_id}/` folder. Preserve the original display name as `title: "..."` in the Step 9 person-entity frontmatter. Warn, don't hard-fail.

### Step 1 — Ensure directory structure

```bash
mkdir -p context knowledge/people knowledge/concepts knowledge/moc state daily reports scripts
```

Skills and templates already exist from the starter repo. If `_templates/` or `.claude/skills/` are missing, warn but continue — do NOT generate them.

### Step 2 — Generate CLAUDE.md (OVERWRITE blank onboarding version)

**CRITICAL FILE.** Must be < 3500 bytes. This OVERWRITE replaces the blank onboarding stub, but it MUST carry the SAME methodology the blank `CLAUDE.md` ships with — just personalized. Do **not** flatten to a generic "## Context" boot: the personalized file has to keep the identity-first Boot (pointing at `context/root.md`), the Scope-gate, the three Orchestration tiers, and the Memory pointer, or scaffolding destroys the doctrine. The blank ships at 3458B, so the sections below lean on pointers to `context/` docs to stay under budget once name/triggers/style are added. Fill `{placeholders}` from the normalized profile:

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
{style} communication. {cognitive_style} learner. Language: {identity.languages[0]}.
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

The entry page the owner opens. It SHIPS in Russian, already structured — **read it, then fill
it in place. Keep it in Russian, keep every section and the plain-word glosses.** What to fill:
- Title: `# {identity.name} — Главная`
- Drop the "Страница пока пустая" line — it is only true before onboarding
- The mindmap: keep the 7 СВОБОДА domains and their plain-word glosses as shipped; add the value
  from `svoboda_scores` ONLY for a domain the interview actually covered. A domain with thin
  coverage keeps the words `об этом не говорили` instead of a number — never invent one
- Quick links: leave as shipped
- North-star line: replace `{{from north_star}}` with `north_star`, verbatim, in the owner's words

### Step 5 — Fill context/identity.md (in place, IN RUSSIAN, preserve hand edits)

`context/identity.md` ships as a template **in plain Russian** — read it first and fill it in
place, keeping every section and its wording. **Заполняется по-русски, бытовыми словами.**
Ярлыков, английских терминов и служебных кодов (`#tags`, названий полей `profile.yaml`) в
этом файле нет: его открывает и правит человек, а не только агент.

**Правки человека сохраняются.** Перед записью прочитай текущий файл и сравни: строку, которую
человек дописал, поправил или вычеркнул, **не восстанавливай и не переписывай**. Обновляй
только то, что пришло из свежего профиля и раньше писал ты сам. Это обещано в шапке файла
(«правьте руками — при пересборке ваши правки сохраняются») и в README.

Куда что кладётся:

| Раздел файла | Из чего |
|---|---|
| Шапка + `## Коротко` | `identity.name/age/role/languages/timezone`, `updated: {today}`, `profile_version` |
| `## Как со мной работать` | `interface_draft` (обращение, длина, темп, язык и регистр, списки, `avoid[]`). Каждая строка с датой. Пустое поле — оставить пустым. **На повторном прогоне НЕ перезаписывается:** его дописывает `/session-save` по живым поправкам; сохранить существующие строки, добавить только новые |
| `## Что вы сами про себя сказали` | дословные цитаты из `stories/` с датами — только его слова |
| `## Как вы думаете и учитесь` | `cognitive_style` + `style`, развёрнутые обычными словами (не «scanning», а «пробегает по верхам и возвращается») |
| `## Что вас заряжает и что выматывает` | `strength_skill_map`, если есть; нет — раздел остаётся пустым |
| `## Что вас злит` | `triggers[]`, его формулировками |
| `## Как вы отвечаете под нагрузкой` | наблюдения с источником + `cadence.chronotype`; ярлыков и диагнозов не писать |
| `## Что вы обычно делаете в типовых ситуациях` | `predictive_model[]` → таблица «ситуация → что сделает» |
| `## Мои догадки о том, чего вы про себя не видите` | `blind_spots[]`, каждая как догадка с основанием (они же засевают профильные анти-паттерны в Step 7) |
| `## Чего я про вас не знаю` | сферы и подвопросы без охвата (`svoboda_scores: null`, низкая уверенность) — честно, а не пусто |
| `## Снято` | `tags.retired_from_baseline` + прежние формулировки, которые человек поправил. Ничего не удалять молча |

Правила заполнения:

- Тегов списком в файл не выносим: каждый значимый тег разворачивается в строку обычными
  словами в подходящем разделе. Служебный список тегов живёт в `knowledge/people/{subject_id}.md`
  (Step 9), где его читает только агент.
- Ярлыков без его цитаты не писать вообще: тип привязанности, «Big Five», «реакция на стресс»
  одним словом — нет цитаты, нет строки.
- Цифры по сферам в этот файл не переносим: они живут в карточках `memory/svoboda/{id}/domains/`
  и в `profile.yaml`. Сюда — только словами, и только то, что человек видел.
- Первый заход = `depth: provisional`: разделы, под которые данных нет, остаются пустыми с их
  курсивной подсказкой. Пустой раздел честнее выдуманного.

### Step 5b — Fill context/root.md (identity anchor — CLAUDE.md boots it every session)

`context/root.md` ships as a fill-in template with `{{ }}` placeholders in §1 and §3 and two illustrative EXAMPLE blockquotes. CLAUDE.md's Boot step 2 loads it as the light-cone anchor, and README + docs/methodology.md promise the scaffolder fills it — so an unfilled root.md is a broken boot. **Read `context/root.md` first** (Write requires read-before-write; it is also fill-in-place — §2 and §4 are portable doctrine that must survive verbatim). Then:

1. **§1 WHO** (the `_{{from identity…}}_` block, ~line 32): write the identity core from `identity.name` + `identity.age` + 4–6 core `tags_all` rendered as `#hashtag`-style descriptors (each a one-clause "how they decode/engage the world" note), + the integrity/anger trigger drawn from `triggers[]` if one exists (frame as `Anger trigger: #… — …`), + agreeableness / neuroticism markers if derivable from tags/style. Match the shape shown in the §1 EXAMPLE blockquote, then **DELETE that EXAMPLE blockquote** (lines ~39–44).
2. **North Star** (the `- **North Star:**` line, ~line 36): fill **verbatim** from `north_star`.
3. **§3 REAL DOMAINS** (the `_{{from svoboda_scores…}}_` block, ~line 64): one line per real life-domain from `domains_active`, grouped (e.g. **WORK / GROWTH / SYSTEM**). Each line: `domain — [where the material lives] · status-emoji`. Set the emoji: сфера из `growth_edges_named` (человек САМ назвал дыру) → 🟡; пусто (`null`) или низкая уверенность → ⚪ с подписью «об этом не говорили» (никогда не ноль и не 🟡); всё остальное → 🟢. **Моя низкая цифра сама по себе 🟡 не даёт** — она остаётся в карточке сферы как моё прочтение; ярлык «куда вложиться» человек получает только со своих слов (то же правило в схеме выше, в Step 6 и в `docs/onboarding-flow.md`). Mark off-repo material explicitly (that boundary is the "OS only sees part of my life" blind spot). Then **DELETE the §3 EXAMPLE blockquote** (lines ~68–80).
4. **Top note** (the blockquote at ~lines 10–16): after fill it is no longer a blank template — replace the "Until then this boots as a template" sentence with a one-line `Personalized {today}.` marker. **Keep** the "single source the field-of-view (the 'cone') is assembled from" sentence.
5. **Leave §2 (the four functions) and §4 (THE CONE RULE) EXACTLY as shipped** — portable engine doctrine, do NOT personalize.
6. Set the frontmatter `updated: {today}`.

**Re-run safety.** §1 / North Star / §3 are profile-derived — **refresh them every run** from the current profile (consistent with how Step 6 refreshes North Star + Domains to Develop). §2 and §4 are never touched.

### Step 6 — Fill context/goals.md (PRESERVE user goals on re-run)

`goals.md` ships as a fill-in template. Read it first, then:
- YAML frontmatter: `type: context`, `tags: [goals, strategy]`
- `## North Star` — verbatim from `north_star` (refresh every run — profile-derived)
- `## Domains to Develop` («куда вложиться») — **только сферы из `growth_edges_named[]`, где человек сам назвал дыру своими словами.** Моя низкая цифра сюда не идёт ни при какой уверенности: она остаётся в карточке сферы как моё прочтение, и человек может с ней не согласиться. Пустая цифра (`null`) — тем более не повод. Одно правило, слово в слово в схеме, Step 5b и `docs/onboarding-flow.md`. Refresh every run — profile-derived
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
- СВОБОДА scores inline
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

If a source file is missing, generate a stub from profile data (see `svoboda-profiler` Phase 4d for format; pre-fill Точка G from `north_star`). If the destination already exists, skip it.

## Verification (mandatory)

After all steps:

1. `wc -c CLAUDE.md` — **must be < 3500 bytes**. Also confirm it still carries the Boot (with `context/root.md`), Scope-gate, three Orchestration tiers, and Memory sections — not a flat "## Context" boot.
2. `find . -maxdepth 1 -name "*.md" | sort` — verify key files at root
3. `ls context/ knowledge/people/ state/` — verify generated dirs
4. `context/root.md` — **no `{{ }}` placeholders and no EXAMPLE blockquotes remain**; §1 WHO, North Star, and §3 domains are filled from the profile; §2 and §4 are untouched.
5. Verify all `[[wikilinks]]` resolve to actual files in the vault
6. Confirm `tags` was read as a nested map and `tags_retired` was NOT applied as live traits
7. `context/identity.md` — по-русски, все разделы на месте, раздел «Как со мной работать»
   заполнен из `interface_draft` (или пуст, если данных не было); ярлыков без источника нет;
   строки, дописанные или поправленные человеком, сохранены
8. Гейт соблюдён: в `session.yaml.cards_confirmed` было ≥2 сферы до начала сборки

## Output

```
Folder personalized — {N} files written.
CLAUDE.md: {bytes} bytes (< 3500 ✓)
context/root.md: identity anchor filled (§1 WHO · North Star · §3 domains) ✓
СВОБОДА: С:{s} В:{v} О:{o} Б:{b} О:{o2} Д:{d} А:{a}
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
- Do NOT собирать папку, пока человек не подтвердил хотя бы две карточки (`cards_confirmed` ≥ 2).
- Do NOT перезаписывать раздел «Как со мной работать» на повторном прогоне — он растёт из поправок человека.
- Do NOT затирать правки человека в `context/identity.md` и do NOT писать этот файл по-английски — человек его открывает и правит руками.
- Do NOT ставить 🟡 / «куда вложиться» по своей низкой цифре — только по сферам из `growth_edges_named` (Step 5b, Step 6).
- Do NOT писать в профиль ярлык без его цитаты (тип привязанности, черты, «реакция на стресс»).
- Do NOT write outside the workspace.
