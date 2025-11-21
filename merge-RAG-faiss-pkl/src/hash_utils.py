#!/usr/bin/env python
"""
Hash utilities for index tracking
Compute MD5 hashes of FAISS index files

Author: AI Assistant
Date: 2025-10-26
LOC: ~45 (< 100)
"""
from __future__ import annotations
import hashlib
from pathlib import Path
from .config import HASH_CHUNK_SIZE


def compute_index_hash(index_dir: Path) -> str:
    """
    Compute combined MD5 hash of index.faiss + index.pkl
    Used to detect changes in individual index

    Args:
        index_dir: Directory containing index.faiss and index.pkl

    Returns:
        MD5 hex string, or empty string if files don't exist
    """
    faiss_path = index_dir / "index.faiss"
    pkl_path = index_dir / "index.pkl"

    if not faiss_path.exists() or not pkl_path.exists():
        return ""

    md5 = hashlib.md5()

    # Hash index.faiss
    with open(faiss_path, "rb") as f:
        for chunk in iter(lambda: f.read(HASH_CHUNK_SIZE), b""):
            md5.update(chunk)

    # Hash index.pkl
    with open(pkl_path, "rb") as f:
        for chunk in iter(lambda: f.read(HASH_CHUNK_SIZE), b""):
            md5.update(chunk)

    return md5.hexdigest()


def compute_concatenated_hash(hash_ids: list[str]) -> str:
    """
    Compute MD5 of concatenated hash IDs (sorted)

    This detects CRUD operations:
    - New PDF added → new hash in list → concat changes
    - PDF deleted → hash removed → concat changes
    - PDF unchanged → concat stays same → no merge needed

    Args:
        hash_ids: List of hash directory names (32-char MD5 strings)

    Returns:
        MD5 hex string of sorted concatenated hashes
    """
    sorted_hashes = sorted(hash_ids)
    concatenated = "".join(sorted_hashes)
    return hashlib.md5(concatenated.encode()).hexdigest()
