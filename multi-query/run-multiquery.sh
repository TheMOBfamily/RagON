#!/bin/bash
# Helper script to run multi-query RAG system
# Usage: ./run-multiquery.sh "Your question here" [options]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load environment from .env (portable)
source "$SCRIPT_DIR/../load-env.sh"

# Activate venv
activate_venv || exit 1

# Run main script
cd "$SCRIPT_DIR"
python main-d1f454371402.py "$@"