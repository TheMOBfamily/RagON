#!/bin/bash
# =============================================================================
# kill-stop-autoclaude.sh - Stop autoclaude processes (by SESSION_ID or all)
# Usage: ./kill-stop-autoclaude.sh [SESSION_ID]
#   - No args: Kill ALL autoclaude processes
#   - With SESSION_ID: Kill only that specific session
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SESSIONS_DIR="${SCRIPT_DIR}/sessions"
SESSION_ID="$1"

# === SELF-PROTECTION ===
CURRENT_PID=$$
PARENT_PID=$PPID
GRANDPARENT_PID=$(ps -o ppid= -p $PPID 2>/dev/null | tr -d ' ')

# Helper: Kill processes matching pattern, excluding protected PIDs
safe_pkill() {
    local pattern="$1"
    local desc="$2"

    local pids=$(pgrep -f "$pattern" 2>/dev/null || true)
    local killed=0

    for pid in $pids; do
        if [[ "$pid" == "$CURRENT_PID" || "$pid" == "$PARENT_PID" || "$pid" == "$GRANDPARENT_PID" ]]; then
            echo "  🛡️ Skipping protected PID $pid"
            continue
        fi
        kill "$pid" 2>/dev/null && killed=$((killed + 1))
    done

    if [[ $killed -gt 0 ]]; then
        echo "  ✅ Killed $killed $desc"
    else
        echo "  ⚪ No $desc found"
    fi
}

# === KILL BY SESSION_ID ===
if [[ -n "$SESSION_ID" ]]; then
    echo "🎯 Killing session: ${SESSION_ID}"

    SESSION_FILE="${SESSIONS_DIR}/${SESSION_ID}.session"

    if [[ -f "$SESSION_FILE" ]]; then
        # Read PID from session file
        source "$SESSION_FILE"

        if [[ -n "$PID" ]]; then
            echo "  Found PID: $PID"

            # Kill the process and its children
            if kill -0 "$PID" 2>/dev/null; then
                pkill -P "$PID" 2>/dev/null || true
                kill "$PID" 2>/dev/null || true
                echo "  ✅ Killed session $SESSION_ID (PID: $PID)"
            else
                echo "  ⚠️ Process $PID not running"
            fi

            # Remove session file
            rm -f "$SESSION_FILE"
            echo "  🗑️ Removed session file"
        fi
    else
        echo "  ⚠️ Session file not found: $SESSION_FILE"
        echo ""
        echo "  📋 Available sessions:"
        ls -1 "$SESSIONS_DIR"/*.session 2>/dev/null | while read f; do
            basename "$f" .session
        done
    fi

    exit 0
fi

# === KILL ALL (no SESSION_ID provided) ===
echo "🛑 Stopping ALL autoclaude processes..."
echo "   (Protected PIDs: $$, $PPID, $GRANDPARENT_PID)"

# 1. Kill terminal windows
echo "[1/4] Killing terminal autoclaude windows..."
safe_pkill "gnome-terminal.*autoclaude" "gnome-terminal windows"

# 2. Kill autoclaude scripts
echo "[2/4] Killing autoclaude scripts..."
safe_pkill "autoclaude-block.sh" "autoclaude-block.sh"
safe_pkill "autoclaude-nonblock.sh" "autoclaude-nonblock.sh"

# 3. Kill legacy scripts
echo "[3/4] Killing legacy scripts..."
safe_pkill "autoclaude-loop.sh" "autoclaude-loop.sh"

# 4. Kill claude CLI
echo "[4/4] Killing claude CLI processes..."
safe_pkill "claude.*dangerously-skip-permissions" "claude CLI"

# 5. Cleanup all session files
echo "[5/5] Cleaning up session files..."
rm -f "$SESSIONS_DIR"/*.session 2>/dev/null && echo "  ✅ Session files cleaned" || echo "  ⚪ No session files"

# Wait and verify
sleep 1
echo ""
echo "📊 Verification:"
remaining=$(ps aux | grep -E "(autoclaude)" | grep -v grep | wc -l)
if [ "$remaining" -eq 0 ]; then
    echo "✅ All autoclaude processes stopped!"
else
    echo "⚠️  $remaining process(es) still running:"
    ps aux | grep -E "(autoclaude)" | grep -v grep
    echo ""
    echo "💡 Force kill: pkill -9 -f autoclaude"
fi

echo ""
echo "Done."
