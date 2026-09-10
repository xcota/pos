---
name: svoboda-profiler
version: 3.2
user_invocable: true
description: "Use when asked to profile someone, unpack a person, build a psychological portrait, run a Svoboda session, or map life state. Triggers on распаковка, профилирование, психопортрет, точка А, колесо баланса, profile someone, unpack, svoboda session."
---

# Svoboda Profiler v3.2

Build (1) a **causal psychological profile** AND (2) a **living life-state document** through structured conversation. Not a personality test, not a balance wheel — a guided unpacking that reveals *why* someone operates the way they do AND maps where they are now → where they're going.

**Approach:** Fixed Point A (current state), not aspirational targets. Re-cut on accrual; annual refresh as the floor.

**Output triple:**
1. Narrative profile (`profile.md`) — psychological portrait with tags, origins, predictive model
2. Machine-readable profile (`profile.yaml`) — feeds downstream `vault-scaffolder`. **Canonical schema is defined once, below in Phase 4, and the scaffolder reads that exact shape.**
3. Operational layer (`pp.md` + `plan-fact.md` template + `plans.md`) — living life-state document

## СВОБОДА = 7 доменов (acronym)

| Letter | Domain | Focus |
|--------|--------|-------|
| **С** | **С**аморазвитие | learning, education, skills, content consumption, personal growth |
| **В** | **В**итальность | health, body, energy, mental state, "жажда жизни" — NOT just physical |
| **О** | **О**кружение | environment, place of living, people, networking, communication channels |
| **Б** | **Б**огатство | philosophical relationship with wealth — what does "rich" mean to them, духовность |
| **О** | **О**тдых | rest, recovery, travel, entertainment, hobbies as recovery (NOT skill-building) |
| **Д** | **Д**ело | work, business, projects, profession, what they DO |
| **А** | **А**ктивы | financial assets, income sources, asset management, liabilities |

