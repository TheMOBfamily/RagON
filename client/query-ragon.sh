#!/bin/bash
# RagON Query Client
# Discovers RagON service in LAN and sends query with API key

set -e

# Load API key from .env
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$SCRIPT_DIR/.env" ]; then
    source "$SCRIPT_DIR/.env"
fi

if [ -z "$RAGON_API_KEY" ]; then
    echo "Error: RAGON_API_KEY not set in $SCRIPT_DIR/.env" >&2
    exit 1
fi

# Config
CONFIG_FILE="$HOME/.ragon-config.json"
PORT="1411"
TIMEOUT=1
TOP_K="${TOP_K:-5}"

# Check query parameter
if [ -z "$1" ]; then
    echo "Usage: $0 \"your question here\" [top_k]"
    echo ""
    echo "Examples:"
    echo "  $0 \"What is SOLID principle?\""
    echo "  $0 \"Explain dependency injection\" 10"
    exit 1
fi

QUERY="$1"
if [ -n "$2" ]; then
    TOP_K="$2"
fi

# Get subnet
get_subnet() {
    ip route | grep -oP 'src \K[0-9.]+' | head -1 | sed 's/\.[0-9]*$/./'
}

# Check cached config
check_cached() {
    if [ -f "$CONFIG_FILE" ]; then
        CACHED_IP=$(jq -r '.ip' "$CONFIG_FILE" 2>/dev/null)
        if [ -n "$CACHED_IP" ] && [ "$CACHED_IP" != "null" ]; then
            if curl -s --connect-timeout $TIMEOUT "http://$CACHED_IP:$PORT/" | grep -q "RagON" 2>/dev/null; then
                echo "$CACHED_IP"
                return 0
            fi
        fi
    fi
    return 1
}

# Scan subnet
scan_subnet() {
    SUBNET=$(get_subnet)
    echo "Scanning ${SUBNET}0/24..." >&2

    for i in $(seq 1 254); do
        IP="${SUBNET}${i}"
        if curl -s --connect-timeout $TIMEOUT "http://$IP:$PORT/" 2>/dev/null | grep -q "RagON"; then
            echo "$IP"
            return 0
        fi
    done
    return 1
}

# Discover RagON
discover_ragon() {
    # Try cached first
    CACHED=$(check_cached)
    if [ -n "$CACHED" ]; then
        echo "RagON: http://$CACHED:$PORT (cached)" >&2
        echo "$CACHED"
        return 0
    fi

    echo "Cache miss, scanning LAN..." >&2
    FOUND=$(scan_subnet)

    if [ -n "$FOUND" ]; then
        echo "{\"ip\": \"$FOUND\", \"port\": $PORT, \"url\": \"http://$FOUND:$PORT\", \"updated\": \"$(date -Iseconds)\"}" > "$CONFIG_FILE"
        echo "RagON found: http://$FOUND:$PORT" >&2
        echo "$FOUND"
        return 0
    else
        echo "RagON not found in LAN" >&2
        return 1
    fi
}

# Main
main() {
    IP=$(discover_ragon)
    if [ -z "$IP" ]; then
        exit 1
    fi

    URL="http://$IP:$PORT/query"

    echo "Querying: $QUERY" >&2
    echo "Top K: $TOP_K" >&2
    echo "" >&2

    # Send query with API key
    RESPONSE=$(curl -s -X POST "$URL" \
        -H "Content-Type: application/json" \
        -H "X-Api-Key: $RAGON_API_KEY" \
        -d "{\"question\": \"$QUERY\", \"top_k\": $TOP_K}")

    # Check for error
    if echo "$RESPONSE" | jq -e '.detail' >/dev/null 2>&1; then
        echo "Error: $(echo "$RESPONSE" | jq -r '.detail')" >&2
        exit 1
    fi

    # Pretty print response (remove 'answer' field - DRY: content already in sources)
    echo "$RESPONSE" | jq 'del(.answer)'
}

main
