from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path


def _load_env_from_ragon_root() -> None:
    """Load .env from RAGON_ROOT (portable)."""
    current = Path(__file__).resolve().parent
    for _ in range(3):
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
class TrainSettings:
    """Settings for training system (copied from minirag, standalone)"""
    hf_embeddings_model: str = os.getenv(
        "HF_EMBEDDINGS_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
    )
    chunk_size: int = getenv_int("CHUNK_SIZE", 1200)
    chunk_overlap: int = getenv_int("CHUNK_OVERLAP", 150)
    pdf_dir: str = os.getenv(
        "TRAIN_PDF_DIR",
        os.getenv("DKM_PDF_PATH", "")
    )
    cache_dir: str = os.getenv(
        "TRAIN_CACHE_DIR",
        os.getenv("DKM_PDF_PATH", "")
    )

    def validate(self) -> None:
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be < CHUNK_SIZE")


def get_settings() -> TrainSettings:
    s = TrainSettings()
    s.validate()
    return s
