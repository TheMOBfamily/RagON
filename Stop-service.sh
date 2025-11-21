#!/bin/bash
# Stop RagON Tunnel ONLY (keeps Flask API running)

TUNNEL_PID_FILE="/tmp/ragon-tunnel.pid"
TUNNEL_URL_FILE="/tmp/ragon-tunnel-url.txt"

echo "=========================================="
echo "  Stop RagON Tunnel"
echo "=========================================="
echo ""

# Stop tunnel by PID file
if [ -f "$TUNNEL_PID_FILE" ]; then
    TUNNEL_PID=$(cat "$TUNNEL_PID_FILE")
    if kill -0 "$TUNNEL_PID" 2>/dev/null; then
        echo "Stopping tunnel (PID: $TUNNEL_PID)..."
        kill "$TUNNEL_PID"
        echo "Tunnel stopped."
    else
        echo "Tunnel process not running."
    fi
    rm -f "$TUNNEL_PID_FILE"
else
    # Fallback: kill all cloudflared
    if pgrep -x cloudflared > /dev/null; then
        echo "Stopping cloudflared processes..."
        pkill cloudflared
        echo "Done."
    else
        echo "No tunnel running."
    fi
fi

# Cleanup URL file
rm -f "$TUNNEL_URL_FILE"

echo ""
echo "Flask API still running on localhost:1411"
echo "To access locally: curl http://localhost:1411/"
echo ""
