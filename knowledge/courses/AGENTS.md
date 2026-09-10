# courses/

Structured learning material you've ingested: courses, books, lecture series, multi-part trainings. A course node is the *navigation hub* for a body of material — its modules, the source, and links out to the concept/research nodes the material produced.

## What goes here

- One hub node per course / book / training
- Per-module or per-chapter nodes when the material is large
- Distilled frameworks extracted from the material (these often become [[concept]] nodes)

## Node anatomy

```yaml
---
type: course           # or: course-module
tags: [domain/<topic>, type/course]
updated: YYYY-MM-DD
source:                # author / platform / where it came from
---
```

Body shape:

```markdown
# <Course Title>

One-line: what it teaches and why you're studying it.

## Modules
| # | Module | Node |
|---|--------|------|
| 1 | …      | [[course-module-1]] |

## Key Frameworks
- [[framework-concept]] — what it gives you

## Applications
- [[project]] — where you apply this

## Related
- [[person]] — author / instructor
```

## How entities link

- A course hub links to its module nodes; modules link back to the hub.
- Frameworks distilled from a course live as [[concept]] nodes and link both ways.
- Courses link to the [[project]] nodes where you apply the material.
- Consider a MOC in `knowledge/moc/` once a course has many module nodes.

## When to read

- When you want to apply something you learned and need the source.
- When deciding whether a new course overlaps with material you already have.
