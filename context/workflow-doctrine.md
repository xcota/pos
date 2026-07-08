---
type: context
tags: [rules, orchestration, agent-runtime, stable]
updated: 2026-07-08
---

# Workflow Doctrine: Tiers and Escalation

**Purpose:** Define when to execute a task directly in-session vs. delegating to a single Agent vs. launching a dynamic Workflow. This doctrine grounds the orchestration rules stated in `CLAUDE.md §Orchestration` with concrete decision gates and standard workflow patterns.

**Principle:** Main thread = dispatcher + synthesizer, not worker. Preserve context budget (60K target / 100K ceiling) and reserve decision-making capacity for arbitration, synthesis, and course correction.

**Scope-gate first (before ANY Tier-2/3 escalation).** Name the owner's verb → name the smallest artifact that closes it → deliver THAT first. A workflow/swarm/apparatus is justified only when the owner explicitly asked for it OR the artifact is impossible without it. Depth of reasoning ≠ size of apparatus. See `context/operating-manual.md` §Scope-Gate — the tiers below apply only *after* the gate confirms the task genuinely exceeds a direct answer.

---

## Tier 1: Direct Work (In-Session, Main Thread)

**Gate:** Task must pass ALL three checks below. If ANY fail, escalate.

1. **Scope:** Single file ≤50 lines, OR ≤20 lines of multi-file edits (all in same directory)
2. **Complexity:** No external API, no branching research, no multi-step iteration
3. **Reversibility:** Edits are low-risk (syntax, semantics, naming). No data loss, no system reconfiguration.

**Execution:** Main thread reads, edits, writes, verifies inline. Result first, explanation second.

**Examples of Tier 1:**
- Fix a typo or wikilink in a single file
- Rename a variable across 3 files in the same folder
- Add one rule to a list
- Update a date/version in metadata
- Write a short-form response to a specific question

**Examples NOT Tier 1:**
- "Refactor the scoring-gate logic" (>50 lines, requires understanding three modules)
- "Update all references when moving a file" (global search+replace, unbounded scope)
- "Research and summarize the latest AI papers" (external API, multi-step iteration)
- "Build an export pipeline" (involves writing a new script, testing, integration)

---

## Tier 2: Single Agent (Delegated Exploration / Planning)

**Gate:** Task exceeds Tier 1 scope but is:
- **Single-threaded** (one agent, one line of inquiry)
- **Well-scoped** (clear input, clear success criteria, bounded effort)
- **Output-focused** (produces artifact: analysis, plan, summary, or code)
- **No orchestration needed** (agent operates independently; main thread reviews result once)

**Execution:** Main thread frames the task → spawns ONE Agent with full context (read relevant files, execute, deliver artifact) → main thread reviews, synthesizes, corrects if needed.

**Standard patterns:**
- **Explore:** Deep reading of a folder/project. Agent reads, synthesizes. (Examples: codebase audit, knowledge graph analysis, competitive research)
- **Plan:** Architect a solution. Agent designs the approach, lists steps, identifies blockers. (Examples: refactoring strategy, deployment plan, integration roadmap)
- **Generate:** Create new content. Agent drafts artifact from requirements. (Examples: email template, documentation, analysis report)

**Examples of Tier 2:**
- "Audit the documentation project folder and produce a status report"
- "Plan the staging-server migration — what needs to move, what stays, what breaks"
- "Extract all decisions and lessons from the last 3 weeks of daily notes"
- "Design a schema for storing client feedback in the knowledge graph"

**Agent guidance (from CLAUDE.md §Orchestration):**
- Agent types: Explore (search/read), Plan (architecture), general-purpose (research/generation)
- Agent does NOT: orchestrate other agents, make user-facing decisions, or run indefinitely
- Main thread receives: structured summary + artifact. If ambiguous or incomplete, main thread asks follow-up or corrects.

---

## Tier 3: Dynamic Workflow (Multi-Agent Orchestration)

