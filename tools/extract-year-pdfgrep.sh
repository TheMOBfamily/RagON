#!/bin/bash
# extract-year-pdfgrep.sh v2.0
# Extract publication year from PDF content using pdfgrep
# Optimized: Focus on © symbol proximity (năm luôn nằm NGAY SAU ©)
# Usage: bash extract-year-pdfgrep.sh <file.PDF>
# Output: YYYY or "UNKNOWN"

set -euo pipefail

PDF="$1"

# Validation
if [ ! -f "$PDF" ]; then
    echo "ERROR: File not found: $PDF" >&2
    echo "UNKNOWN"
    exit 1
fi

# Check if pdfgrep is available
if ! command -v pdfgrep &> /dev/null; then
    echo "ERROR: pdfgrep not installed (apt install pdfgrep)" >&2
    echo "UNKNOWN"
    exit 1
fi

# Method 1: © symbol + IMMEDIATE year (highest success ~95%)
# Pattern: "Copyright © 2022" or "© 2022" - year appears within 0-10 chars after ©
YEAR=$(pdfgrep "©" "$PDF" 2>/dev/null | grep -oE "©\s*(19|20)[0-9]{2}" | grep -oE "(19|20)[0-9]{2}" | head -1)
if [ -n "$YEAR" ]; then
    # Validate year range (1900-2029)
    if [ "$YEAR" -ge 1900 ] && [ "$YEAR" -le 2029 ]; then
        echo "$YEAR"
        exit 0
    fi
fi

# Method 2: Copyright © + year (~90%)
YEAR=$(pdfgrep -i "copyright\s*©" "$PDF" 2>/dev/null | grep -oE "(19|20)[0-9]{2}" | head -1)
if [ -n "$YEAR" ]; then
    if [ "$YEAR" -ge 1900 ] && [ "$YEAR" -le 2029 ]; then
        echo "$YEAR"
        exit 0
    fi
fi

# Method 3: Published + year (~40%)
YEAR=$(pdfgrep -i "published.*20[12][0-9]" "$PDF" 2>/dev/null | grep -oE "20[12][0-9]" | head -1)
if [ -n "$YEAR" ]; then
    if [ "$YEAR" -ge 1900 ] && [ "$YEAR" -le 2029 ]; then
        echo "$YEAR"
        exit 0
    fi
fi

# Method 4: Broader copyright search (last resort)
YEAR=$(pdfgrep -i "copyright.*20[12][0-9]" "$PDF" 2>/dev/null | grep -oE "20[12][0-9]" | head -1)
if [ -n "$YEAR" ]; then
    if [ "$YEAR" -ge 1900 ] && [ "$YEAR" -le 2029 ]; then
        echo "$YEAR"
        exit 0
    fi
fi

# All methods failed
echo "UNKNOWN"
exit 1
