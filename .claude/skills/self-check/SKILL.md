---
name: self-check
description: "Use when checking the overall health of this folder or diagnosing system gaps."
version: 1.0
user_invocable: true
---

# /self-check — System Health Check

Scans every layer of the folder, scores health, surfaces gaps.
Invoke: `/self-check`

## Step 1: Context Layer

```bash
wc -l CLAUDE.md 2>/dev/null
grep "^## " CLAUDE.md 2>/dev/null
```

Check: exists? >50 lines? Has sections: Rules, Boot (with the start hook and its gates), Scope-gate, Orchestration, Memory, Budget, Hard rules, Self-improvement, Architecture? Under 3500 bytes?

Score: 0 (missing) / 1 (exists but thin) / 2 (full, with sections)

## Step 2: Knowledge Graph

```bash
find knowledge/ -name "*.md" -not -name "AGENTS.md" | wc -l
grep -rl "\[\[" knowledge/ | wc -l
```

Check: entity count, wikilink coverage (% of files with links), type distribution.

```bash
for d in knowledge/*/; do echo "$(basename "$d"): $(find "$d" -name '*.md' -not -name 'AGENTS.md' | wc -l)"; done
```

Score: 0 (<10 entities) / 1 (10-100) / 2 (100+ with >50% linked AND <5 floating nodes)

**Graph health check (mandatory):**
```bash
# Count floating nodes (0 incoming links)
python3 -c "
import os, re
kg=os.path.join(os.getcwd(), 'knowledge')
incoming={}
entities=set()
for root,dirs,files in os.walk(kg):
    for f in files:
        if f.endswith('.md') and f not in ('AGENTS.md','INDEX.md'):
            name=f.replace('.md','')
            entities.add(name)
            with open(os.path.join(root,f)) as fh:
                for link in re.findall(r'\[\[([^\]]+)\]\]',fh.read()):
                    incoming.setdefault(link,set()).add(name)
floating=[n for n in entities if n not in incoming]
print(f'Floating nodes: {len(floating)}/{len(entities)}')
for n in sorted(floating)[:10]: print(f'  {n}')
"
```

Also check: `wc -c CLAUDE.md` — must be < 3500 chars.

## Step 3: Projects

```bash
ls -d projects/*/AGENTS.md 2>/dev/null | wc -l
ls -d projects/*/context.md 2>/dev/null | wc -l
```

Score: 0 (no projects) / 1 (some without AGENTS.md) / 2 (all have AGENTS.md + context.md).
**Fresh vault:** if top-level `projects/` doesn't exist yet, score **N/A** — render `PROJECTS N/A (fresh vault)`, keep it out of GAPS, and drop it from the denominator (score /14 not /16). A blank vault is healthy-by-design here.

## Step 4: Skills

```bash
find .claude/skills -name "SKILL.md" 2>/dev/null | wc -l
```

For each: check the YAML frontmatter (`name:`, `version:`, `user_invocable:`).

Score: 0 (0 skills) / 1 (1-5) / 2 (6+ with frontmatter)

## Step 5: State & Cross-Context

```bash
wc -l state/current.md 2>/dev/null
ls state/sessions/*.md 2>/dev/null | wc -l
```

Check: `current.md` freshness (updated today?), session checkpoints exist?

Score: 0 (missing/stale >3 days) / 1 (exists but stale) / 2 (fresh, today)

## Step 6: Daily Notes Streak

```bash
# Count consecutive days with daily notes
for i in $(seq 0 30); do
    d=$(date -d "-${i} days" +%Y-%m-%d 2>/dev/null || date -v-${i}d +%Y-%m-%d 2>/dev/null)
    [ -f "daily/$d.md" ] || break
done
echo "Streak: $i days"
```

Score: 0 (no daily) / 1 (sporadic) / 2 (5+ day streak)

## Step 7: Hooks & Automation

> Scope: this folder ships its own hooks in the WORKSPACE `.claude/settings.json` — SessionStart → `session-start.sh` (pours state, counts sessions, opens the tidy-up / reflection gates), PreToolUse on Write|Edit → `wikilink-lint.sh`, PostToolUse on Bash|Grep → `semantic-recall.sh`. Check the workspace file, not `~/.claude/settings.json`; a fresh folder must score **2/2**.

```bash
python3 - <<'PY2'
import json, os
d = json.load(open('.claude/settings.json'))
n = 0
for event, configs in d.get('hooks', {}).items():
    for c in configs:
        for h in c.get('hooks', []):
            cmd = h.get('command', '')
            script = cmd.split('/.claude/hooks/')[-1].strip('"') if '/.claude/hooks/' in cmd else ''
            ok = os.path.exists(os.path.join('.claude/hooks', script)) if script else False
            n += ok
            print(f"  {event}: {script or cmd[:60]} {'OK' if ok else 'MISSING SCRIPT'}")
print(f"  registered with a present script: {n}")
PY2
```

Score: 0 (no hooks) / 1 (some, or a script missing) / 2 (SessionStart + PreToolUse + PostToolUse all registered and their scripts present)

## Step 8: Self-Improvement

```bash
wc -l context/anti-patterns.md 2>/dev/null
wc -l context/learned.md 2>/dev/null
ls reports/*reflection* 2>/dev/null | wc -l
```

Score: 0 (no anti-patterns) / 1 (exists but <5 entries) / 2 (active, >5 entries + reflections)

## Step 9: Git Health

```bash
git log --oneline -5
git status --short | wc -l
```

Score: 0 (not a repo) / 1 (repo but stale) / 2 (recent commits, clean status)

## Output

```
+-------------------------------------------------+
|  SELF-CHECK · {date}                            |
|  workspace: {cwd}                               |
+-------------------------------------------------+

  CONTEXT (CLAUDE.md)              {score}/2  {note}
  KNOWLEDGE GRAPH                  {score}/2  {N entities, N% linked}
  PROJECTS                         {score}/2  {N projects}
  SKILLS                           {score}/2  {N skills}
  STATE & CROSS-CONTEXT            {score}/2  {freshness}
  DAILY NOTES                      {score}/2  {streak}
  HOOKS & AUTOMATION               {score}/2  {N hooks}
  SELF-IMPROVEMENT                 {score}/2  {entries}
  ---------------------------------------------
  SCORE: {total}/16   (use /14 when PROJECTS is N/A on a fresh vault)

  GAPS (highest impact first):
  1. {gap + specific fix command}
  2. {gap + specific fix command}
  3. {gap + specific fix command}

  HEALTH:
  0-5   → 🔴 Setup needed
  6-10  → 🟡 Growing — focus on the operations layer
  11-14 → 🟢 Solid — optimize and automate
  15-16 → 🟣 Peak — share and evolve
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Counting files without checking content | Read first lines to verify quality |
| Not checking wikilink coverage | Files without links = isolated nodes |
| Ignoring freshness | A full system that's stale is worse than a small fresh one |
| Generic gaps | Each gap must have a specific command to fix it |
| Not checking that hook scripts exist | Script in settings.json but file missing = broken |