**Gate:** Task requires Tier 3 when ANY of these apply:
- **Multi-threaded inquiry** (2+ agents working in parallel or in sequence on related subproblems)
- **Adversarial verification** (claims must be contested, sources verified, findings stress-tested)
- **Judge/arbiter pattern** (competing analyses require synthesis and tiebreak)
- **Unbounded iteration** (a queue that drains to dry, or a gap-set that converges → see Pattern 5: Loop-Until-Dry)
- **High-stakes output** (decision support, financial/legal consequence, public-facing, affects system architecture)

**Execution:** Main thread frames mission → designs workflow topology → orchestrates agents in parallel/pipeline/judge-panel → gathers results → synthesizes final output.

**Standard workflow patterns:**

### Pattern 1: Fan-Out (Parallel Deep Dive)
Multiple agents explore **independent subdomains** in parallel. Used when:
- Research spans multiple domains (history, tech, market, psychology, etc.)
- Different aspects of a problem can be solved independently
- Results are combined in synthesis, not required for each other

**Example:** "Understand the electric-vehicle charging market: regulatory landscape (Agent A), top 10 hardware vendors (Agent B), pricing/positioning (Agent C), customer pain points (Agent D). Synthesize into one playbook."

**Workflow steps:**
1. Frame query
2. Decompose into subquestions (4–6 agents max)
3. Spawn agents in parallel with isolated prompts + source hints
4. Gather structured results
5. Main thread synthesizes: map overlaps, resolve conflicts, extract narrative

### Pattern 2: Pipeline (Sequential Refinement)
Agents work in **sequence**, each refining output of the previous. Used when:
- Output of step N is input to step N+1
- Quality improves through iterative polish (research → analyze → synthesize → formalize)
- Early stages are exploratory; later stages are hardening

**Example:** "Build an investment thesis on a generic project-management SaaS: (1) Market sizing, (2) Competitive landscape, (3) Unit economics analysis, (4) Founder fit assessment, (5) Draft memo."

**Workflow steps:**
1. Frame endpoint (final deliverable)
2. Design stages (5–7 max)
3. Spawn Stage 1 agent with high-level prompt
4. When Stage 1 completes, spawn Stage 2 with Stage 1 output as context
5. Continue until final stage
6. Main thread edits/approves final artifact

### Pattern 3: Adversarial Verify (Claim Stress-Test)
One agent generates **claim + evidence**. Another agent **tries to break it** (find counterexamples, spot logical gaps, test assumptions). Used when:
- Claim carries real weight (affects decision, shapes belief, will be externally shared)
- Cost of being wrong is high
- Source material is ambiguous or contested

**Example:** "the team should add a paid tier as the next revenue line. (1) Agent A drafts thesis with evidence. (2) Agent B plays skeptic: what would disprove this? Find the gaps. (3) Main thread decides yes/no/adjust based on stress-test."

**Workflow steps:**
1. Agent A (proponent): "Build the case for X. Cite evidence. State assumptions."
2. Agent B (skeptic): "Attack this thesis. Find every assumption that could be wrong. Find data that contradicts it."
3. Main thread: "Confidence in original claim? What changed?"
4. If needed, Agent C (resolver): "Integrate feedback. Which counterarguments hold? Revise."

