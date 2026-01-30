#!/bin/bash
# PostToolUse Hook: MCP Tools Handler
# Matcher: mcp__.*

# Read stdin (JSON with tool info)
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

# ==========================================
# PATTERN 1: TS Reader Tools → Graph Debug
# ==========================================
if [[ "$TOOL_NAME" =~ ts.*reader ]] || [[ "$TOOL_NAME" =~ ts-php-reader ]] || [[ "$TOOL_NAME" =~ ts-ts-js-reader ]] || [[ "$TOOL_NAME" =~ ts-py-reader ]]; then
  cat << 'EOF'
{
  "decision": "block",
  "reason": "GRAPH DEBUG: MCP reader depth=5. Cần sâu hơn? Gọi standalone .sh với depth=10.\nPath: /home/fong/Projects/graph-file-tree/graph-*.sh\nSyntax: graph-*.sh <file.*> --scope <project_root> --depth 10\nVariants: graph-php.sh | graph-py.sh | graph-ts.sh | graph-js.sh\nDocs: .fong/instructions/instructions-debug-file-tree-graph.json"
}
EOF
  exit 0
fi

# ==========================================
# PATTERN 2: RAG Query Reminder (20% chance)
# ==========================================
# Deduplication
LOCK_FILE="/tmp/post-tool-mcp-lock"
exec 200>"${LOCK_FILE}"
flock -n 200 || exit 0
LAST_RUN=$(cat "${LOCK_FILE}.ts" 2>/dev/null || echo 0)
NOW=$(date +%s)
[[ $((NOW - LAST_RUN)) -lt 2 ]] && exit 0

# Trigger probability (20%)
TRIGGER_PERCENT=20
[[ $((RANDOM % 100)) -ge $TRIGGER_PERCENT ]] && exit 0

echo "${NOW}" > "${LOCK_FILE}.ts"

cat << 'EOF'
{
  "decision": "block",
  "reason": "RAG PATTERN: Query → <thinking> → Work → Query (if needed). NEVER batch queries. Interleave: 1 query → analyze → do work → query again only if gaps found."
}
EOF

exit 0
