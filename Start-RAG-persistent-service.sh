#!/bin/bash
# Start RagON Persistent Service with External Tunnel

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLASK_API_DIR="$SCRIPT_DIR/Flask-API"
VENV_PATH="$SCRIPT_DIR/venv"
PORT="${1:-1411}"
TUNNEL_PID_FILE="/tmp/ragon-tunnel.pid"
TUNNEL_URL_FILE="/tmp/ragon-tunnel-url.txt"

echo "=========================================="
echo "  RagON Persistent Service"
echo "=========================================="
echo ""

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

# Install cloudflared if not exists
install_cloudflared() {
    if ! command -v cloudflared &> /dev/null; then
        echo "Installing cloudflared..."
        curl -L --output /tmp/cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
        sudo dpkg -i /tmp/cloudflared.deb
        rm /tmp/cloudflared.deb
    fi
}

# Start tunnel function
start_tunnel() {
    install_cloudflared

    # Kill existing tunnel if running
    if [ -f "$TUNNEL_PID_FILE" ]; then
        OLD_PID=$(cat "$TUNNEL_PID_FILE")
        kill "$OLD_PID" 2>/dev/null
        rm -f "$TUNNEL_PID_FILE" "$TUNNEL_URL_FILE"
    fi

    echo ""
    echo "Starting Cloudflare Tunnel..."

    # Start cloudflared in background, capture URL
    cloudflared tunnel --url http://localhost:$PORT 2>&1 | tee /tmp/cloudflared.log &
    TUNNEL_PID=$!
    echo $TUNNEL_PID > "$TUNNEL_PID_FILE"

    # Wait for tunnel URL
    sleep 5
    TUNNEL_URL=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/cloudflared.log | head -1)

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
        echo "To stop tunnel only: $SCRIPT_DIR/Stop-service.sh"
        echo ""
    else
        echo "WARNING: Could not get tunnel URL. Check /tmp/cloudflared.log"
    fi
}

# Check if --no-tunnel flag
if [[ "$*" == *"--no-tunnel"* ]]; then
    echo "Local: http://0.0.0.0:$PORT"
    echo "Docs:  http://0.0.0.0:$PORT/docs"
    echo "(Tunnel disabled)"
else
    # Start tunnel in background
    start_tunnel &
fi

echo ""
echo "Starting FastAPI server on port $PORT..."
echo ""

# Run server (foreground)
cd "$FLASK_API_DIR"
python3 -m uvicorn src.server:app --host 0.0.0.0 --port "$PORT" --reload
