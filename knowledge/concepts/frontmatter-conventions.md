---
type: concept
tags: [domain/meta, type/concept]
updated: YYYY-MM-DD
---

# Frontmatter Conventions

Frontmatter is the small YAML block at the top of every node. Where `[[wikilinks]]` are the *edges* of the graph, frontmatter is each node's **structured face**: the handful of typed fields a tool, a query, or the agent can read without parsing prose. It is plain text, Obsidian-compatible (Obsidian's Properties system reads it as typed fields), and Dataview-queryable — but it stays useful with no tooling at all.

The design rule for the whole convention: **a tiny required core, a rich optional palette.** Every field you *require* is friction on every note you write. Everything past the core is opt-in, added only when it earns a query, a nav affordance, a lint check, or an agent decision.

## The required core (three fields)

Every node in `knowledge/` carries exactly these:

```yaml
---
type: concept
tags: [domain/meta, type/concept]
updated: 2026-07-08
---
```

- **`type`** *(text, enum)* — what kind of node this is. Drives which `AGENTS.md` schema applies and how the node is filtered. Values in use: `concept · research · person · project · business · tool · framework · company · decision · moc · memory-ref · course · health · meta`. One value per node.
- **`tags`** *(list)* — a `domain/<x>` tag plus a `type/<x>` tag, minimum. Tags are the cheap cross-cut: "everything in `domain/health`" without walking directories. Namespaced (`domain/…`, `type/…`) so they don't collide with free tags.
- **`updated`** *(date, `YYYY-MM-DD`)* — last meaningful edit. Feeds recency sorting and the staleness lint. Cheap to keep honest; expensive to reconstruct later.

Everything below is **optional**. Absence means "not annotated," never "error" — index generators and the agent must tolerate missing fields.

## The optional palette

### Identity & classification

| Field | Type | For | Example | How the system uses it |
|---|---|---|---|---|
| `id` / `uid` | text | A stable handle that survives a rename | `id: 20260708-a1` | A `[[link]]` breaks on rename; an `id` doesn't. Cite it in provenance/backlinks when a note may be renamed. Optional — most vaults lean on kebab filenames instead. |
| `status` | text (enum) | Lifecycle: `draft \| active \| archived \| superseded` | `status: active` | "Show all active" filter; `/dream` and recall **skip `archived`/`superseded`** so dead notes don't pollute consolidation or semantic recall; lint can flag `draft` notes older than N days as abandoned. |
| `domain` / `area` | text | PARA-style top-level bucket (a coarser cut than tags) | `domain: health` | Scoping: the agent's light-cone (`context/root.md`) can load "only `domain: business` nodes" for a business task. A MOC groups by domain. |
| `aliases` | list | Other names the same node answers to — jargon bridging | `aliases: [recall, semantic-recall, embedding-layer]` | Obsidian resolves `[[recall]]` to this file. **Also feeds the embedding index**: aliases are searchable surface, so a query in the user's words hits a note titled in jargon (see `[[memory-embedding-layer]]`). |

`status` vs the epistemic ladder: `status` is the note's **editorial lifecycle** (is this note live?). It is *not* the same axis as `epistemic_status` (how much do we believe the *claim*?) — that ladder lives below, in Provenance.

### Provenance & lifecycle

For any node making a **claim** (research, an extracted fact, a person-inference), the epistemic fields are the honesty register. They are already a defined schema in `knowledge/conflicts/AGENTS.md` — this section points at it rather than re-defining it, so the two never drift.

