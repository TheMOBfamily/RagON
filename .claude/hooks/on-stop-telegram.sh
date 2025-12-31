#!/bin/bash
# Hook: Stop - Gửi Telegram khi Claude hoàn thành response
# Non-blocking: chạy background, không ảnh hưởng flow
# Version: 1.1.0 | Created: 2025-12-08 | Updated: 2025-12-08

# Log file for debugging
LOG_FILE="/tmp/claude-stop-hook.log"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "=== Stop hook triggered ==="
log "CLAUDE_PROJECT_DIR: ${CLAUDE_PROJECT_DIR:-'NOT SET'}"
log "PWD: $(pwd)"

# Telegram script path (relative to project)
TELEGRAM_SCRIPT="${CLAUDE_PROJECT_DIR}/.fong/instructions/ftask/telegram.sh"
log "TELEGRAM_SCRIPT: $TELEGRAM_SCRIPT"

# Check file exists
if [[ -f "$TELEGRAM_SCRIPT" ]]; then
    log "Telegram script EXISTS"
    if [[ -x "$TELEGRAM_SCRIPT" ]]; then
        log "Telegram script is EXECUTABLE"
    else
        log "WARNING: Telegram script NOT executable"
    fi
else
    log "WARNING: Telegram script NOT FOUND"
fi

# Non-blocking execution trong subshell
(
    # Check file tồn tại và executable
    if [[ -x "$TELEGRAM_SCRIPT" ]]; then
        PROJECT_NAME=$(basename "${CLAUDE_PROJECT_DIR:-$(pwd)}")
        log "Sending Telegram: done 'Claude đã trả lời xong - ${PROJECT_NAME}'"
        "$TELEGRAM_SCRIPT" done "🔔 Claude đã trả lời xong - ${PROJECT_NAME}" 2>>"$LOG_FILE"
        log "Telegram send result: $?"
    else
        log "Skipped: Telegram script not executable or not found"
    fi
) &

log "=== Stop hook finished (background job started) ==="

# Exit 0 ngay lập tức - không block Claude
exit 0
