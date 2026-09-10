---
name: enable-modules
description: "Install/uninstall optional modules listed in modules.yaml. Use when: enable a module, install module, turn on a skill, /enable-modules, prune disabled modules."
version: 1.0
user_invocable: true
---
# /enable-modules — file-based module installer

Reads `modules.yaml` at the vault root and installs every module marked `enabled: true`. Purely mechanical: copy a SKILL.md, make some dirs, copy some seed files. No DB, no registry, no daemons. Re-running is safe (idempotent overwrite).

## Usage
`/enable-modules` — install all `enabled: true` modules
`/enable-modules --prune` — also remove `.claude/skills/<skill>/` for every `enabled: false` module
`/enable-modules --dry-run` — print the plan (what would be copied/made/removed), change nothing

## What a module is
`modules.yaml` lists each module. The manifest **key** (`<name>`) is the source folder `modules/<name>/`; the `skill:` field (`<skill>`) is the install target `.claude/skills/<skill>/` — usually identical. Per entry:
- `enabled` — install it or not
- `skill` — skill name; install target is `.claude/skills/<skill>/`
- `dirs` — vault-relative dirs to create (`mkdir -p`)
- `seeds` — starter files for the module. Each entry is the **vault-relative destination**; the **source** is `modules/<name>/seeds/<basename>`. Copied only if the destination does not already exist (never clobber the user's data); if the source is absent, warn and continue.
- `requires` — a human precondition; print it, don't enforce it

The module's skill body lives at `modules/<name>/SKILL.md` (already sanitized, generic).

## Steps

1. **Read** `modules.yaml`. If absent → tell the user, stop.
2. For each module, decide the action:
   - `enabled: true` → **install**
   - `enabled: false` → skip (or **remove** if `--prune`)
3. **Install** (per enabled module):
   - `mkdir -p .claude/skills/<skill>`
   - copy `modules/<name>/SKILL.md` → `.claude/skills/<skill>/SKILL.md`
   - if `modules/<name>/references/` exists, copy it alongside the SKILL.md
   - `mkdir -p <dir>` for each entry in `dirs`
   - for each `seed` (destination path): source is `modules/<name>/seeds/<basename>`. If the source exists AND the destination does not, `mkdir -p` the dest parent and copy; if the dest already exists, skip (never overwrite user data); if the source is missing, print a one-line warning and continue
   - print the module's `requires` line as a reminder
4. **Prune** (only with `--prune`, per disabled module): `rm -rf .claude/skills/<skill>/`. Never touch `modules/` (that's the source), never touch workspace dirs or seed data the user may have filled in — only the installed skill dir.
5. **Report**: one line per module — `installed | pruned | skipped | already-present` — plus any seed warnings.

## Shell sketch
```bash
ROOT="$(pwd)"          # run from the vault root
# (a tiny yaml read can be done with a few grep/sed lines, or read modules.yaml yourself)
# per enabled module <name>/<skill>:
mkdir -p "$ROOT/.claude/skills/<skill>"
cp "$ROOT/modules/<name>/SKILL.md" "$ROOT/.claude/skills/<skill>/SKILL.md"
[ -d "$ROOT/modules/<name>/references" ] && cp -R "$ROOT/modules/<name>/references" "$ROOT/.claude/skills/<skill>/"
# dirs:
mkdir -p "$ROOT/<dir>"
# seeds (guarded; source = modules/<name>/seeds/<basename>, dest = vault-relative <seed>):
SRC="$ROOT/modules/<name>/seeds/$(basename "<seed>")"
if [ -f "$SRC" ] && [ ! -e "$ROOT/<seed>" ]; then mkdir -p "$(dirname "$ROOT/<seed>")"; cp "$SRC" "$ROOT/<seed>";
elif [ -e "$ROOT/<seed>" ]; then echo "seed dest exists: <seed> (kept user copy)";
else echo "seed source missing: <seed> (skipped)"; fi
# prune:
rm -rf "$ROOT/.claude/skills/<skill>"
```

## Rules
- Idempotent: re-running installs the same files again, no harm.
- File operations only. No DB, no MCP, no network, no daemons.
- Never delete anything outside `.claude/skills/<skill>/` on prune.
- A seed source that's missing is a warning, not a failure — the module still installs.
- `requires` is advisory text — surface it, never block on it.
- A stanza with `enabled: true` but no `skill:` field → warn and skip (never `mkdir` an empty path — that's a silent non-install).
- `--dry-run`: run the decision logic (Steps 1–2) and PRINT the plan only — perform no mkdir/cp/rm.
- Don't edit `modules.yaml` for the user; they flip `enabled:` by hand.