| Field | Type | For | Example | How the system uses it |
|---|---|---|---|---|
| `created` | date | Birth date, when it differs from `updated` | `created: 2026-06-01` | Age-of-note; distinguishes "old but maintained" from "old and stale." |
| `source` / `sources` | text / list | Where the content came from | `sources: ["PMID:32503637", "webinar transcript"]` | Provenance. Lets the agent cite and re-verify; a claim with no source can be flagged as an assertion. Use `source` for one, `sources` for a list. |
| `author` | text or link | Who authored the *idea* (not the note) | `author: "[[person-node]]"` | Attribution; wikilink form makes the author a graph node. Answers "everything from author X." |
| `epistemic_status` | text (enum) | Confidence ladder for the claim | `epistemic_status: corroborated_claim` | Full 13-value enum + promotion rules in `knowledge/conflicts/AGENTS.md`. Lint enforces the enum; `disputed`/`superseded` gate promotion. |
| `confidence` | number `0.0–1.0` | Scalar belief in the claim | `confidence: 0.85` | A single scalar (not a vector). Sorts/filters claims by strength; pairs with `epistemic_status`. |
| `last_verified` | date | When a claim was last checked against reality | `last_verified: 2026-06-25` | **Drives the staleness lint** (`/lint stale` flags `last_verified` older than 30 days; canonical claims older than 90 days get re-verification prompts). |
| `review_by` / `ttl` | date / duration | An explicit "recheck by" horizon | `review_by: 2026-12-01` | For notes that go stale on a *known* clock (pricing, a roadmap, a person's role). Lint flags anything past `review_by` regardless of `last_verified`. Use where staleness is predictable; otherwise `last_verified` is enough. |

### Relations & graph

Body `[[wikilinks]]` remain the primary edges. Frontmatter relations exist only where a **typed, machine-readable** edge earns its keep (nav rails, hierarchy queries).

| Field | Type | For | Example | How the system uses it |
|---|---|---|---|---|
| `related` | list of links | Peer notes, no hierarchy implied | `related: ["[[node-a]]", "[[node-b]]"]` | A "See also" rail a template renders without scraping prose. Note: these are structured links — keep them resolvable (the wikilink lint checks them like body links). |
| `up` / `parent` | link | The one note this sits *under* | `up: "[[parent-node]]"` | Breadcrumb / hierarchy nav ("walk up to the domain"). Enables a tree view without a folder move. |
| `moc` | link or list | Which Map(s) of Content own this node | `moc: "[[MOC_domain]]"` | The MOC can list its members by query; the note advertises its own map membership so a new node isn't orphaned from navigation. |

`conflicts` is the one relation field that is *required* to live in frontmatter (not the body) — it is a structured, promotion-blocking edge; see `knowledge/conflicts/AGENTS.md`.

### Rendering / UX — Obsidian-only, cosmetic

These change how Obsidian *displays* a note and mean nothing to the agent or the graph. Keep them out of the core; they are pure operator taste and travel with the app, not the OS.

| Field | Type | For | Note |
|---|---|---|---|
| `cssclasses` | list | Per-note CSS hooks in Obsidian | Cosmetic. No agent behavior. |
| `banner` | text (path) | Header image (Banners plugin) | Cosmetic, plugin-dependent. |
| `cover` | text (path) | Card/cover image | Cosmetic, plugin-dependent. |

### Agent-facing

Fields that tell the agent how to treat a note during boot and load. This is where Camomile diverges from a plain Obsidian vault.

| Field | Type | For | Example | How the system uses it |
|---|---|---|---|---|
| `boot` | checkbox | Load this at session boot | `boot: true` | The boot sequence loads `boot: true` nodes eagerly; everything else is lazy, pulled only when the task reaches it. Keeps the boot footprint small. |
| `cone` | text (domain tag) | Which light-cone slice this belongs to | `cone: business` | Ties to `context/root.md`'s light-cone. The agent expands the cone by `cone:` value, loading only the slice a task touches instead of the whole graph. |
| `pin` | checkbox | Keep resident; don't drop under budget pressure | `pin: true` | Compression/`/session-save` treats pinned nodes as sticky — they survive a working-set trim. Use sparingly; a pin is a standing cost. |
| `role` | text | A structural role the node plays | `role: root` | Marks singleton nodes the boot logic addresses by role (e.g. `context/root.md`), not by filename. |

## Universal-engine vs operator-choice

- **Universal-engine** (ships with the starter; skills/lint/dream depend on these existing): `type`, `tags`, `updated`, `status`, `source`/`sources`, the epistemic set (`epistemic_status`, `confidence`, `last_verified`, `conflicts`), `aliases`. Renaming or dropping these breaks tooling.
- **Operator-choice** (adopt if the workflow wants them): `id`/`uid`, `domain`/`area`, `author`, `related`, `up`/`parent`, `moc`, `review_by`/`ttl`, `boot`/`cone`/`pin`, and all rendering fields. The engine tolerates their absence.

## Over-propertifying — the failure mode to avoid

Every required field is a tax paid on **every** note, forever, mostly by future-you at 2am. A field earns its place only if something *reads* it — a query you run, a lint that fires, a nav rail that renders, a load decision the agent makes. If you can't name the reader, don't add the field. Symptoms of the anti-pattern: fields no query ever touches; three near-synonyms (`created`/`date`/`added`) with no rule for which; a `related:` block duplicating links already in the body. When in doubt, put the fact in the **body** (searchable, linkable, free-form) and promote it to frontmatter only once a machine needs it structured.

## Recommended sets per file-type

Core (`type`, `tags`, `updated`) on all. Add only the rows below.

- **Concept note** — core only. Optionally `aliases` (jargon bridging → embedding recall), `related`.
- **Person** — core + `status` (active/archived contact). Optionally `aliases` (name variants), `related` (their connections). Claims *about* a person that are inferred get the epistemic set.
- **Project** — core + `status` (`active | paused | blocked | complete`). Optionally `domain`/`cone`, `up`/`moc`. Body carries the live detail.
- **Research / claim node** — core + `source`/`sources` **and** the epistemic set (`epistemic_status`, `confidence`, `last_verified`). This is where provenance matters most; `related` links out to what it validates or contradicts.
- **Daily note** — core only (`type: daily`). Ephemeral; don't decorate.
- **Report / artifact** — core + `source`/`sources`, optionally `status` (draft/final) and `review_by` if it goes stale on a clock.

## How it ties to the rest of the system

- **`aliases` → embedding index.** Aliases are indexed surface text, so a query in the user's everyday words resolves to a note titled in jargon. See `[[memory-embedding-layer]]`.
- **`source`/`sources` + epistemic set → provenance / honesty register.** A claim's believability is legible without reading the body; the promotion ladder and conflict-as-record schema live in `knowledge/conflicts/AGENTS.md`.
- **`status` + `last_verified`/`review_by` → `/dream` and lint.** `/dream` skips `archived`/`superseded` nodes; lint flags stale `last_verified` and past-`review_by` notes so the graph self-reports rot.
- **`aliases` / `related` → graph.** Both are resolvable edges the wikilink lint checks, keeping frontmatter links as honest as body links.

## Related

- [[wikilink-conventions]] — the edge (body-link) layer this sits beside
- [[how-to-use-the-graph]] — the overall workflow both fit into
- [[memory-embedding-layer]] — the recall layer that indexes `aliases` and node text
