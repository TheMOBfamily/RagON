#!/bin/bash
# basic-edit.sh - Basic DOCX text replacement workflow
# Usage: ./basic-edit.sh input.docx "OLD_TEXT" "NEW_TEXT"

set -euo pipefail

INPUT="$1"
OLD_TEXT="$2"
NEW_TEXT="$3"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
WORK_DIR="_work_${TIMESTAMP}"
OUTPUT="${INPUT%.docx}.${TIMESTAMP}.docx"

echo "=== DOCX Editor ==="
echo "Input: $INPUT"
echo "Replace: '$OLD_TEXT' -> '$NEW_TEXT'"
echo "Output: $OUTPUT"
echo ""

# 1. Backup
cp "$INPUT" "${INPUT%.docx}.${TIMESTAMP}.b.docx"
echo "[1/5] Backup created"

# 2. Extract
unzip -q "$INPUT" -d "$WORK_DIR"
echo "[2/5] Extracted to $WORK_DIR"

# 3. Edit XML
xmlstarlet ed -u "//w:t[text()='$OLD_TEXT']" -v "$NEW_TEXT" \
    "$WORK_DIR/word/document.xml" > "$WORK_DIR/word/document.xml.new"
mv "$WORK_DIR/word/document.xml.new" "$WORK_DIR/word/document.xml"
echo "[3/5] Text replaced"

# 4. Repack
cd "$WORK_DIR"
zip -rq "../$OUTPUT" .
cd ..
echo "[4/5] Repacked to $OUTPUT"

# 5. Verify
echo "[5/5] Verification:"
unzip -l "$OUTPUT" | head -5
echo "..."
echo ""
echo "Done! Output: $OUTPUT"
