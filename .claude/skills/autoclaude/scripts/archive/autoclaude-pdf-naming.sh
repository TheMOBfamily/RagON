#!/bin/bash
# PDF Naming Stateless Runner for autoclaude
# Usage: ./autoclaude-pdf-naming.sh [count]
# Default: Run 10 iterations (50 files total)

set -e
cd /home/fong/Projects/mini-rag

COUNT=${1:-10}
PROMPT_FILE=".fong/claude-code-automation/prompts/prompt-20251203-214500-pdf-naming-stateless.md"
LOG_DIR=".fong/claude-code-automation/logs"

mkdir -p "$LOG_DIR"

echo "=== PDF Naming Autoclaude Runner ==="
echo "Iterations: $COUNT"
echo "Batch size: 5 files per iteration"
echo "Total files to process: $((COUNT * 5))"
echo ""

for i in $(seq 1 $COUNT); do
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    echo "[$i/$COUNT] Starting iteration at $TIMESTAMP..."

    # Check remaining files
    REMAINING=$(cd DKM-PDFs && ls -1 *.PDF 2>/dev/null | grep -vP '^[0-9]{4}-ISBN-[0-9-]+-' | wc -l)
    echo "  Remaining files: $REMAINING"

    if [ "$REMAINING" -eq 0 ]; then
        echo "All files processed!"
        break
    fi

    # Run autoclaude with haiku
    .fong/claude-code-automation/scripts/autoclaude-xterm.sh \
        "$(cat $PROMPT_FILE)" \
        --model haiku \
        --count 1 \
        2>&1 | tee "$LOG_DIR/pdf-naming-$TIMESTAMP.log"

    echo "  Iteration $i complete"
    sleep 5
done

echo ""
echo "=== Summary ==="
echo "Processed logs: $LOG_DIR"
echo "Progress: $(wc -l < .fong/.memory/pdf-naming-progress.log) entries"
