---
type: context
tags: [lessons, evolving]
updated: 2026-01-01
---

# Distilled Lessons

Operating lessons the agent has learned and should not have to re-derive. Where
`anti-patterns.md` records *what not to do*, this file records *how to work well*
— positive heuristics that pay off across sessions.

This is the **universal subset** distilled from a long real operating record. The
owner-specific incidents, names, dates, and one-off tool internals were dropped;
the transferable heuristic was kept. Append your own with the next free `L-NNN`.

## Convention (read before adding entries)

- **Append at the bottom**, with the next free `L-NNN`. Never delete an entry;
  only amend. To retire a lesson, add a status banner in place
  (`SUPERSEDED by L-NNN` / `RETRACTED` / `CLOSED-DOMAIN`) — keep the tombstone so
  a later cycle doesn't re-derive a thing already decided against.
- **Never renumber.** `L-NNN` is a stable citation key referenced from the index
  and from session notes.
- **One lesson per entry**, a few lines, written as a reusable heuristic — not a
  story about a single incident.
- Group entries under a theme heading; mirror the themes in `learned-index.md`.

---

## Orchestration & Subagent discipline

## L-001: The dispatcher doesn't do the work
The main thread orchestrates and synthesizes; it must not become a worker that
hoards context. Hand non-trivial search, generation, and analysis to subagents and
keep the main thread holding only the goal and the latest summaries. The structural
fix for context degradation past a large window is aggressive dispatch — each
subagent is its own isolated window and returns a short summary, not raw reads.

## L-002: Quality-gate subagent output before relaying it
A subagent's result is input, not truth. Score it, check it against your own
anti-patterns and the actual request, and filter or correct it before passing it
on. A cheap scoring gate (accept ≥ threshold, else iterate with specific feedback)
costs a little and prevents shallow or hallucinated output from persisting.

## L-003: Anti-patterns don't propagate into subagents — inject or post-filter
A spawned subagent runs on a clean context plus its prompt; it cannot see your
accumulated anti-patterns. So when orchestrating an audit/review, either inject the
relevant constraints into the subagent prompt, or post-filter its findings against
your anti-patterns before relaying. Never hand a synthesis agent's output to the
operator as truth.

## L-004: Match model and machinery to the task tier
Cheap, fast workers for grunt steps (recon, census, enumeration); reserve the
expensive model for genuine synthesis. Over-provisioning compute is the same
mistake as under-provisioning attention. A hard usage ceiling is real — a large
fan-out on the wrong model can exhaust the operator's session mid-task.

## L-005: Parallel extraction works when agents share zero state
A fan-out of independent workers succeeds when each has a single source, a single
output target, no dependency on another's results, and ideally a different
resource bottleneck. Shared mutable state (one session file, one lock, one DB) is
where parallelism turns into corruption.

## L-006: Save state at phase transitions, not at the context ceiling
The right time to checkpoint is when the *type* of work changes (infra-building →
production, research → build), not when tokens hit a number. Two clean contexts
beat one bloated one; momentum past the natural save point is how sessions
overflow.

## L-007: In a long multi-step run, be terse at every step
On a many-turn autonomous task, a full prose report after each sub-step compounds
into bloat the operator stops reading. Emit 1–3 lines per sub-step (what you did +
a reference), and reserve the full write-up for the end or an explicit request.
Let an artifact or dashboard carry the detail; trim the text around it.

---

## Knowledge graph & Vault integrity

## L-008: A correction is a durable prior, not a one-time patch
When the operator corrects something — a fact about their setup, a preference, a
boundary — write it where it reloads automatically and check against it before
delivering. Re-asking or re-violating a settled point is the fastest way to lose
trust. Profile completeness beats process optimization: the most expensive errors
come from missing facts about the operator (their constraints, income, expertise),
so save hard facts the moment they're revealed.

## L-009: Orient by retrieval before generation
Before answering a non-trivial question or building anything, pull what already
exists — files, prior lessons, the named source. Retrieval first means the answer
is consistent with the system instead of contradicting it. This applies to tooling
too: check for an existing working path before standing one up.

## L-010: A graph entity needs a backlink at creation time
Outgoing links without an incoming link make a floating node the graph won't show
as connected. Update ≥1 hub entity to link the new node *in the same commit*, then
validate that a search for links to it returns ≥1. Track average links-per-note as
a health metric (below ~1.5 = isolated knowledge).

## L-011: Record conflicts instead of overwriting them
When a new fact contradicts a stored one, don't blindly overwrite newer-beats-older.
Keep both as records with their source and tier, and gate promotion to "canonical".
A flat newer-wins model silently loses information; a status ladder (mention →
sourced → corroborated → accepted, plus disputed/superseded) preserves the
disagreement until it's actually resolved.

