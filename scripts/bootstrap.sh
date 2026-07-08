#!/usr/bin/env bash
# One-shot setup of the optional semantic-memory engine (venv + model + index).
# Run by the /start onboarding — a user never needs to call this by hand.
# Safe to re-run: the venv and index rebuild cleanly; your notes are never touched.
set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."

if ! command -v python3 >/dev/null 2>&1; then
  echo "⚠  Python 3 isn't installed, so semantic memory (finding notes by meaning) is off for now."
  echo "   Everything else works — the graph just falls back to plain text search."
  echo "   To enable it later: install Python 3 (python.org or your package manager), then say: start"
  exit 0
fi

echo "→ Setting up your memory engine (one-time, ~1–2 min, all local)…"
bash scripts/memory_index_setup.sh

echo "→ Reading your vault and building the memory index…"
.memory_venv/bin/python scripts/memory_index.py build

echo "✓ Memory ready — /recall now finds notes by meaning, not just keywords."
