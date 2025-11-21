#!/bin/bash
# Commit instructions-dkm-sources-knowledgebase.md at all projects
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

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Commit instructions-dkm-sources-knowledgebase║${NC}"
echo -e "${BLUE}║  at all projects                               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# Commit message
COMMIT_MSG="docs: Sync instructions-dkm-sources-knowledgebase from RagON

Add comprehensive knowledge sources map:
- Internet Research: Perplexity AI, ArXiv, Gemini 2.5 Pro (MCP)
- RAG Collections: Python Clean Code, DE-RAG, NASA+Google, Kali Security, Laravel
- Asana Project Management
- Notion Knowledge Base (MCP)
- Obsidian Personal Notes

Source: ${RAGON_ROOT}/.fong/instructions/
Pushed via: instructions-push-pull-boiler-plate.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Dynamic discovery (PROJECTS_BASE from env)
PROJECTS_BASE="${PROJECTS_BASE:-$(dirname "$RAGON_ROOT")}"
FONG_DIRS=($(find "$PROJECTS_BASE" -maxdepth 2 -name ".fong" -type d 2>/dev/null | sort))

# Counters
TOTAL=0
COMMITTED=0
SKIPPED=0
FAILED=0

# Process each project
for FONG_DIR in "${FONG_DIRS[@]}"; do
    PROJECT_DIR=$(dirname "$FONG_DIR")
    PROJECT_NAME=$(basename "$PROJECT_DIR")
    TARGET_FILE="$FONG_DIR/instructions/instructions-dkm-sources-knowledgebase.md"

    TOTAL=$((TOTAL + 1))

    # Skip if file doesn't exist (shouldn't happen after push)
    if [ ! -f "$TARGET_FILE" ]; then
        echo -e "${YELLOW}[$TOTAL/${#FONG_DIRS[@]}] SKIP (no file): $PROJECT_NAME${NC}"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    # Check if project is a git repo
    if [ ! -d "$PROJECT_DIR/.git" ]; then
        echo -e "${YELLOW}[$TOTAL/${#FONG_DIRS[@]}] SKIP (not git): $PROJECT_NAME${NC}"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    # Navigate to project
    cd "$PROJECT_DIR"

    # Check if file has changes
    if git diff --quiet "$TARGET_FILE" 2>/dev/null && \
       git diff --cached --quiet "$TARGET_FILE" 2>/dev/null && \
       git ls-files --error-unmatch "$TARGET_FILE" &>/dev/null; then
        echo -e "${YELLOW}[$TOTAL/${#FONG_DIRS[@]}] SKIP (no changes): $PROJECT_NAME${NC}"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    # Add file
    if ! git add "$TARGET_FILE" 2>/dev/null; then
        echo -e "${RED}[$TOTAL/${#FONG_DIRS[@]}] ✗ FAILED (git add): $PROJECT_NAME${NC}"
        FAILED=$((FAILED + 1))
        continue
    fi

    # Commit
    if git commit -m "$COMMIT_MSG" 2>/dev/null; then
        echo -e "${GREEN}[$TOTAL/${#FONG_DIRS[@]}] ✓ COMMITTED: $PROJECT_NAME${NC}"
        COMMITTED=$((COMMITTED + 1))
    else
        # Commit might fail if no changes (already tracked)
        echo -e "${YELLOW}[$TOTAL/${#FONG_DIRS[@]}] SKIP (commit failed): $PROJECT_NAME${NC}"
        SKIPPED=$((SKIPPED + 1))
    fi
done

# Return to original directory
cd "$RAGON_ROOT"

# Summary
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Summary                                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
echo -e "Total projects: $TOTAL"
echo -e "${GREEN}Committed: $COMMITTED${NC}"
echo -e "${YELLOW}Skipped: $SKIPPED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $COMMITTED -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Note: Changes are committed but NOT pushed${NC}"
    echo -e "To push all changes, run:"
    echo -e "  for dir in \$(find $PROJECTS_BASE -maxdepth 2 -name \".git\" -type d 2>/dev/null | sed 's/\/.git//'); do (cd \$dir && git push); done"
fi
