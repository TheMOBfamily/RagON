#!/bin/bash
# Start RagON Persistent Service - ID: 8e4367fed117
# SINGLETON: Only one instance runs at a time. Restarts if already running.
# Options:
#   --no-tunnel   : LAN only (no external tunnel)
#   --block-lan   : Block LAN access (localhost only)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ID="8e4367fed117"
FLASK_API_DIR="$SCRIPT_DIR/Flask-API"
VENV_PATH="$SCRIPT_DIR/venv"
TUNNEL_PID_FILE="/tmp/ragon-tunnel-$PROJECT_ID.pid"
TUNNEL_URL_FILE="/tmp/ragon-tunnel-$PROJECT_ID-url.txt"
API_PID_FILE="/tmp/ragon-api-$PROJECT_ID.pid"

# Parse arguments
PORT="1411"
NO_TUNNEL=false
BLOCK_LAN=false
for arg in "$@"; do
    case $arg in
        --no-tunnel)
            NO_TUNNEL=true
            ;;
        --block-lan)
            BLOCK_LAN=true
            ;;
        [0-9]*)
            PORT="$arg"
            ;;
    esac
done

echo "=========================================="
echo "  RagON Persistent Service [$PROJECT_ID]"
echo "=========================================="
echo ""

# Check if already running (SINGLETON check)
check_running() {
    if [ -f "$API_PID_FILE" ]; then
        OLD_PID=$(cat "$API_PID_FILE")
        if kill -0 "$OLD_PID" 2>/dev/null; then
            return 0  # Running
        fi
    fi
    # Also check by port
    if lsof -i ":$PORT" > /dev/null 2>&1; then
        return 0  # Running
    fi
    return 1  # Not running
}

# Stop existing instance
stop_existing() {
    echo "Existing instance detected. Restarting..."

    # Stop API by PID
    if [ -f "$API_PID_FILE" ]; then
        OLD_PID=$(cat "$API_PID_FILE")
        if kill -0 "$OLD_PID" 2>/dev/null; then
            kill "$OLD_PID" 2>/dev/null
            sleep 1
            kill -9 "$OLD_PID" 2>/dev/null
        fi
        rm -f "$API_PID_FILE"
    fi

    # Stop by port (only python/uvicorn)
    if lsof -i ":$PORT" > /dev/null 2>&1; then
        PIDS=$(lsof -ti ":$PORT" 2>/dev/null)
        for pid in $PIDS; do
            PROC_NAME=$(ps -p "$pid" -o comm= 2>/dev/null)
            if [[ "$PROC_NAME" == "python"* ]] || [[ "$PROC_NAME" == "uvicorn"* ]]; then
                kill "$pid" 2>/dev/null
            fi
        done
        sleep 1
    fi

    # Stop tunnel
    if [ -f "$TUNNEL_PID_FILE" ]; then
        OLD_TUNNEL=$(cat "$TUNNEL_PID_FILE")
        kill "$OLD_TUNNEL" 2>/dev/null
        rm -f "$TUNNEL_PID_FILE" "$TUNNEL_URL_FILE"
    fi

    echo "Previous instance stopped."
    echo ""
}

# Block LAN access (requires sudo)
block_lan() {
    sudo iptables -D INPUT -p tcp --dport "$PORT" ! -s 127.0.0.1 -j DROP 2>/dev/null
    sudo iptables -I INPUT -p tcp --dport "$PORT" ! -s 127.0.0.1 -j DROP 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "LAN access BLOCKED (localhost only)"
    else
        echo "WARNING: Could not block LAN (need sudo)"
    fi
}

# Allow LAN access
allow_lan() {
    sudo iptables -D INPUT -p tcp --dport "$PORT" ! -s 127.0.0.1 -j DROP 2>/dev/null
}

# SINGLETON: Check and restart if running
if check_running; then
    stop_existing
fi

# Activate venv
if [ -d "$VENV_PATH" ]; then
    source "$VENV_PATH/bin/activate"
else
    echo "ERROR: venv not found at $VENV_PATH"
    exit 1
fi

# Check FastAPI installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Installing FastAPI..."
    pip install -q fastapi uvicorn[standard]
fi

# Get cloudflared binary path
CLOUDFLARED_BIN="/tmp/cloudflared"

# Install cloudflared if not exists (no sudo needed)
install_cloudflared() {
    if [ ! -x "$CLOUDFLARED_BIN" ]; then
        echo "Downloading cloudflared binary..."
        curl -sL -o "$CLOUDFLARED_BIN" https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
        chmod +x "$CLOUDFLARED_BIN"
    fi
}

# Start tunnel function
start_tunnel() {
    install_cloudflared

    echo ""
    echo "Starting Cloudflare Tunnel..."

    # Start cloudflared in background, capture URL
    "$CLOUDFLARED_BIN" tunnel --url http://localhost:$PORT 2>&1 | tee /tmp/cloudflared-$PROJECT_ID.log &
    TUNNEL_PID=$!
    echo $TUNNEL_PID > "$TUNNEL_PID_FILE"

    # Wait for tunnel URL
    sleep 5
    TUNNEL_URL=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/cloudflared-$PROJECT_ID.log | head -1)

    if [ -n "$TUNNEL_URL" ]; then
        echo "$TUNNEL_URL" > "$TUNNEL_URL_FILE"
        echo ""
        echo "=========================================="
        echo "  EXTERNAL ACCESS ENABLED"
        echo "=========================================="
        echo "  Local:    http://localhost:$PORT"
        echo "  External: $TUNNEL_URL"
        echo "  Docs:     $TUNNEL_URL/docs"
        echo "=========================================="
        echo ""
        echo "To stop: $SCRIPT_DIR/Stop-service-$PROJECT_ID.sh"
        echo ""
    else
        echo "WARNING: Could not get tunnel URL. Check /tmp/cloudflared-$PROJECT_ID.log"
    fi
}

# Get LAN IP
LAN_IP=$(hostname -I | awk '{print $1}')

# Apply LAN blocking if requested
if [ "$BLOCK_LAN" = true ]; then
    block_lan
else
    # Ensure LAN is allowed
    allow_lan
fi

# Check if --no-tunnel flag
if [ "$NO_TUNNEL" = true ]; then
    echo "=========================================="
    if [ "$BLOCK_LAN" = true ]; then
        echo "  LOCALHOST ONLY (LAN BLOCKED)"
        echo "=========================================="
        echo "  Local:  http://localhost:$PORT"
        echo "  Docs:   http://localhost:$PORT/docs"
    else
        echo "  LAN ACCESS ENABLED"
        echo "=========================================="
        echo "  Local:  http://localhost:$PORT"
        echo "  LAN:    http://$LAN_IP:$PORT"
        echo "  Docs:   http://$LAN_IP:$PORT/docs"
    fi
    echo "=========================================="
    echo ""
    echo "LAN control:"
    echo "  Block:  $SCRIPT_DIR/Stop-service-$PROJECT_ID.sh --block-lan"
    echo "  Allow:  $SCRIPT_DIR/Stop-service-$PROJECT_ID.sh --allow-lan"
else
    # Start tunnel in background
    start_tunnel &
fi

echo ""
echo "Starting FastAPI server on port $PORT..."
echo ""

# Run server (foreground)
cd "$FLASK_API_DIR"

# Save PID for singleton management
(
    python3 -m uvicorn src.server:app --host 0.0.0.0 --port "$PORT" --reload &
    echo $! > "$API_PID_FILE"
    wait
)
