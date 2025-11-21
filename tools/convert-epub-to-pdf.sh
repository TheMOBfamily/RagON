#!/bin/bash
# Convert all epub files to PDF in a folder

FOLDER="$1"

if [ -z "$FOLDER" ]; then
    echo "Usage: $0 <folder>"
    exit 1
fi

cd "$FOLDER" || exit 1

for epub in *.epub; do
    [ -f "$epub" ] || continue

    # Skip if PDF already exists
    pdf="${epub%.epub}.pdf"
    if [ -f "$pdf" ]; then
        echo "Skipping (PDF exists): $epub"
        continue
    fi

    echo "Converting: $epub -> $pdf"
    ebook-convert "$epub" "$pdf" --paper-size a4 --pdf-default-font-size 12

    if [ $? -eq 0 ]; then
        echo "✓ Success: $pdf"
    else
        echo "✗ Failed: $epub"
    fi
done

echo "Done!"