### Pattern 4: Judge Panel (Multi-Perspective Decision)
Multiple agents analyze the **same problem from different angles** (business, technical, risk, user impact, etc.). Results feed into main-thread judgment. Used when:
- Decision is multi-dimensional (can't be reduced to one axis)
- Stakeholder perspectives are genuinely different
- Want to avoid single-agent blind spot

**Example:** "Should we migrate the analytics dashboard to a real database? Business view (Agent A), engineering view (Agent B), maintenance burden (Agent C), data-sovereignty view (Agent D). Then decide."

**Workflow steps:**
1. Define perspectives (4–5 max)
2. Spawn agents in parallel, each with their lens + shared context
3. Each agent rates the decision (recommend yes/no/conditional) with reasoning
4. Main thread assembles decision matrix
5. Main thread arbitrates: which perspectives carry weight? What's the call?

### Pattern 5: Loop-Until-Dry (Bounded Iteration)

The executable form of the **"Unbounded iteration"** Tier-3 gate. Patterns 1–4 are single-pass; use Pattern 5 when the work is a *queue that drains* or a *gap-set that converges*. Two shapes, one control skeleton.

**Shape A — Bounded Queue Drain** (often Tier 2: main thread, or one agent per item). The input is enumerable but its size isn't known upfront — an inbox, daily-note gaps, a backlog. Process one item at a time and **commit each result to `state/` / `knowledge/` before touching the next**, so a crash or compaction always leaves a clean resume point, never a half-written batch. Typical uses: draining an inbox folder, working an anti-pattern backlog from recent notes, consolidating entity clusters one at a time.

**Shape B — Verify-Fix Convergence** (Tier 3: multi-agent). The gap-set isn't known upfront — each fix can expose second-order gaps. Loop `verify → fix → re-verify` until zero new gaps. One **top-tier** verifier reads current state from FILES each round (grep/ls the ground truth, not the prior agent's context — this is where the extra agents earn their cost, see §Model Routing shape law); a **worker-tier** fixer addresses only that round's gaps (no scope creep, Anti-Pattern 2). Typical uses: looping a single-pass linter or audit until it reports "0 floating / 0 stale".

**Control skeleton (both shapes — every loop ships with all four):**
1. **Hard cap.** Default 10 items (Shape A) / 3 rounds (Shape B), 6 for deep audits. The cap — not a vibe — is the guard against an unbounded top-tier loop draining the session. No loop ships without one.
2. **Dry / plateau exit.** Stop on empty queue (A) or zero-new-gaps (B). Plateau: if the last 3 items score below the accept threshold (`context/scoring-gate.md`) or a round's gap count didn't drop, BREAK — the root is structural; re-discover next session rather than grinding.
3. **Budget-floor = exit-path cost.** Re-check before each iteration, but size the floor to what still must run after the last item: the closing synthesis + the `/session-save` write. If that synthesis runs **in-thread**, reserve ~30–40K below the ceiling — at a flat ~20K the loop fires one more item and crashes mid-synthesis. If it's **delegated to an agent** (Shape B), that pass costs the main thread only its ≤15K return, so ~20K is enough. Once working-set is within that reserve, `/session-save` instead of starting another item.
4. **Resumable checkpoint.** On any early stop, write the remaining queue into `state/sessions/{workflow}_status.md` (the same checkpoint the Tier-3 coordination rule already mandates — one resume file per run).

**Routing (§Model Routing):** the per-item / per-round body is the **default worker**; the top tier only on items that are genuine seam/judgment calls or a final synthesis pass. Never default the whole loop to the top tier.

---

## Escalation Decision Tree

```
Task arrives
│
├─ Scope ≤50 lines? AND no research/API? AND reversible?
│  └─ YES → TIER 1 (direct work)
│  └─ NO → continue
│
├─ Single-agent sufficient?
│  (One agent can execute fully. Output is atomic.)
│  └─ YES → TIER 2 (single Agent)
│  └─ NO → continue
│
└─ Multi-threaded? OR adversarial? OR judge-panel? OR unbounded?
   └─ YES → TIER 3 (dynamic Workflow)
   └─ NO → reconsider scope or re-frame as Tier 2
```

---

## Tier 3 Coordination Rules

**When launching a workflow:**

1. **Write mission statement** (2–3 sentences). Example: "Understand what a 'Personal OS' means to 5 different communities (investors, engineers, students, artists, scientists). Map consensus and divergence."

2. **Design topology.** Decide:
   - How many agents? (2–6 typical)
   - Parallelizable or sequential?
   - Do results feed into each other or are they independent?

3. **Assign roles** (to agents or Agent instances). Each gets:
   - Specific sub-question or domain
   - Relevant source context (point to files, not dump them)
   - Success criteria ("deliver structured analysis with 3 findings + evidence for each")

