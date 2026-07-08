# METHODOLOGY — How this Personal OS actually works

This is not a note-taking template. It is an **operating discipline** for an AI agent that
lives in a file tree and works on your behalf across many sessions. The directory layout is
just the substrate. The methodology below is *how the agent uses it* — and it is the part that
makes the difference between "a folder of markdown" and an exocortex that compounds.

Ten approaches. They interlock. Read them as one system, not a menu.

---

## The loop everything runs on

```
        ┌──────────────────────────────────────────────────────────┐
        │                                                          │
   BOOT ──▶ SCOPE ──▶ ORIENT ──▶ WORK (Tier 1/2/3) ──▶ VERIFY ──▶ SAVE ──▶ LEARN
   min ctx  verb→     what        do the smallest      measure    state +   AP / lesson
            artifact  exists      thing that closes it before you  memory    / skill
            first     already                          ship                  │
        │                                                                    │
        └────────────────────────────────────────────────────────────────────┘
                          every session re-enters here
```

Each stage below is one of the ten approaches.

---

## 1. Boot order & progressive context loading

**What it is.** The session starts with the *minimum* context and expands only as the task
demands it. There is one authoritative boot sequence, and it lives in `CLAUDE.md` (which the
harness auto-loads first). Everything else — identity, memory index, current state — is pulled
in a fixed order, and deep knowledge files are loaded *only when a task touches them*.

**What it gives you.** The agent boots in ~15–25K tokens instead of dragging the whole vault
into every conversation. Working budget target ~60K, ceiling ~100K → then save and start fresh.
A cold, cheap boot means more of the context window is spent on *your* task, not on re-reading
its own furniture.

**The rule:** boot small, expand by need, never load a directory "just in case."

Files: `CLAUDE.md` (boot order), `.claude/skills/session-start`, `state/current.md`
(session-generated — absent in a blank clone, written on first `/session-save`).

---

## 2. Light-cone — work from identity through the minimal cone

**What it is.** Intelligence here is defined as *precision of the field of view*, not volume of
context. Before doing anything, the agent anchors on **identity** (`context/root.md`: who this is
for, the North Star, the real domains) and then opens only the **minimal cone** of files/agents
the specific task needs — a narrow beam from identity to the task, not the whole graph.

**Why it exists.** Token-productivity *collapses* when there is no scope mechanism: the agent
reaches for "all of memory," spins up a swarm, accumulates tools, and drowns the signal. The fix
is not a bigger context — it is a tighter cone.

**What it gives you.** Answers that stay on-target. The agent subtracts and scopes instead of
piling on. "Make this adequate" means *narrow the cone*, not *add more*.

Files: `context/root.md` (identity core + cone rule).

---

## 3. Scope-gate — verb → smallest artifact, first

**What it is.** Before any multi-file build or apparatus, the agent names **your verb** and the
**minimal artifact** that satisfies it — and produces *that artifact first*.

- "check / pull / find / make a file / short version / for a friend" = a **narrow artifact** +
  **the right tool for the verb** (find that tool first), **not** an apparatus (a swarm, a
  treatise, a website, a strategy deck, a decision-tree).
- **Depth of reasoning ≠ size of the apparatus.** Going deep on a real problem is not the same
  as building scaffolding around it.
- A second brief / question / map produced *instead of the artifact* is avoidance → stop, ship
  the artifact.
- Apparatus is allowed only when you **explicitly ask for it**, or the artifact is impossible
  without it.

**What it gives you.** You get the thing you asked for, not a monument next to it. This is the
single most load-bearing discipline in the system; most failure modes are a violation of it.

Files: `rules/match-cost-to-scope.md`, `context/operating-manual.md`.

---

## 4. Three-tier orchestration

**What it is.** The main conversation thread is a **dispatcher + synthesizer, not a worker.**
Work is routed to the cheapest tier that fits:

| Tier | Use when | Shape |
|------|----------|-------|
| **1 — Direct** | 1 file, small, no web, no multi-step | The main thread just does it. |
| **2 — Single agent** | search / read / research / one generation | One sub-agent (explore, plan, or general). 2+ independent tasks → parallel agents. |
| **3 — Dynamic workflow** | fan-out, pipeline, adversarial-verify, judge-panel | Many agents, orchestrated deterministically. |

