"""Search module for Google Drive files.

Provides search by name, extension, size, and content patterns.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Generator

from .config import GDriveConfig


class GDriveSearch:
    """Search operations for Google Drive files."""

    def __init__(self, config: GDriveConfig) -> None:
        """Initialize search operations.

        Args:
            config: GDrive configuration instance.
        """
        self.config = config

    def by_name(
        self,
        pattern: str,
        search_path: str = "",
        case_sensitive: bool = False,
    ) -> list[Path]:
        """Search files by name pattern.

        Args:
            pattern: Search pattern (supports wildcards).
            search_path: Directory to search in (default: root).
            case_sensitive: Case-sensitive matching.

        Returns:
            List of matching file paths.
        """
        base_path = self.config.get_full_path(search_path)

        if not base_path.exists():
            return []

        flags = 0 if case_sensitive else re.IGNORECASE
        regex = re.compile(pattern.replace("*", ".*"), flags)

        matches = []
        try:
            for item in base_path.rglob("*"):
                if regex.search(item.name):
                    matches.append(item)
        except Exception:
            pass

        return matches

    def by_extension(
        self,
        extension: str,
        search_path: str = "",
    ) -> list[Path]:
        """Search files by extension.

        Args:
            extension: File extension (with or without dot).
            search_path: Directory to search in.

        Returns:
            List of matching file paths.
        """
        if not extension.startswith("."):
            extension = f".{extension}"

        base_path = self.config.get_full_path(search_path)

        if not base_path.exists():
            return []

        try:
            return list(base_path.rglob(f"*{extension}"))
        except Exception:
            return []

    def by_size(
        self,
        min_size: Optional[int] = None,
        max_size: Optional[int] = None,
        search_path: str = "",
    ) -> list[Path]:
        """Search files by size range.

        Args:
            min_size: Minimum file size in bytes.
            max_size: Maximum file size in bytes.
            search_path: Directory to search in.

        Returns:
            List of matching file paths.
        """
        base_path = self.config.get_full_path(search_path)

        if not base_path.exists():
            return []

        matches = []
        try:
            for item in base_path.rglob("*"):
                if not item.is_file():
                    continue

                size = item.stat().st_size

                if min_size is not None and size < min_size:
                    continue
                if max_size is not None and size > max_size:
                    continue

                matches.append(item)
        except Exception:
            pass

        return matches

    def pdfs_only(self, search_path: str = "") -> list[Path]:
        """Search for PDF files only.

        Args:
            search_path: Directory to search in.

        Returns:
            List of PDF file paths.
        """
        return self.by_extension(".pdf", search_path)

    def walk(
        self,
        search_path: str = "",
    ) -> Generator[tuple[Path, list[Path], list[Path]], None, None]:
        """Walk through directory tree like os.walk.

        Args:
            search_path: Directory to walk.

        Yields:
            Tuple of (dirpath, dirnames, filenames).
        """
        base_path = self.config.get_full_path(search_path)

        if not base_path.exists() or not base_path.is_dir():
            return

        try:
            for dirpath in base_path.rglob("*"):
                if not dirpath.is_dir():
                    continue

                dirs = [d for d in dirpath.iterdir() if d.is_dir()]
                files = [f for f in dirpath.iterdir() if f.is_file()]

                yield (dirpath, dirs, files)
        except Exception:
            pass
