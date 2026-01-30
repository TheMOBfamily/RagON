#!/bin/bash
# PostToolUse Hook: LOC Limit Enforcement
# Matcher: Write
# Version: 3.0.0
# Updated: 2026-01-03

# === CONFIG ===
LOC_LIMIT_PHP=150
LOC_LIMIT_DEFAULT=100
LARGE_FILE_THRESHOLD=300

# === READ STDIN ===
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

# Exit if no file path or file doesn't exist
[[ -z "$FILE_PATH" ]] && exit 0
[[ ! -f "$FILE_PATH" ]] && exit 0

# Get file extension
EXT="${FILE_PATH##*.}"

# Skip non-code files
case "$EXT" in
    php|js|jsx|ts|tsx|py) ;;
    *) exit 0 ;;
esac

# === COUNT LOC ===
LOC=$(wc -l < "$FILE_PATH" 2>/dev/null || echo 0)

# === DETERMINE LIMIT ===
if [[ "$EXT" == "php" ]]; then
    LIMIT=$LOC_LIMIT_PHP
else
    LIMIT=$LOC_LIMIT_DEFAULT
fi

# === CHECK VIOLATION ===
if [[ "$LOC" -gt "$LIMIT" ]]; then
    FILENAME=$(basename "$FILE_PATH")

    if [[ "$LOC" -gt "$LARGE_FILE_THRESHOLD" ]]; then
        # Large file: sliding window suggestion
        WINDOW=$((LOC / 10))
        [[ "$WINDOW" -lt 30 ]] && WINDOW=30
        cat << EOF
{
  "decision": "block",
  "reason": "LOC_VIOLATION: $FILENAME has $LOC LOC (limit: $LIMIT for .$EXT). LARGE FILE detected. Split into modules. Use sliding window (~$WINDOW lines) for reading. BEFORE write: \`smart search\` for existing utils/helpers/classes. Reuse > Reinvent. DRY: No duplicate logic. No hardcoding: extract constants. SOLID/SRP: 1 unit = 1 responsibility. Ref: CLAUDE.md"
}
EOF
    else
        cat << EOF
{
  "decision": "block",
  "reason": "LOC_VIOLATION: $FILENAME has $LOC LOC (limit: $LIMIT for .$EXT). Modularize now. BEFORE write: \`smart search\` for existing utils/helpers/classes. Reuse > Reinvent. DRY: No duplicate logic. No hardcoding: extract constants. SOLID/SRP/KISS/DRY/SSoT/YAGNI. Ref: CLAUDE.md"
}
EOF
    fi
    exit 0
fi

exit 0
