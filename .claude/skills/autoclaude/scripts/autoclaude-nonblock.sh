#!/bin/bash
# autoclaude-nonblock.sh - Open gnome-terminal to run autoclaude-block.sh (non-blocking)
# Usage: ./autoclaude-nonblock.sh "/abs/path/to/init-autoclaude.json" 30 [--cheap|--haiku]
# Args: $1 = init file path, $2 = count, [--cheap] = use haiku model
# Default: opus (CLI default). Use --cheap or --haiku for haiku (cost-saving).
# CRITICAL: Always verify terminal is running after launch!

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BLOCK_SCRIPT="${SCRIPT_DIR}/autoclaude-block.sh"
PROJECT_DIR="$(pwd)"
SESSIONS_DIR="${SCRIPT_DIR}/sessions"

# Set DISPLAY for X11 (required when running from non-GUI context)
export DISPLAY="${DISPLAY:-:0}"

# Generate SESSION_ID here for terminal title (block script will use same format)
SESSION_DATE=$(TZ='Asia/Ho_Chi_Minh' date '+%Y%m%d-%H%M%S')
SESSION_UUID=$(uuidgen | head -c 4)
SESSION_ID="${SESSION_DATE}-${SESSION_UUID}"

# Build full command with proper quoting
CMD="${BLOCK_SCRIPT}"
for arg in "$@"; do
    CMD="$CMD $(printf '%q' "$arg")"
done

# Export PROJECT_DIR for block script
export PROJECT_DIR

# Spawn gnome-terminal with SESSION_ID in title
gnome-terminal --title="🤖 AC: ${SESSION_ID}" -- bash -c "cd '$PROJECT_DIR' && $CMD; echo 'Press Enter to close...'; read" &
TERM_PID=$!

# CRITICAL: Wait and verify terminal is actually running
sleep 2
if ps -p $TERM_PID > /dev/null 2>&1 || pgrep -f "autoclaude-block" > /dev/null; then
    echo "╔═══════════════════════════════════════════════════════╗"
    echo "║  🚀 LAUNCHED: ${SESSION_ID}  "
    echo "╠═══════════════════════════════════════════════════════╣"
    echo "║  Terminal PID: $TERM_PID"
    echo "╠═══════════════════════════════════════════════════════╣"
    echo "║  📋 List sessions:  ls ${SESSIONS_DIR}/"
    echo "║  📊 Monitor:        tail -f ${SCRIPT_DIR}/debug.log"
    echo "║  🛑 Kill this:      ${SCRIPT_DIR}/kill-stop-autoclaude.sh ${SESSION_ID}"
    echo "║  🛑 Kill all:       ${SCRIPT_DIR}/kill-stop-autoclaude.sh"
    echo "╚═══════════════════════════════════════════════════════╝"
else
    echo "ERROR: Terminal failed to start or exited immediately!"
    echo "Check: ${SCRIPT_DIR}/debug.log"
    exit 1
fi
