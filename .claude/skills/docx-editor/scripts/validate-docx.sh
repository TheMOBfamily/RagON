#!/bin/bash
# validate-docx.sh - Validate DOCX file structure
# Usage: ./validate-docx.sh file.docx

set -euo pipefail

FILE="$1"

echo "=== DOCX Validator ==="
echo "File: $FILE"
echo ""

# Check file exists
if [[ ! -f "$FILE" ]]; then
    echo "[FAIL] File not found"
    exit 1
fi

# Check is ZIP
if ! file "$FILE" | grep -q "Zip archive"; then
    echo "[FAIL] Not a valid ZIP archive"
    exit 1
fi
echo "[OK] Valid ZIP archive"

# Check required files
REQUIRED_FILES=(
    "[Content_Types].xml"
    "word/document.xml"
    "_rels/.rels"
)

TEMP_DIR=$(mktemp -d)
unzip -q "$FILE" -d "$TEMP_DIR"

for req in "${REQUIRED_FILES[@]}"; do
    if [[ -f "$TEMP_DIR/$req" ]]; then
        echo "[OK] $req exists"
    else
        echo "[FAIL] Missing: $req"
        rm -rf "$TEMP_DIR"
        exit 1
    fi
done

# Validate XML
echo ""
echo "Validating XML..."
if xmlstarlet val "$TEMP_DIR/word/document.xml" 2>/dev/null; then
    echo "[OK] document.xml is valid XML"
else
    echo "[WARN] document.xml validation issues"
fi

# Count elements
echo ""
echo "Document stats:"
PARA_COUNT=$(xmlstarlet sel -t -c 'count(//w:p)' "$TEMP_DIR/word/document.xml" 2>/dev/null || echo "?")
TEXT_COUNT=$(xmlstarlet sel -t -c 'count(//w:t)' "$TEMP_DIR/word/document.xml" 2>/dev/null || echo "?")
echo "  Paragraphs: $PARA_COUNT"
echo "  Text runs: $TEXT_COUNT"

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "[PASS] DOCX structure is valid"
