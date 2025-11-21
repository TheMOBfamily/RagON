"""Shared Memory Cache Validators

TTL and space validation logic.
Separated for SRP (Single Responsibility Principle).
"""

from __future__ import annotations

from pathlib import Path
import shutil
from datetime import datetime, timedelta
from typing import Dict

SHM_DIR = Path("/dev/shm")


def check_ttl(meta: Dict, ttl_hours: int) -> bool:
    """Check if cache is within TTL (time-to-live).

    Args:
        meta: Cache metadata dict
        ttl_hours: TTL in hours

    Returns:
        True if cache is fresh, False if expired
    """
    try:
        save_time_str = meta.get("save_time")
        if not save_time_str:
            return False

        save_time = datetime.fromisoformat(save_time_str)
        now = datetime.now()
        age = now - save_time

        if age > timedelta(hours=ttl_hours):
            age_hours = age.total_seconds() / 3600
            print(f"⏰ Cache expired (age: {age_hours:.1f}h > TTL: {ttl_hours}h)")
            return False

        return True
    except Exception as e:
        print(f"⚠️  TTL check failed: {e}")
        return False


def check_space_available(
    required_bytes: int = 0,
    threshold_percent: int = 80,
    min_free_mb: int = 500
) -> bool:
    """Check if /dev/shm/ has safe space available.

    Best practices from DKM research:
    - Use max 80% of total space (20% buffer)
    - Keep min 500MB free

    Args:
        required_bytes: Additional space needed
        threshold_percent: Max usage percent (default 80%)
        min_free_mb: Minimum free space in MB (default 500MB)

    Returns:
        True if safe to write, False if space constrained
    """
    try:
        stats = shutil.disk_usage(SHM_DIR)
        total = stats.total
        used = stats.used
        free = stats.free

        # Check 1: Don't exceed threshold
        usage_percent = (used / total) * 100
        if usage_percent > threshold_percent:
            print(f"⚠️  /dev/shm/ usage {usage_percent:.1f}% > {threshold_percent}% threshold")
            return False

        # Check 2: Keep minimum free space
        free_mb = free / (1024 * 1024)
        if free_mb < min_free_mb:
            print(f"⚠️  /dev/shm/ free {free_mb:.1f}MB < {min_free_mb}MB minimum")
            return False

        # Check 3: Can fit required bytes?
        if required_bytes > 0 and free < required_bytes:
            required_mb = required_bytes / (1024 * 1024)
            print(f"⚠️  Not enough space: need {required_mb:.1f}MB, have {free_mb:.1f}MB")
            return False

        return True
    except Exception as e:
        print(f"⚠️  Space check failed: {e}")
        return False
