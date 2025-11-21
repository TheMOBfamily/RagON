#!/bin/bash
# Push instructions-dkm-sources-knowledgebase.md to all projects
# Date: 2025-10-26
# Following: instructions-push-pull-boiler-plate.md

set -euo pipefail

# Load environment
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../load-env.sh"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Source file (from env)
SOURCE_FILE="${RAGON_ROOT}/.fong/instructions/instructions-dkm-sources-knowledgebase.md"

# Verify source file exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo -e "${RED}✗ Source file not found: $SOURCE_FILE${NC}"
    exit 1
fi

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Push instructions-dkm-sources-knowledgebase  ║${NC}"
echo -e "${BLUE}║  to all projects with .fong directory         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Source: $SOURCE_FILE${NC}"
echo -e "${GREEN}Size: $(ls -lh "$SOURCE_FILE" | awk '{print $5}')${NC}"
echo -e "${GREEN}Lines: $(wc -l < "$SOURCE_FILE")${NC}"
echo ""

# Dynamic discovery (PROJECTS_BASE from env, defaults to parent of RAGON_ROOT)
PROJECTS_BASE="${PROJECTS_BASE:-$(dirname "$RAGON_ROOT")}"
echo -e "${YELLOW}Discovering projects with .fong directory...${NC}"
FONG_DIRS=($(find "$PROJECTS_BASE" -maxdepth 2 -name ".fong" -type d 2>/dev/null | sort))

echo -e "${GREEN}Found ${#FONG_DIRS[@]} projects${NC}"
echo ""

# Counters
TOTAL=0
SUCCESS=0
SKIPPED=0
FAILED=0

# Process each project
for FONG_DIR in "${FONG_DIRS[@]}"; do
    PROJECT_DIR=$(dirname "$FONG_DIR")
    PROJECT_NAME=$(basename "$PROJECT_DIR")
    TARGET_DIR="$FONG_DIR/instructions/"
    TARGET_FILE="$TARGET_DIR/instructions-dkm-sources-knowledgebase.md"

    TOTAL=$((TOTAL + 1))

    # Create instructions directory if not exists
    if [ ! -d "$TARGET_DIR" ]; then
        mkdir -p "$TARGET_DIR"
        echo -e "${YELLOW}  Created: $TARGET_DIR${NC}"
    fi

    # Skip if source is same as target (RagON itself)
    if [ "$SOURCE_FILE" == "$TARGET_FILE" ]; then
        echo -e "${YELLOW}[$TOTAL/${#FONG_DIRS[@]}] SKIP (source): $PROJECT_NAME${NC}"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    # Copy file
    if cp "$SOURCE_FILE" "$TARGET_FILE"; then
        echo -e "${GREEN}[$TOTAL/${#FONG_DIRS[@]}] ✓ COPIED: $PROJECT_NAME${NC}"
        echo -e "   → $TARGET_FILE"
        SUCCESS=$((SUCCESS + 1))
    else
        echo -e "${RED}[$TOTAL/${#FONG_DIRS[@]}] ✗ FAILED: $PROJECT_NAME${NC}"
        FAILED=$((FAILED + 1))
    fi

    echo ""
done

# Summary
echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Summary                                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo -e "Total projects: $TOTAL"
echo -e "${GREEN}Success: $SUCCESS${NC}"
echo -e "${YELLOW}Skipped: $SKIPPED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $SUCCESS -gt 0 ]; then
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "1. Verify copied files"
    echo -e "2. Commit changes at each project"
    echo -e "3. Update .memory/ and mem0"
fi
