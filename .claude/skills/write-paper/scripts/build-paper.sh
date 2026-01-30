#!/bin/bash
# =============================================================================
# Build Paper Script
# Compile LaTeX paper with XeLaTeX + Biber
# =============================================================================

set -e

# Check arguments
if [ -z "$1" ]; then
    echo "Usage: $0 <main.tex>"
    echo "Example: $0 paper/main.tex"
    exit 1
fi

MAIN_TEX="$1"
MAIN_NAME="${MAIN_TEX%.tex}"

# Check file exists
if [ ! -f "$MAIN_TEX" ]; then
    echo "Error: File not found: $MAIN_TEX"
    exit 1
fi

# Get directory
DIR=$(dirname "$MAIN_TEX")
cd "$DIR"

# Compile
echo "=== Building: $MAIN_TEX ==="

echo "[1/4] First XeLaTeX pass..."
xelatex -interaction=nonstopmode "$(basename "$MAIN_TEX")"

echo "[2/4] Running Biber..."
biber "$(basename "$MAIN_NAME")" || echo "Warning: Biber failed (may be no citations)"

echo "[3/4] Second XeLaTeX pass..."
xelatex -interaction=nonstopmode "$(basename "$MAIN_TEX")"

echo "[4/4] Third XeLaTeX pass..."
xelatex -interaction=nonstopmode "$(basename "$MAIN_TEX")"

echo "=== Build complete: ${MAIN_NAME}.pdf ==="

# Check output
if [ -f "${MAIN_NAME}.pdf" ]; then
    echo "Output: $(readlink -f "${MAIN_NAME}.pdf")"
    ls -lh "${MAIN_NAME}.pdf"
else
    echo "Error: PDF not generated"
    exit 1
fi
