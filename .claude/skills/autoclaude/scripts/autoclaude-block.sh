#!/bin/bash
# autoclaude-block.sh - Run Claude with init file path N times (blocking mode)
# Usage: ./autoclaude-block.sh "/abs/path/to/init-autoclaude.json" 30 [--cheap|--haiku]
# Args: $1 = init file path, $2 = count, [--cheap] = use haiku model
# Default: opus (CLI default). Use --cheap or --haiku for haiku (cost-saving).

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/../config.json"
# PROJECT_DIR: từ env variable hoặc pwd (KHÔNG hardcode)
PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"

# === SESSION ID (Unique identifier for this autoclaude instance) ===
# Format: YYYYMMDD-HHMMSS-uuid4 (e.g., 20251230-234500-a1b2)
# Used for: terminal title, logs, telegram, kill by ID
SESSION_DATE=$(TZ='Asia/Ho_Chi_Minh' date '+%Y%m%d-%H%M%S')
SESSION_UUID=$(uuidgen | head -c 4)
SESSION_ID="${SESSION_DATE}-${SESSION_UUID}"

# === SESSIONS DIR (Track running instances) ===
SESSIONS_DIR="${SCRIPT_DIR}/sessions"
mkdir -p "$SESSIONS_DIR"
SESSION_FILE="${SESSIONS_DIR}/${SESSION_ID}.session"

# === DEBUG LOG (HARDCODED) ===
DEBUG_LOG="${SCRIPT_DIR}/debug.log"
log_debug() {
    local msg="$1"
    local timestamp=$(TZ='Asia/Ho_Chi_Minh' date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] ${msg}" >> "$DEBUG_LOG"
    echo "[DEBUG] ${msg}"
}

# Clear old log on start
echo "=== NEW SESSION: ${SESSION_ID} ===" > "$DEBUG_LOG"
log_debug "🆔 SESSION_ID: $SESSION_ID"
log_debug "Script started"
log_debug "SCRIPT_DIR: $SCRIPT_DIR"
log_debug "CONFIG_FILE: $CONFIG_FILE"

# === CREATE SESSION FILE (for tracking and kill by ID) ===
cat > "$SESSION_FILE" << EOF
SESSION_ID=${SESSION_ID}
PID=$$
START_TIME=$(TZ='Asia/Ho_Chi_Minh' date '+%Y-%m-%d %H:%M:%S')
PROJECT_DIR=${PROJECT_DIR}
EOF
log_debug "Session file created: $SESSION_FILE"

# === LOAD CONFIG (SSoT) ===
TOKEN=$(jq -r '.telegram.token' "$CONFIG_FILE")
CHAT_ID=$(jq -r '.telegram.chat_id' "$CONFIG_FILE")
PROMPT_PREFIX=$(jq -r '.prompt_prefix' "$CONFIG_FILE")
PROMPT_SUFFIX=$(jq -r '.prompt_suffix // ""' "$CONFIG_FILE")
USE_VERBOSE=$(jq -r '.claude_flags.verbose' "$CONFIG_FILE")
USE_SKIP_PERMS=$(jq -r '.claude_flags.dangerously_skip_permissions' "$CONFIG_FILE")
AUTO_CLOSE_DELAY=$(jq -r '.xterm.auto_close_delay // 5' "$CONFIG_FILE")

log_debug "Config loaded: USE_VERBOSE=$USE_VERBOSE, USE_SKIP_PERMS=$USE_SKIP_PERMS"

# === PROMPTS DIR ===
# FIX: Prompts phải trong PROJECT_DIR, không phải SCRIPT_DIR
# Mỗi dự án có prompts folder riêng
PROMPTS_DIR="${PROJECT_DIR}/.fong/claude-code-automation/prompts"
mkdir -p "$PROMPTS_DIR"

# === HELPERS ===
get_vn_time() {
    TZ='Asia/Ho_Chi_Minh' date '+%Y-%m-%d %H:%M:%S'
}

send_telegram() {
    local message="$1"
    curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
        -d chat_id="${CHAT_ID}" \
        -d text="${message}" \
        -d parse_mode="HTML" > /dev/null 2>&1
}

