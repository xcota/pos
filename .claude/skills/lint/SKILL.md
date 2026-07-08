---
name: lint
description: "Use weekly or after major ingest sessions to check wiki health."
version: 1.0
user_invocable: true
---
# /lint — Wiki Health Check

LLM-wiki pattern: a periodic lint prevents entropy. Run weekly or after major ingest sessions.

## Usage
`/lint` — full scan
`/lint orphans` — just the floating-nodes check
`/lint stale` — just stale entities
`/lint contradictions` — just contradictions
`/lint drift` — source drift check (content_hash validation)

## Checks

### 1. Floating Nodes
A floating node is an entity with zero incoming links — invisible in the graph. Target: 0.
```bash
python3 -c "
import os, re
workspace=os.getcwd()
kg=os.path.join(workspace, 'knowledge')
# Directories to skip when scanning for links. Add any non-knowledge or build dirs here.
EXCLUDE = {'memory','archive','backups','agents','skills','content','data','node_modules','.venv','inbox'}
aliases = {}
for root,dirs,files in os.walk(kg):
    for f in files:
        if f.endswith('.md') and f not in ('AGENTS.md','INDEX.md'):
            name = f.replace('.md','')
            aliases[name] = name
            with open(os.path.join(root,f)) as fh:
                content = fh.read()
            if content.startswith('---'):
                try:
                    fm = content[3:content.index('---',3)]
                    m = re.search(r'aliases:\s*\[([^\]]+)\]', fm)
                    if m:
                        for a in m.group(1).split(','):
                            aliases[a.strip().strip('\"').strip(\"'\")] = name
                except: pass

entities = set(aliases.values())
incoming = {}
for root,dirs,files in os.walk(workspace):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in EXCLUDE]
    for f in files:
        if not f.endswith('.md'): continue
        try:
            with open(os.path.join(root,f)) as fh:
                for link in re.findall(r'\[\[([^\]|]+)', fh.read()):
                    target = link.strip().split('/')[-1]
                    resolved = aliases.get(target, target)
                    incoming.setdefault(resolved, set()).add(f)
        except: pass

floating = sorted([n for n in entities if n not in incoming])
print(f'Floating: {len(floating)}')
for n in floating: print(f'  {n}')
"
```

### 2. Stale Claims
Entities with a `last_verified` field older than 30 days:
```bash
python3 -c "
import os, re
from datetime import datetime, timedelta
cutoff = datetime.now() - timedelta(days=30)
for root,_,files in os.walk('knowledge'):
    for f in files:
        if not f.endswith('.md'): continue
        path = os.path.join(root,f)
        with open(path) as fh:
            content = fh.read()
        m = re.search(r'last_verified:\s*(\S+)', content)
        if m:
            try:
                lv = datetime.strptime(m.group(1), '%Y-%m-%d')
                if lv < cutoff:
                    print(f'STALE: {path} (last verified {m.group(1)})')
            except: pass
"
```

### 3. Contradictions
Cross-entity numeric-claim check. For key numbers (thresholds, percentages, counts):
- Grep for a recurring numeric claim → compare all entries.
- Flag when the same claim has different values across entities.

```bash
# Example: replace the pattern with whatever recurring numeric claim your graph tracks
grep -r "threshold.*\$[0-9]" knowledge/ | awk -F: '{print $2}' | sort -u
grep -r "rate" knowledge/ | awk -F: '{print $2}' | sort -u
```

### 4. Missing Cross-References
Entities mentioning a name without linking to it:
```bash
# For each person in people/, find mentions without a [[wikilink]]
for p in knowledge/people/*.md; do
    name=$(basename "$p" .md)
    grep -rL "\[\[$name" knowledge/ | xargs -I{} grep -l "$name" {} 2>/dev/null
done
```

### 5. Source Drift
For entities with `content_hash`, recompute the source hash and compare:
```bash
python3 -c "
import os, re, hashlib
for root,_,files in os.walk('knowledge'):
    for f in files:
        if not f.endswith('.md'): continue
        path = os.path.join(root,f)
        with open(path) as fh:
            content = fh.read()
        src_m = re.search(r'source:\s*(\S+)', content)
        hash_m = re.search(r'content_hash:\s*sha256:(\w+)', content)
        if src_m and hash_m:
            src = src_m.group(1)
            stored = hash_m.group(1)
            if os.path.exists(src):
                actual = hashlib.sha256(open(src,'rb').read()).hexdigest()[:12]
                if actual != stored:
                    print(f'DRIFT: {path} — source changed ({stored} -> {actual})')
"
```

### 6. CLAUDE.md Size
```bash
size=$(wc -c < CLAUDE.md)
[ "$size" -gt 3500 ] && echo "WARNING: CLAUDE.md = $size bytes (limit 4000, safety 3500)"
```

### 7. Index Freshness (optional, script-backed)
If your vault ships an index generator script, regenerate the index when it's stale.
This starter ships markdown skills, not the generator script — treat this step as optional and wire it to your own script path if you have one.
```bash
# Optional: only if scripts/index_gen.py (or your equivalent) exists
[ -f scripts/index_gen.py ] && [ "$(find index.md -mtime +1 2>/dev/null | wc -l)" -gt 0 ] && python3 scripts/index_gen.py
```

### 8. Conflict Integrity (conflict-as-record)
```bash
# Open conflicts awaiting resolution
grep -rl "resolution: null" knowledge/conflicts/ 2>/dev/null | while read -r f; do echo "OPEN CONFLICT: $f"; done
# Orphaned downgrades: a note marked disputed but with no matching conflict record (or vice versa)
grep -rl "epistemic_status: disputed" knowledge/ 2>/dev/null | while read -r f; do
  grep -q "conflicts:" "$f" || echo "ORPHAN disputed (no conflicts:[]): $f"
done
```

### 9. Epistemic Enum Validation
```bash
# modality / epistemic_status outside the allowed enum (knowledge/conflicts/AGENTS.md) → drift/typo
# allowed modality: factual_claim observation assumption hypothesis decision policy preference requirement risk capability definition deprecation
# allowed epistemic_status: mention extracted_candidate sourced_claim corroborated_claim reviewed_claim accepted_knowledge canonical_knowledge disputed deprecated superseded forbidden_for_use assumption hypothesis
grep -rhoE "^(modality|epistemic_status): *[a-z_]+" knowledge/ 2>/dev/null | sort -u
# Eyeball against the enum; any value not in the list is a flag.
```
Also: `epistemic_status: canonical_knowledge` with `last_verified` >90d → suggest re-verification (canonical claims go stale too).

## Output

```
+-----------------------------------------+
|  LINT · {date}                          |
+-----------------------------------------+

  FLOATING NODES      : {N} / {total}
  STALE CLAIMS        : {N} entities with last_verified > 30 days
  CONTRADICTIONS      : {N} numeric disagreements flagged
  MISSING CROSS-REFS  : {N} unlinked mentions
  SOURCE DRIFT        : {N} entities out of sync with source
  CLAUDE.md SIZE      : {bytes} / 4000
  INDEX FRESHNESS     : {days old}

  HEALTH SCORE: {0-100}

  ACTIONS:
  1. {most critical fix}
  2. ...
```

## Log Entry
```
[{YYYY-MM-DD HH:MM}] [lint] {total} entities | {floating} floating | {stale} stale | {contradictions} contradictions | score: {N}
```

## Rules
- Run weekly (Mondays) or after major ingest sessions.
- Fix floating nodes immediately.
- Stale claims = ask the user to verify OR re-ingest from source.
- Contradictions = escalate to the user for resolution.
