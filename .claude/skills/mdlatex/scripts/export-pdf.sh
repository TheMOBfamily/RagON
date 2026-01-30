#!/bin/bash
# Quick export helper for Textor Doc Converter
# Usage: ./export-pdf.sh <file.md> [icon]
# Icons: hub, buh, deutschfuns, de, irontan, nexiumlab

TEXTOR="/home/fong/Projects/textor-doc-converter/run-807f321188c6.sh"

if [ -z "$1" ]; then
    echo "Usage: $0 <file.md> [icon]"
    echo "Icons: hub, buh, deutschfuns, de, irontan, nexiumlab"
    exit 1
fi

FILE="$1"
ICON="$2"

if [ ! -f "$FILE" ]; then
    echo "Error: File not found: $FILE"
    exit 1
fi

if [ -n "$ICON" ]; then
    $TEXTOR "{\"command\":\"export-md-to-pdf\",\"data\":\"$FILE\",\"icon\":\"$ICON\"}"
else
    $TEXTOR "{\"command\":\"export-md-to-pdf\",\"data\":\"$FILE\"}"
fi
