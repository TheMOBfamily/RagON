#!/usr/bin/env bash
# Wrapper to build TOC indexes.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV="$ROOT_DIR/venv"
if [ -d "$VENV" ]; then
  source "$VENV/bin/activate"
fi
python "$ROOT_DIR/tools/build_toc_index.py" "$@"