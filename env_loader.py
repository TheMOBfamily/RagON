"""
env_loader.py - Portable environment loader for RagON project
Usage: from env_loader import env, get_path

Loads environment variables from .env file and provides helper functions.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

# Find RAGON_ROOT (directory containing this file)
_THIS_FILE = Path(__file__).resolve()
RAGON_ROOT = _THIS_FILE.parent

# Find .env file
_ENV_FILE: Optional[Path] = None
for candidate in [
    RAGON_ROOT / ".env",
    RAGON_ROOT.parent / ".env",
]:
    if candidate.exists():
        _ENV_FILE = candidate
        break

if _ENV_FILE is None:
    raise FileNotFoundError(f"Cannot find .env file. Expected at: {RAGON_ROOT / '.env'}")


def _load_env_file(env_path: Path) -> dict[str, str]:
    """Parse .env file and return as dict."""
    env_vars = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                env_vars[key] = value
    return env_vars


# Load environment variables
_env_vars = _load_env_file(_ENV_FILE)

# Set environment variables (so os.getenv works)
for key, value in _env_vars.items():
    os.environ.setdefault(key, value)


class EnvConfig:
    """Environment configuration with typed access."""

    def __init__(self, env_vars: dict[str, str]):
        self._env = env_vars

    def get(self, key: str, default: str = "") -> str:
        """Get environment variable."""
        return self._env.get(key, os.environ.get(key, default))

    @property
    def ragon_root(self) -> Path:
        return Path(self.get("RAGON_ROOT", str(RAGON_ROOT)))

    @property
    def dkm_pdf_path(self) -> Path:
        return Path(self.get("DKM_PDF_PATH", str(RAGON_ROOT / "DKM-PDFs")))

    @property
    def venv_path(self) -> Path:
        return Path(self.get("VENV_PATH", str(RAGON_ROOT / "venv")))

    @property
    def log_dir(self) -> Path:
        return Path(self.get("LOG_DIR", str(RAGON_ROOT / "logs")))

    @property
    def dropbox_pdf_path(self) -> Path:
        return Path(self.get("DROPBOX_PDF_PATH", ""))

    @property
    def downloads_dir(self) -> Path:
        return Path(self.get("DOWNLOADS_DIR", str(Path.home() / "Downloads")))


# Singleton instance
env = EnvConfig(_env_vars)


def get_path(key: str) -> Path:
    """Helper to get path from env."""
    value = env.get(key)
    if not value:
        raise ValueError(f"Environment variable {key} not set")
    return Path(value)
