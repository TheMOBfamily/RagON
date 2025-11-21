"""Shared Memory Cache for FAISS Index

Minimal implementation - cache operations only.
Config managed in config.py (SSOT).
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import pickle
from datetime import datetime
from typing import Optional, Any

# Use /tmp instead of /dev/shm (avoid RAM disk full issues)
SHM_DIR = Path("/tmp")
CACHE_PREFIX = "minirag_faiss"


class SharedMemoryCache:
    """Linux /tmp/ cache for FAISS vector store."""

    def __init__(self, pdf_dir: str):
        from .config import get_settings
        self.settings = get_settings()
        self.pdf_dir = Path(pdf_dir).resolve()
        self.manifest_hash = self._compute_manifest_hash()
        self.cache_key = self._compute_cache_key()
        self.cache_path = SHM_DIR / f"{CACHE_PREFIX}_{self.cache_key}.pkl"
        self.meta_path = SHM_DIR / f"{CACHE_PREFIX}_{self.cache_key}.meta"

    def _compute_manifest_hash(self) -> str:
        """Compute manifest.json hash for invalidation tracking."""
        manifest_path = self.pdf_dir / ".mini_rag_index" / "manifest.json"
        if not manifest_path.exists():
            return ""
        data = manifest_path.read_text()
        return hashlib.md5(data.encode()).hexdigest()

    def _compute_cache_key(self) -> str:
        """Cache key = MD5(path + manifest_hash)[:16]"""
        combined = f"{self.pdf_dir}::{self.manifest_hash}"
        return hashlib.md5(combined.encode()).hexdigest()[:16]

    def is_cached(self) -> bool:
        """Check if valid cache exists."""
        if not self.settings.cache_enabled:
            return False

        if not self.cache_path.exists():
            return False

        if self.meta_path.exists():
            try:
                meta = pickle.loads(self.meta_path.read_bytes())
                if meta.get("manifest_hash") != self.manifest_hash:
                    print(f"⚠️  Manifest changed, invalidating cache {self.cache_key}")
                    self.clear()
                    return False
            except Exception as e:
                print(f"⚠️  Cache metadata corrupted: {e}")
                self.clear()
                return False

        return True

    def save(self, faiss_index: Any) -> None:
        """Save FAISS index to /tmp/"""
        if not self.settings.cache_enabled:
            return

        try:
            with open(self.cache_path, 'wb') as f:
                pickle.dump(faiss_index, f, protocol=pickle.HIGHEST_PROTOCOL)

            meta = {
                "manifest_hash": self.manifest_hash,
                "pdf_dir": str(self.pdf_dir),
                "save_time": datetime.now().isoformat(),
                "cache_key": self.cache_key,
            }
            with open(self.meta_path, 'wb') as f:
                pickle.dump(meta, f)

            print(f"💾 Cached to /tmp/ (key: {self.cache_key})")

        except OSError as e:
            print(f"⚠️  /tmp/ full or unavailable: {e}")
        except Exception as e:
            print(f"⚠️  Cache save failed: {e}")

    def load(self) -> Optional[Any]:
        """Load FAISS index from /tmp/"""
        if not self.is_cached():
            return None

        try:
            with open(self.cache_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"⚠️  Cache corrupted: {e}")
            self.clear()
            return None

    def clear(self) -> None:
        """Clear cache files."""
        try:
            if self.cache_path.exists():
                self.cache_path.unlink()
            if self.meta_path.exists():
                self.meta_path.unlink()
        except Exception as e:
            print(f"⚠️  Cache clear failed: {e}")
