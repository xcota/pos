# projects/

Things you are actively building or running. A project node is the hub for a body of work: its current state, goals, architecture, blockers, and history. Deep operational detail can live in a `projects/<name>/` folder elsewhere in the workspace; this graph node is the *index* into it.

## What goes here

- One node per active or paused project
- Task tickets / work items, if you track them as nodes
- The current compiled state of the work

## Node anatomy

```yaml
---
type: project
tags: [domain/<project_code>, type/project]
updated: YYYY-MM-DD
status: active   # active / paused / blocked / complete
---
```

Body shape (mirrors `_templates/project_template.md`):

```markdown
# <Project Name>

One-line: what it is and why it exists.

## Compiled Truth
_Current synthesis — rewrite on significant updates._
**Status:** active/paused/blocked/complete · **Phase:** research/build/launch/operate
Problem solved, current state, decisions in effect.

## Goals
- G1: …

## Architecture / How It Works
Key technical or process decisions.

## Blockers
- Blocker → who resolves it

## Related
- [[entity]] — connection

## Evidence Timeline
_Append-only._
- YYYY-MM-DD: project created
```

## How entities link

- A project is a hub: it links to the [[concept]] / [[tool]] / [[decision]] / [[person]] nodes it touches.
- Task tickets link back to their parent project.
- Projects link to a [[business]] node when there's a commercial side.
- Cross-link to a MOC in `knowledge/moc/` for navigation when the project grows.

## When to read

- When planning or reviewing work on a project.
- When checking the status of a specific work item.
- When you need the "why" behind a project's current shape.
