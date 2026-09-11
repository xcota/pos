# Profile Synthesis Template

Generate the final profile using this structure. Adapt sections as needed — not every person maps to every section. Section headings below are the English shape; write the profile in the language the person writes in, and keep their quotes exactly as they said them.

## Document Structure

```markdown
# Psychological profile: [Name]
**Version:** [X.X]
**Synthesis date:** [date]
**Sources:** [what data was collected]

> On `resynthesize` (v3.1): this is a **versioned diff**, not a rewrite. Open with "Δ since vN" — moved scores, new/retired tags, predictive-model updates — then the full body. The causal core (Section X genesis, origin-traced tags) is sticky: deltas update facts and active domains, not childhood etiology, unless a genuine new origin surfaced.

---

## I. Core: [One-phrase pattern name]
The single pattern that runs through their entire life. Described with a concrete example chain
spanning childhood → present. This is the throughline.

## II. Cognitive style
How they think: scanning vs deep-dive, chronological vs associative, burst vs gradual learning.
Concrete evidence from speech patterns and self-described behavior.
v3.2: fold in rumination-vs-reflection (L9 — does thought loop or turn a new side) and load-mode (L13 — does analytic mode hold or flip under stress, where it goes rigid).

## III. Emotional architecture
How they process emotions. Granularity level. Control mechanisms.
v3.1: cite the coverage map (`references/granularity_instrument.md`) — emotion families reached vs **systematically absent**, body channels reached. The absent family is the key finding, not a vibe.
Key finding: what's the ONE emotion/state that doesn't fit their system?

## IV. Body
Relationship with body. Substances history if relevant. Optimization approach.
Interoception channel: felt-sense vs metrics vs ignoring.

## V. Relationships
Architecture (not history). What they structurally need.
Attachment pattern with evidence. Current gaps.
v3.2: state the attachment TYPE as mechanics + genesis (L7), not a clinical label. Include the boundary switch-point (L10 — where self-erasure flips to system-integrity). Render the social graph here as a sub-structure under Surroundings (`social_graph`): 5–10 named people × energy direction (gives/takes) × attachment × unresolved relational loss.

## VI. Losses and resilience
How they handle loss. Speed of reframing.
The one loss that doesn't convert (if found).
v3.2: include attributional grammar (L8 — where the cause flies on failure vs who gets credit on success). The asymmetry (which one category gets internal attribution while the rest externalize) is the load-bearing finding.

## VII. Anger
What triggers it. System-based or people-based.
What it reveals about their real boundaries.

## VIII. Content / worldview
What shaped them culturally. Subcultures, media, aesthetic preferences.

## IX. Recovery
How they recover from overload. Social vs solitary. Dream-state vs activity.

## X. Parents — where the architecture came from
Family system. Role in it. How it generated current patterns.
Genesis table: pattern → origin.
v3.2: add the memory-availability map (`memory_access`) — which periods are vivid / factual-only / amnesiac. The distribution itself is suppression data and points at where the pattern-generator hides; map it, don't excavate.

## XI. Meta-profile: blind spots
What they can't see about themselves. Where their self-model diverges from observed behavior.
Corrections log: where your projections were wrong and what replaced them.

## XII. Tag summary
Table: tag → description. Every significant pattern gets a tag.

## XIII. Predictive model
Table: situation → predicted behavior. 5-7 common decision points.
Based on collected evidence, not stereotypes.
v3.2: use load-mode (L13) as the crisis-behavior predictor (holds vs flips under overload) and attribution asymmetry (L8) to predict whether they'll change behavior after a failure or externalize it. Time-orientation (L11) predicts plan vs deferral.
```

## Tagging Convention

Tags are lowercase, underscore-separated, prefixed with `#`. Create tags FRESH for each person from their actual data. Do NOT reuse tags from other profiles.

Rules:
- Each tag must have at least 2 evidence points from THIS person's data
- Tags describe behavioral patterns, not personality types
- Name the pattern by what it DOES, not what it resembles
- If you find yourself writing a tag you've seen before — check whether you're anchoring on a prior profile or genuinely observing it

## Corrections Log

Critical section. Every profile starts with projections (standard models applied to the person). Some will be wrong. Track:

```markdown
| Initial projection | Correction from subject | Updated understanding |
|--------------------|------------------------|----------------------|
| (your initial read) | (what they actually said) | (revised understanding) |
```

This is what makes the profile *honest*. A profile without corrections is a profile that didn't listen.

## Profile Quality Checklist

- [ ] Every tag has an origin (traced to childhood/experience)
- [ ] Predictive model based on evidence, not archetypes
- [ ] At least 2 corrections logged
- [ ] Blind spots section present and non-obvious
- [ ] One "doesn't fit the system" finding (the crack in their self-model)
- [ ] Speech pattern analysis included (if voice data available)
- [ ] Attachment type named as mechanics + genesis, not a clinical label read to the subject (v3.2)
- [ ] Deep layers 7–13 rendered flat — no academic/clinical jargon (attribution axes, distortion names, VIA virtues) leaked into the subject-facing profile (v3.2)
