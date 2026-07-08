#!/bin/bash
# Create/recreate the runtime venv for the memory embedding layer.
#
# The venv is gitignored (~1 GB) and may vanish (a cleanup, a python upgrade) —
# that loses NO data (nodes.npz + the model cache stay intact), only the runtime.
# Recreate it any time with: bash scripts/memory_index_setup.sh
#
# Path-agnostic: resolves the vault root from this script's own location, so it
# works from any fresh clone. Override the venv dir with MEMORY_VENV if you like.
set -e

# Vault root = the parent of the scripts/ directory that holds this file.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
cd "$ROOT"

VENV="${MEMORY_VENV:-.memory_venv}"

python3 -m venv "$VENV"
"$VENV/bin/pip" install -q --upgrade pip
# prod (the memory_index.py engine):
"$VENV/bin/pip" install -q numpy onnxruntime transformers huggingface_hub sentencepiece

echo "OK — venv ready at $VENV. The model downloads itself on the first"
echo "     build/search (cached under ~/.cache/huggingface)."
