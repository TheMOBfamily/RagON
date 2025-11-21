"""CRUD operations module for Google Drive files.

Provides Create, Read, Update, Delete functionality via gvfs.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Optional, Union

from .config import GDriveConfig


class GDriveCRUD:
    """CRUD operations for Google Drive files via gvfs."""

    def __init__(self, config: GDriveConfig) -> None:
        """Initialize CRUD operations.

        Args:
            config: GDrive configuration instance.
        """
        self.config = config

    def create_folder(self, folder_path: str) -> bool:
        """Create a folder in Google Drive.

        Args:
            folder_path: Path to folder relative to Drive root.

        Returns:
            True if successful, False otherwise.
        """
        full_path = self.config.get_full_path(folder_path)

        try:
            full_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False

    def upload_file(
        self,
        local_path: Union[str, Path],
        drive_path: str,
    ) -> bool:
        """Upload a file to Google Drive.

        Args:
            local_path: Local file path.
            drive_path: Destination path in Drive.

        Returns:
            True if successful, False otherwise.
        """
        local_file = Path(local_path)
        if not local_file.exists():
            return False

        drive_file = self.config.get_full_path(drive_path)

        try:
            # Create parent directories if needed
            drive_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(local_file, drive_file)
            return True
        except Exception:
            return False

    def read_file(self, drive_path: str) -> Optional[bytes]:
        """Read a file from Google Drive.

        Args:
            drive_path: Path to file in Drive.

        Returns:
            File content as bytes, or None if failed.
        """
        drive_file = self.config.get_full_path(drive_path)

        if not drive_file.exists():
            return None

        try:
            return drive_file.read_bytes()
        except Exception:
            return None

    def download_file(
        self,
        drive_path: str,
        local_path: Union[str, Path],
    ) -> bool:
        """Download a file from Google Drive.

        Args:
            drive_path: Path to file in Drive.
            local_path: Local destination path.

        Returns:
            True if successful, False otherwise.
        """
        drive_file = self.config.get_full_path(drive_path)

        if not drive_file.exists():
            return False

        local_file = Path(local_path)

        try:
            local_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(drive_file, local_file)
            return True
        except Exception:
            return False

    def delete_file(self, drive_path: str) -> bool:
        """Delete a file from Google Drive.

        Args:
            drive_path: Path to file in Drive.

        Returns:
            True if successful, False otherwise.
        """
        drive_file = self.config.get_full_path(drive_path)

        if not drive_file.exists():
            return False

        try:
            if drive_file.is_file():
                drive_file.unlink()
            elif drive_file.is_dir():
                shutil.rmtree(drive_file)
            return True
        except Exception:
            return False

    def list_files(self, drive_path: str = "") -> list[Path]:
        """List files in a Google Drive directory.

        Args:
            drive_path: Path to directory in Drive.

        Returns:
            List of file paths.
        """
        drive_dir = self.config.get_full_path(drive_path)

        if not drive_dir.exists() or not drive_dir.is_dir():
            return []

        try:
            return list(drive_dir.iterdir())
        except Exception:
            return []

    def file_exists(self, drive_path: str) -> bool:
        """Check if a file exists in Google Drive.

        Args:
            drive_path: Path to file in Drive.

        Returns:
            True if exists, False otherwise.
        """
        drive_file = self.config.get_full_path(drive_path)
        return drive_file.exists()
