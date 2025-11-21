from __future__ import annotations
import os
from dataclasses import dataclass


def getenv_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass
class TrainSettings:
    """Settings for training system (copied from minirag, standalone)"""
    hf_embeddings_model: str = os.getenv(
        "HF_EMBEDDINGS_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
    )
    chunk_size: int = getenv_int("CHUNK_SIZE", 1200)
    chunk_overlap: int = getenv_int("CHUNK_OVERLAP", 150)
    pdf_dir: str = os.getenv(
        "TRAIN_PDF_DIR",
        "/home/fong/Projects/mini-rag/DKM-PDFs"
    )
    cache_dir: str = os.getenv(
        "TRAIN_CACHE_DIR",
        "/home/fong/Projects/mini-rag/DKM-PDFs"
    )

    def validate(self) -> None:
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be < CHUNK_SIZE")


def get_settings() -> TrainSettings:
    s = TrainSettings()
    s.validate()
    return s
