#!/bin/bash
# list-sessions.sh - List all running autoclaude sessions
# Usage: ./list-sessions.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SESSIONS_DIR="${SCRIPT_DIR}/sessions"

echo "╔═══════════════════════════════════════════════════════╗"
echo "║  📋 AUTOCLAUDE SESSIONS                               ║"
echo "╠═══════════════════════════════════════════════════════╣"

if [[ ! -d "$SESSIONS_DIR" ]] || [[ -z "$(ls -A "$SESSIONS_DIR" 2>/dev/null)" ]]; then
    echo "║  ⚪ No active sessions                                ║"
    echo "╚═══════════════════════════════════════════════════════╝"
    exit 0
fi

for session_file in "$SESSIONS_DIR"/*.session; do
    [[ -f "$session_file" ]] || continue

    # Read session info
    source "$session_file"

    # Check if still running
    if kill -0 "$PID" 2>/dev/null; then
        STATUS="🟢 RUNNING"
    else
        STATUS="🔴 DEAD"
    fi

    echo "║  $STATUS"
    echo "║  🆔 ${SESSION_ID}"
    echo "║  📁 ${PROJECT_DIR##*/}"
    echo "║  ⏰ ${START_TIME}"
    echo "║  PID: ${PID}"
    echo "╠═══════════════════════════════════════════════════════╣"
done

echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "Commands:"
echo "  Kill specific: ./kill-stop-autoclaude.sh <SESSION_ID>"
echo "  Kill all:      ./kill-stop-autoclaude.sh"
