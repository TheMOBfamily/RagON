"""Simple .env file loader using stdlib only.

Loads environment variables from .env file without external dependencies.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


def load_env_file(env_path: Optional[Path] = None) -> dict[str, str]:
    """Load environment variables from .env file.

    Args:
        env_path: Path to .env file (default: .env in current dir).

    Returns:
        Dictionary of environment variables.
    """
    if env_path is None:
        env_path = Path.cwd() / ".env"

    if not env_path.exists():
        return {}

    env_vars = {}

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                value = value.strip('"').strip("'")

                env_vars[key] = value

    except Exception:
        pass

    return env_vars


def load_env(env_path: Optional[Path] = None) -> None:
    """Load .env file and set environment variables.

    Args:
        env_path: Path to .env file (default: .env in current dir).
    """
    env_vars = load_env_file(env_path)

    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable value.

    Args:
        key: Environment variable name.
        default: Default value if not found.

    Returns:
        Environment variable value or default.
    """
    return os.getenv(key, default)
