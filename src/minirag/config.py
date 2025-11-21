from __future__ import annotations
import os
from dataclasses import dataclass, field
from typing import List


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
    no_train_dirs: List[str] = field(default_factory=lambda: [
        "/home/fong/Projects/mini-rag/DKM-PDFs",
    ])

    # Shared Memory Cache Settings (/dev/shm/)
    # Best practices from DKM research + industry standards
    cache_enabled: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    cache_ttl_hours: int = getenv_int("CACHE_TTL_HOURS", 24)  # 24h = balance freshness & performance
    cache_safe_threshold_percent: int = getenv_int("CACHE_SAFE_THRESHOLD_PERCENT", 80)  # Use max 80% of /dev/shm/ (20% buffer)
    cache_min_free_space_mb: int = getenv_int("CACHE_MIN_FREE_SPACE_MB", 500)  # Keep minimum 500MB free

    def validate(self) -> None:
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be < CHUNK_SIZE")


def get_settings() -> Settings:
    s = Settings()
    s.validate()
    return s