## L-012: Verify integration, not just creation
Creating N entity files is not the same as integrating them into the graph. After
creation, check for incoming backlinks; zero = a floating node, not integration.
Maintain index coverage too — a navigation layer that indexes a small fraction of
files breaks discovery and quietly erodes trust.

## L-013: A wikilink lint that requires the target to exist forces a write order
If a pre-write check blocks links to nonexistent entities, circular references
break parallel writes. Resolve by writing stubs without cross-links first, then a
second pass to add the cross-links — bulk-create, then batch-link.

## L-014: Bulk graph cleanup is high-leverage and safer than expected
When link health degrades, classify the broken references into a handful of buckets
(aliases, path-style refs, noise, missing stubs), apply the right transform per
bucket, then run one programmatic pass. Classifying first avoids touching files
multiple times and avoids creating noise stubs for things that aren't real entities.

## L-015: A map-of-content is a navigation layer, not a flat list
An MOC is a curated entry point with context (who/what/why), not a dump of
everything in a domain. The vault's home file is the cognitive anchor — one file
that shows all domains, current priorities, and recent work; sort it first.
Minimal templates (a few fields) get used; maximal ones (many fields) get
abandoned. Separate processed summaries from raw transcripts — summaries are
knowledge, raw text is archive.

---

## Communication, Trust & Frame-switching

## L-016: Restate the frame when the operator pushes back
Frustration or a correction is a signal to re-establish what's actually being
asked, not to defend the previous attempt. After two pushback markers in a row,
stop and restate the frame in your own words ("you want X, not Y — here's X")
*before* the substantive answer. This forces an explicit frame switch instead of a
partial drift, and it's where shallow-but-confident answers get caught.

## L-017: When the operator converges, validate the gaps — don't re-derive
If their last few messages show they've already articulated a thesis, the marginal
value is in the *gaps* (missing dates, contradictions, specific numbers), not in
restating the frame. A long re-derivation of a held position is bloat. Likewise:
when they share something framed "look at this", the value is your read of it, not
a re-statement of what they said.

## L-018: Trust the operator's domain expertise over agent landscape analysis
Agent swarms are good at mapping a landscape and bad at judgment calls in a domain
where the operator has deep experience (pricing, market reality, their own field).
When their intuition contradicts the analysis, trust them and investigate why the
analysis was wrong.

## L-019: Deliver the artifact or the dig — not a strategic comment on their position
When the operator queues "go through these findings", deliver a concrete output per
item (a built thing, a real piece of research persisted to the graph) — not a
meta-analysis evaluating *their* situation. They want you to build or to dig, not
to grade their bets. The problem with framework-decorated commentary isn't the
words, it's the genre.

## L-020: Shorthand resolves to the tooling stack before the concept
A short or unexpected token from the operator is more likely their shorthand for a
tool/account/source than the generic concept it resembles. First grep env, config,
scripts, and knowledge for it as a name; concept-level interpretation is the second
pass. When ambiguous, ask before building a plan on a guessed meaning.

## L-021: Ask for load-bearing context before a personalized answer, not after the failure
For deep personalized advice (health, diet, protocols, anything operator-specific),
load the relevant profile and explicitly ask for the missing load-bearing axes up
front. A generic answer followed by correction costs more than one question asked
first — this is exactly where an early focused question is right.

## L-022: When asked for the source/origin, keep regressing upstream — don't enumerate downstream
If the operator asks what's *deeper* / earlier / the root of something, the answer
is "what came before that this borrowed from", not a list of modern operational
consequences. Keep tracing the lineage until first principles; operational
descendants are a different question even when they share vocabulary.

---

## Process discipline & Anti-procrastination

## L-023: Lesson/reflection count is not a health metric
Generating lessons about a failure mode faster than you fix it is itself the
failure mode — reflection can become sophisticated procrastination. The health
metric is the real output (the thing shipped, the question answered), not the
volume of meta-work about it.

## L-024: A recurring failure is fixed at the directive layer, not the advisory one
If a pattern recurs despite an anti-pattern naming it, the problem isn't a missing
anti-pattern — it's a *directive* file (goals, priorities, a skill's standing
instruction) that overrides the advice. Advice loses to a directive every time.
Find and fix the directive (or promote to a hard rule); don't add another advisory
entry. *(See the escalation mechanism in `anti-patterns-index.md`.)*

