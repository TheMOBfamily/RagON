from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path


def _load_env_from_ragon_root() -> None:
    """Load .env from RAGON_ROOT (portable)."""
    # Find RAGON_ROOT: go up from src/ to multi-query/ to RagON/
    current = Path(__file__).resolve().parent
    for _ in range(3):  # Try up to 3 levels
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


# Load environment on module import
_load_env_from_ragon_root()


def getenv_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass
class MultiRAGSettings:
    """Settings for multi-source RAG query system"""
    base_rag_dir: str = os.getenv(
        "MULTI_RAG_BASE_DIR",
        os.getenv("DKM_PDF_PATH", "")
    )
    max_workers: int = getenv_int("MULTI_RAG_WORKERS", 4)
    # TOP_K configuration
    # For small scale (5-10 sources): TOP_K=8 is optimal
    # For large scale (200-300 sources): TOP_K=3 recommended (see PERPLEXITY_RESEARCH_TOP_K.md)
    # Total chunks = sources × TOP_K (before dedup)
    top_k_per_source: int = getenv_int("MULTI_RAG_TOP_K", 3)
    timeout_per_source: int = getenv_int("MULTI_RAG_TIMEOUT", 30)
    chunk_size: int = getenv_int("CHUNK_SIZE", 1200)
    chunk_overlap: int = getenv_int("CHUNK_OVERLAP", 150)
    query_all_by_default: bool = True  # KISS: Always query all folders
    
    def validate(self) -> None:
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be < CHUNK_SIZE")
        if self.max_workers < 1:
            raise ValueError("MULTI_RAG_WORKERS must be >= 1")
        if self.top_k_per_source < 1:
            raise ValueError("MULTI_RAG_TOP_K must be >= 1")


def get_settings() -> MultiRAGSettings:
    s = MultiRAGSettings()
    s.validate()
    return s
