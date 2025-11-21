#!/bin/bash
# Start RagON Persistent Service

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_PATH="$PROJECT_ROOT/venv"
PORT="${1:-2011}"

echo "🚀 Starting RagON Persistent Service..."
echo "📍 http://0.0.0.0:$PORT"
echo "📖 Docs: http://0.0.0.0:$PORT/docs"
echo ""

# Activate venv
if [ -d "$VENV_PATH" ]; then
    source "$VENV_PATH/bin/activate"
else
    echo "❌ ERROR: venv not found at $VENV_PATH"
    exit 1
fi

# Check FastAPI installed
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing FastAPI..."
    pip install -q fastapi uvicorn[standard]
fi

# Run server
cd "$SCRIPT_DIR"
python3 -m uvicorn src.server:app --host 0.0.0.0 --port "$PORT" --reload
