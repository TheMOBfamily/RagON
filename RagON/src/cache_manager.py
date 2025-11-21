"""Cache manager cho FAISS index trong RAM"""
from __future__ import annotations
import sys
import time
from pathlib import Path
from typing import Dict
from datetime import datetime

# Thêm mini-rag vào path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from minirag.vectorstore import build_or_load_vectorstore

# In-memory cache: {pdf_dir: {index: FAISS, loaded_at: datetime}}
INDEX_CACHE: Dict[str, Dict[str, any]] = {}


def get_cache_stats() -> dict:
    """Lấy thống kê cache"""
    stats = []
    for path, data in INDEX_CACHE.items():
        stats.append({
            "path": path,
            "loaded_at": data["loaded_at"].isoformat(),
            "docs_count": data["index"].index.ntotal if hasattr(data["index"], 'index') else "unknown"
        })

    return {
        "total_cached": len(INDEX_CACHE),
        "indices": stats
    }


def clear_cache_by_path(path: str) -> bool:
    """Xóa 1 path khỏi cache. Return True nếu xóa thành công"""
    if path in INDEX_CACHE:
        del INDEX_CACHE[path]
        return True
    return False


def clear_all_cache() -> int:
    """Xóa toàn bộ cache. Return số lượng đã xóa"""
    count = len(INDEX_CACHE)
    INDEX_CACHE.clear()
    return count


def load_index(pdf_dir: str, force_rebuild: bool = False) -> tuple:
    """Load FAISS index vào cache. Return (index, load_time, from_cache)"""
    from_cache = pdf_dir in INDEX_CACHE

    if from_cache:
        print(f"🔥 Cache HIT: {pdf_dir}")
        return INDEX_CACHE[pdf_dir]["index"], 0.0, True

    # Cache miss - load từ disk
    print(f"⏳ Loading index: {pdf_dir}")
    load_start = time.time()
    index = build_or_load_vectorstore(pdf_dir, force_rebuild=force_rebuild)
    load_time = time.time() - load_start

    # Cache it
    INDEX_CACHE[pdf_dir] = {
        "index": index,
        "loaded_at": datetime.now()
    }
    print(f"✅ Loaded in {load_time:.2f}s")

    return index, load_time, False


def reload_index(pdf_dir: str) -> tuple:
    """Reload index (clear + load lại). Return (index, load_time, docs_count)"""
    # Clear cache cũ nếu có
    if pdf_dir in INDEX_CACHE:
        del INDEX_CACHE[pdf_dir]

    # Load lại
    load_start = time.time()
    index = build_or_load_vectorstore(pdf_dir, force_rebuild=False)
    load_time = time.time() - load_start

    INDEX_CACHE[pdf_dir] = {
        "index": index,
        "loaded_at": datetime.now()
    }

    docs_count = index.index.ntotal if hasattr(index, 'index') else "unknown"
    return index, load_time, docs_count


def preload_default_index() -> None:
    """Preload DKM-PDFs vào cache khi startup"""
    dkm_path = "/home/fong/Projects/mini-rag/DKM-PDFs"
    print("🚀 RagON Starting...")
    print("📦 Preloading DKM-PDFs...")

    start = time.time()
    try:
        index = build_or_load_vectorstore(dkm_path, force_rebuild=False)
        INDEX_CACHE[dkm_path] = {
            "index": index,
            "loaded_at": datetime.now()
        }
        elapsed = time.time() - start
        print(f"✅ DKM-PDFs loaded in {elapsed:.2f}s")
        print(f"🔥 Cache ready - queries will be <1s")
    except Exception as e:
        print(f"⚠️  Failed to preload DKM-PDFs: {e}")
        print(f"   Will load on first query")
