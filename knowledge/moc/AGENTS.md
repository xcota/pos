# moc/ — Maps of Content

A MOC (Map of Content) is a navigation node: a hand-curated index into one domain of the graph. It is not where knowledge *lives* — it's the table of contents that links *out* to the real nodes. Build a MOC for a domain once it has enough nodes that you can't hold the layout in your head.

## What goes here

- One MOC per domain that has grown large (a project, a topic, a body of people, a course series)
- Curated links grouped by sub-topic, with a one-line "why" beside each

## Naming

`MOC_<domain>.md` — e.g. `MOC_<topic>.md`. Lowercase domain, `MOC_` prefix is the convention so they sort together.

## Node anatomy

```yaml
---
type: moc
tags: [domain/<domain>, type/moc, moc]
updated: YYYY-MM-DD
---
```

Body shape:

```markdown
# MOC: <Domain>

One-paragraph orientation: what this domain is and what's mapped here.

## <Sub-group A>
- [[entity-1]] — one line: what it is / why it's here
- [[entity-2]] — …

## <Sub-group B>
- [[entity-3]] — …
```

An optional `mermaid` mindmap at the top gives a visual overview, but the linked list below it is the load-bearing part.

## How entities link

- A MOC links *out* to nodes across many directories (concepts, tools, people, projects…).
- Individual nodes don't have to link back to the MOC, but a project hub often does.
- MOCs can link to sibling MOCs when domains overlap.

## Discipline

- Curate, don't dump. A MOC is editorial — include what helps navigation, group meaningfully.
- It mirrors the graph; it doesn't duplicate content. If you find yourself writing explanation here, it belongs in the node.

## When to read / build

- Read a MOC to get oriented in an unfamiliar domain fast.
- Build one when a domain crosses ~10 nodes and browsing the folder stops being enough.
