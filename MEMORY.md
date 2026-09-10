# MEMORY.md — Index

> **Index only — never content.** This file is a table of one-line pointers to memory entries.
> The actual facts live in the entries themselves. Keep this lean (target ≤ 200 lines, ≤ 25 KB)
> so it fits the boot footprint. Loaded on session start, right after `CLAUDE.md`.

## Entry point on session start

1. `CLAUDE.md` — boot / runtime rules.
2. This file — what to load next.
3. `state/current.md` — cross-context state, active directions. _(Created on first `/session-save`; absent until you've run `/vault-scaffolder` — a missing read here is normal in a fresh, unpersonalized vault.)_

## How an entry works

Each memory is one short file. The index here holds a single pointer line per memory:

```
- [Short title](relative/path.md) — one-line summary of the fact and when to load it
```

Each memory file carries frontmatter so it can be filtered and routed:

```yaml
---
name: short-stable-id            # kebab-case, stable across edits
description: one line — what this remembers and why it matters
metadata:
  type: user | feedback | project | reference
---
```

### `metadata.type` taxonomy

| type | Holds | Example use |
|------|-------|-------------|
| `user` | A durable fact about the owner (preference, constraint, identity detail). | "Prefers metric units — use km/kg by default." |
| `feedback` | A correction the owner gave — a rule for future behavior. | "Don't rename session files." |
| `project` | State of an ongoing piece of work. | "{{app}} store is live; backend location TBD." |
| `reference` | A reusable fact / recipe / lookup, not tied to one project. | "Fast local transcription recipe." |

## Conventions

- **One line per pointer.** If you need more than a line to describe it, the detail belongs
  inside the entry, not here.
- **Stable `name`.** Edit the body freely; keep the id so links don't rot.
- **Route by `type`.** `user` + `feedback` are near-always relevant; `project` + `reference`
  load on demand.
- **Tombstone, don't delete.** When a memory is superseded, mark it superseded with a pointer
  to the replacement rather than removing it silently.

## What does NOT go here

- Content of any kind (it goes in the entry).
- Daily logs → `daily/YYYY-MM-DD.md`.
- Rules already in `CLAUDE.md`.
- The psychological profile → `context/identity.md`.

---

## Memories

_(empty — populated as the agent learns. One pointer line per memory, grouped loosely by type.)_

### User facts
<!-- - [Title](path.md) — summary -->

### Feedback / corrections
<!-- - [Title](path.md) — summary -->

### Projects
<!-- - [Title](path.md) — summary -->

### Reference
<!-- - [Title](path.md) — summary -->
