---
type: context
tags: [self-improvement, staging]
updated: ""
---

# Skill Candidates — staging for distilled skills

**What this is:** the self-improvement loop extracts not only failures (→
`anti-patterns.md`) and lessons (→ `learned.md`) but also **wins** — repeatable
winning procedures. When `/reflect` or `/session-save` notices that some working
procedure paid off across **2+ sessions** and would be worth running again, it
writes a candidate skill here.

**Why HERE and not in the skills directory:** candidates must **not** auto-load by
description and must **not** trigger like finished skills. This file is cold
staging — it is not in the boot order and is pulled only during `/reflect`,
`/session-save`, or a review. Its boot cost is zero.

**Promotion to a real skill is a deliberate gate — it needs the operator's explicit
OK.** The agent does **not** create a `SKILL.md` automatically. A candidate lives
here until the operator says "promote it".

**Discipline (so this doesn't become a dumping ground):**
- Selective: only what is genuinely reusable (like anti-patterns — not everything).
- Triangulation: a procedure seen in **2+ sessions** → candidate; seen once → a
  lesson note in `learned.md`.
- Distill heavy work (reading raw session traces) in a subagent; return only a
  compact stub.
- Dedup: before writing, grep existing candidates and the skills directory — already
  there? → strengthen it, don't multiply.
- Periodic compaction via the memory-consolidation pass.

---

## Candidate format

```
### CAND-NNN — {name} · status: candidate | promoted | rejected
- **Automates:** {the repeating procedure}
- **Evidence:** {sessions / checkpoints where it worked, 2+}
- **Procedure draft:** {steps — the seed of a future SKILL.md}
- **Triggers:** {when to invoke}
- **Gate:** awaiting the operator's OK to promote
```

> _EXAMPLE row (delete on first real candidate):_
>
> ```
> ### CAND-001 — pre-ingest dedup sweep · status: candidate
> - Automates: checking the graph for an existing entity before creating a new one.
> - Evidence: session A (avoided a duplicate person node), session B (merged instead
>   of forking a concept).
> - Procedure draft: grep entity name + aliases → if hit, strengthen; else create.
> - Triggers: any "add to graph" / ingest task.
> - Gate: awaiting the operator's OK to promote.
> ```

---

## Candidates

_(empty — filled by the loop. The first candidate appears at the next `/reflect` or
`/session-save` that finds a repeatable winning procedure.)_
