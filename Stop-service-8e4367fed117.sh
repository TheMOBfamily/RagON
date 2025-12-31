#!/bin/bash
# Stop RagON Service - ID: 8e4367fed117
# Commands:
#   (no args)     : Stop service completely
#   --block-lan   : Block LAN access (service keeps running)
#   --allow-lan   : Allow LAN access (service keeps running)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ID="8e4367fed117"
PORT="${PORT:-1411}"
TUNNEL_PID_FILE="/tmp/ragon-tunnel-$PROJECT_ID.pid"
TUNNEL_URL_FILE="/tmp/ragon-tunnel-$PROJECT_ID-url.txt"
API_PID_FILE="/tmp/ragon-api-$PROJECT_ID.pid"

# Parse port from positional arg
for arg in "$@"; do
    case $arg in
        [0-9]*)
            PORT="$arg"
            ;;
    esac
done

# LAN control functions (requires sudo)
block_lan() {
    echo "=========================================="
    echo "  Block LAN Access [$PROJECT_ID]"
    echo "=========================================="
    sudo iptables -D INPUT -p tcp --dport "$PORT" ! -s 127.0.0.1 -j DROP 2>/dev/null
    sudo iptables -I INPUT -p tcp --dport "$PORT" ! -s 127.0.0.1 -j DROP 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "LAN access BLOCKED on port $PORT"
        echo "localhost still works: http://localhost:$PORT"
        echo ""
        echo "To allow LAN: $0 --allow-lan"
    else
        echo "ERROR: Need sudo permission"
    fi
    exit 0
}

allow_lan() {
    LAN_IP=$(hostname -I | awk '{print $1}')
    echo "=========================================="
    echo "  Allow LAN Access [$PROJECT_ID]"
    echo "=========================================="
    sudo iptables -D INPUT -p tcp --dport "$PORT" ! -s 127.0.0.1 -j DROP 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "LAN access ALLOWED on port $PORT"
    else
        echo "No block rule found (LAN already allowed)"
    fi
    echo ""
    echo "Access URLs:"
    echo "  Local: http://localhost:$PORT"
    echo "  LAN:   http://$LAN_IP:$PORT"
    echo ""
    echo "To block LAN: $0 --block-lan"
    exit 0
}

# Handle LAN control commands first
for arg in "$@"; do
    case $arg in
        --block-lan)
            block_lan
            ;;
        --allow-lan)
            allow_lan
            ;;
    esac
done

# Default: Stop service
echo "=========================================="
echo "  Stop RagON Service [$PROJECT_ID]"
echo "=========================================="
echo ""

# Stop API server by PID file first
if [ -f "$API_PID_FILE" ]; then
    API_PID=$(cat "$API_PID_FILE")
    if kill -0 "$API_PID" 2>/dev/null; then
        echo "Stopping API server (PID: $API_PID, port: $PORT)..."
        kill "$API_PID" 2>/dev/null
        sleep 1
        # Force kill if still running
        kill -9 "$API_PID" 2>/dev/null
        echo "API server stopped."
    else
        echo "API process not running (stale PID file)."
    fi
    rm -f "$API_PID_FILE"
fi

# Fallback: Kill by port (only THIS project's port)
if lsof -i ":$PORT" > /dev/null 2>&1; then
    echo "Killing process on port $PORT..."
    # Get PID and kill only uvicorn/python processes
    PIDS=$(lsof -ti ":$PORT" 2>/dev/null)
    for pid in $PIDS; do
        PROC_NAME=$(ps -p "$pid" -o comm= 2>/dev/null)
        if [[ "$PROC_NAME" == "python"* ]] || [[ "$PROC_NAME" == "uvicorn"* ]]; then
            kill "$pid" 2>/dev/null
            echo "Killed $PROC_NAME (PID: $pid)"
        fi
    done
fi

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
fi

# Cleanup URL file and iptables rule
rm -f "$TUNNEL_URL_FILE"
sudo iptables -D INPUT -p tcp --dport "$PORT" ! -s 127.0.0.1 -j DROP 2>/dev/null

echo ""
echo "RagON service stopped."
echo "To start again: $SCRIPT_DIR/Start-service-$PROJECT_ID.sh"
echo ""
