#!/bin/bash
# PostToolUse Hook: LOC & Principles Reminder + Large File Warning
# Matcher: Write
# Version: 2.0.0

# === CONFIG ===
RATE=10           # Percentage for general reminder (1-100)
LOC_THRESHOLD=300 # Files > this LOC get sliding window suggestion
WINDOW_PERCENT=5  # Sliding window percentage

# === READ STDIN ===
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

# Exit if no file path or file doesn't exist
[[ -z "$FILE_PATH" ]] && exit 0
[[ ! -f "$FILE_PATH" ]] && exit 0

# === CHECK LOC FOR LARGE FILES ===
LOC=$(wc -l < "$FILE_PATH" 2>/dev/null || echo 0)

if [[ "$LOC" -gt "$LOC_THRESHOLD" ]]; then
    WINDOW_LINES=$((LOC * WINDOW_PERCENT / 100))
    [[ "$WINDOW_LINES" -lt 20 ]] && WINDOW_LINES=20

    cat << EOF
{
  "decision": "block",
  "reason": "LARGE_FILE: $FILE_PATH has $LOC LOC (>$LOC_THRESHOLD). For precise reading, use sliding window ${WINDOW_PERCENT}% (~${WINDOW_LINES} lines): sed -n '1,${WINDOW_LINES}p' file | Then sed -n '${WINDOW_LINES},$((WINDOW_LINES*2))p' etc. Or use awk/grep for targeted search."
}
EOF
    exit 0
fi

# === GENERAL REMINDER (RATE%) ===
[[ $((RANDOM % 100)) -ge $RATE ]] && exit 0

cat << 'EOF'
{
  "decision": "block",
  "reason": "CODE_REMINDER: Function/Logic <100 LOC, Class <150 LOC (excluding docs/comments). Principles: SOLID (SRP), KISS, DRY, SSoT, YAGNI. Extensions: .php .js .jsx .ts .tsx .py"
}
EOF

exit 0
