#!/bin/bash
# filter3-dkm-dedup.sh - Find and deduplicate books between input folder and DKM-PDFs
# Version: 1.0.0
# Date: 2025-11-10
# Author: Fong + Claude
#
# Usage: bash filter3-dkm-dedup.sh <input-folder>
# Example: bash filter3-dkm-dedup.sh /home/fong/Dropbox/_tmp/book-files-report-verified
#
# Output:
#   - /tmp/filter3-duplicates.txt (files already in DKM-PDFs)
#   - /tmp/filter3-new.txt (truly new files)
#   - /tmp/filter3-suspicious.txt (need manual check - title similar but not exact match)

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Config
INPUT_FOLDER="${1:-.}"
DKM_PDFs="/home/fong/Projects/mini-rag/DKM-PDFs"
REPORT_DIR="/tmp"
DUPLICATES_FILE="$REPORT_DIR/filter3-duplicates.txt"
NEW_FILE="$REPORT_DIR/filter3-new.txt"
SUSPICIOUS_FILE="$REPORT_DIR/filter3-suspicious.txt"

# Validate input
if [ ! -d "$INPUT_FOLDER" ]; then
    echo -e "${RED}Error: Input folder does not exist: $INPUT_FOLDER${NC}"
    exit 1
fi

if [ ! -d "$DKM_PDFs" ]; then
    echo -e "${RED}Error: DKM-PDFs folder does not exist: $DKM_PDFs${NC}"
    exit 1
fi

# Initialize report files
> "$DUPLICATES_FILE"
> "$NEW_FILE"
> "$SUSPICIOUS_FILE"

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Filter3 -> DKM Deduplication Tool${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Input folder: $INPUT_FOLDER"
echo "DKM-PDFs folder: $DKM_PDFs"
echo ""

# Count input files
cd "$INPUT_FOLDER"
TOTAL_FILES=$(ls -1 *.PDF 2>/dev/null | wc -l)
echo -e "${BLUE}Total input files: $TOTAL_FILES${NC}"
echo ""

# Build DKM-PDFs filename list (for fast lookup)
echo -e "${YELLOW}[1/3] Building DKM-PDFs filename index...${NC}"
DKM_LIST="/tmp/filter3-dkm-list.txt"
(cd "$DKM_PDFs" && ls -1 *.PDF 2>/dev/null) > "$DKM_LIST"
DKM_COUNT=$(wc -l < "$DKM_LIST")
echo "   DKM-PDFs files: $DKM_COUNT"
echo ""

# Process each input file
echo -e "${YELLOW}[2/3] Checking each file against DKM-PDFs...${NC}"
CHECKED=0
DUPLICATES=0
NEW=0
SUSPICIOUS=0

for input_file in *.PDF; do
    [ ! -f "$input_file" ] && continue

    CHECKED=$((CHECKED + 1))

    # Extract year and title keywords (first 3-5 words)
    YEAR=$(echo "$input_file" | grep -oP '^\d{4}' || echo "")
    # Remove year prefix, take first 5 words, replace separators with space
    TITLE_KEYWORDS=$(echo "$input_file" | sed 's/^[0-9]\{4\}-//' | cut -d'-' -f1-5 | sed 's/[-_]/ /g' | tr -s ' ')

    # Method 1: Check exact filename match (fastest)
    if grep -Fxq "$input_file" "$DKM_LIST"; then
        echo -e "  ${RED}[DUPLICATE]${NC} $input_file (exact filename match)"
        echo "$input_file|exact_match|$input_file" >> "$DUPLICATES_FILE"
        DUPLICATES=$((DUPLICATES + 1))
        continue
    fi

    # Method 2: Check by year + title keywords (fuzzy)
    if [ -n "$YEAR" ] && [ -n "$TITLE_KEYWORDS" ]; then
        # Search for similar files in DKM (same year + at least 3 matching words)
        FIRST_3_WORDS=$(echo "$TITLE_KEYWORDS" | awk '{print $1" "$2" "$3}')

        # Use grep to find similar titles
        SIMILAR=$(grep -i "^$YEAR-" "$DKM_LIST" | grep -i "$FIRST_3_WORDS" | head -1 || true)

        if [ -n "$SIMILAR" ]; then
            echo -e "  ${YELLOW}[SUSPICIOUS]${NC} $input_file"
            echo "     Similar: $SIMILAR"
            echo "$input_file|similar_title|$SIMILAR" >> "$SUSPICIOUS_FILE"
            SUSPICIOUS=$((SUSPICIOUS + 1))
            continue
        fi
    fi

    # Method 3: Truly new file
    echo -e "  ${GREEN}[NEW]${NC} $input_file"
    echo "$input_file" >> "$NEW_FILE"
    NEW=$((NEW + 1))

    # Progress indicator every 10 files
    if [ $((CHECKED % 10)) -eq 0 ]; then
        PERCENT=$((CHECKED * 100 / TOTAL_FILES))
        echo -e "  ${BLUE}Progress: $CHECKED/$TOTAL_FILES files ($PERCENT%)${NC}"
    fi
done

echo ""
echo -e "${YELLOW}[3/3] Generating reports...${NC}"
echo ""

# Summary
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Summary${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "Total checked:      ${BLUE}$CHECKED${NC}"
echo -e "Duplicates (exact): ${RED}$DUPLICATES${NC}"
echo -e "Suspicious:         ${YELLOW}$SUSPICIOUS${NC} (need manual check)"
echo -e "Truly new:          ${GREEN}$NEW${NC}"
echo ""

# Verification
EXPECTED=$((DUPLICATES + SUSPICIOUS + NEW))
if [ $CHECKED -eq $EXPECTED ]; then
    echo -e "${GREEN}✅ Count matches! All files categorized.${NC}"
else
    echo -e "${RED}⚠️  WARNING: Count mismatch! $CHECKED checked, but $EXPECTED categorized.${NC}"
fi
echo ""

# Report files
echo -e "${BLUE}Reports saved to:${NC}"
echo "  - Duplicates: $DUPLICATES_FILE ($DUPLICATES files)"
echo "  - Suspicious: $SUSPICIOUS_FILE ($SUSPICIOUS files)"
echo "  - New files:  $NEW_FILE ($NEW files)"
echo ""

# Cleanup
rm -f "$DKM_LIST"

# Next steps
if [ $SUSPICIOUS -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Next: Review suspicious files in $SUSPICIOUS_FILE${NC}"
    echo "   Compare first 3-5 pages to confirm duplicates"
    echo ""
fi

if [ $NEW -gt 0 ]; then
    echo -e "${GREEN}✅ Ready to copy $NEW new files to DKM-PDFs${NC}"
    echo "   Command: while IFS= read -r file; do cp \"$INPUT_FOLDER/\$file\" \"$DKM_PDFs/\"; done < \"$NEW_FILE\""
    echo ""
fi

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
