#!/usr/bin/env bash
# Installs the optional search-by-meaning (Python environment + model + index).
# Called from onboarding (/start) — no need to run it by hand.
# Safe to re-run: the environment and the index are rebuilt from scratch, and the
# person's own notes are never touched.
#
# No error here may break onboarding: any failure = one plain line and exit 0.
# Everything else works without search by meaning.
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 0

if ! command -v python3 >/dev/null 2>&1; then
  echo "There is no Python on this computer, so search by meaning doesn't work yet."
  echo "Everything else works: notes are searched by exact words."
  echo "If you want it later — install Python 3 and type: /start"
  exit 0
fi

echo "-> Setting up search by meaning. One time only, about 300 MB to download."
if ! bash scripts/memory_index_setup.sh >/dev/null 2>&1; then
  echo "Could not set up search by meaning — there seem to be no ready-made parts for this Python version."
  echo "Everything else works: notes are searched by exact words. We can come back to this later."
  exit 0
fi

echo "-> Reading the folder and building the index over your notes..."
if ! .memory_venv/bin/python scripts/memory_index.py build >/dev/null 2>&1; then
  echo "The index could not be built — most likely the model didn't finish downloading."
  echo "Everything else works: notes are searched by exact words. To try again: /start"
  exit 0
fi

echo "Done: notes are now found by meaning, not only by exact words."
