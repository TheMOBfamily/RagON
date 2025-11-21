#!/bin/bash
# Helper script to run multi-query RAG system
# Usage: ./run-multiquery.sh "Your question here" [options]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="/home/fong/Projects/mini-rag/venv"

# Activate venv
if [ ! -d "$VENV_PATH" ]; then
    echo "Error: venv not found at $VENV_PATH"
    exit 1
fi

source "$VENV_PATH/bin/activate"

# Run main script
cd "$SCRIPT_DIR"
python main-d1f454371402.py "$@"