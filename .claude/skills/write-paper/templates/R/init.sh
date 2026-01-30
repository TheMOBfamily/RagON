#!/bin/bash
# init.sh - Entry point for R analysis pipeline
# Usage: ./init.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "=== R Analysis Pipeline ==="
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"

# Run scripts in order
for script in src/[0-9][0-9]-*.R; do
  if [[ -f "$script" ]]; then
    echo "→ Running: $script"
    Rscript "$script"
  fi
done

echo "=== Done: $(date '+%Y-%m-%d %H:%M:%S') ==="
echo "Check output/ for results."
