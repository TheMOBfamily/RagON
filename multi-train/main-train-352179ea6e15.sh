#!/bin/bash
# Training script for mini-rag with hash-based caching
# Usage: ./main-train-352179ea6e15.sh [options]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_PATH="$PROJECT_ROOT/venv"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Activate venv
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${RED}Error: venv not found at $VENV_PATH${NC}"
    exit 1
fi

echo -e "${GREEN}Activating venv...${NC}"
source "$VENV_PATH/bin/activate"

# Check Python
if ! command -v python &> /dev/null; then
    echo -e "${RED}Error: Python not found in venv${NC}"
    exit 1
fi

echo -e "${GREEN}Python: $(which python)${NC}"
echo -e "${GREEN}Starting training...${NC}"
echo ""

# Run training script
cd "$SCRIPT_DIR"
python main-train-352179ea6e15.py "$@"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Training completed successfully${NC}"
else
    echo ""
    echo -e "${RED}✗ Training failed with exit code $EXIT_CODE${NC}"
fi

exit $EXIT_CODE