**Critical distinction:** Богатство (philosophical) ≠ Активы (operational). Богатство is "what does wealth mean to you / you can be rich and stingy or poor and generous". Активы is "what assets do you actually own and how do you manage them".

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
domains_scored: {}      # {domain: 1-10, ...} self-rating at start of each block
layers_completed: []    # subset of [granularity, motivation, losses, loneliness, anger, irreversibility, attachment, attribution, rumination, boundary, temporal, strengths, load_mode]
parents_done: false
synthesized: false
operational_layer_done: false   # NEW v3: ПП + ПЛАН-ФАКТ + ПЛАНЫ generated
scaffolded: false
profile_version: 0              # v3.1: bumps on each (re)synthesis
last_delta: null                # v3.1: iso_date of last logged drift fact
delta_count_since_synthesis: 0  # v3.1: staleness trigger — re-cut a domain when this crosses threshold
data_path: memory/svoboda/{subject_id}/
channel: {claude-code|telegram}
language: {ru|en}
```

Continue from `phase` + next uncompleted block. Never restart completed blocks. Every exchange writes raw data + updates session YAML atomically.

## Protocol

### Phase 1: 7 Доменов СВОБОДА (data collection + scoring)

For EACH domain, do this 2-step:

**Step A — Self-score gate + triangulation (v3.1):**
> "Оцени от 1 до 10 свою {domain} на текущий момент"

Record the self-number in `domains_scored[domain]`. But a bare self-score is gameable (self-flattery / blind spots). After Step B, set your OWN profiler-observed score from the evidence collected — that observed number is what goes into `profile.yaml.svoboda_scores` (the honest baseline downstream uses). Where self ≠ observed, log the gap to `score_divergence`. **The divergence is data** — same logic as the corrections log, applied to numbers: a subject who rates Дело 8 but describes only stalled projects → record `{self:8, observed:4}`, don't average it away. Keep triangulation organic, NOT a forced-choice battery, which would break the conversation ethos.

**Step B — Open unpacking** with domain-specific probes:

1. **Саморазвитие** — НЕ дипломы, а *как* учится. Burst-mode? Conformist? What они rejected matters more. Skills (existing + wanted), content consumed, какие книги изменили жизнь.

2. **Витальность** — body relationship + mental state + "жажда жизни". Substances history if any. How they monitor/optimize. Interoception level. О чем думаешь когда просыпаешься. Что вдохновляет.

3. **Окружение** — physical environment (place of living, atmosphere), people network, communication channels. Кого хочешь в окружении (фантазия) vs кто есть (факт). Networking strategies. **Includes parents/family if person doesn't separate Phase 3.**

4. **Богатство** — *philosophical*. "Что для тебя богатство? Как ты поймешь что оно наступило?" Духовность. Relationship with abundance/scarcity. Что бы делали с unlimited resources.

5. **Отдых** — recovery patterns, travel, entertainment. Не хобби-проекты (те идут в Дело/Саморазвитие) — а то что *восстанавливает*. Влияние путешествий. Время на природе.

6. **Дело** — what they build, how they work, what tools, what they refuse to do. Бизнес/работа/проекты. Источники профессионального дохода.

7. **Активы** — operational. Источники дохода (числа если дают), пассивный доход, ликвидные/неликвидные активы, пассивы, кредиты, финансовая грамотность, неверные финансовые решения в анамнезе.

**Collection guidelines:**
- One domain per exchange. Brief question, no preamble.
- Voice preferred (reveals speech patterns + density).
- Accept whatever format. After each domain: acknowledge, note key data, score, move on.
- If they go off-script into another domain — let them, remap later.
- Off-script content → `data_path/freeform.md`, integrate in synthesis.

### Phase 2: 13 Deep Layers (depth → causal map)

After 5+ domains collected, probe these. Read `references/deep_layers.md`. Layers 1–6 are the core; 7–13 (v3.2) add causal angles as MEASUREMENT, never therapy. Where a layer carries an academic typology (attachment type, attribution axes, mode-under-load), hold it as a **silent profiler yardstick** scored from speech — never read the labels to the subject.

1. **Эмоциональная гранулярность** — feel with high resolution or process emotions as data? **(v3.1: score against the coverage map in `references/granularity_instrument.md` — which emotion families + body-signal channels they spontaneously reach vs systematically never name.)**
2. **Мотивация инструмента** — *why* do they want what they say they want?
3. **Проигрыши** — wounds (not lessons). What they lost and couldn't convert.
4. **Одиночество** — distinguish solitude from loneliness?
5. **Гнев** — what triggers real anger? Most diagnostic suppressed emotion.
6. **Необратимость** — what do they consider irreversible?
7. **Привязанность** (v3.2) — when someone close pulls away, what fires first? Type as causal pattern + genesis. → Section V.
8. **Атрибуция** (v3.2) — where the cause flies on failure vs who gets credit on success. Asymmetry = predictive lever. → Section VI + XIII.
9. **Руминация vs рефлексия** (v3.2) — does the thought loop in place or turn a new side? Resolves "no off-switch."
10. **Граница под давлением** (v3.2) — self-erasure (yield to keep the bond) vs system-integrity (hold + anger), and the switch-point.
11. **Временна́я перспектива** (v3.2) — which time they decide from; future-as-plan vs future-as-deferral.
12. **Силы vs навыки** (v3.2) — what charges vs what drains; causal to burnout / role-fit. Deepens Дело.
13. **Когнитивный режим под нагрузкой** (v3.2) — does analytic mode hold or flip under stress; where it goes rigid. Strictest non-therapy watch.

Layer 1 + Layer 3 most diagnostic — prioritize these. Layer 7 (привязанность) + Layer 10 (граница) feed Section V; Layer 13 predicts crisis behavior.

### Phase 3: Parents/Origin (optional, high-value)

If open to it, read `references/parents_brief.md`. Genesis of patterns from Phases 1-2. Without it, profile describes but doesn't explain.

**v3.2 — memory-availability map (lens, not a new phase):** across the session (esp. here) notice the DENSITY of access by period — which years come with emotion and detail, which only as dry fact, which get skipped. The distribution itself is suppression data, independent of content (e.g. a vivid window around one parent vs a functional/compressed account of a painful stretch points at where the pattern-generator hides). Probe gently and optionally ("that stretch — what do you remember alive, not facts?"). **Map the distribution, do NOT excavate or "process" the repressed** — this is a pointer for attention, not trauma work (Principle 8). Fold the narrative-coherence signal in here too: a self-version discarded without integration (an earlier self spoken of as a closed, disowned chapter) = the same fragmentation signal, one line, not a separate construct. Record to `memory_access` in profile.yaml.

### Phase 4: Synthesis

Minimum: 5 Phase 1 domains + 3 Phase 2 layers. Read `references/synthesis_template.md`.

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

svoboda_scores:                     # [scaffolder] nested map, OBSERVED 1-10 per domain (profiler's honest read)
  samorazvitie: {1-10}
  vitalnost: {1-10}
  okruzhenie: {1-10}
  bogatstvo: {1-10}
  otdyh: {1-10}
  delo: {1-10}
  aktivy: {1-10}

score_divergence:                   # v3.1: only domains where self ≠ observed — the gap IS the data
  - {domain: delo, self: 8, observed: 4, note: "rates high, describes only stalled projects"}

domains_active: [...]               # [scaffolder] subset of svoboda where person actually operates

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
- Every tag → traced origin (childhood/family/experience)
- Predictive model: 5-7 common decision points
- Blind spots: what they can't see
- Corrections log: where initial read was wrong

### Phase 4b: Scoring Gate (≥80 to accept)

Self-score against `context/scoring-gate.md` AND Profile Quality Checklist:
- Every tag has traceable origin (+20)
- Predictive model evidence-based, not archetypal (+20)
- ≥2 corrections logged (+15)
- Non-obvious blind spots (+15)
- One "doesn't fit the system" finding (+15)
- Speech pattern analysis present if voice data (+10)
- Phase 1 ≥5/7 AND Phase 2 ≥3/6 (+5)

<80 → iterate the weakest section, re-probe (**max 2 cycles** — never loop a guarded subject indefinitely). Still 65–79 after 2 cycles → accept as **provisional**: emit the profile with a header caveat `Depth: provisional — re-cut when the subject is ready`, set `depth: provisional` in profile.yaml, and proceed (skip no downstream phase). <65 after 2 cycles → stop; tell the user the session was too guarded to synthesize and offer to resume later. ≥80 → Phase 4c.

### Phase 4c: Entity Creation (knowledge graph integration)

1. Create/update `knowledge/people/{subject_id}.md` with YAML frontmatter (type, tags from profile, profile_version, dates). Body = condensed profile (no link to a separate profile file — none is generated, so don't emit a dangling wikilink).
2. Add `[[{subject_id}]]` backlink in `knowledge/moc/MOC_people.md` (if it doesn't exist yet — it ships with only AGENTS.md — create it with a `# People` header first, matching vault-scaffolder Step 10).
3. For each `#tag`: link to or stub `knowledge/concepts/{tag}.md`.
4. Log to `memory/svoboda/{subject_id}/log.md`: `[date] [svoboda] {id} synthesized → score={N}, phases={...}, tags={N}`
5. Update session YAML: `synthesized: true, synthesis_score: {N}`.

