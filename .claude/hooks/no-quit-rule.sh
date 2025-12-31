#!/bin/bash
# PostToolUse Hook: NO-QUIT-RULE reminder
# Location: .claude/hooks/no-quit-rule.sh
# FIX: Use plain text stdout instead of JSON (Claude Code bug #3983)

# === CONFIG ===
ACTIVATED=1
# ACTIVE_PROBABILITY now read from JSON config (default 20 if not found)

# === PATHS ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JSON_FILE="/home/fong/Projects/boiler-plate-cursor-project-with-init-prompt/claude-automation-config/no-quit-rule-config.json"
DEBUG_LOG="${SCRIPT_DIR}/debug.log"

# === DEBUG LOGGING ===
log_debug() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "${DEBUG_LOG}"
}

# === FUNCTIONS ===
get_json_field() {
  local field=$1
  jq -r ".${field}" "${JSON_FILE}" 2>/dev/null
}

# === DEDUPLICATION (Claude Code calls hook twice) ===
LOCK_FILE="/tmp/no-quit-rule-lock"
LOCK_TIMEOUT=2  # seconds

# Use flock for atomic locking (handles parallel calls)
exec 200>"${LOCK_FILE}"
if ! flock -n 200; then
  exit 0  # Another instance is running, skip
fi

# Check timestamp for calls within LOCK_TIMEOUT
LAST_RUN=$(cat "${LOCK_FILE}.ts" 2>/dev/null || echo 0)
NOW=$(date +%s)
DIFF=$((NOW - LAST_RUN))
if [[ $DIFF -lt $LOCK_TIMEOUT ]]; then
  exit 0  # Called too recently, skip
fi

# Update timestamp
echo "${NOW}" > "${LOCK_FILE}.ts"

# === MAIN LOGIC ===
# Read probability from JSON config (default 20 if not found)
if [[ -f "${JSON_FILE}" ]]; then
  ACTIVE_PROBABILITY=$(jq -r '.active.probability // 20' "${JSON_FILE}" 2>/dev/null)
else
  ACTIVE_PROBABILITY=20
fi

log_debug "=== START: ACTIVATED=${ACTIVATED}, PROB=${ACTIVE_PROBABILITY}"

# Exit if not activated
if [[ "${ACTIVATED}" != "1" ]]; then
  log_debug "INACTIVE: exiting"
  exit 0
fi

# Probability check
ROLL=$((RANDOM % 100))
log_debug "ROLL=${ROLL}, THRESHOLD=${ACTIVE_PROBABILITY}"

if [[ $ROLL -ge $ACTIVE_PROBABILITY ]]; then
  log_debug "SKIP: roll >= threshold"
  exit 0
fi

# === BUILD MESSAGE (plain text) ===
# Random: 50% warning, 50% random message
MSG_ROLL=$((RANDOM % 100))

if [[ -f "${JSON_FILE}" ]]; then
  if [[ $MSG_ROLL -lt 50 ]]; then
    MESSAGE=$(get_json_field "active.warning_message")
  else
    COUNT=$(jq -r '.messages | length' "${JSON_FILE}" 2>/dev/null)
    INDEX=$((RANDOM % COUNT))
    MESSAGE=$(jq -r ".messages[${INDEX}]" "${JSON_FILE}" 2>/dev/null)
  fi

  # Get ONE random append_message (not all 3)
  APPEND_COUNT=$(jq -r '.append_messages | length' "${JSON_FILE}" 2>/dev/null)
  if [[ -n "${APPEND_COUNT}" && "${APPEND_COUNT}" != "null" && "${APPEND_COUNT}" -gt 0 ]]; then
    APPEND_INDEX=$((RANDOM % APPEND_COUNT))
    APPEND_MSGS=$(jq -r ".append_messages[${APPEND_INDEX}]" "${JSON_FILE}" 2>/dev/null)
    log_debug "APPEND: selected index ${APPEND_INDEX} of ${APPEND_COUNT}"
  else
    APPEND_MSGS=""
  fi
else
  MESSAGE="NO-QUIT-RULE: Complete ALL tasks until OKR achieved."
  APPEND_MSGS=""
fi

# Fallback
if [[ -z "${MESSAGE}" || "${MESSAGE}" == "null" ]]; then
  MESSAGE="NO-QUIT-RULE: Complete ALL tasks until OKR achieved."
fi

# === OUTPUT JSON (Workaround: decision:block + exit 0) ===
# Per claude-code-guide: decision:"block" with exit 0 shows reason to AI without blocking
log_debug "OUTPUT JSON with decision:block: ${MESSAGE:0:50}..."

# Build full message with append_msgs
FULL_MESSAGE="${MESSAGE}"
if [[ -n "${APPEND_MSGS}" ]]; then
  FULL_MESSAGE="${FULL_MESSAGE}\n\n${APPEND_MSGS}"
fi

# Escape for JSON
ESCAPED_MESSAGE=$(echo -e "${FULL_MESSAGE}" | jq -Rs '.')

# Output JSON - decision:block makes reason visible to AI, exit 0 means don't actually block
# Only use "reason" field (remove additionalContext to avoid duplicate display)
cat << EOF
{
  "decision": "block",
  "reason": ${ESCAPED_MESSAGE}
}
EOF

exit 0
