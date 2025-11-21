from __future__ import annotations
import os
from dataclasses import dataclass


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
        "/home/fong/Projects/mini-rag/DKM-PDFs"
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
