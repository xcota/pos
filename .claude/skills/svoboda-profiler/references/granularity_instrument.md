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

A "reach" = naming a felt **state**, not an outcome or a cognitive verdict. The example tokens are
in English; score whatever language the person actually speaks — what matters is the family, not
the word list.

| # | Family | Example tokens | Notes |
|---|--------|----------------|-------|
| 1 | Joy / elation | joy, delight, buzz, excitement, euphoria | high-arousal positive |
| 2 | Calm / contentment | calm, peace, contentment, relaxed | low-arousal positive — often absent in driven people |
| 3 | Tenderness / love | tenderness, warmth, affection, being in love, melting | attachment-positive |
| 4 | Gratitude | grateful, thankful, moved, touched | prosocial — telling when absent |
| 5 | Interest / drive | curiosity, absorption, eagerness, anticipation | drive-positive — usually present in builders |
| 6 | Pride / confidence | pride, confidence, satisfaction with oneself | agency-positive |
| 7 | Sadness / sorrow | sadness, sorrow, grief, gloom, heaviness | low-arousal negative |
| 8 | Loneliness / longing | loneliness, abandonment, missing someone | distinct from #7 — feed Layer 4 |
| 9 | Fear / anxiety | fear, anxiety, worry, panic, dread | threat-negative |
| 10 | Shame / guilt | shame, guilt, embarrassment, awkwardness, regret | self-conscious — heavily suppressed in many |
| 11 | Anger | irritation, anger, rage, fury, indignation | feed Layer 5; outcome-substitution common here |
| 12 | Disgust / contempt | disgust, revulsion, contempt | boundary-negative |
| 13 | Envy / jealousy | envy, jealousy, resentment | comparative — rarely volunteered, high-signal |
| 14 | Overload / depletion | overload, exhaustion, apathy, emptiness, numbness, blankness | the "fine / not fine / overloaded" floor — if this is the ONLY register reached, granularity is low |

## Body-signal channels (8)

Interoception map. A subject who narrates feeling only through #14-floor words but locates precise body signals has felt-sense access without a vocabulary — different finding than someone with neither.

| # | Channel | Example signals |
|---|---------|-----------------|
| 1 | Chest | tightness / heaviness / bursting / openness in the chest |
| 2 | Throat | a lump, closing up, catching |
| 3 | Stomach / gut | a knot, a pull, butterflies, dropping, nausea |
| 4 | Head | pressure, fog, lightness, ringing |
| 5 | Shoulders / neck | tension, clamping, weight |
| 6 | Breathing | shallow / held / free / broken |
| 7 | Temperature / energy | heat, cold, goosebumps, discharged, humming |
| 8 | Muscle tone | clenched fists or jaw, relaxed, can't sit still |

## Reading the map

- **Wide families + precise body channels + control** → integrated EI. Note as strength.
- **Floor-only (#14) + few channels** → low granularity. NOT a deficit to "fix" (not therapy) — a structural fact: feeds the Emotional architecture section and likely a tag for how the subject relates to their own affect.
- **v3.2 — on the floor register, distinguish two very different reads:** an *even, neutral baseline* (steady positive/negative tone, just low resolution) vs a *muted/flattened affect* (a dampened tone that reads as defended-down rather than simply low-resolution — e.g. early environments that punished or never named feeling can leave this). Same floor-only vocabulary, opposite meaning — the second is a genesis signal to trace, not just low granularity. This is the entire affective-set-point add; no PA/NA axis, no PANAS.
- **Outcome-substitution tell** (describes #1/#11/#7 only via results — "I was productive", "I just closed it out") → emotions processed as data. Highest-value Layer 1 finding; corroborate with Layer 2 (motivation) and Layer 3 (loss).
- **One conspicuously absent family** that the events clearly contained → suppression. Route to the matching deep layer (anger→L5, loss/sadness→L3, loneliness→L4).

Coverage is a snapshot like everything else — re-score on `resynthesize`; a widening map over time is itself data (deltas).