# === PARSE ARGS ===
# Usage: ./autoclaude-block.sh "/path/to/init.json" 30 [--cheap] [--max-time 600]
INIT_FILE_PATH=""
COUNT=1
MODEL=""
DELAY=5
TASK_SUMMARY=""
MAX_TIME=600  # Default 10 phút (600 giây) - MANDATORY timeout để tránh hang

# === EXPONENTIAL BACKOFF RETRY CONFIG ===
# Delays: 30s x3, then 60s, 120s, 180s (max 3 min)
# Rationale: Empty output rarely recovers after 3min. Avoid wasting time.
# Test mode: 1s, 2s, 3s (for quick verification)
RETRY_DELAYS=(30 30 30 60 120 180)
RETRY_DELAYS_TEST=(1 2 3)
MIN_OUTPUT_SIZE=50  # Minimum bytes to consider valid output
TEST_MODE=false
MOCK_EMPTY=false  # Simulate empty output for testing retry

# Retry function with exponential backoff
run_claude_with_retry() {
    local prompt_content="$1"
    local stdout_file="$2"
    local stderr_file="$3"
    local attempt=0
    local max_attempts=${#RETRY_DELAYS[@]}

    while true; do
        # Mock mode: simulate empty output for testing (last attempt returns valid output)
        if [[ "$MOCK_EMPTY" == "true" ]]; then
            if [[ $attempt -lt $((max_attempts - 1)) ]]; then
                log_debug "🧪 MOCK MODE: Simulating empty output (attempt $attempt)"
                echo -n "" > "$stdout_file"
            else
                log_debug "🧪 MOCK MODE: Last attempt - returning valid output"
                echo "MOCK SUCCESS: Retry mechanism works! All $max_attempts attempts completed." > "$stdout_file"
            fi
            echo -n "" > "$stderr_file"
            local exit_code=0
        else
            # Real Claude call
            timeout --signal=SIGTERM --kill-after=30 "$MAX_TIME" claude $CLAUDE_FLAGS "$prompt_content" 2> "$stderr_file" | tee "$stdout_file"
            local exit_code=$?
        fi
        local output_size=$(wc -c < "$stdout_file" 2>/dev/null || echo 0)

        # Check if output is valid
        if [[ $output_size -ge $MIN_OUTPUT_SIZE ]]; then
            log_debug "✅ Valid output received (${output_size} bytes)"
            return $exit_code
        fi

        # Empty/short output detected
        if [[ $attempt -ge $max_attempts ]]; then
            log_debug "❌ All ${max_attempts} retries exhausted. Continuing with empty output."
            send_telegram "[$(get_vn_time)] ❌ <b>RETRY EXHAUSTED</b>: ${max_attempts} attempts failed. Continuing..."
            return $exit_code
        fi

        local delay=${RETRY_DELAYS[$attempt]}
        local delay_human=""
        if [[ $delay -ge 3600 ]]; then
            delay_human="$((delay/3600))h"
        elif [[ $delay -ge 60 ]]; then
            delay_human="$((delay/60))m"
        else
            delay_human="${delay}s"
        fi

        attempt=$((attempt + 1))
        log_debug "⚠️ Empty output (${output_size} bytes). Retry ${attempt}/${max_attempts} in ${delay_human}..."
        send_telegram "[$(get_vn_time)] 🔄 <b>RETRY ${attempt}/${max_attempts}</b>: Empty output. Waiting ${delay_human}..."

        sleep "$delay"
    done
}

# First positional = init file path
# Second positional = count
# Rest = flags
POSITIONAL_COUNT=0
while [[ $# -gt 0 ]]; do
    case $1 in
        --cheap|--haiku) MODEL="haiku"; shift ;;
        --delay|-d) DELAY="$2"; shift 2 ;;
        --summary|-s) TASK_SUMMARY="$2"; shift 2 ;;
        --max-time|-t) MAX_TIME="$2"; shift 2 ;;
        --test-retry) TEST_MODE=true; RETRY_DELAYS=("${RETRY_DELAYS_TEST[@]}"); shift ;;
        --mock-empty) MOCK_EMPTY=true; shift ;;
        *)
            POSITIONAL_COUNT=$((POSITIONAL_COUNT + 1))
            if [[ $POSITIONAL_COUNT -eq 1 ]]; then
                INIT_FILE_PATH="$1"
            elif [[ $POSITIONAL_COUNT -eq 2 ]]; then
                COUNT="$1"
            fi
            shift
            ;;
    esac
