#!/bin/bash
# autoclaude-oneshot.sh - One-shot Claude CLI execution
# Single prompt, single run, no loop, no init file.
#
# Usage:
#   ./autoclaude-oneshot.sh "your prompt" [flags]
#   ./autoclaude-oneshot.sh -f prompt.md [flags]
#
# Flags:
#   --cheap|--haiku    Haiku model (default: opus)
#   --raw              No prefix/suffix wrapping (direct prompt)
#   --max-time N       Timeout seconds (default: 600)
#   -f|--file FILE     Read prompt from file
#   --no-telegram      Skip Telegram notifications
#   --save             Save prompt to prompts/ folder
#
# Examples:
#   ./autoclaude-oneshot.sh "Check PHP files for SQL injection"
#   ./autoclaude-oneshot.sh "Fix login bug" --cheap --max-time 300
#   ./autoclaude-oneshot.sh -f task.md --raw

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/../config.json"
PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"

# === CLEANUP TRAP ===
STDOUT_FILE=""
STDERR_FILE=""
cleanup() {
    rm -f "$STDOUT_FILE" "$STDERR_FILE"
}
trap cleanup EXIT INT TERM

# === LOAD CONFIG (SSoT) ===
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "ERROR: config.json not found at $CONFIG_FILE"
    exit 1
fi

TOKEN=$(jq -r '.telegram.token' "$CONFIG_FILE")
CHAT_ID=$(jq -r '.telegram.chat_id' "$CONFIG_FILE")
PROMPT_PREFIX=$(jq -r '.prompt_prefix' "$CONFIG_FILE")
PROMPT_SUFFIX=$(jq -r '.prompt_suffix // ""' "$CONFIG_FILE")
USE_VERBOSE=$(jq -r '.claude_flags.verbose' "$CONFIG_FILE")
USE_SKIP_PERMS=$(jq -r '.claude_flags.dangerously_skip_permissions' "$CONFIG_FILE")

# === HELPERS ===
get_vn_time() {
    TZ='Asia/Ho_Chi_Minh' date '+%Y-%m-%d %H:%M:%S'
}

send_telegram() {
    local message="$1"
    [[ "$NO_TELEGRAM" == "true" ]] && return
    curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
        -d chat_id="${CHAT_ID}" \
        -d text="${message}" \
        -d parse_mode="HTML" > /dev/null 2>&1
}

# === PARSE ARGS ===
PROMPT_TEXT=""
PROMPT_FILE=""
MODEL=""
MAX_TIME=600
RAW_MODE=false
NO_TELEGRAM=false
SAVE_PROMPT=false

POSITIONAL_COUNT=0
while [[ $# -gt 0 ]]; do
    case $1 in
        --cheap|--haiku) MODEL="haiku"; shift ;;
        --raw) RAW_MODE=true; shift ;;
        --max-time|-t) MAX_TIME="$2"; shift 2 ;;
        -f|--file) PROMPT_FILE="$2"; shift 2 ;;
        --no-telegram) NO_TELEGRAM=true; shift ;;
        --save) SAVE_PROMPT=true; shift ;;
        *)
            POSITIONAL_COUNT=$((POSITIONAL_COUNT + 1))
            if [[ $POSITIONAL_COUNT -eq 1 ]]; then
                PROMPT_TEXT="$1"
            fi
            shift
            ;;
    esac
done

# === VALIDATE INPUT ===
if [[ -z "$PROMPT_TEXT" && -z "$PROMPT_FILE" ]]; then
    echo "autoclaude-oneshot.sh - One-shot Claude CLI execution"
    echo ""
    echo "Usage:"
    echo "  $0 \"prompt text\" [flags]"
    echo "  $0 -f prompt.md [flags]"
    echo ""
    echo "Flags:"
    echo "  --cheap|--haiku    Haiku model (default: opus)"
    echo "  --raw              No prefix/suffix wrapping"
    echo "  --max-time N       Timeout seconds (default: 600)"
    echo "  -f|--file FILE     Read prompt from file"
    echo "  --no-telegram      Skip Telegram notifications"
    echo "  --save             Save prompt to prompts/ folder"
    echo ""
    echo "Examples:"
    echo "  $0 \"Check PHP files for SQL injection\""
    echo "  $0 \"Fix login bug\" --cheap --max-time 300"
    echo "  $0 -f task.md --raw --no-telegram"
    exit 1
