#!/bin/bash
# find-duplicates-in-folder.sh
# Find duplicate PDF files within a folder using MD5 hash
# Version: 1.0.0
# Date: 2025-10-28

set -euo pipefail

TARGET_FOLDER="${1:-.}"

echo "🔍 Scanning for duplicates in: $TARGET_FOLDER"
echo ""

cd "$TARGET_FOLDER"

# Generate hash list
echo "Computing MD5 hashes..."
find . -maxdepth 1 -type f \( -name "*.PDF" -o -name "*.pdf" \) -exec md5sum {} \; > /tmp/hash-list.txt

# Find duplicate hashes
DUPLICATES=$(awk '{print $1}' /tmp/hash-list.txt | sort | uniq -cd)

if [ -n "$DUPLICATES" ]; then
  echo "⚠️  Duplicates found:"
  echo ""

  # Show files for each duplicate hash
  while read count hash; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Hash: $hash (appears $count times)"
    grep "^$hash" /tmp/hash-list.txt | awk '{$1=""; print "  📄" $0}'
    echo ""
  done <<< "$DUPLICATES"
else
  echo "✅ No duplicates found in folder"
fi

rm /tmp/hash-list.txt