done

log_debug "Args parsed: INIT_FILE_PATH=$INIT_FILE_PATH, COUNT=$COUNT, MODEL=$MODEL, DELAY=$DELAY, MAX_TIME=$MAX_TIME"

# === LOAD PROMPT TEMPLATE ===
PROMPT_TEMPLATE_FILE="${SCRIPT_DIR}/start-prompt.md"
if [[ ! -f "$PROMPT_TEMPLATE_FILE" ]]; then
    echo "ERROR: start-prompt.md not found at $PROMPT_TEMPLATE_FILE"
    exit 1
fi

if [[ -z "$INIT_FILE_PATH" ]]; then
    echo "Usage: $0 \"/abs/path/to/init-autoclaude.json\" 30 [--cheap] [--delay 5]"
    echo "Args: \$1 = init file path, \$2 = count"
    echo "Default: opus (CLI default). --cheap = haiku."
    exit 1
fi

# Read template and substitute {INIT_FILE_PATH}
PROMPT_TEMPLATE=$(cat "$PROMPT_TEMPLATE_FILE")
PROMPT="${PROMPT_TEMPLATE//\{INIT_FILE_PATH\}/$INIT_FILE_PATH}"

log_debug "PROMPT length: ${#PROMPT} chars"

# === BUILD CLAUDE FLAGS ===
CLAUDE_FLAGS="-p"
[[ "$USE_VERBOSE" == "true" ]] && CLAUDE_FLAGS="$CLAUDE_FLAGS --verbose"
[[ "$USE_SKIP_PERMS" == "true" ]] && CLAUDE_FLAGS="$CLAUDE_FLAGS --dangerously-skip-permissions"
[[ -n "$MODEL" ]] && CLAUDE_FLAGS="$CLAUDE_FLAGS --model $MODEL"

log_debug "CLAUDE_FLAGS: $CLAUDE_FLAGS"
log_debug "MODEL: ${MODEL:-'(default=opus)'}"

# === BUILD FULL PROMPT (PREFIX + USER + SUFFIX) ===
FULL_PROMPT="${PROMPT_PREFIX}

USER REQUEST: ${PROMPT}

${PROMPT_SUFFIX}"

# Task summary: use init file basename if not provided
INIT_BASENAME=$(basename "$INIT_FILE_PATH")
TASK_SUMMARY="${TASK_SUMMARY:-${INIT_BASENAME}}"

# === WRITE PROMPT TO FILE (fix stuck issue) ===
# Naming: prompt-YYYYMMDD-HHMMSS-{uuid8}.md
PROMPT_DATE=$(TZ='Asia/Ho_Chi_Minh' date '+%Y%m%d-%H%M%S')
PROMPT_UUID=$(uuidgen | head -c 8)
PROMPT_FILE="${PROMPTS_DIR}/prompt-${PROMPT_DATE}-${PROMPT_UUID}.md"
echo "$FULL_PROMPT" > "$PROMPT_FILE"
echo ">>> Prompt saved to: $PROMPT_FILE"
log_debug "Prompt file created: $PROMPT_FILE"
log_debug "Prompt file size: $(wc -c < "$PROMPT_FILE") bytes"

# === MAIN LOOP ===
START_TIME=$(get_vn_time)
send_telegram "[${START_TIME}] 🚀 <b>BẮT ĐẦU</b> [<code>${SESSION_ID}</code>]
${COUNT}x ${MODEL:-opus} | ${TASK_SUMMARY}"

echo "╔═══════════════════════════════════════════╗"
echo "║  🆔 SESSION: ${SESSION_ID}  "
echo "╠═══════════════════════════════════════════╣"
echo "║  Count: ${COUNT} | Model: ${MODEL:-opus} | Delay: ${DELAY}s"
echo "║  Flags: ${CLAUDE_FLAGS}"
echo "╚═══════════════════════════════════════════╝"

cd "$PROJECT_DIR"
log_debug "Changed to PROJECT_DIR: $PROJECT_DIR"

