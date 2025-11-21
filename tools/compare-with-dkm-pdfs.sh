#!/bin/bash
# compare-with-dkm-pdfs.sh
# Compare new books folder with DKM-PDFs collection to find truly new books
# Version: 1.0.0
# Author: Fong
# Date: 2025-10-28

set -euo pipefail

NEW_FOLDER="/home/fong/Dropbox/PDFs/new"
DKM_FOLDER="/home/fong/Projects/mini-rag/DKM-PDFs"
REPORT_FILE="/tmp/new-books-report.txt"

echo "🔍 Comparing new books with DKM-PDFs collection..."
echo "" > "$REPORT_FILE"

# Check if folders exist
if [ ! -d "$NEW_FOLDER" ]; then
  echo "❌ Error: New folder not found: $NEW_FOLDER"
  exit 1
fi

if [ ! -d "$DKM_FOLDER" ]; then
  echo "❌ Error: DKM folder not found: $DKM_FOLDER"
  exit 1
fi

# Generate hash lists
echo "Computing MD5 hashes..."
(cd "$NEW_FOLDER" && find . -maxdepth 1 -type f -name "*.PDF" -exec md5sum {} \; 2>/dev/null) | sort > /tmp/new-hashes.txt
(cd "$DKM_FOLDER" && find . -maxdepth 1 -type f -name "*.PDF" -exec md5sum {} \; 2>/dev/null) | sort > /tmp/dkm-hashes.txt

# Count files
NEW_COUNT=$(wc -l < /tmp/new-hashes.txt)
DKM_COUNT=$(wc -l < /tmp/dkm-hashes.txt)

echo "  New folder: $NEW_COUNT PDFs"
echo "  DKM folder: $DKM_COUNT PDFs"
echo ""

# Find exact hash matches
echo "Checking for exact duplicates (same MD5 hash)..."
EXACT_DUPES=$(comm -12 <(awk '{print $1}' /tmp/new-hashes.txt) <(awk '{print $1}' /tmp/dkm-hashes.txt) || true)

EXACT_COUNT=0
if [ -n "$EXACT_DUPES" ]; then
  echo "⚠️  Exact duplicates found (same MD5 hash):" | tee -a "$REPORT_FILE"
  while IFS= read -r hash; do
    NEW_FILE=$(grep "^$hash" /tmp/new-hashes.txt | awk '{print $2}' | sed 's|^\./||')
    DKM_FILE=$(grep "^$hash" /tmp/dkm-hashes.txt | awk '{print $2}' | sed 's|^\./||')
    echo "  Hash: $hash" | tee -a "$REPORT_FILE"
    echo "    New: $NEW_FILE" | tee -a "$REPORT_FILE"
    echo "    DKM: $DKM_FILE" | tee -a "$REPORT_FILE"
    echo "" | tee -a "$REPORT_FILE"
    ((EXACT_COUNT++))
  done <<< "$EXACT_DUPES"
else
  echo "✅ No exact hash duplicates" | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
fi

# Find filename similarities (potential duplicates)
echo "Checking for filename similarities..." | tee -a "$REPORT_FILE"
NEW_FILES=$(cd "$NEW_FOLDER" && ls -1 *.PDF 2>/dev/null || true)
DKM_FILES=$(cd "$DKM_FOLDER" && ls -1 *.PDF 2>/dev/null || true)

SIMILAR_COUNT=0
# Extract title patterns (everything after year and before author)
# Example: 2023-Causal-Inference-and-Discovery-... → "Causal-Inference"
while IFS= read -r new_file; do
  [ -z "$new_file" ] && continue

  # Extract key words from title (first 2-3 significant words)
  TITLE_PATTERN=$(echo "$new_file" | sed 's/^[0-9]\{4\}-//' | sed 's/-.*//' | cut -d'-' -f1-3)

  # Skip if pattern too short
  [ ${#TITLE_PATTERN} -lt 5 ] && continue

  # Search for similar titles in DKM
  SIMILAR=$(echo "$DKM_FILES" | grep -i "$TITLE_PATTERN" || true)

  if [ -n "$SIMILAR" ]; then
    # Check if it's not an exact duplicate (already reported)
    NEW_HASH=$(grep "$new_file" /tmp/new-hashes.txt | awk '{print $1}')
    IS_EXACT=$(echo "$EXACT_DUPES" | grep -c "^$NEW_HASH$" || true)

    if [ "$IS_EXACT" -eq 0 ]; then
      echo "⚠️  Potential duplicate (similar title):" | tee -a "$REPORT_FILE"
      echo "    New: $new_file" | tee -a "$REPORT_FILE"
      echo "    DKM: $SIMILAR" | tee -a "$REPORT_FILE"
      echo "    → Manual verification needed (compare first page)" | tee -a "$REPORT_FILE"
      echo "" | tee -a "$REPORT_FILE"
      ((SIMILAR_COUNT++))
    fi
  fi
done <<< "$NEW_FILES"

if [ "$SIMILAR_COUNT" -eq 0 ]; then
  echo "✅ No similar filenames found" | tee -a "$REPORT_FILE"
  echo "" | tee -a "$REPORT_FILE"
fi

# List truly new books (no hash or filename match)
echo "✅ Truly NEW books (not in DKM-PDFs):" | tee -a "$REPORT_FILE"
TRULY_NEW=0

while IFS= read -r new_file; do
  [ -z "$new_file" ] && continue

  HASH=$(grep "$new_file" /tmp/new-hashes.txt | awk '{print $1}')

  # Check if hash exists in DKM
  if ! grep -q "^$HASH" /tmp/dkm-hashes.txt; then
    # Extract title for similarity check
    TITLE_PATTERN=$(echo "$new_file" | sed 's/^[0-9]\{4\}-//' | sed 's/-.*//' | cut -d'-' -f1-3)

    # Check if similar title exists (loose match)
    if ! echo "$DKM_FILES" | grep -qi "$TITLE_PATTERN"; then
      echo "  ✅ $new_file" | tee -a "$REPORT_FILE"
      ((TRULY_NEW++))
    fi
  fi
done <<< "$NEW_FILES"

echo ""
echo "=" | tee -a "$REPORT_FILE"
echo "Summary:" | tee -a "$REPORT_FILE"
echo "  Total new files: $NEW_COUNT" | tee -a "$REPORT_FILE"
echo "  Total DKM files: $DKM_COUNT" | tee -a "$REPORT_FILE"
echo "  Exact duplicates: $EXACT_COUNT" | tee -a "$REPORT_FILE"
echo "  Similar filenames (manual check): $SIMILAR_COUNT" | tee -a "$REPORT_FILE"
echo "  Truly new books: $TRULY_NEW" | tee -a "$REPORT_FILE"
echo ""
echo "📄 Full report saved to: $REPORT_FILE"

# Cleanup
rm -f /tmp/new-hashes.txt /tmp/dkm-hashes.txt

echo ""
echo "Next steps:"
echo "  1. Review potential duplicates manually (compare first page)"
echo "  2. Copy truly new books to DKM-PDFs:"
echo "     cp /home/fong/Dropbox/PDFs/new/YYYY-*.PDF /home/fong/Projects/mini-rag/DKM-PDFs/"
echo "  3. Commit changes: cd /home/fong/Projects/mini-rag && git add DKM-PDFs/ && git commit"
