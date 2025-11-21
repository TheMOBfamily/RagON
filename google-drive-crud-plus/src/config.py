"""Configuration module for Google Drive CRUD Plus.

Handles path detection, user configuration, and environment setup.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from .envloader import load_env, get_env


@dataclass
class GDriveConfig:
    """Configuration for Google Drive access via gvfs."""

    email: str
    mount_path: Optional[Path] = None
    uid: Optional[int] = None

    def __post_init__(self) -> None:
        """Auto-detect mount path and UID after initialization."""
        if self.uid is None:
            self.uid = os.getuid()

        if self.mount_path is None:
            self.mount_path = self._detect_mount_path()

    def _detect_mount_path(self) -> Path:
        """Detect gvfs mount path for Google Drive.

        Returns:
            Path to mounted Google Drive directory.

        Raises:
            FileNotFoundError: If Google Drive is not mounted.
        """
        gvfs_base = Path(f"/run/user/{self.uid}/gvfs")

        if not gvfs_base.exists():
            raise FileNotFoundError(
                f"gvfs directory not found: {gvfs_base}. "
                "Is Google Drive mounted in Nautilus?"
            )

        # Try full email format first: google-drive:host=gmail.com,user=email@gmail.com
        mount_name = f"google-drive:host=gmail.com,user={self.email}"
        mount_path = gvfs_base / mount_name

        if mount_path.exists():
            return mount_path

        # Fallback: Try username-only format (gvfs drops @domain)
        # Extract username from email (part before @)
        username = self.email.split("@")[0] if "@" in self.email else self.email
        mount_name_alt = f"google-drive:host=gmail.com,user={username}"
        mount_path_alt = gvfs_base / mount_name_alt

        if mount_path_alt.exists():
            return mount_path_alt

        # Neither format found, list available mounts for debugging
        available = list(gvfs_base.glob("google-drive:*"))
        raise FileNotFoundError(
            f"Google Drive not mounted for {self.email}. "
            f"Available mounts: {[m.name for m in available]}"
        )

    def get_full_path(self, relative_path: str = "") -> Path:
        """Get full path to a file/folder in Google Drive.

        Args:
            relative_path: Path relative to Drive root (default: root).

        Returns:
            Full absolute path to the resource.
        """
        if self.mount_path is None:
            raise ValueError("Mount path not initialized")

        return self.mount_path / relative_path

    @classmethod
    def from_env(cls, email_env: str = "GDRIVE_EMAIL", env_file: Optional[Path] = None) -> GDriveConfig:
        """Create config from environment variable.

        Args:
            email_env: Environment variable name for email.
            env_file: Path to .env file (default: auto-detect).

        Returns:
            Configured GDriveConfig instance.

        Raises:
            ValueError: If email not found in environment.
        """
        if env_file is None:
            script_dir = Path(__file__).parent.parent
            env_file = script_dir / ".env"

        if env_file.exists():
            load_env(env_file)

        email = get_env(email_env)
        if not email:
            raise ValueError(f"Environment variable {email_env} not set")

        return cls(email=email)
