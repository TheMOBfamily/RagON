"""Utility functions for Google Drive CRUD Plus.

Helper functions for formatting, logging, and common operations.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """Setup logging configuration.

    Args:
        level: Logging level.
        log_file: Optional log file path.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("gdrive-crud-plus")
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes.

    Returns:
        Formatted size string (e.g., "1.5 MB").
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

    return f"{size_bytes:.2f} PB"


def get_file_info(file_path: Path) -> dict[str, str | int]:
    """Get file information as dictionary.

    Args:
        file_path: Path to file.

    Returns:
        Dictionary with file info (name, size, modified time).
    """
    if not file_path.exists():
        return {}

    stat = file_path.stat()

    return {
        "name": file_path.name,
        "path": str(file_path),
        "size": stat.st_size,
        "size_formatted": format_size(stat.st_size),
        "modified": stat.st_mtime,
        "is_file": file_path.is_file(),
        "is_dir": file_path.is_dir(),
    }


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing invalid characters.

    Args:
        filename: Original filename.

    Returns:
        Sanitized filename safe for filesystem.
    """
    # Remove/replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")

    # Remove leading/trailing spaces and dots
    filename = filename.strip(". ")

    return filename
