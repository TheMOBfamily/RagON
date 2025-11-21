#!/usr/bin/env bash
#═══════════════════════════════════════════════════════════════════════════════
# Google Drive CRUD Plus - Wrapper Script
#═══════════════════════════════════════════════════════════════════════════════
#
# Purpose: Universal wrapper for google-drive-crud-plus CLI tool
#
# Features:
# - Absolute paths (can be called from anywhere)
# - Auto-activates venv
# - Logs to log/debug.log
# - Follows auto-run-auto-debug-auto-fix mindset
#
# Usage:
#     /path/to/Google-Drive-CRUD.sh <command> [options]
#
# Examples:
#     Google-Drive-CRUD.sh list
#     Google-Drive-CRUD.sh upload /tmp/test.pdf "folder/test.pdf"
#     Google-Drive-CRUD.sh pdfs
#     Google-Drive-CRUD.sh checksum "folder/file.pdf"
#
# Environment:
#     GDRIVE_EMAIL         - Your Google Drive email (REQUIRED)
#     GDRIVE_LOG_LEVEL     - Log level: DEBUG, INFO, WARNING, ERROR (default: INFO)
#
# Setup:
#     export GDRIVE_EMAIL="limpaul.fin@gmail.com"
#
#═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail  # Exit on error, undefined var, pipe failure

#───────────────────────────────────────────────────────────────────────────────
# Constants (Absolute Paths)
#───────────────────────────────────────────────────────────────────────────────

# Get script directory (absolute path resolution)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Main Python script
MAIN_SCRIPT="${SCRIPT_DIR}/main-3d72f3ba212d.py"

# Virtual environment
VENV_DIR="${SCRIPT_DIR}/venv"
VENV_PYTHON="${VENV_DIR}/bin/python3"

# Log directory and file
LOG_DIR="${SCRIPT_DIR}/log"
DEBUG_LOG="${LOG_DIR}/debug.log"

#───────────────────────────────────────────────────────────────────────────────
# Functions
#───────────────────────────────────────────────────────────────────────────────

log_info() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] [INFO] $*" | tee -a "${DEBUG_LOG}"
}

log_error() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] [ERROR] $*" | tee -a "${DEBUG_LOG}" >&2
}

check_prerequisites() {
    # Check if all prerequisites are met.

    # Check if venv exists
    if [[ ! -d "${VENV_DIR}" ]]; then
        log_error "Virtual environment not found: ${VENV_DIR}"
        log_info "Creating venv..."

        python3 -m venv "${VENV_DIR}" || {
            log_error "Failed to create venv"
            return 1
        }

        log_info "✅ venv created successfully"
    fi

    # Check if Python script exists
    if [[ ! -f "${MAIN_SCRIPT}" ]]; then
        log_error "Main script not found: ${MAIN_SCRIPT}"
        return 1
    fi

    # Create log directory if needed
    mkdir -p "${LOG_DIR}"

    # Note: GDRIVE_EMAIL can be set via environment variable OR .env file
    # Python script will handle loading from .env if not in environment

    return 0
}

activate_venv() {
    # Activate virtual environment.

    if [[ ! -f "${VENV_PYTHON}" ]]; then
        log_error "Python executable not found in venv: ${VENV_PYTHON}"
        return 1
    fi

    log_info "Activating venv: ${VENV_DIR}"

    # No need to source activate, we can call python directly
    export VIRTUAL_ENV="${VENV_DIR}"
    export PATH="${VENV_DIR}/bin:${PATH}"

    return 0
}

run_main_script() {
    # Run the main Python script with all arguments.

    log_info "Running: ${MAIN_SCRIPT} $*"
    log_info "Logging to: ${DEBUG_LOG}"

    # Execute with venv Python
    "${VENV_PYTHON}" "${MAIN_SCRIPT}" "$@" 2>&1 | tee -a "${DEBUG_LOG}"

    local exit_code=${PIPESTATUS[0]}

    if [[ ${exit_code} -eq 0 ]]; then
        log_info "✅ Command completed successfully"
    else
        log_error "❌ Command failed with exit code: ${exit_code}"
    fi

    return ${exit_code}
}

show_usage() {
    cat <<EOF
Google Drive CRUD Plus - CLI Wrapper

Usage:
    $(basename "$0") <command> [options]

Commands:
    list [path]              - List files in directory
    upload <local> <remote>  - Upload file to Drive
    download <remote> <local> - Download file from Drive
    delete <path>            - Delete file/folder
    checksum <path>          - Calculate MD5/SHA256 hash
    search <pattern>         - Search files by name
    pdfs [path]              - List all PDF files

Environment:
    GDRIVE_EMAIL             - Google Drive email (REQUIRED)
    GDRIVE_LOG_LEVEL         - Log level (default: INFO)

Setup (choose one):
    1. Via environment variable:
       export GDRIVE_EMAIL="your@gmail.com"

    2. Via .env file (recommended):
       Create .env file with:
       GDRIVE_EMAIL=your@gmail.com

Examples:
    $0 list
    $0 upload /tmp/test.pdf "folder/test.pdf"
    $0 pdfs
    $0 checksum "folder/file.pdf"
    $0 search "*python*"

Logs:
    Debug log: ${DEBUG_LOG}

EOF
}

#───────────────────────────────────────────────────────────────────────────────
# Main Execution
#───────────────────────────────────────────────────────────────────────────────

main() {
    # Show usage if no arguments
    if [[ $# -eq 0 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
        show_usage
        return 0
    fi

    # Initialize log file with header
    {
        echo ""
        echo "═══════════════════════════════════════════════════════════════════════════════"
        echo "Google Drive CRUD Plus - Session Start"
        echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "Command: $0 $*"
        echo "Working Dir: $(pwd)"
        echo "Script Dir: ${SCRIPT_DIR}"
        echo "═══════════════════════════════════════════════════════════════════════════════"
        echo ""
    } >> "${DEBUG_LOG}"

    # Run prerequisite checks
    check_prerequisites || return 1

    # Activate venv
    activate_venv || return 1

    # Run main script
    run_main_script "$@"

    return $?
}

#───────────────────────────────────────────────────────────────────────────────
# Entry Point
#───────────────────────────────────────────────────────────────────────────────

main "$@"
exit $?
