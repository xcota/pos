---
name: example-skill
description: "Example module showing the format. Use when: testing /enable-modules, learning to author a module."
version: 1.0
user_invocable: true
---

# /example-skill — example module

This is a **worked example** of a module — the smallest thing that plugs into the engine. Copy this folder to `modules/<yourname>/`, edit it, add a stanza in `modules.yaml`, then run `/enable-modules` to install it. Delete or replace this example whenever you like.

## What a module is
A directory under `modules/` with:
- `SKILL.md` (required) — a normal skill with frontmatter (`name`, `description`, `version`, `user_invocable`).
- `seeds/` (optional) — starter files copied into your vault on enable.
- `references/` (optional) — extra files installed alongside the skill.
Plus one stanza in `modules.yaml` declaring `enabled / skill / dirs / seeds / requires`.

## /example-skill
Greet `{{user}}` and read the starter note at `reports/example-note.md` (seeded on enable). That's it — proof the mechanism works. Replace this with whatever your module actually does.

Mechanism only. No DB, no network, no daemons — just files.
