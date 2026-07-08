---
type: concept
tags: [domain/meta, type/concept]
updated: YYYY-MM-DD
---

# Wikilink Conventions

`[[wikilinks]]` are the edges of the graph. They are plain text, Obsidian-compatible, and require no tooling to read. These are the rules that keep the link layer healthy.

## Syntax

- `[[node-name]]` — links to `node-name.md` anywhere in the graph. Match the filename without the `.md`.
- `[[node-name|display text]]` — link with custom display text when the filename reads awkwardly in a sentence.
- Links are inline in the body, not in frontmatter (frontmatter `conflicts: ["[[...]]"]` is the one structured exception).

## Naming nodes (so links resolve)

- Filenames use `[a-z0-9-]` only: kebab-case, no spaces, no uppercase, no non-latin characters.
- If a source name is in another script or has spaces, **slugify** it for the filename and keep the original in frontmatter (`title: "…"`).
- One canonical file per entity. If you find duplicates, merge — don't let two files describe the same thing.

## Edge discipline

- **Every link target must exist.** A `[[link]]` with no file behind it is a dangling edge — the lint flags these.
- **No floating nodes.** Every new node should link to at least one existing node, in at least one direction.
- **Annotate the edge.** Write *why* two nodes connect: `[[concept-x]] — the principle behind this decision`.
- Prefer linking to the canonical node over restating its content; the graph stays DRY.

## Health

Run the wiki lint periodically (after a big ingest session, or weekly): it checks that every `[[link]]` resolves and surfaces orphan nodes. Fix dangling links by either creating the missing node or correcting the name.

## Related

- [[how-to-use-the-graph]] — the overall workflow this fits into
- [[frontmatter-conventions]] — the structured (YAML) layer that sits beside these body-link edges
