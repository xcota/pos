# decisions/

Decisions you've made and want to remember *why*. A decision node is a durable record of a choice between alternatives, the reasoning, and the trigger that would make you reconsider. It is not a task and not a finding.

## What goes here

- Architectural choices ("we use X not Y because…")
- Policy choices ("from now on we always…")
- Strategic directions you committed to

## Node anatomy

```yaml
---
type: decision
tags: [domain/<domain>, type/decision]
updated: YYYY-MM-DD
status: decided   # decided / reconsidering / reversed
---
```

Body shape (mirrors `_templates/decision_template.md`):

```markdown
# Decision: <Title>

## Context
What situation forced a choice; what constraints applied.

## Options Considered
Option A — pros/cons · Option B — pros/cons

## Decision
Chose X because…

## Consequences
What this implies going forward.

## Review Trigger
When to reconsider this (a condition, not a date).

## Related
- [[concept]] — rationale
- [[research]] — evidence
```

## How entities link

- Decisions cite [[concept]] nodes as rationale.
- They are motivated by [[research]] nodes.
- They apply to [[project]] nodes.

## When to read

- When you (or future-you) ask "why did we do it this way?"
- Before changing an established approach — read the review trigger first.
- When onboarding into a project's design rationale.
