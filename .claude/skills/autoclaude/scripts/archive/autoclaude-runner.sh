#!/bin/bash
# autoclaude-runner.sh - Claude Code automation with Telegram notification
# Usage: ./autoclaude-runner.sh "prompt" [--cheap|--haiku]
# Default: opus (CLI default). Use --cheap or --haiku for haiku.

set -e

# === CONFIG ===
TOKEN="8550967390:AAEZcUW78U6QA9CI71YA1eDWTlttkbj4O7M"
CHAT_ID="7274005773"
# PROJECT_DIR: từ env variable hoặc pwd (KHÔNG hardcode)
PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"
# Model: empty = opus (CLI default), "haiku" = cheap mode
MODEL=""

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
PROMPT=""
PROMPT_FILE=""
TASK_SUMMARY=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --cheap|--haiku)
            MODEL="haiku"
            shift
            ;;
        --file)
            PROMPT_FILE="$2"
            shift 2
            ;;
        --summary)
            TASK_SUMMARY="$2"
            shift 2
            ;;
        *)
            PROMPT="$1"
            shift
            ;;
    esac
done

# Load from file if specified
if [[ -n "$PROMPT_FILE" && -f "$PROMPT_FILE" ]]; then
    PROMPT=$(cat "$PROMPT_FILE")
    TASK_SUMMARY="${TASK_SUMMARY:-$(basename "$PROMPT_FILE" .txt)}"
fi

# Validate
if [[ -z "$PROMPT" ]]; then
    echo "Usage: $0 \"prompt\" [--cheap] [--summary \"task desc\"]"
    echo "       $0 --file prompt.txt [--cheap]"
    echo "Default: opus (CLI default). --cheap = haiku."
    exit 1
fi

# Auto-generate summary if not provided (first 50 chars)
TASK_SUMMARY="${TASK_SUMMARY:-${PROMPT:0:50}...}"

# === MAIN ===
START_TIME=$(get_vn_time)

# Notify START
send_telegram "[${START_TIME}] 🚀 <b>BẮT ĐẦU</b>: ${TASK_SUMMARY}"

echo "=== Claude Code Automation ==="
echo "Time: ${START_TIME}"
echo "Model: ${MODEL:-opus (default)}"
echo "Summary: ${TASK_SUMMARY}"
echo "=============================="

# Run Claude
cd "$PROJECT_DIR"
if [[ -n "$MODEL" ]]; then
    OUTPUT=$(claude -p "$PROMPT" --model "$MODEL" 2>&1) || true
else
    OUTPUT=$(claude -p "$PROMPT" 2>&1) || true
fi

END_TIME=$(get_vn_time)

# Determine status
if [[ $? -eq 0 ]]; then
    STATUS="✅ HOÀN THÀNH"
else
    STATUS="❌ LỖI"
fi

# Notify END
send_telegram "[${END_TIME}] ${STATUS}: ${TASK_SUMMARY}"

echo ""
echo "=== OUTPUT ==="
echo "$OUTPUT"
echo "=============="
echo ""
echo "[${END_TIME}] ${STATUS}"