fi

# === READ PROMPT FROM FILE ===
if [[ -n "$PROMPT_FILE" ]]; then
    if [[ ! -f "$PROMPT_FILE" ]]; then
        echo "ERROR: File not found: $PROMPT_FILE"
        exit 1
    fi
    PROMPT_TEXT=$(cat "$PROMPT_FILE")
fi

# === BUILD PROMPT ===
if [[ "$RAW_MODE" == "true" ]]; then
    FULL_PROMPT="$PROMPT_TEXT"
else
    FULL_PROMPT="${PROMPT_PREFIX}

USER REQUEST: ${PROMPT_TEXT}

${PROMPT_SUFFIX}"
fi

# === BUILD CLAUDE FLAGS (array to avoid word-splitting) ===
CLAUDE_FLAGS=(-p)
[[ "$USE_VERBOSE" == "true" ]] && CLAUDE_FLAGS+=("--verbose")
[[ "$USE_SKIP_PERMS" == "true" ]] && CLAUDE_FLAGS+=("--dangerously-skip-permissions")
[[ -n "$MODEL" ]] && CLAUDE_FLAGS+=("--model" "$MODEL")

# === SAVE PROMPT (optional) ===
if [[ "$SAVE_PROMPT" == "true" ]]; then
    PROMPTS_DIR="${PROJECT_DIR}/.fong/claude-code-automation/prompts"
    mkdir -p "$PROMPTS_DIR"
    PROMPT_DATE=$(TZ='Asia/Ho_Chi_Minh' date '+%Y%m%d-%H%M%S')
    PROMPT_UUID=$(uuidgen | head -c 8)
    SAVED_FILE="${PROMPTS_DIR}/oneshot-${PROMPT_DATE}-${PROMPT_UUID}.md"
    echo "$FULL_PROMPT" > "$SAVED_FILE"
    echo ">>> Prompt saved: $SAVED_FILE"
fi

# === NOTIFY START ===
START_TIME=$(get_vn_time)
PROMPT_SHORT="${PROMPT_TEXT:0:100}"
send_telegram "[${START_TIME}] 🎯 <b>ONE-SHOT</b>: ${MODEL:-opus}
${PROMPT_SHORT}..."

# === RUN CLAUDE ===
echo "╔═══════════════════════════════════════════╗"
echo "║  🎯 ONE-SHOT | ${MODEL:-opus} | max ${MAX_TIME}s"
echo "║  Raw: ${RAW_MODE} | Telegram: $([[ "$NO_TELEGRAM" == "true" ]] && echo "off" || echo "on")"
echo "║  Prompt: ${PROMPT_SHORT}..."
echo "╚═══════════════════════════════════════════╝"

cd "$PROJECT_DIR"

STDOUT_FILE="/tmp/claude_oneshot_$$.txt"
STDERR_FILE="/tmp/claude_oneshot_stderr_$$.txt"

set +e
timeout --signal=SIGTERM --kill-after=30 "$MAX_TIME" \
    claude "${CLAUDE_FLAGS[@]}" "$FULL_PROMPT" 2> "$STDERR_FILE" | tee "$STDOUT_FILE"
EXIT_CODE=${PIPESTATUS[0]}
set -e

# === HANDLE RESULTS ===
OUTPUT_SIZE=$(wc -c < "$STDOUT_FILE" 2>/dev/null || echo 0)
END_TIME=$(get_vn_time)

if [[ $EXIT_CODE -eq 124 ]]; then
    send_telegram "[${END_TIME}] ⚠️ <b>TIMEOUT</b>: Exceeded ${MAX_TIME}s"
elif [[ $EXIT_CODE -eq 0 ]]; then
    OUTPUT_SHORT=$(head -c 200 "$STDOUT_FILE")
    send_telegram "[${END_TIME}] ✅ <b>ONE-SHOT DONE</b>: ${OUTPUT_SIZE} bytes
${OUTPUT_SHORT}..."
else
    STDERR_SHORT=$(head -c 200 "$STDERR_FILE")
    send_telegram "[${END_TIME}] ❌ <b>ONE-SHOT FAILED</b> (exit ${EXIT_CODE})
${STDERR_SHORT}"
fi

echo ""
echo ">>> ONE-SHOT complete (exit: ${EXIT_CODE})"
