---
name: svoboda-profiler
version: 3.1
user_invocable: true
description: "Deep psychological profiling + life-state mapping through structured conversation. 7 life domains + 6 deep layers + origin mapping. Multi-session, resume-able, language-adaptive. Triggers: profile, unpack, get to know me, setup, распаковка, профиль."
---

# Profiler v3.1

Build (1) a **causal psychological profile** AND (2) a **living life-state document** through structured conversation. Not a personality test — a guided unpacking that reveals *why* someone operates the way they do AND maps where they are now.

**Output:**
1. Narrative profile (`profile.md`) — psychological portrait with tags, origins, predictive model
2. Machine-readable profile (`profile.yaml`) — feeds downstream `vault-scaffolder`
3. Operational layer (`pp.md` + `plan-fact.md` + `plans.md`) — living life-state tracking

## CRITICAL: Language adaptation

**All user-facing text must be in the user's language.** The session language is set from the user's first message (stored in session YAML as `language`).

- Domain names: translate to user's language (see table below for meaning)
- Questions: adapt, don't literally translate from Russian
- Progress card: in user's language
- Profile output: in user's language
- Internal keys in YAML stay English (samorazvitie, vitalnost, etc.)

## 7 Life Domains

| Key | Meaning | What to explore |
|-----|---------|-----------------|
| **growth** | Personal growth & learning | How they learn, education, skills, content, books, spiritual practices |
| **vitality** | Health & life force | Body, mental state, energy, relationship with health — NOT just physical |
| **environment** | People & surroundings | Where they live, who's around, networking, family, communication |
| **wealth** | Philosophy of abundance | What "rich" means to them. Spiritual/philosophical. NOT financial facts |
| **rest** | Recovery & leisure | What actually restores them — travel, nature, hobbies as REST not work |
| **work** | Career & projects | What they build, how they work, profession, business, revenue streams |
| **assets** | Financial reality | Income, savings, debts, passive income, financial literacy |

**Critical:** Wealth (philosophical) ≠ Assets (operational). Wealth = "what does abundance mean to you?" Assets = "what do you actually own?"

**For Russian speakers:** use СВОБОДА acronym (С-В-О-Б-О-Д-А). For others: use translated domain names.

## Invocation

- `/svoboda-profiler {subject_id}` — start new or resume existing session
- `/svoboda-profiler {subject_id} status` — current phase, blocks_completed, ETA
- `/svoboda-profiler {subject_id} synthesize` — force Phase 4 with collected data
- `/svoboda-profiler {subject_id} scaffold` — Phase 5 hand-off to vault-scaffolder
- `/svoboda-profiler {subject_id} update {domain}` — re-cut a single domain (annual refresh)

## Session State (multi-phase, resume-able)

```yaml
subject_id: {id}
started: {iso_date}
last_updated: {iso_date}
phase: 1
domains_completed: []   # subset of [samorazvitie, vitalnost, okruzhenie, bogatstvo, otdyh, delo, aktivy]
domains_scored: {}      # {domain: 1-10, ...} self-rating at start of each block
layers_completed: []    # subset of [granularity, motivation, losses, loneliness, anger, irreversibility]
parents_done: false
synthesized: false
operational_layer_done: false   # NEW v3: ПП + ПЛАН-ФАКТ + ПЛАНЫ generated
scaffolded: false
data_path: memory/svoboda/{subject_id}/
channel: claude-code
language: {ru|en}
```

Continue from `phase` + next uncompleted block. Never restart completed blocks. Every exchange writes raw data + updates session YAML atomically.

## Protocol

### Phase 1: 7 Доменов СВОБОДА (data collection + scoring)

For EACH domain, do this 2-step:

