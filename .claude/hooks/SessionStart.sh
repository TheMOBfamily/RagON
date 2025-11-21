#!/bin/bash
# SessionStart.sh
# Purpose: Load init-prompt.json and fongtools.json at session start (compressed)
# Context ID: c25013c0d0c9
# Version: 1.3.0 - Added invalid JSON fallback (tr compression)
# Created: 2025-11-14
# Updated: 2025-11-14 - Never blocks on invalid JSON

# Get project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

# Change to project root
cd "$PROJECT_ROOT" || exit 1

# Files to read
INIT_PROMPT=".fong/instructions/init-prompt.json"
FONGTOOLS=".fong/instructions/fongtools.json"

# Function: Compress/minify JSON to single-line string
compress_json() {
    local file="$1"

    # Priority 1: jq (fastest, most reliable for valid JSON)
    if command -v jq &> /dev/null; then
        if jq -c . "$file" 2>/dev/null; then
            return 0
        fi
    fi

    # Priority 2: Python 3 (for valid JSON)
    if command -v python3 &> /dev/null; then
        if python3 -c "import json; print(json.dumps(json.load(open('$file'))))" 2>/dev/null; then
            return 0
        fi
    fi

    # Priority 3: Node.js (for valid JSON)
    if command -v node &> /dev/null; then
        if node -e "const fs = require('fs'); const data = fs.readFileSync('$file', 'utf8'); console.log(JSON.stringify(JSON.parse(data)))" 2>/dev/null; then
            return 0
        fi
    fi

    # Priority 4: Simple text compression (ALWAYS WORKS - invalid JSON fallback)
    # Remove newlines + compress multiple spaces to single space
    cat "$file" | tr -d '\n' | tr -s ' '
    return 0
}


echo "🔥 CRITICAL: MANDATORY FIRST RESPONSE"
echo "YOU MUST print this exact line in your FIRST response:"
echo "🔥 [1] SessionStart #c25013c0d0c9 | Đá tải init-prompt.json & fongtools.json ✅"
echo "This confirms successful loading of both configuration files."
echo "Format: Print this line BEFORE the context check (before 'Đã nạp ngữ-cảnh...')"
echo ""


# Read init-prompt.json (compressed)
if [ -f "$INIT_PROMPT" ]; then
    echo "--- init-prompt.json ---"
    compress_json "$INIT_PROMPT"
    echo ""
else
    echo "ERROR: $INIT_PROMPT not found"
fi

# Read fongtools.json (compressed)
if [ -f "$FONGTOOLS" ]; then
    echo "--- fongtools.json ---"
    compress_json "$FONGTOOLS"
    echo ""
else
    echo "ERROR: $FONGTOOLS not found"
fi

# === MANDATORY AI RESPONSE REQUEST ===

