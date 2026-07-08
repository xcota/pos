# concepts/

Abstract concepts, architectural patterns, protocols, mental models, and technical ideas referenced across the knowledge graph. A concept node captures an *idea* — something you reason *with*, not a thing you *do* (that's a tool) or a thing you're *building* (that's a project).

## What goes here

- Architectural patterns and design principles
- Protocols and standards
- Mental models and frameworks you reuse
- Definitions of recurring terms

## Node anatomy

Frontmatter (all optional, but `type` + `tags` + `updated` recommended):

```yaml
---
type: concept
tags: [domain/<domain>, type/concept]
updated: YYYY-MM-DD
---
```

Full frontmatter convention (required core + optional palette, per-file-type sets, how each field is used): `frontmatter-conventions.md`.

Body shape:

```markdown
# <Concept Name>

One-line definition.

## What it is
Short explanation in plain language.

## Why it matters
Where this concept shows up and what it lets you decide.

## Related
- [[other-concept]] — how they connect
- [[some-tool]] — implements this concept
```

## How entities link

- Concepts are referenced *from* project nodes as the rationale behind a decision.
- Research nodes validate, propose, or contradict a concept.
- Tool nodes implement a concept.
- Link with `[[wikilink]]` inline; every link target should exist as a file (lint checks this).

## When to read

- When making an architectural or design decision and you need the principle behind it.
- When evaluating whether a new idea is genuinely new or a restatement of something already captured.