**Step A — Self-score gate (Anton's pattern):**
> "Оцени от 1 до 10 свою {domain} на текущий момент"

Record in `domains_scored[domain]`. This is the **baseline** for re-cuts.

**Step B — Open unpacking** with domain-specific probes:

1. **Саморазвитие** — НЕ дипломы, а *как* учится. Burst-mode? Conformist? What они rejected matters more. Skills (existing + wanted), content consumed, какие книги изменили жизнь.

2. **Витальность** — body relationship + mental state + "жажда жизни". Substances history if any. How they monitor/optimize. Interoception level. О чем думаешь когда просыпаешься. Что вдохновляет.

3. **Окружение** — physical environment (place of living, atmosphere), people network, communication channels. Кого хочешь в окружении (фантазия) vs кто есть (факт). Networking strategies. **Includes parents/family if person doesn't separate Phase 3.**

4. **Богатство** — *philosophical*. "Что для тебя богатство? Как ты поймешь что оно наступило?" Духовность. Relationship with abundance/scarcity. Что бы делали с unlimited resources.

5. **Отдых** — recovery patterns, travel, entertainment. Не хобби-проекты (те идут в Дело/Саморазвитие) — а то что *восстанавливает*. Влияние путешествий. Время на природе.

6. **Дело** — what they build, how they work, what tools, what they refuse to do. Бизнес/работа/проекты. Источники профессионального дохода (название проектов).

7. **Активы** — operational. Источники дохода (числа если дают), пассивный доход, ликвидные/неликвидные активы, пассивы, кредиты, финансовая грамотность, неверные финансовые решения в анамнезе.

**Collection guidelines:**
- One domain per exchange. Brief question, no preamble.
- Accept whatever format. After each domain: acknowledge, note key data, score, move on.
- If they go off-script into another domain — let them, remap later.
- Off-script content → `data_path/freeform.md`, integrate in synthesis.

**Progress display — MANDATORY after every completed domain:**

Show updated progress card in the USER'S LANGUAGE:

Example (Russian):
```
━━━ Распаковка: {name} ━━━
✅ Саморазвитие (7/10)
✅ Витальность (8/10)
▶ Окружение ← сейчас
◻ Богатство
◻ Отдых
◻ Дело
◻ Активы
───────────────
Фаза 1 из 4 · 3/7 · ~25 мин
```

Example (English):
```
━━━ Unpacking: {name} ━━━
✅ Growth (7/10)
✅ Vitality (8/10)
▶ Environment ← now
◻ Wealth
◻ Rest
◻ Work
◻ Assets
───────────────
Phase 1 of 4 · 3/7 · ~25 min
```

Example (Chinese):
```
━━━ 解锁: {name} ━━━
✅ 自我成长 (7/10)
✅ 生命力 (8/10)
▶ 环境与人际 ← 当前
◻ 财富哲学
◻ 休息与恢复
◻ 事业
◻ 资产
───────────────
阶段 1/4 · 3/7 · 约25分钟
```

Rules for progress:
- ✅ = completed (show self-score)
- ▶ = current
- ◻ = upcoming
- Time estimate: ~5-8 min per domain, ~15 min for deep layers, ~10 min for parents
- When Phase 1 completes, announce transition to deeper exploration
- When Phase 2 starts, show deep layers progress
- If user stops: show what's done, what's left, reassure progress is saved

### Phase 2: 6 Deep Layers (depth → causal map)

After 5+ domains collected, probe these. Read `references/deep_layers.md`.

1. **Эмоциональная гранулярность** — feel with high resolution or process emotions as data?
2. **Мотивация инструмента** — *why* do they want what they say they want?
3. **Проигрыши** — wounds (not lessons). What they lost and couldn't convert.
4. **Одиночество** — distinguish solitude from loneliness?
5. **Гнев** — what triggers real anger? Most diagnostic suppressed emotion.
6. **Необратимость** — what do they consider irreversible?

Layer 1 + Layer 3 most diagnostic — prioritize these.

### Phase 3: Parents/Origin (optional, high-value)

If open to it, read `references/parents_brief.md`. Genesis of patterns from Phases 1-2. Without it, profile describes but doesn't explain.

### Phase 4: Synthesis

Minimum: 5 Phase 1 domains + 3 Phase 2 layers. Read `references/synthesis_template.md`.

**Two artifacts in same turn:**

1. **Narrative profile** → `memory/svoboda/{subject_id}/profile.md` — full document per template (11 sections, tags, predictive model, blind spots, corrections log).

2. **Machine-readable profile** → `memory/svoboda/{subject_id}/profile.yaml`:
   ```yaml
   subject_id: {id}
   profile_version: {N.N}
   synthesized: {iso_date}
   identity:
     name: {...}
     age: {...}
     role: {...}
     languages: [...]
     timezone: {...}
   svoboda_scores:        # NEW v3: from domains_scored
     samorazvitie: {1-10}
     vitalnost: {1-10}
     okruzhenie: {1-10}
     bogatstvo: {1-10}
     otdyh: {1-10}
     delo: {1-10}
     aktivy: {1-10}
   domains_active: [...]  # subset of svoboda where person actually operates
   north_star: {...}      # 1 sentence
   style: direct|explanatory|mixed
   triggers: [...]        # 3-5 instant-frustration
   cognitive_style: scanning|deep-dive|burst|gradual
   cadence:
     chronotype: {...}
     reflection: weekly|biweekly|monthly|annual
   blind_spots: [...]
   predictive_model:
     - situation: {...}
       behavior: {...}
   tags: [...]
   ```

**Synthesis rules:**
- Every pattern → tag (create fresh from this person's data)
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

<80 → iterate weakest section, re-probe. ≥80 → Phase 4c.

### Phase 4c: Entity Creation (knowledge graph integration)

1. Create/update `knowledge/people/{subject_id}.md` with YAML frontmatter (type, tags from profile, profile_version, dates). Body = condensed profile + link `[[svoboda-profile-{subject_id}]]`.
2. Add `[[{subject_id}]]` backlink in `knowledge/moc/MOC_people.md`.
3. For each `#tag`: link to or stub `knowledge/concepts/{tag}.md`.
4. Log to `log.md`: `[date] [svoboda] {id} synthesized → score={N}, phases={...}, tags={N}`
5. Update session YAML: `synthesized: true, synthesis_score: {N}`.

### Phase 4d: Operational Layer (NEW v3 — Anton's contribution)

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
   ```

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
2. Run `/vault-scaffold {subject_id}` — generates full Personal OS vault
3. Verify vault created at `vaults/{subject_id}/` (or custom `--target`)
4. Update session YAML: `scaffolded: true, vault_path: vaults/{subject_id}/`
5. Tell user: `"Vault ready → cd vaults/{subject_id}/ && claude"`

## Key Principles

1. **Каузальность > описание.** "He's analytical" = worthless. "He processes emotions as data because he was his mother's emotional absorber at age 8" = profile.

2. **Точка А ≠ цель.** Anton's core insight: this is about FIXING current state, not aspirational. Don't push subject toward "10s everywhere" — record where they actually are.

3. **Living document, not snapshot.** v3 adds operational layer because static profile decays. Re-cut domains annually minimum.

4. **Цвет/скоринг как сигнал, не оценка.** When subject scores low — that's information about where attention needed, not judgment. Anti-pattern: framing as "good/bad".

5. **Коррекции > проекции.** If subject corrects you — log it. The correction IS the data.

6. **Речь = данные.** How they speak matters as much as what. Voice preferred for that reason.

7. **Отказ = данные.** What they skip is diagnostic.

8. **Не терапия.** Profiling, not healing. No "you should work on this." Just the map.

## Voice Input

If the user sends voice messages or audio files, ask them to transcribe or type the key points. Analyze speech patterns from text: topic switching, self-corrections, emotional vocabulary density.

## References

- `references/deep_layers.md` — Phase 2 questioning framework
- `references/parents_brief.md` — Phase 3 family system brief
- `references/synthesis_template.md` — Phase 4 narrative output structure + Quality Checklist
- `references/svoboda_questions.md` — 632 вопроса по 7 доменам (fallback при синдроме пустого листа, НЕ анкета)