## L-025: "Mechanical" sub-tasks slip past the orient/filter discipline
The headline failures share a shape: the discipline was in context, but you didn't
invoke it on a step you mentally filed as routine. The moment a task *feels*
mechanical is the trigger to **slow down** (grep the stack, run it past your
anti-patterns) — not to speed up. That's exactly where you relax and miss.

## L-026: The growth edge is calibration and restraint, not capability
A cluster of failures often traces not to a lack of skill but to over-production —
high-quality processing of too much, without restraint or the form the operator
actually needs in the moment. Before a big move (a swarm, a long report, thousands
of lines), ask: did they want *volume* or a *result in a specific form*? Default to
less and more precise. When you notice a recurrence forming, flag it in one line
immediately, don't wait for a reflection cycle.

## L-027: Build → run → verify can close the case for the tool itself
Building a small instrument and adversarially verifying its own output is a valid
experiment: sometimes it proves the tool isn't needed (a real "zero delta",
established by evidence rather than from the armchair) while surfacing a genuine
finding along the way. The build isn't wasted if it answered the question.

## L-028: Time-box a "warmup" or "quick" side task
When a task is explicitly framed as warmup / quick / a side-quest, time-box it at
the start. When the budget is breached, surface it and ask whether to continue or
return to the main lane. Don't let the warmup quietly consume the session.

## L-029: Research without an execution deadline is procrastination
Knowledge accumulation feels like progress but produces nothing tangible until
applied. Every research output needs an action attached with a deadline. The
forcing function — an external commitment to *do* something with it — is what makes
the research pay off, not the volume of it.

---

## Infrastructure, Reliability & Ops

## L-030: Init files before any job assumes them
Cron jobs and reflection loops often assume their target files exist; they may not.
Initialize target files at bootstrap, before scheduling anything that depends on
them.

## L-031: Anything that "runs automatically" needs a heartbeat
A scheduled job that fails silently isn't noticed until its absence is. Every such
job should log a success timestamp, alert on failure through the active channel,
and be covered by an audit that compares "last successful run" to its expected
frequency.

## L-032: A persistent daemon needs a managed unit from day one
A bare process (launched by hand) doesn't survive a reboot or a kill. If something
must persist, give it a managed service unit with auto-restart from the start —
"I'll do it later" means you forget, it dies after an update, and no one notices.
When recreating a unit, reproduce the *exact* launch path of the running process,
don't guess it.

## L-033: Track failures by root cause, not by count
A large failure count often collapses to a few roots — most of the failures share
one cause. Tag each failure by cause and fix roots; one root fix can eliminate many
failures. The raw count misleads.

## L-034: Never rsync a `.git` directory — sync git through git
Partial file inclusion can strand index files without their pack objects, producing
a silent time-bomb that only surfaces on a full tree-walk operation. Sync git via
push/pull/fetch; if you must back up `.git`, copy the whole thing as one opaque
blob, never partially. For heterogeneous-host sync, only the consolidated output
should travel — raw media/source stays where it was ingested, behind aggressive
excludes.

## L-035: Don't commit raw media — hard-block it in `.gitignore` from the first commit
A repo bloats irrecoverably when raw media (video/audio/archives/large binaries)
enters history; later filtering is expensive and a fresh init may be the only cure.
Add the media block to `.gitignore` as the first file, and sanity-check total size
after the first `git add`. For a single-operator repo, a fresh init plus a text
archive of the old log beats a heavyweight history rewrite.

## L-036: Add a cheap proactive check for any class of state that can rot silently
If a class of state can degrade quietly and surface only at high cost (a failed
deploy, lost work, broken sync), add a cheap check to the most-frequent recurring
entry point. The cost of detection should be ≤1% of the cost of repair. Candidates:
git pack integrity, scheduled-task heartbeats, unbounded log growth, link-health
delta, stale worktrees.

## L-037: A restricted process can fail networking identically to a real outage
A process running inside a sandboxed app may be silently denied LAN/unicast access
while a normal terminal on the same machine reaches the target fine — the failure
looks identical to "host down". Distinguish them: if a low-level reachability probe
(ARP resolve, a UDP traceroute) succeeds while TCP fails, the host is alive and the
*process* is blocked — pivot to process-scope permissions, don't keep debugging the
network. The fix is a host-level permission toggle, or handing the final command to
the operator's real terminal.

## L-038: Delivery through a notification channel is best-effort — don't block on it
When a report needs to reach the operator and the channel is down, persist the
content to a checkpoint and give them the recovery steps; don't loop retries or
count the task as failed because the *notification* failed. Have a fallback path,
and never rename/move live session files a daemon may be holding.

---

## Extraction & Reverse-engineering