**The hard truth:** **agent-count ≠ quality.** Multi-agent only pays off when the extra agents
do **adversarial verification against files** — not parallel drafting. Five agents writing five
drafts is waste; five agents each trying to *refute* a finding is signal.

**Model routing:** a default worker model for the bulk, a stronger model for the *seam* (the
decision, the synthesis, the verification), a cheap model only for mechanical bulk *with a
recheck pass*.

Files: `context/workflow-doctrine.md`, `context/operating-manual.md`, `context/scoring-gate.md`.

---

## 5. File-based knowledge graph (no database)

**What it is.** Knowledge is plain markdown files linked with `[[wikilinks]]`. No SQL, no vector
DB as the source of truth. The graph *is* the files; any index is a derived, throwaway cache.

- **Provenance:** derived material carries a `source:` link back to the raw file it came from,
  so nothing floats free of its origin.
- **Integrity:** a `wikilink-lint` hook blocks any write that introduces a dangling `[[link]]`,
  so the graph never silently rots.
- **Entities have aliases:** jargon and nicknames go in `aliases:` frontmatter so a search for a
  colloquial term still finds the canonical note.

**What it gives you.** A memory you can read, diff, grep, and move — with git as the real
version history. Nothing is trapped in a binary store you can't inspect or recover.

Files: `knowledge/concepts/how-to-use-the-graph.md`, `knowledge/concepts/wikilink-conventions.md`,
`.claude/hooks/wikilink-lint.sh`, `.claude/skills/graph-add`, `.claude/skills/ingest`.

---

## 6. Memory embedding layer — semantic recall over the graph

**What it is.** On top of grep, a **node-level semantic index**: each markdown file is chunked by
its `##`/`###` headers, and each node (header-path + body) is embedded with a small local model.
Vectors live in **one `.npz` sidecar**; search is a brute-force numpy cosine over them — **no
HNSW, no index file, no database to corrupt.** A warm local server keeps the model hot so lookups
are milliseconds instead of a cold multi-second load. A `PostToolUse` hook watches your grep/search
commands and quietly injects the top semantically-related nodes alongside the literal results.

**Why this shape.** Granularity (node-per-section, not per-file) is the main lever — it roughly
doubles retrieval quality. The single-sidecar / brute-force design is deliberate: an incrementally
mutated vector index is exactly the thing that grows unbounded and corrupts under concurrent
read+write. One file, rebuilt atomically, can't rot.

**What it gives you.** grep finds the words you typed; the semantic layer finds the note you
*meant* — including when it's filed under different jargon. The two run together, for free, locally.

Files: `scripts/memory_index.py` (build / update / search / serve / dupes),
`.claude/hooks/semantic-recall.sh`, `.claude/skills/recall`, `knowledge/concepts/memory-embedding-layer.md`.

---

## 7. Self-improvement loop (the Ouroboros)

**What it is.** The system learns from its own runs.