### Phase 4d: Operational Layer (NEW v3)

Generate THREE operational artifacts that turn the profile from snapshot → living document:

1. **`memory/svoboda/{subject_id}/pp.md`** — Приборная панель. Monthly self-rating dashboard:
   ```markdown
   # Приборная панель — {subject_id}

   Self-score 1-10 each domain monthly. Track trajectory, not absolute.

   | Месяц | С | В | О | Б | О | Д | А | Notes |
   |-------|---|---|---|---|---|---|---|-------|
   | {YYYY-MM} | {1-10} | ... | | | | | | initial baseline from Phase 1 |
   ```
   Pre-fill row with `domains_scored` from session YAML.

2. **`memory/svoboda/{subject_id}/plan-fact.md`** — daily journal template:
   ```markdown
   # ПЛАН-ФАКТ — {subject_id}

   ## {YYYY-MM-DD}
   **План:** {что планировал}
   **Факт:** {что сделал}
   **Рефлексия:**
   1. Каким был сегодняшний день? (2-3 прилагательных)
   2. Кому/чему благодарен?
   3. Главный урок?

   **Скоринг:** Здоровье _ | Энергия _ | Работа _ | Финансы _ | Развлечения _ | Любовь _
   **Буфер НС (последние 2 недели):** на дне / в норме / на пределе
   ```
   v3.2: the **NS buffer** line is a session-state modifier, NOT a domain and NOT a trait. Svoboda records it so the same reaction reads correctly (a flare in `overloaded` = physiology; in `normal` = a stable pattern) and it **modifies interpretation, it does not trigger an intervention**.

