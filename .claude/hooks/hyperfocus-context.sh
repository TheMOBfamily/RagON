#!/bin/bash
# hyperfocus-context-collector.sh
# Purpose: Collect comprehensive context data for hyperfocus.json initialization
# Version: 1.6.1 - Parameterized INIT_PROMPT_PATH
# Updated: 2025-11-16

# Debug log file (relative to script location)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEBUG_LOG="$SCRIPT_DIR/debug.log"

# Init prompt path (parameterized)
INIT_PROMPT_PATH="/home/fong/Projects/boiler-plate-cursor-project-with-init-prompt/.fong/init-prompt.md"

# Log function
log_debug() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$DEBUG_LOG"
}

log_debug "=== Script started ==="
log_debug "CLAUDE_PROJECT_DIR: ${CLAUDE_PROJECT_DIR:-'(not set)'}"

# Change to project root - Fallback to script location
if [ -n "$CLAUDE_PROJECT_DIR" ]; then
    PROJECT_ROOT="$CLAUDE_PROJECT_DIR"
    log_debug "Using CLAUDE_PROJECT_DIR: $PROJECT_ROOT"
else
    # Fallback: Detect script directory and go up 2 levels (.claude/hooks → project root)
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
    log_debug "CLAUDE_PROJECT_DIR not set, using fallback"
    log_debug "SCRIPT_DIR: $SCRIPT_DIR"
    log_debug "PROJECT_ROOT (fallback): $PROJECT_ROOT"
fi

cd "$PROJECT_ROOT" || {
    log_debug "ERROR: Cannot cd to PROJECT_ROOT: $PROJECT_ROOT"
    exit 1
}

log_debug "Successfully cd to PROJECT_ROOT: $PROJECT_ROOT"
log_debug "Current directory: $(pwd)"

# 1. Current timestamp
NOW=$(date '+%Y-%m-%d %H:%M:%S %Z (%a)')
log_debug "NOW: $NOW"

# 2. Current git branch
BRANCH=$(git branch --show-current 2>&1)
if [ $? -ne 0 ]; then
    log_debug "ERROR: git branch failed: $BRANCH"
    BRANCH="(not a git repo)"
fi
log_debug "BRANCH: $BRANCH"

# 3. 15 most recent .memory files (by mtime)
RECENT_15=$(ls -t .fong/.memory/*.{md,json} 2>/dev/null | head -15 | xargs -n1 basename | tr '\n' ',' | sed 's/,$//')
log_debug "RECENT_15 count: $(echo "$RECENT_15" | grep -o ',' | wc -l)"

# 4. 9 most recent SOURCE files in codebase (include .md, .json, .php, .js; exclude backups, logs)
RECENT_CRU_9=$(find . -type f \
  \( -name '*.php' -o -name '*.js' -o -name '*.md' -o -name '*.json' \) \
  -not -path './.git/*' \
  -not -name '*.log' \
  -not -name '*.jsonl' \
  -not -name '*.b' \
  -not -name '*.bak' \
  -not -name '*.backup' \
  -not -name '*~' \
  -printf '%T@ %p\n' 2>/dev/null \
  | sort -rn \
  | head -9 \
  | awk '{print $2}' \
  | sed 's|^\./||' \
  | tr '\n' ',' \
  | sed 's/,$//')
log_debug "RECENT_CRU_9 count: $(echo "$RECENT_CRU_9" | grep -o ',' | wc -l)"

# Output pipe-separated (4 fields only)
echo "Auto Kick-off Context 00ef3b0a066f -- NOW: $NOW | BRANCH: $BRANCH | RECENT 15 MEMORY FILES: $RECENT_15 | RECENT 9 CRU-files: $RECENT_CRU_9"

# Print init-prompt.md content (compact: remove blank lines + squeeze spaces)
if [ -f "$INIT_PROMPT_PATH" ]; then
  log_debug "Found init-prompt.md, printing content (compact mode)"
  echo ""
  echo "--- INIT PROMPT INSTRUCTIONS ---"
  cat "$INIT_PROMPT_PATH" | grep -v '^$' | tr -s ' '
  echo ""
  echo "--- END INIT PROMPT ---"
else
  log_debug "WARNING: init-prompt.md not found at $INIT_PROMPT_PATH"
fi

log_debug "=== Script completed successfully ==="