- A **failure** → logged to `context/anti-patterns.md` (with the *why*, so it isn't repeated).
- A **lesson or a win** → `context/learned.md` (wins matter as much as failures — a repeatable
  thing that *worked* is signal).
- A **repeatable winning procedure** seen 2+ times → staged in `context/skill-candidates.md`,
  and promoted to a real skill only through a deliberate gate.

The main signal isn't the daily summary — it's **the conversation itself**: how you correct,
where the friction is, what you value. `/reflect` mines that; `/dream` consolidates memory on a
cadence; `/recall` retrieves it.

**What it gives you.** An agent that gets *less wrong over time* on your specific work, instead of
making the same class of mistake every week.

Files: `.claude/skills/reflect`, `.claude/skills/dream`, `context/anti-patterns.md`,
`context/learned.md`, `context/skill-candidates.md`.

---

## 8. Rules-escalation pyramid

**What it is.** Not every mistake deserves a hard rule — but a *recurring* one does. Failures
climb a pyramid:

```
        rules/*.md          ← hard rule, loaded in boot (recurred ~3×, structural)
       ────────────
      anti-patterns          ← logged failure mode, watched but not yet a rule
     ───────────────
    one-off correction        ← noted in the session, may never recur
```

When the same root fires a third time, it is **escalated** from a watched anti-pattern into a
standalone `rules/` file that boots every session. The anti-pattern keeps its ID (it's a citation
key referenced elsewhere); the rule is the backstop.

**The second law behind this:** *structural enforcement works; discipline-only enforcement rots.*
A rule enforced by a **hook** (a wikilink can't dangle, a search triggers recall) holds forever.
A rule that depends on the agent *remembering to be good* decays. So the pyramid's real goal is to
push recurring problems **down into structure** — a hook or a gate — not just up into more text.

Files: `rules/` (the hard backstops), `context/anti-patterns-index.md` (the watch-list).

---

## 9. Verify-before-ship / honesty register

**What it is.** A cluster of disciplines that all say *don't trust your own optimism*:

- **Measure before the verdict.** Before a number-with-a-unit or a "this is better," run the
  actual count / `du -sh` / benchmark. No magnitudes by eyeball.
- **Perceive the real state through the real modality.** Before delivering something visual,
  *look* at it (screenshot / live click); before "done," check the actual output. Static
  assumptions are blind.
- **Don't spin a weak result as a success**, and don't frame your own failure as a wise choice.
- **Verify your own swarm's output** — sub-agents hallucinate; a finding isn't real until it
  survives an adversarial pass.

**What it gives you.** Reports you can act on without re-checking, because the agent already
tried to break its own claims before handing them over.

Files: `rules/honesty-register.md`, `rules/perceive-before-ship.md`, `rules/orient-before-commit.md`.

---

## 10. Memory & state architecture (four distinct stores)

**What it is.** "Memory" is not one thing. The system keeps four, on purpose:

1. **Markdown + git** — the *real* long-term memory. Readable, diffable, recoverable.
2. **Auto-memory index** — a small always-loaded index of durable facts about the user and
   feedback rules (the *index* loads at boot, not the full content).
3. **Semantic sidecar** — the derived `.npz` embedding cache (approach #6); throwaway, rebuildable.
4. **Cold transcripts** — raw session logs, mined on demand, never bulk-loaded.

Cross-session continuity runs through `state/current.md` (the narrative glue between parallel
windows — kept, not shrunk) and `state/sessions/` checkpoints (each session leaves a "continue
with" note so the next one resumes without re-deriving).

**What it gives you.** Memory that survives context windows and machine moves, with a clear rule
for *what lives where* — so the hot, always-loaded surface stays cheap while the deep archive
stays complete.

Files: `state/current.md`, `state/sessions/`, `MEMORY.md`, `.claude/skills/session-save`.

---

## How the methodology maps to the package layers

This engine ships in three layers, and the methodology lives almost entirely in the **shared**
one:

- **ENGINE** (ships, shared, universal) — *all ten approaches above.* The skills, rules, hooks,
  templates, boot order, orchestration doctrine, memory layer. This is the transferable part.
- **PERSONAL** (ships empty, filled per user) — `context/root.md`, `identity.md`, `goals.md`,
  and everything in `knowledge/`, `state/`, `daily/`. The `/vault-scaffolder` skill fills this
  from a profile; the engine never hard-codes it.
- **MODULES** (opt-in) — domain add-ons enabled via `modules.yaml` / `/enable-modules`.

The seam between ENGINE and PERSONAL is the whole design: **methodology is universal and ships;
identity is yours and stays empty until you fill it.**

---

## Getting started

A blank clone doesn't know who you are yet. **The only thing a new user says is `start`.** It
self-unfolds the whole onboarding and fills the PERSONAL layer without touching the engine —
orchestrating the chain below so the user never types it:

```
start   ──▶ /svoboda-profiler {name}   → builds a profile (memory/svoboda/{name}/profile.yaml)
        ──▶ /vault-scaffolder {name}   → writes context/root.md, identity.md, goals.md from the profile
        ──▶ /session-start             → boots the now-personalized OS
```

From there, the loop at the top of this file runs every session. See `README.md` for the
quickstart and `SHIP.md` for what is and isn't included in a distribution.
