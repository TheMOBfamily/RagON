#!/bin/bash
# convert-djvu-to-pdf.sh
# Convert DJVU files to PDF using ddjvu command
# Version: 1.0.0
# Date: 2025-10-28

set -euo pipefail

# Check if ddjvu is installed
if ! command -v ddjvu &> /dev/null; then
    echo "❌ Error: ddjvu not found"
    echo "Please install djvulibre-bin:"
    echo "  sudo apt-get install -y djvulibre-bin"
    exit 1
fi

TARGET_FOLDER="${1:-.}"

echo "🔄 Converting DJVU files to PDF in: $TARGET_FOLDER"
echo ""

cd "$TARGET_FOLDER"

CONVERTED=0
FAILED=0

shopt -s nullglob
for djvu in *.djvu *.DJVU; do
    [ ! -f "$djvu" ] && continue

    # Generate output PDF filename
    pdf="${djvu%.*}.pdf"

    echo "Converting: $djvu → $pdf"

    if ddjvu -format=pdf -quality=85 "$djvu" "$pdf"; then
        echo "✅ Success: $pdf"
        ((CONVERTED++))
    else
        echo "❌ Failed: $djvu"
        ((FAILED++))
    fi
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Summary:"
echo "  Converted: $CONVERTED"
echo "  Failed: $FAILED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
