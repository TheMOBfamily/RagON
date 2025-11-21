from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Tuple


def compute_file_hash(file_path: str | Path) -> str:
    """
    Compute MD5 hash of file content for caching.
    Uses streaming to handle large PDFs efficiently.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        MD5 hexadecimal hash string
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    hasher = hashlib.md5()
    
    # Stream file in 1MB chunks to handle large PDFs
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    
    return hasher.hexdigest()


def get_cache_dir(pdf_path: str | Path, base_cache_dir: str | Path) -> Path:
    """
    Get cache directory for a PDF based on its content hash.
    KISS: DKM-PDFs/<hash>/ directly contains index files.
    
    Args:
        pdf_path: Path to PDF file
        base_cache_dir: Base directory (DKM-PDFs)
        
    Returns:
        Path to cache directory (DKM-PDFs/<hash>/)
    """
    pdf_hash = compute_file_hash(pdf_path)
    cache_dir = Path(base_cache_dir) / pdf_hash
    return cache_dir


def is_trained(pdf_path: str | Path, base_cache_dir: str | Path) -> Tuple[bool, Path]:
    """
    Check if PDF is already trained (cache exists).
    KISS: Check if <hash>/index.faiss and <hash>/index.pkl exist.
    
    Args:
        pdf_path: Path to PDF file
        base_cache_dir: Base directory (DKM-PDFs)
        
    Returns:
        (is_trained, cache_dir)
    """
    cache_dir = get_cache_dir(pdf_path, base_cache_dir)
    
    # KISS: Index files directly in cache_dir
    faiss_exists = (cache_dir / "index.faiss").exists()
    pkl_exists = (cache_dir / "index.pkl").exists()
    manifest_exists = (cache_dir / "manifest.json").exists()
    
    return (faiss_exists and pkl_exists and manifest_exists), cache_dir


def create_pdf_metadata(pdf_path: str | Path, cache_dir: Path) -> dict:
    """Create metadata for trained PDF"""
    import os
    from datetime import datetime
    
    pdf_path = Path(pdf_path)
    file_hash = compute_file_hash(pdf_path)
    file_stats = os.stat(pdf_path)
    
    return {
        "filename": pdf_path.name,
        "file_hash": file_hash,
        "file_size": file_stats.st_size,
        "trained_at": datetime.now().isoformat(),
        "cache_dir": str(cache_dir)
    }
