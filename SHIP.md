# SHIP — build & distribution note

How this Starter was built and how to hand it to someone without leaking your own vault.

## Principle
The live vault is too saturated with personal data to "blank" file-by-file. So the Starter is **author-fresh**: boot files (`CLAUDE.md`, `AGENTS.md`, `README.md`) were rewritten from the principle, not copied. Skills under `.claude/skills/` and `modules/` are **sanitized copies** — same operational logic, every personal reference stripped and replaced with placeholders (`{{owner}}`, `{{partner}}`, `{{app}}`, `{{host}}`, `~/path`).

## Distribute (allowlist, not blocklist)
Never `git init` inside the live vault and `.gitignore` your way to safety — one missed path leaks. Instead, ship **only** an explicit allowlist from a clean tree:

1. Work inside `pos-starter/` (separate from the live vault).
2. Fresh, isolated git history — never reuse the vault's `.git`:
   ```
   cd pos-starter
   rm -rf .git
   git init
   git add CLAUDE.md AGENTS.md README.md SHIP.md \
           context/ knowledge/ state/ daily/ reports/ \
           memory/ modules/ rules/ _templates/ .claude/
   git status            # eyeball the staged list — nothing unexpected
   ```
3. Confirm every staged file is empty/`.gitkeep`/sanitized/author-fresh. If a file isn't on the allowlist, it doesn't ship.

## Leak sweep (run before every handoff)
Build a regex of **your own** forbidden vocabulary, then grep the whole tree for it. **Zero matches required.** Put your real terms in a local file you don't ship — handle, aliases, project codenames, partner/people names, home paths (`/Users/you`, `~/your-workspace`), LAN IPs (`192\.168`, `10\.`), credentials/tokens, bot/chat ids, and any private health/finance facts:

```
cd pos-starter
grep -rinEf ../leak-terms.txt . --exclude-dir=.git
```

`leak-terms.txt` holds one case-insensitive regex per line (e.g. `your-handle`, `/Users/you`, `192\.168`, `secret-project-name`). If grep prints anything, that line is a leak — fix it, re-run, repeat until clean. Keep `leak-terms.txt` outside the shipped tree. `{{placeholder}}` tokens are fine to keep.

Also confirm the engine carries **no module catalog of its own**:
```
ls modules/              # only example-skill/ (the neutral worked example)
grep -nE 'your-module-a|your-module-b|your-module-c' \
  README.md modules.yaml AGENTS.md CLAUDE.md HOME.md SHIP.md docs/architecture.html   # zero hits
#   ^ replace with your own module codenames from leak-terms.txt
```
The engine ships the module *mechanism* + one worked example; your own modules are catalog, not engine.

Also sanity-check the boot file size:
```
wc -c CLAUDE.md          # must stay under 3500 bytes
```

## Not included (intentionally personal — explicit, not silent gaps)
The engine ships the transferable methodology, not the owner's private operating surface. These live-vault systems are deliberately left out — a recipient does not get them:

- **Localhost dashboard** (`dashboard_build.py` / `dashboard_server.py` / `dashboard.html` / `state/dashboard.json`) — the browser task/progress view. The engine ships the plain-text `session-start` summary instead.
- **PM / growth-tracker** (`/pm`, `scripts/progress.py`, `state/board.md`, `progress-log.tsv`) — tracks the OWNER's execution toward THEIR North Star; not universal.
- **recall-eval** — the retrieval-quality harness (MRR / hit@k) tuned to a private Q&A corpus.
- **Personal skills** — `music`, `zh`, `sync-to-*`, `app-reverse`, `tg-deliver`, `morning-brief`, `daily-work`, `ceo-council`, `match-simulator`, `fab-sheet`.
- **Claude Code auto-memory** (`~/.claude/.../memory/`) — a per-user runtime store outside the vault; it cannot travel in git and starts empty on a new machine.

Each is a scoping decision, not a defect. Port a generic version if a recipient needs it.

## Handoff
Once the sweep is clean: `git commit`, then zip or push the `pos-starter/` tree. The recipient unpacks, opens it in Claude Code, and says `start` — the single front door that sets everything up with them (see `README.md`). The vault personalizes itself on their machine — nothing of yours rides along.
