#!/bin/bash
# init.sh - Entry point for Python analysis pipeline
# Usage: ./init.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Python Analysis Pipeline ==="
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"

# Run scripts in order
for script in src/[0-9][0-9]_*.py; do
  if [[ -f "$script" ]]; then
    echo "→ Running: $script"
    python3 "$script"
  fi
done

echo "=== Done: $(date '+%Y-%m-%d %H:%M:%S') ==="
echo "Check output/ for results."
