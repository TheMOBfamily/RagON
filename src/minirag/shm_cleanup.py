"""Shared Memory Cache Cleanup & Stats

Maintenance operations for /dev/shm/ cache.
Separated for SRP (Single Responsibility Principle).
"""

from __future__ import annotations

from pathlib import Path
import shutil
from typing import Dict

SHM_DIR = Path("/dev/shm")
CACHE_PREFIX = "minirag_faiss"


def cleanup_old_caches(max_age_hours: int = 24) -> int:
    """Remove caches older than X hours.

    Args:
        max_age_hours: Maximum age in hours (default 24h)

    Returns:
        Number of caches cleaned
    """
    import time
    now = time.time()
    cutoff = now - (max_age_hours * 3600)
    cleaned = 0

    for cache_file in SHM_DIR.glob(f"{CACHE_PREFIX}_*.pkl"):
        try:
            if cache_file.stat().st_mtime < cutoff:
                cache_file.unlink()
                meta_file = cache_file.with_suffix(".meta")
                if meta_file.exists():
                    meta_file.unlink()
                print(f"🗑️  Cleaned old cache: {cache_file.name}")
                cleaned += 1
        except Exception as e:
            print(f"⚠️  Cleanup failed for {cache_file.name}: {e}")

    return cleaned


def get_cache_stats() -> Dict:
    """Get statistics about /dev/shm/ cache usage.

    Returns:
        Dict with cache stats (count, total_size_mb, shm_usage_percent, etc.)
    """
    try:
        stats = shutil.disk_usage(SHM_DIR)
        cache_files = list(SHM_DIR.glob(f"{CACHE_PREFIX}_*.pkl"))

        total_cache_size = sum(f.stat().st_size for f in cache_files)
        total_cache_mb = total_cache_size / (1024 * 1024)
        shm_total_mb = stats.total / (1024 * 1024)
        shm_used_mb = stats.used / (1024 * 1024)
        shm_free_mb = stats.free / (1024 * 1024)
        shm_usage_percent = (stats.used / stats.total) * 100

        return {
            "cache_count": len(cache_files),
            "cache_total_mb": round(total_cache_mb, 2),
            "shm_total_mb": round(shm_total_mb, 2),
            "shm_used_mb": round(shm_used_mb, 2),
            "shm_free_mb": round(shm_free_mb, 2),
            "shm_usage_percent": round(shm_usage_percent, 2),
        }
    except Exception as e:
        print(f"⚠️  Stats collection failed: {e}")
        return {}


def clear_all_caches() -> int:
    """Clear ALL minirag caches from /dev/shm/.

    WARNING: Destructive operation!

    Returns:
        Number of caches cleared
    """
    cleared = 0

    for cache_file in SHM_DIR.glob(f"{CACHE_PREFIX}_*"):
        try:
            cache_file.unlink()
            print(f"🗑️  Cleared: {cache_file.name}")
            cleared += 1
        except Exception as e:
            print(f"⚠️  Clear failed for {cache_file.name}: {e}")

    return cleared
