#!/bin/bash
# PostToolUse Hook: MCP File Analyzer + Large File Warning
# Matcher: Read
# Version: 3.1.0 - Both checks run (LOC + MCP type)

# === CONFIG ===
# Evidence-based thresholds (2025-12-16):
# - Clean Code/Uncle Bob: avg 50 LOC, max 100, largest 200-500 LOC
# - Claude context: 200k tokens ≈ 50k-100k LOC (4 tokens/LOC)
# - Ref: Obsidian note "2025-12-16 Optimal LOC Threshold Research"
LOC_THRESHOLD=500
WINDOW_PERCENT=15
TRIGGER_PERCENT=100  # 100% for code files, change to 20 for production

# === DEBUG ===
DEBUG_LOG="/tmp/post-tool-read-debug.log"
INPUT=$(cat)
echo "$(date '+%Y-%m-%d %H:%M:%S') INPUT: $INPUT" >> "$DEBUG_LOG"

# === PARSE JSON ===
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
echo "$(date '+%Y-%m-%d %H:%M:%S') FILE_PATH: $FILE_PATH" >> "$DEBUG_LOG"

[[ -z "$FILE_PATH" ]] && exit 0
[[ ! -f "$FILE_PATH" ]] && exit 0

# === COLLECT MESSAGES (both checks run) ===
MESSAGES=""

# --- CHECK 1: Large file ---
LOC=$(wc -l < "$FILE_PATH" 2>/dev/null || echo 0)
if [[ "$LOC" -gt "$LOC_THRESHOLD" ]]; then
    WINDOW_LINES=$((LOC * WINDOW_PERCENT / 100))
    [[ "$WINDOW_LINES" -lt 150 ]] && WINDOW_LINES=150
    echo "$(date '+%Y-%m-%d %H:%M:%S') LARGE_FILE: $LOC LOC" >> "$DEBUG_LOG"
    MESSAGES+="LARGE_FILE: ${LOC} LOC. Recommend read 200 LOC/chunk + 15% sliding window overlap. Or sed/awk or grep for targeted search."
fi

# --- CHECK 2: Code file MCP suggestion ---
if [[ "$FILE_PATH" =~ \.(php|js|ts|tsx|py)$ ]]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') MATCHED CODE: $FILE_PATH" >> "$DEBUG_LOG"

    # Deduplication
    LOCK_FILE="/tmp/post-tool-read-lock"
    exec 200>"${LOCK_FILE}"
    flock -n 200 || exit 0
    LAST_RUN=$(cat "${LOCK_FILE}.ts" 2>/dev/null || echo 0)
    NOW=$(date +%s)
    [[ $((NOW - LAST_RUN)) -lt 2 ]] && exit 0
    echo "${NOW}" > "${LOCK_FILE}.ts"

    # Trigger probability
    [[ $((RANDOM % 100)) -ge $TRIGGER_PERCENT ]] && exit 0

    # MCP tool suggestion
    EXT="${FILE_PATH##*.}"
    case "$EXT" in
        php) MCP_TOOL="mcp__ts-php-reader__analyzePHPFile" ;;
        js|ts|tsx) MCP_TOOL="mcp__ts-ts-js-reader__analyzeTSJSFile" ;;
        py) MCP_TOOL="mcp__ts-py-reader__analyzePythonFile" ;;
    esac

    [[ -n "$MESSAGES" ]] && MESSAGES+=" | "
    MESSAGES+="Use $MCP_TOOL for .$EXT (dependency analysis, imports/exports)."
    echo "$(date '+%Y-%m-%d %H:%M:%S') MCP_SUGGESTION: $MCP_TOOL" >> "$DEBUG_LOG"
fi

# === OUTPUT ===
if [[ -n "$MESSAGES" ]]; then
    cat << EOF
{
  "decision": "block",
  "reason": "$MESSAGES"
}
EOF
fi

exit 0