4. **Orchestrate.**
   - Parallel agents: spawn all at once. Give them all common context (mission + role specifics). Main thread waits for all to complete.
   - Sequential: spawn Stage 1 → main thread stages result → spawn Stage 2 with staged result as context.
   - Adversarial: spawn proponent + skeptic in parallel (or skeptic second after reviewing proponent output).

5. **Synthesize result.** Main thread:
   - Reads all agent outputs
   - Identifies convergence (what's consistent across agents?)
   - Spots conflicts (where do agents disagree? Why?)
   - Fills gaps (what's missing from the 5 viewpoints?)
   - Produces final narrative or decision

6. **Checkpoints for long workflows** (>2h / complex multi-stage):
   - Create `state/sessions/{workflow-name}_status.md` tracking progress
   - Append each agent result as a section
   - Use `plan.md` template if rearchitecting mid-workflow
   - Save checkpoints in `state/sessions/` before context compaction

---

## Context Budget in Tier 3

When spawning agents for a workflow:

- **Don't dump full vault context.** Agent inherits main-thread context (CLAUDE.md, AGENTS.md, boot) automatically.
- **Point to, don't paste.** Tell agent "See `knowledge/{domain}/MOC_{domain}.md` for domain overview" rather than loading 50 entities.
- **One MOC per agent.** If agent needs a map, give it ONE entry point (MOC or hub). From there, agent navigates.
- **Compressed input.** If briefing agent on previous work, use `daily/` summary + one pinned checkpoint, not full history.

**Budget math (reconciled with the 100K main-thread ceiling):**
- Main thread: 60K target / **100K ceiling**. Session-lifetime ≤ 200K (this includes the agents' own internal token spend, which runs in a separate context — it does NOT all land back on the main thread).
- **Agents return COMPACT structured summaries (≤ 15K each), not their full working context.** A 4-agent fan-out that each returned 40K would dump 160K back onto a 100K-ceiling dispatcher — that breaks synthesis. Cap agent *returns*, point them at files instead of pasting.
- If a fan-out's combined returns would still exceed the ceiling, read agent RESULTS sequentially and checkpoint each to `state/sessions/{workflow}_status.md` between reads, rather than holding all in context at once.
- Approaching the ceiling mid-workflow → `/session-save` to compact before spawning the next wave.

---

## Return Contracts in Tier 3

Size is capped above (≤15K). This caps **shape**. When a wave of 2+ agents produces outputs that will be **compared, scored, voted, or counted** (not just narrated), state the return shape in the prompt *before* spawning — so the main thread tallies mechanically instead of re-parsing prose:
- Judge-panel → each judge returns `{vote: accept|reject|conditional, score, rationale}` → count/average.
- Adversarial-verify → refuter returns `{survives: bool, reason, evidence_file_line}` → read the booleans.
- Fan-out → each agent returns `{topic, findings[], confidence}` → merge arrays.

Not new capability — `context/scoring-gate.md` already defines a scored return, `/pos-audit` returns a per-dimension score, `/ingest` emits per-chunk confidence + coverage enums. This generalizes that discipline to ad-hoc waves. No MCP, no parser — just a prompt contract.

**Scope limit (don't overstate):** the shape covers the *aggregatable* fields (votes, scores, survives, confidence) so the tally is mechanical. The findings/evidence themselves still get main-thread **synthesis** — resolve conflicts, fill gaps, write narrative (§Tier 3 Coordination step 5). Schema speeds the count; it does not replace the seam-pass judgment.

---

## Model Routing — which model per role

Workflow agents inherit the main-loop model unless you set `model:` per agent. Staff cheaply without losing quality (empirically derived, not guessed):

| Agent role | Default | Cheapest OK | Never |
|---|---|---|---|
| Cartographer / inventory (accuracy = the job) | opus¹ | **sonnet** | haiku (fabricates counts + invents proper nouns even here) |
| Analyst / synthesizer (reconcile over settled arch) | opus¹ | **sonnet** (~85% of opus) | haiku (confidently-wrong synthesis) |
| Adversarial verifier / refuter / premise-check | **opus** | opus | sonnet/haiku — they answer the wrong frame |
| Builder / scoped generation | **sonnet** | haiku (if a stronger model re-checks) | — |
| Final synthesis / arbiter / decision-gate | **opus** | opus | — |

¹ best-for-role, pay the premium only when a wrong framing is expensive (the seam/decision pass). Otherwise sonnet is the **default worker**.

**The shape law (the load-bearing finding): agent count ≠ quality.** A solo opus beat a 4-agent haiku fan-out. Multi-agent overhead pays off **only when the extra agents do adversarial verification against ground truth** (grep/ls the real files), NOT parallel drafting. So:
- Pure reasoning / few external facts → **solo opus or sonnet** (don't fan out).
- Fact-dense / irreversible / "does X exist, is Y wired" → **add an adversarial-verify barrier** (1 proposer + 1–2 opus refuters who check files). This is where the agents earn their cost.
- Parallel drafting + a synth polish (fan-out) is the **worst value** — same agent budget, confident prose, weakest grounding.

Mirrors `context/scoring-gate.md` (the canonical model-tier table — keep routing there, this is the workflow-specific overlay). Note: the cartographer / analyst / verifier / builder routings are the load-bearing ones; the merged-pipeline and live-state refinements are single-datapoint priors — don't harden them.

## Anti-Patterns (What Not to Do)

1. **Fake parallelism.** Spawning 2 agents but agent B can't start until agent A finishes. Use sequential pattern instead.
2. **Scope creep.** Agent starts as Tier 2 (single focused task) but discovers 5 new questions mid-run. Either add sub-agents (Tier 3) or stop and report gaps.
3. **Decision avoidance.** Spawning a workflow instead of making a call. ("Let agents decide whether we should X.") Workflows inform; main thread decides.
4. **Agent isolation.** Tier 2 agent operates with zero context. Always load enough domain context for the agent to be productive (MOC + 2–3 hub entities).
5. **Workflow without mission.** Launching agents without a clear endpoint. "Research the market" is vague. "Build playbook: what's working for your target segment right now?" is clear.

---

## When to Use Each Tier

| Task | Tier | Reason |
|------|------|--------|
| Fix typo in CLAUDE.md | 1 | <50 lines, reversible |
| Rename one entity across 5 backlinks | 2 | Single agent handles wikilink audit |
| Audit entire analytics dashboard folder | 2 | Explore pattern: one agent reads, synthesizes |
| Should we hire? | 3 | Multiple perspectives + judge panel needed |
| Language-learning progress report | 2 | One agent reviews daily notes + skills |
| Rebuild a data pipeline | 3 | Multi-stage: design (Agent A) → implement roadmap (Agent B) → risk review (Agent C) |
| Add one learned lesson to anti-patterns | 1 | ≤5 lines, no dependencies |
| Resolve conflict between two founders | 3 | Adversarial pattern: each perspective stressed-tested |
| Extract all AP- entries from daily notes | 2 | One agent parses + indexes |

---

## Authoring Defaults (mechanics of the tool)

- **Web/LLM fan-out beyond ~6 agents in one burst → fire in WAVES of 3–4** (loop over batches, awaiting between them). The provider throttles a large simultaneous burst ("temporarily limiting requests" — distinct from a usage-limit error); a retry inside the agent call does NOT punch through it, but staggered waves do. Make this the default for any large web/research swarm.
- **A pipeline returns ONLY its last stage.** If you need the intermediate stage's output for synthesis, the final stage MUST bundle it: `return {...intermediate_result, audit: final_result}`. Otherwise the intermediate layer is lost and has to be recovered from raw agent logs.

---

## See Also

- `CLAUDE.md` — boot-order orchestration rules
- `context/operating-manual.md` — how the owner prefers to work
- `context/agent-runtime.md` — agent loading discipline
- `state/sessions/` — checkpoints for long-running work
- `_templates/plan_template.md` — for Tier 3 planning
