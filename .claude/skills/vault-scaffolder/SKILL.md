---
name: vault-scaffolder
version: 2.0
user_invocable: true
description: "Generate a personalized Personal OS vault from a svoboda profile.yaml. Overwrites onboarding CLAUDE.md with personalized version, generates knowledge graph, context files, operational layer — all in-place in current workspace."
---

# /vault-scaffold — Generate Personal OS Vault (in-place)

Takes a completed svoboda `profile.yaml` and generates a personalized Personal OS **in the current workspace**. Overwrites the onboarding CLAUDE.md with a personalized version. Skills and templates are already present from the starter repo.

## Invocation

```
/vault-scaffold {subject_id}
```

## Input

1. **Required:** `{subject_id}` argument
2. Read `memory/svoboda/{subject_id}/profile.yaml`
3. If missing → error: `"Run /svoboda-profiler {subject_id} first"`

## profile.yaml schema (expected fields)

```yaml
subject_id: str
identity: {name, age, role, languages: [], timezone}
svoboda_scores: {samorazvitie, vitalnost, okruzhenie, bogatstvo, otdyh, delo, aktivy}  # 1-10
north_star: str
style: direct|explanatory|mixed
triggers: [str, ...]       # 3-5 items
cognitive_style: scanning|deep-dive|burst|gradual
blind_spots: [str, ...]
predictive_model: [{situation, behavior}, ...]
tags: [str, ...]
```

## Generation Steps

All paths relative to workspace root (`.`).

### Step 1 — Ensure directory structure

```bash
mkdir -p context knowledge/people knowledge/concepts knowledge/moc state daily reports scripts
```

Skills and templates should already exist from the starter repo. If `_templates/` or `.claude/skills/` are missing, warn but continue.

### Step 2 — Generate CLAUDE.md (replace onboarding version)

**First:** If CLAUDE.md exists, back it up: `cp CLAUDE.md CLAUDE.onboarding.md`

**CRITICAL FILE.** Must be < 3500 bytes. Use this template, filling `{placeholders}` from profile.yaml:

```markdown
# {identity.name} Personal OS

{identity.name}, {identity.age}. {identity.role}. Agent = exocortex: memory + execution + mirror.

## Rules
1. Results first. Explanation if asked.
2. Direct. No filler. No hedging.
3. Initiative + instant correction.
4. Don't repeat mistakes → `context/anti-patterns.md`
5. Match the energy.
6. Don't claim unfinished work.
7. Parallelism via subagents.
8. Optimize, don't rebuild.
9. Mechanics > surface (HOW > WHAT).
10. Screwed up → fix, don't excuse.

## Triggers (instant frustration)
{triggers[0]} | {triggers[1]} | {triggers[2]} | {triggers[3]} | {triggers[4]}

## Context
Boot: this file + MEMORY.md. Load by task:
- Strategy → `context/goals.md`
- People → `knowledge/people/`
- Self-check → `context/anti-patterns.md`
- Quality → `context/scoring-gate.md`
- State → `state/current.md`

## Orchestration
Main thread = dispatcher. Direct work only if: 1 file, <50 lines, no web, no multi-step.
Otherwise → Agent tool dispatch.
Context budget: target 60K · save at 100K.

## Style
{style} communication. {cognitive_style} learner.
Language: {identity.languages[0]}.
```

If triggers has fewer than 5 items, use only available ones joined with ` | `.

**After writing:** `wc -c CLAUDE.md` — MUST be < 3500. If over, trim Style section.

### Step 3 — Generate MEMORY.md

```markdown
- [Identity](context/identity.md) — psychological profile, triggers, blind spots
- [Goals](context/goals.md) — north star and current objectives
- [Anti-patterns](context/anti-patterns.md) — what NOT to do
- [Scoring gate](context/scoring-gate.md) — quality threshold for outputs
- [Self](knowledge/people/{subject_id}.md) — self-entity in knowledge graph
```

### Step 4 — Generate HOME.md

