#!/bin/bash
# load-env.sh - Portable environment loader for RagON project
# Usage: source "$(dirname "$0")/../load-env.sh" (from any script)
# Or:    source /path/to/RagON/load-env.sh

# Find RAGON_ROOT (directory containing this script)
# Use _LOADENV_DIR to avoid conflict with caller's SCRIPT_DIR
if [[ -n "${BASH_SOURCE[0]}" ]]; then
    _LOADENV_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
    _LOADENV_DIR="$(cd "$(dirname "$0")" && pwd)"
fi

# Try to find .env in order of preference
ENV_FILE=""
if [[ -f "$_LOADENV_DIR/.env" ]]; then
    ENV_FILE="$_LOADENV_DIR/.env"
elif [[ -f "$_LOADENV_DIR/../.env" ]]; then
    ENV_FILE="$(cd "$_LOADENV_DIR/.." && pwd)/.env"
elif [[ -n "$RAGON_ROOT" && -f "$RAGON_ROOT/.env" ]]; then
    ENV_FILE="$RAGON_ROOT/.env"
fi

if [[ -z "$ENV_FILE" ]]; then
    echo "ERROR: Cannot find .env file" >&2
    echo "Expected at: $_LOADENV_DIR/.env" >&2
    return 1 2>/dev/null || exit 1
fi

# Export RAGON_ROOT based on .env location
export RAGON_ROOT="$(dirname "$ENV_FILE")"

# Source .env and export all variables
set -a
source "$ENV_FILE"
set +a

# Validate critical paths exist
if [[ ! -d "$DKM_PDF_PATH" ]]; then
    echo "WARNING: DKM_PDF_PATH does not exist: $DKM_PDF_PATH" >&2
fi

if [[ ! -d "$VENV_PATH" ]]; then
    echo "WARNING: VENV_PATH does not exist: $VENV_PATH" >&2
fi

# Helper function: activate venv
activate_venv() {
    if [[ -f "$VENV_PATH/bin/activate" ]]; then
        source "$VENV_PATH/bin/activate"
    else
        echo "ERROR: venv not found at $VENV_PATH" >&2
        return 1
    fi
}

export -f activate_venv
