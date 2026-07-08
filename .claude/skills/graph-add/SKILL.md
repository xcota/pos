---
name: graph-add
description: "Use when adding a new entity or fact to the knowledge graph."
version: 1.0
user_invocable: true
---
# /graph-add — Add Knowledge to the Graph

Quickly add a new entity or fact to the knowledge graph.

## Usage
`/graph-add` — interactive mode, asks questions
`/graph-add {type} {name} {facts}` — direct mode

## Entity Types
- `person` → `knowledge/people/{name}.md`
- `project` → `knowledge/projects/{name}.md`
- `concept` → `knowledge/concepts/{name}.md`
- `tool` → `knowledge/tools/{name}.md`
- `decision` → `knowledge/decisions/{date}-{name}.md`
- `research` → `knowledge/research/{date}-{name}.md`
- `business` → `knowledge/business/{name}.md`

## Steps

1. Determine type (ask if not provided).
2. Determine name (ask if not provided).
3. Collect key facts (ask if not provided).
3b. **Conflict check** — `grep -rl "{normalized subject}" knowledge/`. If an existing note asserts a DIFFERENT value for the same subject → do NOT overwrite: use conflict-as-record (see `knowledge/conflicts/AGENTS.md`) — create `knowledge/conflicts/<slug>-conflict-{date}.md` (both claims + provenance + `promotion_blocked: true`), downgrade the original to `disputed`, then stop and report to the user.
4. Identify related entities — search existing files:
   ```bash
   grep -rl "{related term}" knowledge/
   ```
5. Create the entity file:
   ```markdown
   ---
   type: {type}
   tags: [{relevant tags}]
   updated: {today}
   # epistemic (optional, enums: knowledge/conflicts/AGENTS.md): modality · epistemic_status (fresh single-source → extracted_candidate) · confidence · last_verified · conflicts: []
   ---
   # {Name}

   {Key facts as prose or bullet points}

   ## Connections
   - Related to [[{entity-1}]] — {why}
   - Related to [[{entity-2}]] — {why}
   ```
6. Update related entity files to add a backlink `[[{new-entity}]]`.
7. Report what was created and linked.

## File Naming
- Lowercase, hyphens for spaces: "Acme Corp" → `acme-corp.md`.
- Decisions and research are date-prefixed: `2026-01-05-chose-obsidian.md`.
- Max 60 chars.

## Rules
- Always add `[[wikilinks]]` to related entities.
- **MANDATORY: update backlinks in ≥1 related file** — a new entity MUST have ≥1 incoming link. If you create a file and no other file links to it, it's invisible in the graph. This is the #1 graph quality rule.
- Don't create duplicates — search first: `grep -rl "term" knowledge/`.
- Keep entity files focused: one entity = one file.
- Minimum content: YAML frontmatter + 1 paragraph + ≥2 outgoing `[[wikilinks]]` + ≥1 incoming backlink added to another file.

## Validation (run after every graph-add)
```bash
# Verify the new entity has incoming links
grep -rl "\[\[{new-entity-name}\]\]" knowledge/ | grep -v "{new-entity-name}.md"
# Must return ≥1 file. If 0 → FIX before committing.
```

## Anti-Pattern: Floating Nodes
NEVER create an entity without ensuring at least one other entity links to it.
Root cause when this slips: entities get created with outgoing links but nobody updates the hub files to link back. Always close the loop.
