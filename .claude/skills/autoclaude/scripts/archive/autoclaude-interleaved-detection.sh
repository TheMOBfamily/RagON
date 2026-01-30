#!/bin/bash
# autoclaude-interleaved-detection.sh
# Chạy xen kẽ: Detection → Adversarial Review (3 iterations mỗi loại)
# Non-blocking, liên tiếp

set -e

# Config
PROJECT_ROOT="/home/fong/Projects/mini-rag"
PROMPTS_DIR="$PROJECT_ROOT/.fong/claude-code-automation/prompts"
MEMORY_DIR="$PROJECT_ROOT/.fong/.memory"
LOG_FILE="$PROJECT_ROOT/.fong/claude-code-automation/logs/interleaved-$(date +%Y%m%d-%H%M%S).log"
AUTOCLAUDE_SCRIPT="$PROJECT_ROOT/.fong/claude-code-automation/scripts/autoclaude-xterm.sh"

# Telegram config
TELEGRAM_TOKEN="8550967390:AAEZcUW78U6QA9CI71YA1eDWTlttkbj4O7M"
TELEGRAM_CHAT_ID="7274005773"

# Create log directory
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$MEMORY_DIR"

# Functions
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

send_telegram() {
    local msg="$1"
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        -d chat_id="${TELEGRAM_CHAT_ID}" \
        -d parse_mode="HTML" \
        -d text="$msg" > /dev/null 2>&1 || true
}

# Generate prompt with iteration number
generate_detection_prompt() {
    local iter=$1
    local prompt_file="$PROMPTS_DIR/prompt-detection-iter${iter}-$(date +%H%M%S).md"
    
    sed "s/{ITERATION}/${iter}/g" "$PROMPTS_DIR/prompt-20251203-211700-detect-papers.md" > "$prompt_file"
    echo "$prompt_file"
}

generate_adversarial_prompt() {
    local iter=$1
    local prev_iter=$((iter))
    local prompt_file="$PROMPTS_DIR/prompt-adversarial-iter${iter}-$(date +%H%M%S).md"
    
    sed -e "s/{ITERATION}/${iter}/g" -e "s/{PREV_ITERATION}/${prev_iter}/g" \
        "$PROMPTS_DIR/prompt-20251203-211800-adversarial-review.md" > "$prompt_file"
    echo "$prompt_file"
}

run_claude() {
    local prompt_file="$1"
    local task_name="$2"
    
    log "🚀 Starting: $task_name"
    log "   Prompt: $prompt_file"
    
    # Read prompt content
    local prompt_content
    prompt_content=$(cat "$prompt_file")
    
    # Run claude (non-blocking with timeout)
    cd "$PROJECT_ROOT/DKM-PDFs"
    timeout 300 claude -p "$prompt_content" --dangerously-skip-permissions 2>&1 | tee -a "$LOG_FILE" || {
        log "⚠️ Task timed out or failed: $task_name"
    }
    
    log "✅ Completed: $task_name"
}

# Main execution
main() {
    log "============================================"
    log "🎯 INTERLEAVED DETECTION + ADVERSARIAL REVIEW"
    log "   Pattern: D1 → A1 → D2 → A2 → D3 → A3"
    log "============================================"
    
    send_telegram "🚀 <b>Autoclaude Interleaved</b>
📋 Task: Paper Detection + Adversarial Review
🔄 Pattern: D1→A1→D2→A2→D3→A3
⏰ Started: $(date '+%H:%M:%S %d/%m')"
    
    # Interleaved loop: 3 iterations
    for i in 1 2 3; do
        log ""
        log "======== ITERATION $i / 3 ========"
        
        # Step 1: Detection
        log "--- Detection Phase $i ---"
        detection_prompt=$(generate_detection_prompt $i)
        run_claude "$detection_prompt" "Detection-Iter$i"
        
        # Small delay
        sleep 5
        
        # Step 2: Adversarial Review
        log "--- Adversarial Review Phase $i ---"
        adversarial_prompt=$(generate_adversarial_prompt $i)
        run_claude "$adversarial_prompt" "Adversarial-Iter$i"
        
        # Delay between iterations
        sleep 10
        
        log "======== ITERATION $i COMPLETE ========"
    done
    
    log ""
    log "============================================"
    log "✅ ALL 6 TASKS COMPLETED"
    log "============================================"
    
    send_telegram "✅ <b>Autoclaude Interleaved Complete</b>
📊 Completed: 6/6 tasks (3 Detection + 3 Adversarial)
📁 Log: $LOG_FILE
⏰ Finished: $(date '+%H:%M:%S %d/%m')"
}

# Entry point
main "$@"