for ((i=1; i<=COUNT; i++)); do
    ITER_TIME=$(get_vn_time)
    echo ""
    echo ">>> Iteration ${i}/${COUNT} [${ITER_TIME}]"
    log_debug "=== ITERATION ${i}/${COUNT} START ==="

    send_telegram "[${ITER_TIME}] ⏳ <b>Run ${i}/${COUNT}</b>: ${TASK_SUMMARY}"

    # === RUN CLAUDE WITH DETAILED DEBUG ===
    # FIX: Prompt must be passed as argument, NOT piped via stdin
    PROMPT_CONTENT="$(cat "$PROMPT_FILE")"
    log_debug "Running: claude $CLAUDE_FLAGS \"<prompt>\" (${#PROMPT_CONTENT} chars)"

    # Capture stdout, stderr, and exit code separately
    STDOUT_FILE="/tmp/claude_stdout_$$_${i}.txt"
    STDERR_FILE="/tmp/claude_stderr_$$_${i}.txt"

    log_debug "STDOUT_FILE: $STDOUT_FILE"
    log_debug "STDERR_FILE: $STDERR_FILE"

    # Run Claude with exponential backoff retry
    # Handles: empty output, rate limits, network glitches
    set +e
    run_claude_with_retry "$PROMPT_CONTENT" "$STDOUT_FILE" "$STDERR_FILE"
    EXIT_CODE=$?
    set -e

    # Handle timeout exit code (124 = timeout, 137 = killed after grace period)
    if [[ $EXIT_CODE -eq 124 ]]; then
        log_debug "⚠️ TIMEOUT: Claude exceeded ${MAX_TIME}s limit"
        send_telegram "[$(get_vn_time)] ⚠️ <b>TIMEOUT</b> Run ${i}/${COUNT}: Exceeded ${MAX_TIME}s"
    elif [[ $EXIT_CODE -eq 137 ]]; then
        log_debug "⚠️ FORCE KILLED: Claude didn't respond to SIGTERM"
        send_telegram "[$(get_vn_time)] ⚠️ <b>FORCE KILLED</b> Run ${i}/${COUNT}"
    fi

    log_debug "Claude EXIT_CODE: $EXIT_CODE"
    log_debug "STDOUT size: $(wc -c < "$STDOUT_FILE") bytes"
    log_debug "STDERR size: $(wc -c < "$STDERR_FILE") bytes"

    # Log first 500 chars of each
    log_debug "STDOUT (first 500): $(head -c 500 "$STDOUT_FILE")"
    log_debug "STDERR (first 500): $(head -c 500 "$STDERR_FILE")"

    # Combine for OUTPUT
    OUTPUT=$(cat "$STDOUT_FILE")
    STDERR_CONTENT=$(cat "$STDERR_FILE")

    if [[ -n "$STDERR_CONTENT" ]]; then
        log_debug "STDERR not empty, appending to output"
        OUTPUT="${OUTPUT}
[STDERR]: ${STDERR_CONTENT}"
    fi

    OUTPUT_SHORT="${OUTPUT:0:200}"
    ITER_END=$(get_vn_time)
    send_telegram "[${ITER_END}] ✅ <b>Done ${i}/${COUNT}</b>
Output: ${OUTPUT_SHORT}..."

    echo "Output: ${OUTPUT}"
    log_debug "=== ITERATION ${i}/${COUNT} END ==="

    # Cleanup temp files
    rm -f "$STDOUT_FILE" "$STDERR_FILE"

    [[ $i -lt $COUNT ]] && sleep "$DELAY"
done

END_TIME=$(get_vn_time)
send_telegram "[${END_TIME}] 🎉 <b>HOÀN THÀNH</b> [<code>${SESSION_ID}</code>]
${COUNT}x ${MODEL:-opus} | ${TASK_SUMMARY}"

log_debug "=== LOOP COMPLETE ==="

# === CLEANUP SESSION FILE ===
rm -f "$SESSION_FILE"
log_debug "Session file removed: $SESSION_FILE"

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║  ✅ LOOP COMPLETE: ${SESSION_ID}  "
echo "╚═══════════════════════════════════════════╝"
echo ">>> Debug log: $DEBUG_LOG"
echo ">>> Closing in ${AUTO_CLOSE_DELAY}s..."
sleep "$AUTO_CLOSE_DELAY"
