---
type: concept
tags: [domain/meta, type/concept]
updated: YYYY-MM-DD
---

# How To Use The Graph

The knowledge base is a **file-based graph**: plain markdown notes connected by `[[wikilinks]]`. No database, no special app required — every node is a readable file. This note explains how to work in it.

## The shape

- Each directory under `knowledge/` is a **node type** (concepts, research, tools, decisions, people, projects, business, courses, health, psychology, memory-refs). Each has an `AGENTS.md` that defines its schema and when to read it.
- A **node** is one markdown file: a short frontmatter block plus a body.
- **Edges** are `[[wikilinks]]` inline in the body. A link means "these two ideas are related"; the text next to it says *how*.
- `knowledge/moc/` holds **Maps of Content** — curated indexes you build once a domain gets large.
- `knowledge/conflicts/` holds the **epistemic layer** — how contradictions are recorded without overwriting.

## Adding a node

1. Pick the directory by *what kind of thing* it is (idea → concepts, thing-you-operate → tools, work → projects, …).
2. Name the file in kebab-case: `[a-z0-9-]` only. No spaces, no uppercase, no non-latin characters.
3. Start from the matching template in `_templates/` if one fits.
4. Write a one-line definition first — if you can't, you don't yet understand the node.
5. Link it to at least one existing node. **No floating nodes.**

## Linking discipline

- Link generously, but every `[[target]]` must resolve to a real file (run the lint to catch dangling links).
- Put the *relationship* next to the link: `[[some-tool]] — implements this pattern`, not a bare `[[some-tool]]`.
- When two nodes disagree, don't overwrite — record a conflict (see `knowledge/conflicts/AGENTS.md`).

## Recall

- Scan `knowledge/memory-refs/` for the thin index of durable facts.
- Use a MOC to get oriented in a domain quickly.
- Before researching something, check whether a node already exists.

## Related

- [[wikilink-conventions]] — the linking syntax and rules in detail
- [[frontmatter-conventions]] — the YAML properties each node carries (required core + optional palette)
