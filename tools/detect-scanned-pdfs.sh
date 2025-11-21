#!/bin/bash
# detect-scanned-pdfs.sh
# Multi-method scanned PDF detection with scoring system
# Version: 2.0.0
# Author: Fong
# Date: 2025-10-28

set -euo pipefail

TARGET_FOLDER="${1:-.}"

echo "🔍 Scanning for scanned PDFs in: $TARGET_FOLDER"
echo ""

cd "$TARGET_FOLDER"

TOTAL_FILES=0
SCANNED_COUNT=0
NATIVE_COUNT=0

shopt -s nullglob  # Handle case when no PDFs match pattern

for pdf in *.PDF *.pdf; do
  [ ! -f "$pdf" ] && continue

  # Skip if already prefixed
  if [[ "$pdf" =~ ^scanned- ]]; then
    echo "⏭️  Skip (already marked): $pdf"
    continue
  fi

  ((TOTAL_FILES++))

  # Method 1: Font detection (MOST RELIABLE - primary check)
  FONT_COUNT=$(pdffonts "$pdf" 2>/dev/null | wc -l || echo "0")
  HAS_FONTS=false
  [ "$FONT_COUNT" -ge 4 ] && HAS_FONTS=true  # ≥4 lines = header + multiple fonts (native PDF)

  # Method 2: Character count (check pages 1, 5, 10 to skip empty covers)
  CHARS_P1=$(pdftotext -f 1 -l 1 "$pdf" - 2>/dev/null | wc -c || echo "0")
  CHARS_P5=$(pdftotext -f 5 -l 5 "$pdf" - 2>/dev/null | wc -c || echo "0")
  CHARS_P10=$(pdftotext -f 10 -l 10 "$pdf" - 2>/dev/null | wc -c || echo "0")
  MAX_CHARS=$((CHARS_P1 > CHARS_P5 ? CHARS_P1 : CHARS_P5))
  MAX_CHARS=$((MAX_CHARS > CHARS_P10 ? MAX_CHARS : CHARS_P10))

  # Method 3: Word count (best page from above)
  WORDS_P5=$(pdftotext -f 5 -l 5 "$pdf" - 2>/dev/null | wc -w || echo "0")
  WORDS_P10=$(pdftotext -f 10 -l 10 "$pdf" - 2>/dev/null | wc -w || echo "0")
  MAX_WORDS=$((WORDS_P5 > WORDS_P10 ? WORDS_P5 : WORDS_P10))

  # Method 4: Total page count (scanned PDFs often have few pages)
  PAGE_COUNT=$(pdfinfo "$pdf" 2>/dev/null | grep -i "^Pages:" | awk '{print $2}' || echo "0")

  # Decision logic with font check as primary
  if [ "$HAS_FONTS" = true ]; then
    # Has fonts = definitely NOT scanned (even if cover pages are empty)
    SCANNED_SCORE=0
  else
    # No fonts = likely scanned, verify with other methods
    SCANNED_SCORE=3
    [ "$MAX_CHARS" -lt 100 ] && ((SCANNED_SCORE++))
    [ "$MAX_WORDS" -lt 20 ] && ((SCANNED_SCORE++))
  fi

  if [ "$SCANNED_SCORE" -ge 3 ]; then
    echo "⚠️  Scanned PDF detected: $pdf"
    echo "   Fonts: $FONT_COUNT, Max chars: $MAX_CHARS, Max words: $MAX_WORDS, Pages: $PAGE_COUNT"
    echo "   Score: $SCANNED_SCORE/5 (≥3 = scanned)"

    # Rename with scanned- prefix
    NEW_NAME="scanned-${pdf}"
    mv "$pdf" "$NEW_NAME"
    echo "   ✅ Renamed to: $NEW_NAME"
    echo ""

    ((SCANNED_COUNT++))
  else
    echo "✓  Native text PDF: $pdf"
    echo "   Fonts: $FONT_COUNT, Max chars: $MAX_CHARS, Max words: $MAX_WORDS (Score: $SCANNED_SCORE/5)"
    ((NATIVE_COUNT++))
  fi
done

echo ""
echo "="
echo "Summary:"
echo "  Total PDFs scanned: $TOTAL_FILES"
echo "  Scanned (no text layer): $SCANNED_COUNT"
echo "  Native (with text): $NATIVE_COUNT"
echo ""

if [ "$SCANNED_COUNT" -gt 0 ]; then
  echo "⚠️  $SCANNED_COUNT scanned PDF(s) found and prefixed with 'scanned-'"
  echo "   These files may need OCR processing for full-text search"
else
  echo "✅ All PDFs have native text layers"
fi
