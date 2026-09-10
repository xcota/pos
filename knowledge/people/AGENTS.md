# people/

People who matter to your work and life: collaborators, contacts, anyone you want durable context on. One file per person. Privacy note: this directory holds personal data — keep it out of anything you share.

## What goes here

- A node per person you interact with repeatedly
- Compiled understanding of who they are and how to work with them
- An append-only log of what you've learned, with sources

## Node anatomy

```yaml
---
type: person
tags: [domain/people, type/person]
updated: YYYY-MM-DD
---
```

Body shape (mirrors `_templates/person_template.md`):

```markdown
# <Name>

One-line: who they are and why they're in your graph.

## Compiled Truth
_Current synthesis — rewrite on significant updates._
- Role / current focus
- Domain expertise
- Best channel, how they communicate

## Key Insights
Things learned *from* this person.

## Connections
- [[entity]] — relationship

## Evidence Timeline
_Append-only. Never edit past entries._
- YYYY-MM-DD: entity created — source
```

## How entities link

- People connect to the [[project]] nodes they're involved in.
- People connect to [[business]] nodes (a company, a deal).
- People connect to each other (introductions, reporting lines).

## Epistemic discipline

When recording claims about a person, distinguish what they *said* (high confidence) from what you *inferred* (a hypothesis). See `knowledge/conflicts/AGENTS.md` for the modality / epistemic-status fields. Never promote an inference to fact without a corroborating source.

## When to read

- Before reaching out to or meeting someone.
- When personalizing communication.
- When a task involves coordinating with a specific person.
