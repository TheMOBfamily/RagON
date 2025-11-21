#!/bin/bash
# backup-books.sh v1.0
# Create timestamped backup before destructive operations
# Usage: bash backup-books.sh [target_dir]
# Default target: current directory

set -euo pipefail

# Target directory (default: current)
TARGET_DIR="${1:-.}"
cd "$TARGET_DIR" || exit 1

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="_backup-${TIMESTAMP}"

echo "📦 Creating backup: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Backup all book files (multiple extensions)
EXTENSIONS=("PDF" "pdf" "epub" "mobi" "EPUB" "MOBI" "fb2" "FB2" "djvu" "DJVU")
TOTAL_COPIED=0

for ext in "${EXTENSIONS[@]}"; do
    # Count files with this extension
    COUNT=$(find . -maxdepth 1 -name "*.$ext" -type f 2>/dev/null | wc -l)

    if [ "$COUNT" -gt 0 ]; then
        # Copy files
        find . -maxdepth 1 -name "*.$ext" -type f -exec cp -v {} "$BACKUP_DIR/" \; 2>/dev/null
        echo "  ✅ Copied $COUNT .$ext files"
        TOTAL_COPIED=$((TOTAL_COPIED + COUNT))
    fi
done

# Verification
BACKUP_COUNT=$(find "$BACKUP_DIR" -type f 2>/dev/null | wc -l)

echo ""
echo "=== Backup Summary ==="
echo "Target directory: $(pwd)"
echo "Backup folder: $BACKUP_DIR"
echo "Total files backed up: $BACKUP_COUNT"

if [ "$BACKUP_COUNT" -eq 0 ]; then
    echo "⚠️  WARNING: No files backed up! (no PDFs/EPUBs/MOBIs found)"
    rmdir "$BACKUP_DIR" 2>/dev/null || true
    exit 1
fi

if [ "$TOTAL_COPIED" -eq "$BACKUP_COUNT" ]; then
    echo "✅ Backup COMPLETE & VERIFIED"
    exit 0
else
    echo "⚠️  WARNING: Count mismatch (Expected: $TOTAL_COPIED, Got: $BACKUP_COUNT)"
    exit 1
fi
