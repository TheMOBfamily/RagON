#!/bin/bash
# PostToolUse Hook: MCP RAG Query Reminder
# Matcher: mcp__.*

# Deduplication
LOCK_FILE="/tmp/post-tool-mcp-lock"
exec 200>"${LOCK_FILE}"
flock -n 200 || exit 0
LAST_RUN=$(cat "${LOCK_FILE}.ts" 2>/dev/null || echo 0)
NOW=$(date +%s)
[[ $((NOW - LAST_RUN)) -lt 2 ]] && exit 0

# Trigger probability (20% = optimal spaced repetition)
TRIGGER_PERCENT=20
[[ $((RANDOM % 100)) -ge $TRIGGER_PERCENT ]] && exit 0

# Only update timestamp AFTER passing probability check
echo "${NOW}" > "${LOCK_FILE}.ts"

# Message
MESSAGE="RAG PATTERN: Query → <thinking> → Work → Query (if needed). NEVER batch queries. Interleave: 1 query → analyze → do work → query again only if gaps found."

cat << EOF
{
  "decision": "block",
  "reason": "${MESSAGE}"
}
EOF

exit 0
