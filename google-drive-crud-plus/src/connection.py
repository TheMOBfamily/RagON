"""Connection module for Google Drive via gvfs/gio.

Handles mounting, unmounting, and connection verification.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

from .config import GDriveConfig


class GDriveConnection:
    """Manages Google Drive connection via gvfs/gio."""

    def __init__(self, config: GDriveConfig) -> None:
        """Initialize connection manager.

        Args:
            config: GDrive configuration instance.
        """
        self.config = config

    def is_mounted(self) -> bool:
        """Check if Google Drive is mounted.

        Returns:
            True if mounted, False otherwise.
        """
        if self.config.mount_path is None:
            return False

        return self.config.mount_path.exists()

    def mount(self) -> bool:
        """Mount Google Drive using gio.

        Returns:
            True if successful, False otherwise.
        """
        uri = f"google-drive://{self.config.email}/"

        try:
            result = subprocess.run(
                ["gio", "mount", uri],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def unmount(self) -> bool:
        """Unmount Google Drive using gio.

        Returns:
            True if successful, False otherwise.
        """
        uri = f"google-drive://{self.config.email}/"

        try:
            result = subprocess.run(
                ["gio", "mount", "-u", uri],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def list_mounts(self) -> list[str]:
        """List all gvfs mounts.

        Returns:
            List of mount URIs.
        """
        try:
            result = subprocess.run(
                ["gio", "mount", "-l"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                # Parse output to extract mount URIs
                lines = result.stdout.strip().split("\n")
                return [line.strip() for line in lines if "google-drive" in line]

            return []
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []

    def get_drive_uri(self, relative_path: str = "") -> str:
        """Get gio URI for a path in Google Drive.

        Args:
            relative_path: Path relative to Drive root.

        Returns:
            Full gio URI.
        """
        base_uri = f"google-drive://{self.config.email}"
        if relative_path:
            return f"{base_uri}/{relative_path}"
        return f"{base_uri}/"
