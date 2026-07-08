---
name: reflect
description: "Use every 3 days or when explicitly asked to review and improve recent work patterns."
version: 1.0
user_invocable: true
---
# /reflect — Periodic Self-Reflection

Analyze recent work, extract patterns, learn from mistakes, propose improvements.

**Core principle:** the strongest self-improvement signal is NOT the daily summary — it is **the conversation itself**: what the user says, in what tone, where friction or correction shows up; and how the agent responds (where it landed, where it substituted its own agenda, failed to orient, or over-produced). Mining recent transcripts for that friction is the crown jewel of this skill.

## When to Use
- Manually: when you want to review and improve
- Auto: wire up a periodic trigger yourself (e.g. a cron job or `/loop` calling `/reflect`) — not shipped by default

## Steps

1. **Gather data:**
   - Read last 3-5 daily notes from `daily/`
   - Read recent entries in `state/decisions/`
   - Read `context/anti-patterns.md` (what were we watching for?) + `anti-patterns-index.md` watch-list
   - Read `context/learned.md` (what did we already know?)
   - Check recent git log: `git log --oneline -20`

1b. **Analyze the CONVERSATION (the main signal):**
   - Source = recent session transcripts. Resolve the path generically from this project's slug under the Claude projects dir, e.g.:
     ```bash
     PROJECT_SLUG=$(pwd | sed 's#/#-#g')
     TRANSCRIPT_DIR="$HOME/.claude/projects/$PROJECT_SLUG"
     NEWEST=$(ls -t "$TRANSCRIPT_DIR"/*.jsonl 2>/dev/null | head -1)
     ```
     (Adjust the slug derivation to your harness; the point is workspace-derived, not hardcoded.) Do NOT bulk-load — extract only user turns + agent replies + friction points.
   - Extract user turns, e.g.:
     ```bash
     cat "$NEWEST" | python3 -c "import json,sys; [print('U:', json.loads(l).get('message',{}).get('content','')[:300]) for l in sys.stdin if json.loads(l).get('type')=='user']"
     ```
     (Adapt to the actual transcript format.) Look for: corrections, frustration/anger (friction), "not that / not like that", energy shifts, what the user re-asks.
   - About the USER: how they respond (tone, length, what they value/dislike in THIS session), what latent needs surfaced → candidates for `context/identity.md` / memory, with a source-tier.
   - About the AGENT: where it landed, where it **substituted** its own agenda (substitution-instinct), where it **failed to orient** before committing, over-produced or added noise, made the user wait. Each real friction point → anti-pattern candidate.

2. **Analyze patterns:**
   - What went well? What patterns led to good outcomes?
   - What went wrong? What patterns led to bad outcomes?
   - Were any anti-patterns triggered? Which ones? (especially from the watch-list)
   - What mistakes were repeated despite being in anti-patterns?
   - What new capabilities or knowledge emerged?
   - **What could the agent reasonably initiate on its own** to serve the user's goals — a concrete proactive candidate, not generic.

3. **Extract learnings:**
   - New operational lessons → append to `context/learned.md`
   - New anti-patterns → append to `context/anti-patterns.md`
   - New knowledge entities → create in `knowledge/`

4. **Propose improvements:**
   - If a script/skill keeps failing → propose a fix
   - If a workflow is inefficient → propose optimization
   - If context management is suboptimal → propose restructuring
   - Be specific: what to change, where, why

5. **Update goals if needed:**
   - Review `context/goals.md` — are horizons still relevant?
   - Update status of goals
   - Add new goals if they emerged from reflection

6. **Write reflection report:**
   - Save to `reports/reflection-{date}.md`
   - Compact: patterns, learnings, improvements, stats
   - Reflect on the work in its own terms. Judge work against the user's stated priorities — don't impose an external "infra-vs-output" or productivity ratio the user hasn't asked for.

7. **Git commit:**
   ```bash
   git add -A && git commit -m "[reflect]: {key insight or change}"
   ```

## Metrics to Track
- Tasks completed vs created
- Anti-patterns triggered (should decrease over time)
- New knowledge entities added
- Recurring mistakes resurfacing despite anti-patterns (→ escalate to rules/)
- Context efficiency (were sessions within budget?)

## Rules
- Be honest. Don't sugarcoat failures.
- One concrete improvement > ten vague observations
- Update anti-patterns.md with EVERY new mistake pattern
- If the same mistake appears 3+ times → escalate to rules/