## L-039: Capture the reference response first — it's the cheapest step
When reverse-engineering a client/server protocol, step 1 is to capture the real
response from the real server (a direct request, dev-tools, a replay log), then diff
a known-working state against the broken one. Mock iterations without that baseline
are guess-loops. After ~3 iterations with no change in the error class, re-acquire
the reference instead of trying another variant.

## L-040: Identify the packer/format before planning the decompile
Recovery cost varies wildly by how a thing was packaged. A few bytes of
`strings`/magic identification up front tells you which path applies and what scope
is realistic — promising "full recovery" before checking the format is how you
over-commit. Triage first, then pick the strategy.

## L-041: The valuable product logic is usually the engine, not the UI shell
After reverse-engineering a GUI tool, separate the behavioral engine (schema,
transforms, the actual logic) from the disposable UI. If the operator's workflow is
batch/ops-heavy, a CLI-first spec captures the value and the GUI details are noise.
Cloning the GUI is the wrong granularity.

## L-042: A browser-visible source can bypass a shell-network failure
If the operator has a source open in a browser but shell/CLI network is unreliable,
use the browser session or its in-app API as the source path instead of retrying
the CLI indefinitely. Don't over-engineer DOM filtering when a downstream LLM pass
cleans residual noise cheaply.

## L-043: Verify *who* is speaking before attributing extracted facts
In multi-speaker material, file location and folder convention do not guarantee
speaker identity. Confirm the speaker before extracting, and tag facts per-speaker
in mixed transcripts — otherwise one person's facts get attributed to another and
cached downstream.

## L-044: Keep three buckets separate — match, true-not-found, and tool error
In any validator or enricher, a parser/API exception is not a negative result.
Conflating "the tool errored" with "no match" poisons downstream data. Keep
positive match, true not-found, and tool error as distinct outcomes; never write an
exception into negative data.

## L-045: For aggregated/merged data, trust strong signals over a single dirty field
In data merged from many sources, a convenient field (a country column, a
self-reported tag) is often mis-mapped garbage. Derive the attribute from stronger,
harder-to-corrupt signals (multiple corroborating fields), and always inspect the
top of an extract for contamination before delivering or acting on it.

## L-046: Keyword/substring harvesting has predictable false-positive classes
Substring matching produces predictable false positives (a token inside a longer
word, a brand homonym, a surname). Scan once expensively, **dump the result**, then
iterate the false-positive filters locally on the cache instead of re-scanning.
Tier by confidence rather than a flat list, and inspect the highest-volume hits
first — the biggest false positive tends to float to the top.

---

## Architecture philosophy

## L-047: The most-loaded file is the most critical — guard it hardest
The file loaded every session sets the frame for every session; if it's wrong,
every session is wrong. Respect its hard size limit (truncation can be silent),
verify after every edit, and move non-essential content to files loaded on demand.
A directory restructure must grep the old paths out of every index/boot file in the
same commit, or navigation rots invisibly.

## L-048: Steal patterns, not infrastructure
An external tool's design (its information architecture, conventions, schema) often
transfers across stacks even when its code doesn't. Read the design docs and
conventions first, the code second; adopt the pattern and reject the
implementation. Judge an external repo by its *code*, not its pitch — and read it
before deciding either way (don't adopt blind, don't dismiss blind).

## L-049: Tight loops are the system; structure alone is inert
Structure (a schema, a vault layout) feels like a system but stays static without
operations running over it. Explicit recurring operations — ingest, query, lint,
reflect — are what make a knowledge base compound. Don't over-automate the capture
step, though: manual processing is where understanding forms; capture fast but
process by hand.

## L-050: A discoverability test decides whether a feature exists
If the operator (or end user) can't find a feature independently — if it needs
explanation to discover, learn, and use — it doesn't exist for them. The right
action is deletion, not documentation. Documenting an undiscoverable feature is
decoration.

## L-051: Design the UI from the machine outward
A good operator UI is a thin face over real handles — files, scripts, pools, logs —
where every control names its backing object and terminal-equivalent command. If a
control can't name what it's backed by, delete it. Show inventory and readiness,
not vanity metrics.

## L-052: Templates and patterns without application are decoration
Extracting a pattern into a template is not implementing it. After creating a
template, apply it to at least a sample of real cases or document why not.
Taxonomy must derive from how the operator actually navigates (by domain, by their
mental model), not from a tool's inherited entity types — the cost of a wrong
taxonomy is re-tagging everything.

## L-053: Closed lanes need a tombstone and a handoff
When a line of work is explicitly closed, write the tombstone in every active
navigation surface (state, goals, priorities, profile) and name which live lane
gets the attention next. Closure without a handoff quietly becomes future drift, as
a later session revives the stale work.
