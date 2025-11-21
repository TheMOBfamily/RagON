from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


def _load_env_from_ragon_root() -> None:
    """Load .env from RAGON_ROOT."""
    current = Path(__file__).resolve().parent
    for _ in range(5):
        env_file = current / ".env"
        if env_file.exists():
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, _, value = line.partition("=")
                        os.environ.setdefault(key.strip(), value.strip().strip('"'))
            break
        current = current.parent


_load_env_from_ragon_root()


def getenv_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass
class Settings:
    """Settings for Mini-RAG retrieval system (no LLM generation)"""
    hf_embeddings_model: str = os.getenv(
        "HF_EMBEDDINGS_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
    )
    chunk_size: int = getenv_int("CHUNK_SIZE", 1200)
    chunk_overlap: int = getenv_int("CHUNK_OVERLAP", 150)
    top_k: int = getenv_int("TOP_K", 5)  # Changed from 4 to 5 based on Perplexity research (2025-10-26)

    # Directories that should NEVER be rebuilt (read-only mode)
    # TEMPORARILY EMPTY to allow initial build
    no_train_dirs: List[str] = field(default_factory=lambda: [])

    # Shared Memory Cache Settings (/tmp/)
    # Best practices from DKM research + industry standards
    cache_enabled: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    cache_ttl_hours: int = getenv_int("CACHE_TTL_HOURS", 24)  # 24h = balance freshness & performance
    cache_safe_threshold_percent: int = getenv_int("CACHE_SAFE_THRESHOLD_PERCENT", 80)  # Use max 80% of /tmp/ (20% buffer)
    cache_min_free_space_mb: int = getenv_int("CACHE_MIN_FREE_SPACE_MB", 500)  # Keep minimum 500MB free

    def validate(self) -> None:
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be < CHUNK_SIZE")


def get_settings() -> Settings:
    s = Settings()
    s.validate()
    return s