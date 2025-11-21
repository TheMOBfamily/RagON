#!/bin/bash
# PDF Text Converter - Shell wrapper
# Usage: ./main-convert-scanned-pdf-text-pdf-bbe98f8c8221.sh <input.pdf|folder>
# Output: Creates subfolder "output-text-pdfs" in input parent directory

# Get absolute path to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Shared venv path
VENV_PATH="$PROJECT_ROOT/venv"

# Activate virtual environment
if [ ! -d "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    echo "Please create venv: python3 -m venv $VENV_PATH"
    exit 1
fi

source "$VENV_PATH/bin/activate"

# Run Python script with all arguments
python3 "$SCRIPT_DIR/main-132feb25-bbe98f8c8221.py" "$@"

EXIT_CODE=$?

# Deactivate venv
deactivate

exit $EXIT_CODE
