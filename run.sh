#!/bin/bash
# RagON Runner Script - RagON API Mode + Legacy Fallback
# Usage: /home/fong/Projects/RagON/run.sh "question" [pdf_path] [--force-rebuild] [--top-k N] [--legacy]

# Get absolute path to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

# Virtual environment path (absolute)
VENV_PATH="$PROJECT_ROOT/venv"
MAIN_SCRIPT="$PROJECT_ROOT/main-minirag.py"
DEFAULT_PDF_PATH="$PROJECT_ROOT/DKM-PDFs"
# Load RAGON_API_URL from .env (SSOT)
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(grep -E '^RAGON_API_URL=' "$PROJECT_ROOT/.env" | xargs)
fi
RAGON_API_URL="${RAGON_API_URL:-http://localhost:1411}"

# Check if venv exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual environment not found at: $VENV_PATH"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if main script exists
if [ ! -f "$MAIN_SCRIPT" ]; then
    echo "❌ Main script not found at: $MAIN_SCRIPT"
    exit 1
fi

# Parse arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 \"question\" [pdf_path] [--force-rebuild] [--top-k N] [--legacy]"
    echo "Example: $0 \"What are the key findings?\" /absolute/path/to/pdfs"
    echo "Example: $0 \"Summarize methodology\" # Uses default path (via RagON API)"
    echo "Example: $0 \"Question?\" /path/to/pdfs --top-k 8 # Retrieve 8 chunks"
    echo "Example: $0 \"Question?\" --legacy # Force legacy mode (direct Python execution)"
    echo ""
    echo "Modes:"
    echo "  Default: RagON API mode (fast, requires service running)"
    echo "  --legacy: Legacy mode (slower, direct execution)"
    exit 1
fi

QUESTION="$1"
PDF_PATH=""
FORCE_REBUILD=""
TOP_K=""
USE_LEGACY=false

# Parse remaining arguments
shift # Skip the question argument
while [[ $# -gt 0 ]]; do
    case $1 in
        --legacy)
            USE_LEGACY=true
            shift
            ;;
        --force-rebuild)
            FORCE_REBUILD="--force-rebuild"
            shift
            ;;
        --top-k|--chunks)
            TOP_K="$2"
            shift 2
            ;;
        *)
            if [ -z "$PDF_PATH" ]; then
                PDF_PATH="$1"
            fi
            shift
            ;;
    esac
done

# Set default PDF path if not provided
PDF_PATH="${PDF_PATH:-$DEFAULT_PDF_PATH}"

# Convert relative path to absolute if provided
if [[ ! "$PDF_PATH" = /* ]]; then
    PDF_PATH="$(cd "$(dirname "$PDF_PATH")" && pwd)/$(basename "$PDF_PATH")"
fi

# Check if PDF path exists
if [ ! -d "$PDF_PATH" ]; then
    echo "❌ PDF directory not found: $PDF_PATH"
    exit 1
fi

echo "🤖 Mini-RAG Runner"
echo "📁 PDF Directory: $PDF_PATH"
echo "❓ Question: $QUESTION"
if [ -n "$TOP_K" ]; then
    echo "📊 TOP_K (chunks): $TOP_K"
fi

# Force rebuild requires legacy mode
if [ -n "$FORCE_REBUILD" ]; then
    USE_LEGACY=true
    echo "ℹ️  --force-rebuild detected → switching to LEGACY mode"
fi

# Route to legacy or API mode
if [ "$USE_LEGACY" = true ]; then
    echo "🔧 Mode: LEGACY (direct Python execution)"
    if [ -n "$FORCE_REBUILD" ]; then
        echo "🔄 Force rebuild: ENABLED"
    fi
    echo "🔄 Processing..."
    echo ""

    # Build arguments for Python script
    PYTHON_ARGS="$FORCE_REBUILD"
    if [ -n "$TOP_K" ]; then
        PYTHON_ARGS="$PYTHON_ARGS --top-k $TOP_K"
    fi

    # Activate venv and run main script
    source "$VENV_PATH/bin/activate" && python "$MAIN_SCRIPT" "$QUESTION" "$PDF_PATH" $PYTHON_ARGS
    EXIT_CODE=$?

    # If force rebuild succeeded, reload API cache (if service running)
    if [ $EXIT_CODE -eq 0 ] && [ -n "$FORCE_REBUILD" ]; then
        if curl -s -f "$RAGON_API_URL" > /dev/null 2>&1; then
            echo ""
            echo "🔄 Reloading RagON API cache..."
            RELOAD_RESPONSE=$(curl -s -X POST "$RAGON_API_URL/cache/reload")
            echo "✅ Cache reloaded"
            echo "$RELOAD_RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f\"   Load time: {data.get('load_time_seconds', 0):.2f}s\")
    print(f\"   Docs: {data.get('docs_count', 'unknown')}\")
except: pass
"
        fi
    fi

else
    echo "🚀 Mode: RagON API (fast query)"

    # Check RagON service availability
    if ! curl -s -f "$RAGON_API_URL" > /dev/null 2>&1; then
        echo "⚠️  RagON service not running - auto-starting..."
        echo "🚀 Starting service at $RAGON_API_URL"

        # Start service in background
        cd "$PROJECT_ROOT/RagON"
        RAGON_PORT=$(echo "$RAGON_API_URL" | grep -oP ':\K[0-9]+$' || echo "1411")
        nohup "$PROJECT_ROOT/RagON/Start-RAG-persistent-service.sh" "$RAGON_PORT" > /dev/null 2>&1 &

        # Wait for service to be ready (max 30 seconds)
        echo "⏳ Waiting for service to start..."
        for i in {1..30}; do
            sleep 1
            if curl -s -f "$RAGON_API_URL" > /dev/null 2>&1; then
                echo "✅ Service started successfully"
                break
            fi
            if [ $i -eq 30 ]; then
                echo "❌ Service failed to start after 30 seconds"
                echo "   Try manual start: $PROJECT_ROOT/RagON/Start-RAG-persistent-service.sh 2011"
                echo "   Or use --legacy flag to run without service"
                exit 1
            fi
        done
        cd "$PROJECT_ROOT"
    fi

    echo "✅ RagON service detected"
    echo "🔄 Querying via API..."
    echo ""

    # Construct JSON payload
    JSON_PAYLOAD=$(cat <<EOF
{
  "pdf_directory": "$PDF_PATH",
  "question": "$QUESTION"
EOF
)

    # Add top_k if provided
    if [ -n "$TOP_K" ]; then
        JSON_PAYLOAD="${JSON_PAYLOAD},\n  \"top_k\": $TOP_K"
    fi

    JSON_PAYLOAD="${JSON_PAYLOAD}\n}"

    # Query RagON API
    RESPONSE=$(echo -e "$JSON_PAYLOAD" | curl -s -X POST "$RAGON_API_URL/query" \
        -H "Content-Type: application/json" \
        -d @-)

    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        # Parse and display response
        echo "📄 Answer:"
        echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('answer', 'No answer'))
    print('\n' + '='*80)
    print(f\"⏱️  Load time: {data.get('load_time_seconds', 0):.2f}s\")
    print(f\"⏱️  Retrieval time: {data.get('retrieval_time_seconds', 0):.2f}s\")
    print(f\"💾 From cache: {data.get('from_cache', False)}\")
except Exception as e:
    print(f'Error parsing response: {e}')
    sys.exit(1)
"
        EXIT_CODE=$?
    else
        echo "❌ API request failed"
    fi
fi

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Process completed successfully"
else
    echo ""
    echo "❌ Process failed with exit code: $EXIT_CODE"
fi

exit $EXIT_CODE