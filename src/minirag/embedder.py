from __future__ import annotations
from typing import Any, List
from .config import get_settings
from rich.console import Console
import os
import math
import hashlib

console = Console()


class DummyHashEmbeddings:
    """Fallback tiny embedding model (not semantic) used when real model unavailable.

    Produces deterministic vectors of fixed size by hashing tokens.
    This is ONLY for local testing when dependencies cannot be installed.
    """

    def __init__(self, dim: int = 384):
        self.dim = dim

    def _embed(self, text: str) -> List[float]:
        vec = [0.0] * self.dim
        if not text:
            return vec
        # simple whitespace tokenization
        tokens = text.lower().split()
        for tok in tokens:
            h = int(hashlib.md5(tok.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dim
            vec[idx] += 1.0
        # l2 normalize
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:  # LangChain style
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed(text)

    # Allow being used where a callable embedding_function is expected
    def __call__(self, text: str) -> List[float]:  # noqa: D401
        return self.embed_query(text)




def _load_huggingface(model_name: str):
    try:
        # Try new langchain-huggingface package first
        from langchain_huggingface import HuggingFaceEmbeddings  # type: ignore
        return HuggingFaceEmbeddings(model_name=model_name)
    except ImportError:
        try:
            # Fallback to old langchain_community
            from langchain_community.embeddings import HuggingFaceEmbeddings  # type: ignore
            return HuggingFaceEmbeddings(model_name=model_name)
        except Exception as e:  # noqa: BLE001
            console.print(
                f"[yellow]Không thể load HuggingFace embeddings ({e}). Dùng DummyHashEmbeddings thay thế tạm thời.[/yellow]"
            )
            return DummyHashEmbeddings()


def get_embeddings() -> Any:
    settings = get_settings()
    # Pure HuggingFace embeddings - no OpenAI
    return _load_huggingface(settings.hf_embeddings_model)
