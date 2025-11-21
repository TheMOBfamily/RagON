#!/bin/bash
# Merge all DKM-PDFs indexes - Wrapper script
# Author: AI Assistant
# Date: 2025-10-26

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Parse arguments
DRY_RUN=""
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--dry-run)
            DRY_RUN="--dry-run"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -d, --dry-run    Preview only (no files modified)"
            echo "  -h, --help       Show this help"
            echo ""
            echo "Examples:"
            echo "  $0                # Normal merge (all DKM-PDFs)"
            echo "  $0 --dry-run      # Preview merge (no changes)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  DKM-PDFs FAISS Merge Tool${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check venv
VENV_PATH="$PROJECT_ROOT/venv"
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${RED}Error: venv not found at $VENV_PATH${NC}"
    exit 1
fi

# Activate venv
echo -e "${BLUE}Activating virtual environment...${NC}"
source "$VENV_PATH/bin/activate"

# Check main script
MAIN_SCRIPT="$SCRIPT_DIR/main-4f63f059.py"
if [ ! -f "$MAIN_SCRIPT" ]; then
    echo -e "${RED}Error: $MAIN_SCRIPT not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Environment ready${NC}"
echo ""

# Run merge
if [ -n "$DRY_RUN" ]; then
    echo -e "${YELLOW}DRY RUN MODE - Preview only, no files will be modified${NC}"
fi
echo -e "${BLUE}Starting merge of ALL DKM-PDFs...${NC}"
echo -e "${YELLOW}This will take 15-30 minutes for ~206 PDFs${NC}"
echo ""

# Run with logging
LOG_FILE="/tmp/merge-dkm-pdfs.log"
python "$MAIN_SCRIPT" --merge $DRY_RUN 2>&1 | tee "$LOG_FILE"

# Check result
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}  ✅ Merge completed successfully!${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    echo -e "${BLUE}Output location:${NC}"
    echo "  $PROJECT_ROOT/DKM-PDFs/.mini_rag_index/"
    echo ""
    echo -e "${BLUE}Manifest location:${NC}"
    echo "  $PROJECT_ROOT/DKM-PDFs/manifest.json"
    echo ""
    echo -e "${BLUE}Query with MCP RAG:${NC}"
    echo "  mcp__dkm-knowledgebase__queryRAG"
    echo ""
else
    echo ""
    echo -e "${RED}================================================${NC}"
    echo -e "${RED}  ❌ Merge failed - check log${NC}"
    echo -e "${RED}================================================${NC}"
    echo ""
    echo -e "${YELLOW}Log: $LOG_FILE${NC}"
    exit 1
fi
