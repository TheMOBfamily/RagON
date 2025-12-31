# RagON Client Tools

Client tools to connect to RagON service in LAN.

## Setup

1. Copy `.env` file with your API key:
```bash
# Already configured with:
RAGON_API_KEY=de-eab2d684-936b-46af-bdfe-3948995c2344
```

2. Make script executable (if needed):
```bash
chmod +x query-ragon.sh
```

## query-ragon.sh

Query RagON service with automatic LAN discovery and API key authentication.

### Usage

```bash
# Basic query
./query-ragon.sh "What is SOLID principle?"

# Query with custom top_k
./query-ragon.sh "Explain dependency injection" 10

# With environment variable
TOP_K=8 ./query-ragon.sh "Design patterns"
```

### How it works

1. Loads API key from `.env`
2. Checks cache (`~/.ragon-config.json`) for RagON IP
3. If cache miss -> scans LAN to find service
4. Sends query with `X-Api-Key` header
5. Returns JSON response with answer and sources

### Requirements

- `curl` - HTTP client
- `jq` - JSON parser

### Config file

Cached at `~/.ragon-config.json`:

```json
{
  "ip": "192.168.1.47",
  "port": 1411,
  "url": "http://192.168.1.47:1411",
  "updated": "2025-11-21T15:39:06+07:00"
}
```

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | No | Health check |
| `/docs` | GET | No | API documentation |
| `/query` | POST | Yes | Query RAG (requires X-Api-Key header) |
| `/cache/stats` | GET | No | Cache statistics |

## Manual curl examples

```bash
# Get service IP
RAGON_IP=$(cat ~/.ragon-config.json | jq -r '.ip')

# Health check (no auth needed)
curl -s "http://$RAGON_IP:1411/"

# Query (requires API key)
curl -s -X POST "http://$RAGON_IP:1411/query" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: de-eab2d684-936b-46af-bdfe-3948995c2344" \
  -d '{"question": "dependency injection", "top_k": 5}' | jq .
```