3. **`memory/svoboda/{subject_id}/plans.md`** — Точка A → B → C → G roadmap:
   ```markdown
   # ПЛАНЫ — {subject_id}

   ## Ключевая метрика
   {измеримая, e.g. "личный доход в мес"}

   ## Точка A (сейчас)
   {value} — {date}

   ## Точка B (через 3 месяца)
   {target} — {date}
   **Зачем:** {motivation}
   **Как:** {steps}

   ## Точка C (через 6 месяцев)
   {target}

   ## Точка G (стратегическая)
   {long-term north star — derived from profile.north_star}
   ```
   Pre-fill Точка G from `profile.yaml.north_star`.

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
- Self-score triangulation (`{self, observed}` pair).
- v3.2 deep layers 7–13 — conversational MEASUREMENT scored from speech, each rendered flat (no clinical labels to the subject), each with a non-therapy boundary baked into its probe.
- Social graph (refines Окружение) + memory-availability map (lens in Phase 3) — diagnostic refinements, not new domains.
- NS-buffer session-state — an interpretation modifier only, NOT wired to regulation routing.

**Out of scope (intervention / retention):**
- Guided paths / CBT worksheets, "regulation tasks" → diagnose, do not intervene. If intervention is ever wanted, it lives in a SEPARATE skill that *reads* `profile.yaml` as context and never writes judgments into it. Keep the diagnostic↔intervention boundary at the file level.
- Symptom-screening telos (rate distress → route to a treatment track) → contradicts fixed Point A, non-judgmental scoring.
- Streaks / mascot / proactive nudges / gamification → retention apparatus, noise for a personal tool.
- Subject-facing daily mood log → the taxonomy is the profiler's instrument, not a logging burden on the subject.

## Key Principles

1. **Каузальность > описание.** "He's analytical" = worthless. "She rehearses every decision in advance because a volatile parent made surprises unsafe in childhood" = profile.
2. **Точка А ≠ цель.** This is about FIXING current state, not aspirational. Don't push subject toward "10s everywhere" — record where they actually are.
3. **Living document, not snapshot.** v3 added the operational layer; v3.1 adds the delta layer. Log drift as it happens, resynthesize on accrual, re-cut domains annually as the floor.
4. **Цвет/скоринг как сигнал, не оценка.** When subject scores low — that's information about where attention is needed, not judgment. Anti-pattern: framing as "good/bad".
5. **Коррекции > проекции.** If subject corrects you — log it. The correction IS the data.
6. **Речь = данные.** How they speak matters as much as what. Voice preferred for that reason.
7. **Отказ = данные.** What they skip is diagnostic.
8. **Не терапия.** Profiling, not healing. No "you should work on this." Just the map.

## Voice Input

Voices → local transcription (use whatever local transcriber you have — e.g. `mlx_whisper` on Mac, or any whisper build; no script ships). If none is available, ask the user to paste a text transcript — voice is *preferred* for speech-pattern data, but text intake is fully supported. Then analyze content + speech patterns (topic switching, self-corrections, emotional vocabulary density, pause patterns).

## References

- `references/deep_layers.md` — Phase 2 questioning framework
- `references/granularity_instrument.md` — v3.1: emotion-family + body-signal coverage map (Layer 1 diagnostic yardstick)
- `references/parents_brief.md` — Phase 3 family system brief
- `references/synthesis_template.md` — Phase 4 narrative output structure + Quality Checklist
- `memory/svoboda/profile.template.yaml` — blank canonical profile.yaml to copy and fill
