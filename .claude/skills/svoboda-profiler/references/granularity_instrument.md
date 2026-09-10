# Granularity Instrument — coverage map (v3.1)

Layer 1 (emotional granularity) used to be scored impressionistically ("count emotion words vs cognitive words"). This turns it into a **measurable coverage map**: which emotion families and body-signal channels the subject *spontaneously reaches* in natural speech vs which they *systematically never name*.

Distilled from a clinical emotion catalog (a ~66-emotion + body-feeling taxonomy). Repurposed: this is the **profiler's yardstick**, NOT a list to read to the subject or have them fill in. Never prompt with the list — that contaminates the measurement. You score against it silently from how they already talk.

## How to use

1. Run the Layer 1 probes from `deep_layers.md` (recent specific event + present-moment "what's the feeling right now").
2. Listen across the whole session, not just Layer 1 — emotional vocabulary leaks everywhere.
3. Mark each family/channel the subject **reaches on their own**. Don't credit a family they only confirm after you name it.
4. Record three things in `profile.yaml.granularity_coverage`: families reached, families **absent**, body channels reached.

**v3.2 active body-probe (optional, one beat):** on a clearly charged recent episode, ask once "where did that sit in your body?" — it surfaces which body channels they can reach under live affect. This is the entire somatic add; do NOT turn it into a per-state body axis the subject logs daily (that's the rejected mood-tracker posture).

**The absence is the signal.** Reached families show range. The family they *never* touch — and especially one they detour around when an event clearly contains it — is the diagnostic finding. Cross-reference: a subject whose every story has obvious anger but who never names an anger-family word is suppressing it (feed Layer 5); one who never reaches any longing/sadness family is either resilient or bypassing (feed Layer 3/4).

## Emotion families (14)

A "reach" = naming a felt **state**, not an outcome or a cognitive verdict.

| # | Family | Example tokens (RU) | Notes |
|---|--------|---------------------|-------|
| 1 | Радость / подъём | радость, восторг, кайф, воодушевление, эйфория | high-arousal positive |
| 2 | Покой / удовлетворённость | спокойствие, умиротворение, довольство, расслабленность | low-arousal positive — often absent in driven people |
| 3 | Нежность / любовь | нежность, тепло, привязанность, влюблённость, умиление | attachment-positive |
| 4 | Благодарность | благодарность, признательность, тронут | prosocial — telling when absent |
| 5 | Интерес / азарт | любопытство, увлечённость, азарт, предвкушение | drive-positive — usually present in builders |
| 6 | Гордость / уверенность | гордость, уверенность, удовлетворение собой | agency-positive |
| 7 | Грусть / печаль | грусть, печаль, тоска, уныние, горе | low-arousal negative |
| 8 | Одиночество / тоска по | одиночество, заброшенность, тоска по кому-то | distinct from #7 — feed Layer 4 |
| 9 | Страх / тревога | страх, тревога, беспокойство, паника, опасение | threat-negative |
| 10 | Стыд / вина | стыд, вина, смущение, неловкость, сожаление | self-conscious — heavily suppressed in many |
| 11 | Злость / гнев | раздражение, злость, гнев, ярость, возмущение | feed Layer 5; outcome-substitution common here |
| 12 | Отвращение / презрение | отвращение, брезгливость, презрение | boundary-negative |
| 13 | Зависть / ревность | зависть, ревность, обида | comparative — rarely volunteered, high-signal |
| 14 | Перегруз / опустошение | перегрузка, истощение, апатия, пустота, оцепенение, отупение | the "норм/не норм/перегрузка" floor — if this is the ONLY register reached, granularity is low |

## Body-signal channels (8)

Interoception map. A subject who narrates feeling only through #14-floor words but locates precise body signals has felt-sense access without a vocabulary — different finding than someone with neither.

| # | Channel | Example signals |
|---|---------|-----------------|
| 1 | Грудь | сжатие / тяжесть / распирание / открытость в груди |
| 2 | Горло | ком, сжатие, перехват |
| 3 | Живот / нутро | узел, сосёт, бабочки, провал, тошнота |
| 4 | Голова | давление, туман, лёгкость, звон |
| 5 | Плечи / шея | напряжение, зажим, тяжесть |
| 6 | Дыхание | поверхностное / задержка / свободное / сбитое |
| 7 | Температура / энергия | жар, холод, мурашки, разряженность, гудит |
| 8 | Мышечный тонус | сжатые кулаки/челюсть, расслабленность, не усидеть |

## Reading the map

- **Wide families + precise body channels + control** → integrated EI. Note as strength.
- **Floor-only (#14) + few channels** → low granularity. NOT a deficit to "fix" (not therapy) — a structural fact: feeds the Эмоциональная архитектура section and likely a tag for how the subject relates to their own affect.
- **v3.2 — on the floor register, distinguish two very different reads:** an *even, neutral baseline* (steady positive/negative tone, just low resolution) vs a *muted/flattened affect* (a dampened tone that reads as defended-down rather than simply low-resolution — e.g. early environments that punished or never named feeling can leave this). Same floor-only vocabulary, opposite meaning — the second is a genesis signal to trace, not just low granularity. This is the entire affective-set-point add; no PA/NA axis, no PANAS.
- **Outcome-substitution tell** (describes #1/#11/#7 only via results — "я был продуктивен", "я просто закрыл вопрос") → emotions processed as data. Highest-value Layer 1 finding; corroborate with Layer 2 (motivation) and Layer 3 (loss).
- **One conspicuously absent family** that the events clearly contained → suppression. Route to the matching deep layer (anger→L5, loss/sadness→L3, loneliness→L4).

Coverage is a snapshot like everything else — re-score on `resynthesize`; a widening map over time is itself data (deltas).
