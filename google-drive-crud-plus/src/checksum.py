"""Checksum and hashing module for Google Drive files.

Provides MD5, SHA256, and other hash calculations for file verification.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Optional, Literal

from .config import GDriveConfig

HashAlgorithm = Literal["md5", "sha1", "sha256", "sha512"]


class GDriveChecksum:
    """Checksum operations for Google Drive files."""

    def __init__(self, config: GDriveConfig) -> None:
        """Initialize checksum operations.

        Args:
            config: GDrive configuration instance.
        """
        self.config = config

    def _calculate_hash(
        self,
        file_path: Path,
        algorithm: HashAlgorithm = "md5",
        chunk_size: int = 8192,
    ) -> Optional[str]:
        """Calculate hash for a file.

        Args:
            file_path: Path to file.
            algorithm: Hash algorithm to use.
            chunk_size: Size of chunks for streaming (default: 8KB).

        Returns:
            Hex digest of hash, or None if failed.
        """
        if not file_path.exists():
            return None

        hash_func = getattr(hashlib, algorithm)()

        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(chunk_size):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception:
            return None

    def md5(self, drive_path: str) -> Optional[str]:
        """Calculate MD5 hash of a file in Google Drive.

        Args:
            drive_path: Path to file in Drive.

        Returns:
            MD5 hash as hex string, or None if failed.
        """
        file_path = self.config.get_full_path(drive_path)
        return self._calculate_hash(file_path, "md5")

    def sha256(self, drive_path: str) -> Optional[str]:
        """Calculate SHA256 hash of a file in Google Drive.

        Args:
            drive_path: Path to file in Drive.

        Returns:
            SHA256 hash as hex string, or None if failed.
        """
        file_path = self.config.get_full_path(drive_path)
        return self._calculate_hash(file_path, "sha256")

    def calculate(
        self,
        drive_path: str,
        algorithm: HashAlgorithm = "md5",
    ) -> Optional[str]:
        """Calculate hash using specified algorithm.

        Args:
            drive_path: Path to file in Drive.
            algorithm: Hash algorithm (md5, sha1, sha256, sha512).

        Returns:
            Hash as hex string, or None if failed.
        """
        file_path = self.config.get_full_path(drive_path)
        return self._calculate_hash(file_path, algorithm)

    def verify(
        self,
        drive_path: str,
        expected_hash: str,
        algorithm: HashAlgorithm = "md5",
    ) -> bool:
        """Verify file hash matches expected value.

        Args:
            drive_path: Path to file in Drive.
            expected_hash: Expected hash value.
            algorithm: Hash algorithm to use.

        Returns:
            True if hash matches, False otherwise.
        """
        actual_hash = self.calculate(drive_path, algorithm)
        if actual_hash is None:
            return False

        return actual_hash.lower() == expected_hash.lower()

    def compare_files(
        self,
        drive_path1: str,
        drive_path2: str,
        algorithm: HashAlgorithm = "md5",
    ) -> bool:
        """Compare two files by hash.

        Args:
            drive_path1: First file path in Drive.
            drive_path2: Second file path in Drive.
            algorithm: Hash algorithm to use.

        Returns:
            True if hashes match, False otherwise.
        """
        hash1 = self.calculate(drive_path1, algorithm)
        hash2 = self.calculate(drive_path2, algorithm)

        if hash1 is None or hash2 is None:
            return False

        return hash1 == hash2
