#!/bin/bash
# PostToolUse Hook: TypeScript Type Checking
# Matcher: Edit, Write
# Version: 1.0.0
# Updated: 2026-01-08
# Purpose: Run tsc --noEmit after editing .ts/.tsx files to catch type errors

# === CONFIG ===
# Timeout for tsc (seconds) - prevent hanging
TSC_TIMEOUT=30

# === READ STDIN ===
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

# Exit if no file path
[[ -z "$FILE_PATH" ]] && exit 0

# Get file extension
EXT="${FILE_PATH##*.}"

# Only check .ts files (not .tsx)
case "$EXT" in
    ts) ;;
    *) exit 0 ;;
esac

# === DETERMINE PROJECT ROOT ===
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$FILE_PATH")" && git rev-parse --show-toplevel 2>/dev/null)}"
[[ -z "$PROJECT_ROOT" ]] && exit 0

# === DETERMINE WHICH TSCONFIG TO USE ===
# NestJS files (src/) may need different config
if [[ "$FILE_PATH" == *"/src/"* ]]; then
    # Check if tsconfig.nest.json exists
    if [[ -f "$PROJECT_ROOT/tsconfig.nest.json" ]]; then
        TSCONFIG="$PROJECT_ROOT/tsconfig.nest.json"
    else
        TSCONFIG="$PROJECT_ROOT/tsconfig.json"
    fi
else
    TSCONFIG="$PROJECT_ROOT/tsconfig.json"
fi

# Exit if no tsconfig found
[[ ! -f "$TSCONFIG" ]] && exit 0

# === RUN TYPE CHECK ===
cd "$PROJECT_ROOT" || exit 0

# Run tsc with timeout
TSC_OUTPUT=$(timeout "${TSC_TIMEOUT}s" npx tsc --noEmit -p "$TSCONFIG" 2>&1)
TSC_EXIT=$?

# If timeout
if [[ $TSC_EXIT -eq 124 ]]; then
    cat << EOF
{
  "decision": "block",
  "reason": "⏱️ TypeScript check timeout (>${TSC_TIMEOUT}s). Run manually: npx tsc --noEmit"
}
EOF
    exit 0
fi

# If type errors found
if [[ $TSC_EXIT -ne 0 && -n "$TSC_OUTPUT" ]]; then
    # Count errors
    ERROR_COUNT=$(echo "$TSC_OUTPUT" | grep -c "error TS")

    # Get first 5 errors for display
    FIRST_ERRORS=$(echo "$TSC_OUTPUT" | grep "error TS" | head -5)

    # Escape for JSON
    ESCAPED_ERRORS=$(echo "$FIRST_ERRORS" | jq -Rs '.')

    cat << EOF
{
  "decision": "block",
  "reason": "❌ TypeScript: ${ERROR_COUNT} type error(s) found. Fix before proceeding.\n\nFirst errors:\n${FIRST_ERRORS}\n\nRun: npx tsc --noEmit"
}
EOF
    exit 0
fi

# All good - no output needed
exit 0
