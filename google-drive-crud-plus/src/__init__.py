"""
Google Drive CRUD Plus - A Python library for Google Drive operations via gvfs.

Provides CRUD operations, checksum verification, and search functionality
for files on Google Drive mounted through GNOME gvfs.
"""

from __future__ import annotations

__version__ = "0.1.0"
__author__ = "Fong"

from .config import GDriveConfig
from .connection import GDriveConnection
from .crud import GDriveCRUD
from .checksum import GDriveChecksum
from .search import GDriveSearch
from .envloader import load_env, load_env_file, get_env

__all__ = [
    "GDriveConfig",
    "GDriveConnection",
    "GDriveCRUD",
    "GDriveChecksum",
    "GDriveSearch",
    "load_env",
    "load_env_file",
    "get_env",
]
