#!/bin/bash
# Test embeddings service optimization with 1, 9, 30 hashes

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load environment from .env (portable)
source "$SCRIPT_DIR/../load-env.sh"

MULTIQUERY="$RAGON_ROOT/multi-query/run-multiquery.sh"

# Activate venv
activate_venv

echo "==================================================================="
echo "🧪 BENCHMARK: Embeddings Service Optimization"
echo "==================================================================="
echo ""

# Test hashes (from DKM-PDFs)
HASH_1="cdd78ad022b0a3d0e9e892e5ebf4b979"  # Data Structures book
HASHES_9=(
    "cdd78ad022b0a3d0e9e892e5ebf4b979"  # Data Structures
    "277d623da39e23c8f098c8918d21904b"  # Refactoring
    "1c3912fadc886ab6161526533c82aaba"  # Nvidia Way
    "074c518d4fc4c42b63ce10e0c8850927"  # Statistics
    "5aa60b8a10391073c2303128454da873"  # Deep RL
    "96d5585ae27e6e70cc2b5e4655731d08"  # Database Design
    "f660bc0c857f189d4909b62c83855d8b"  # Kali Linux
    "aea29d62416c43c4b3c94444ecad5beb"  # Causality
    "32bc277cb720919bfd4ebc1318c8993b"  # Legacy Code
)
HASHES_30=(
    "cdd78ad022b0a3d0e9e892e5ebf4b979" "277d623da39e23c8f098c8918d21904b"
    "1c3912fadc886ab6161526533c82aaba" "074c518d4fc4c42b63ce10e0c8850927"
    "5aa60b8a10391073c2303128454da873" "96d5585ae27e6e70cc2b5e4655731d08"
    "f660bc0c857f189d4909b62c83855d8b" "aea29d62416c43c4b3c94444ecad5beb"
    "32bc277cb720919bfd4ebc1318c8993b" "d5fd487804991db1d0658cfa0b893cfa"
    "88f76169373645a771424357d09c6e63" "9248408c2d821a216fadb3fa5f363954"
    "7c68c6c7ad0d1f65ecafe053a9a8fc99" "2484b95bc7213cb2bf667f544a1e302d"
    "a4620e1e9cc5b7d15d5f2944784596ec" "6e74f6a5139fd18172e158cca74cf1db"
    "d8a3d33b9453a83e14a3c5bad3f4f37b" "0f1bafd0d7bf655bee1a5c9b64b34f40"
    "44eb641496420a09d4e87d5e7e5e7acf" "dece4de8b9c48a2a0378564cc5fca779"
    "8e9047f518db18dd6dd382ef6cfdb867" "e3e33508eb99655d98c66c3fbbde149e"
    "2593117c61118a78f3df360a913619f7" "2ce3415de8c0370f156a201254b222fe"
    "4e408bb9606d18631766f4dc7b2ef131" "7bc4ef36ec8449c7b3ba4f94f37b3053"
    "aece10f52ee795b09390d84ee57986e3" "41f23cde0c7c8ccdb744b7278fa75b23"
    "26534a199aeaf0bfc867c4a98769f4de" "c34fe5dd87e86cd5e4f116a1294c51bd"
)

# Test query
QUERY="SOLID principles"

# ═════════════════════════════════════════════════════════════════════
# TEST 1: Single hash (1 book)
# ═════════════════════════════════════════════════════════════════════
echo "📊 TEST 1: Single Hash (1 book)"
echo "───────────────────────────────────────────────────────────────────"
echo "Hash: $HASH_1"
echo "Query: $QUERY"
echo ""

time "$MULTIQUERY" --json "{
  \"queries\": [\"$QUERY\"],
  \"source_hashes\": \"$HASH_1\"
}" 2>&1 | grep -E "(🔄|♻️|💾|✅|Total time|Query:)" || true

echo ""
echo ""

# ═════════════════════════════════════════════════════════════════════
# TEST 2: 9 hashes (9 books)
# ═════════════════════════════════════════════════════════════════════
echo "📊 TEST 2: 9 Hashes (9 books)"
echo "───────────────────────────────────────────────────────────────────"
HASH_STR_9=$(IFS=,; echo "${HASHES_9[*]}")
echo "Hashes: $HASH_STR_9"
echo "Query: $QUERY"
echo ""

time "$MULTIQUERY" --json "{
  \"queries\": [\"$QUERY\"],
  \"source_hashes\": \"$HASH_STR_9\"
}" 2>&1 | grep -E "(🔄|♻️|💾|✅|Total time|Query:)" || true

echo ""
echo ""

# ═════════════════════════════════════════════════════════════════════
# TEST 3: 30 hashes (30 books)
# ═════════════════════════════════════════════════════════════════════
echo "📊 TEST 3: 30 Hashes (30 books)"
echo "───────────────────────────────────────────────────────────────────"
HASH_STR_30=$(IFS=,; echo "${HASHES_30[*]}")
echo "Hashes: $HASH_STR_30"
echo "Query: $QUERY"
echo ""

time "$MULTIQUERY" --json "{
  \"queries\": [\"$QUERY\"],
  \"source_hashes\": \"$HASH_STR_30\"
}" 2>&1 | grep -E "(🔄|♻️|💾|✅|Total time|Query:)" || true

echo ""
echo "==================================================================="
echo "✅ BENCHMARK COMPLETE"
echo "==================================================================="