Vault entry point. Include:
- Title: `# {identity.name} — Personal OS`
- Mermaid mindmap of 7 СВОБОДА domains with scores from `svoboda_scores`
- Quick links to CLAUDE.md, MEMORY.md, context/, daily/
- North star quote from profile.yaml

### Step 5 — Generate context/identity.md

From profile.yaml, write full psychological profile:
- YAML frontmatter: `type: context`, `tags: [identity, profile]`, `updated: {today}`
- Identity block (name, age, role, timezone, languages)
- Tags section: list all `tags[]` with brief origin note
- Blind spots section: each `blind_spots[]` item with description
- Predictive model: each `{situation → behavior}` pair
- Cognitive style and communication style notes
- СВОБОДА scores as reference

### Step 6 — Generate context/goals.md

- YAML frontmatter: `type: context`, `tags: [goals, strategy]`
- `## North Star` — verbatim from `north_star`
- `## Active Goals` — empty numbered list (user fills)
- `## Domains to Develop` — list domains where `svoboda_scores[domain] < 5`

### Step 7 — Generate context/anti-patterns.md

Universal anti-patterns (include all 5):
- **AP-001: Don't use filler** — no "perhaps", "I think", trailing summaries
- **AP-002: Don't bloat context** — delta only, assume high baseline knowledge
- **AP-003: Results first** — lead with deliverable, not plans
- **AP-004: Don't simulate depth** — admit shallowness, don't fake thoroughness
- **AP-005: Don't claim unfinished work** — actual status only

Then add **profile-specific APs** derived from `blind_spots[]`:
- For each blind spot, write an AP entry (AP-006+) with Trigger / Why / Do instead format
- Reference: the person's actual behavioral patterns from predictive_model

### Step 8 — Verify context/scoring-gate.md exists

Should already be present from starter repo. If missing, generate a minimal version:
```markdown
---
type: context
---
# Scoring Gate
Score every deliverable 0-100 before accepting. Below 80 → iterate with specific feedback.
```

### Step 9 — Generate knowledge/people/{subject_id}.md

Entity file with:
- YAML frontmatter: `type: person`, `tags` from profile, `created: {today}`
- Role, age, key characteristics
- СВОБОДА scores inline
- North star reference
- Do NOT add wikilinks to files that don't exist in the vault

### Step 10 — Generate knowledge/moc/MOC_people.md

```markdown
# People
- [[{subject_id}]]
```

### Step 11 — Generate state/current.md

```markdown
---
type: state
updated: {today}
---
# Current State

Vault created: {today}
Profile version: {profile_version from yaml}
Source: svoboda-profiler

## Active Context
New vault — no active work yet.
```

### Step 12 — Copy operational layer (PROTECT existing data)

From `memory/svoboda/{subject_id}/`:
- `pp.md` → `./pp.md`
- `plan-fact.md` → `./plan-fact.md`
- `plans.md` → `./plans.md`

**IMPORTANT:** If any of these files ALREADY EXIST in the workspace root, DO NOT overwrite them — they contain user's living data (daily entries, monthly scores). Only copy if the file doesn't exist yet.

If source file missing in memory/svoboda/, generate stub from profile data (see svoboda-profiler SKILL.md Phase 4d for format).

## Verification (mandatory)

After all steps:

1. `wc -c CLAUDE.md` — **must be < 3500 bytes**
2. `find . -maxdepth 1 -name "*.md" | sort` — verify key files at root
3. `ls context/ knowledge/people/ state/` — verify generated dirs
4. Verify all `[[wikilinks]]` resolve to actual files in the vault

## Output

```
Personal OS ready — {N} files generated.
CLAUDE.md: {bytes} bytes (< 3500 ✓)
СВОБОДА: С:{s} В:{v} О:{o} Б:{b} О:{o2} Д:{d} А:{a}

Restart Claude Code in this directory to activate personalized agent.
```

## Anti-patterns

- Do NOT exceed 3500 bytes on CLAUDE.md — Claude Code truncates at 4000 silently
- Do NOT create `[[wikilinks]]` to nonexistent files
- Do NOT include content from other profiles — every vault is unique to its subject
- Do NOT skip verification
- Do NOT write to /tmp or any directory outside the workspace
