#!/bin/bash
# autoclaude-batch.sh - Batch run multiple prompts with delay
# Usage: ./autoclaude-batch.sh prompts/ [--delay 60] [--cheap|--haiku]
# Default: opus (CLI default). --cheap or --haiku = haiku.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUNNER="${SCRIPT_DIR}/autoclaude-runner.sh"

# === CONFIG ===
DELAY=60  # seconds between runs
MODEL=""  # empty = opus (CLI default)

# === PARSE ARGS ===
PROMPTS_DIR=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --delay)
            DELAY="$2"
            shift 2
            ;;
        --cheap|--haiku)
            MODEL="haiku"
            shift
            ;;
        *)
            PROMPTS_DIR="$1"
            shift
            ;;
    esac
done

if [[ -z "$PROMPTS_DIR" || ! -d "$PROMPTS_DIR" ]]; then
    echo "Usage: $0 <prompts_directory> [--delay 60] [--cheap]"
    echo "Default: opus (CLI default). --cheap = haiku."
    exit 1
fi

# === MAIN ===
echo "=== Batch Runner ==="
echo "Directory: $PROMPTS_DIR"
echo "Delay: ${DELAY}s"
echo "Model: ${MODEL:-opus (default)}"
echo "===================="

COUNT=0
for prompt_file in "$PROMPTS_DIR"/prompt-*.txt; do
    if [[ -f "$prompt_file" ]]; then
        COUNT=$((COUNT + 1))
        echo ""
        echo ">>> Running [$COUNT]: $(basename "$prompt_file")"

        if [[ -n "$MODEL" ]]; then
            "$RUNNER" --file "$prompt_file" --cheap
        else
            "$RUNNER" --file "$prompt_file"
        fi

        echo ">>> Waiting ${DELAY}s before next..."
        sleep "$DELAY"
    fi
done

echo ""
echo "=== Batch Complete: $COUNT prompts ==="
