# health/

Personal health context: baseline profile, lab results, protocols, supplement/medication notes, and what you've learned about your own body. Privacy note: this is sensitive personal data — keep it out of anything you share, and load the profile node *before* answering any health question so advice is grounded in your actual numbers, not generic defaults.

## What goes here

- A baseline profile node (diet, body composition, known conditions, current stack)
- Lab / measurement results over time
- Protocols you follow and why
- Mechanism notes (how a given intervention works for *you*)

## Node anatomy

```yaml
---
type: health
tags: [domain/health, type/health]
updated: YYYY-MM-DD
---
```

Body shape:

```markdown
# <Topic>  (e.g. baseline profile, a specific marker, a protocol)

## Compiled Truth
_Current synthesis — your actual baseline._
Relevant numbers, context, constraints.

## Mechanism
Why this works the way it does, in physiological/medical terms — not vague.

## Related
- [[other-health-node]] — connection

## Evidence Timeline
_Append-only. Lab dates, measurements, changes._
- YYYY-MM-DD: result / change — source
```

## How entities link

- The baseline profile node is the hub; specific marker/protocol nodes link to it.
- Protocol nodes link to the marker they target.

## Discipline

- Reason from the person's own data, not population averages.
- Mechanism over caution-boilerplate; no alarmism.
- Keep claims epistemically honest: lab result = fact, your interpretation = hypothesis (see `knowledge/conflicts/AGENTS.md`).

## When to read

- Before answering *any* health question — load the baseline first.
- When tracking a marker over time.
