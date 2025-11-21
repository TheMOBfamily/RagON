"""Embeddings Service - Singleton pattern for reusing embeddings across multiple indices

Optimization: Load embeddings ONCE, reuse for ALL FAISS indices.

Performance:
- Without service: N × (FAISS_load + embeddings_load) = N × 6s
- With service: embeddings_load + N × FAISS_load = 5.6s + N × 0.022s

Example (30 indices):
- Without: 30 × 6s = 180s
- With: 5.6s + 30 × 0.022s = 6.26s
- Speedup: 28.7x faster!
"""

from __future__ import annotations
from typing import Any, Optional
import time


class EmbeddingsService:
    """Singleton service for reusing embeddings model across multiple FAISS loads."""

    _instance: Optional[EmbeddingsService] = None
    _embeddings: Optional[Any] = None
    _load_time: float = 0.0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_embeddings(self) -> Any:
        """Get or load embeddings model (singleton)."""
        if self._embeddings is None:
            print("🔄 Loading embeddings model (first time)...")
            t_start = time.perf_counter()
            self._embeddings = self._load_embeddings()
            self._load_time = time.perf_counter() - t_start
            print(f"✅ Embeddings loaded in {self._load_time:.3f}s")
        else:
            print(f"♻️  Reusing embeddings (loaded {self._load_time:.3f}s ago)")
        return self._embeddings

    def _load_embeddings(self) -> Any:
        """Internal: Load HuggingFace embeddings."""
        import os
        model_name = os.getenv("HF_EMBEDDINGS_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(model_name=model_name)
        except ImportError:
            try:
                from langchain_community.embeddings import HuggingFaceEmbeddings
                return HuggingFaceEmbeddings(model_name=model_name)
            except Exception as e:
                raise RuntimeError(f"Cannot load HuggingFace embeddings: {e}")

    @classmethod
    def reset(cls):
        """Reset singleton (for testing)."""
        cls._instance = None
        cls._embeddings = None
        cls._load_time = 0.0


# Global instance
_service = EmbeddingsService()


def get_embeddings_service() -> EmbeddingsService:
    """Get global embeddings service."""
    return _service
