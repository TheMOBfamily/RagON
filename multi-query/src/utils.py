from __future__ import annotations
import time
import logging
import hashlib
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime
from typing import Iterator


@contextmanager
def timed(label: str) -> Iterator[None]:
    """Context manager for timing operations"""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        logging.info(f"{label}: {elapsed:.2f}s")


def setup_logging(log_dir: Path) -> str:
    """
    Setup logging to file ONLY (not console).
    
    Console output is reserved for clean JSON results.
    All INFO/ERROR logs go to file only.
    """
    log_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"multirag_{timestamp}.log"
    
    # Clear any existing handlers
    logging.root.handlers = []
    
    # File handler only - NO StreamHandler (no console spam)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file)
        ]
    )
    
    # Also suppress external library logs from console
    logging.getLogger('sentence_transformers').setLevel(logging.WARNING)
    logging.getLogger('transformers').setLevel(logging.WARNING)
    logging.getLogger('torch').setLevel(logging.WARNING)
    
    return str(log_file)


def compute_content_hash(content: str) -> str:
    """Compute MD5 hash of content for deduplication"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def safe_path_name(name: str) -> str:
    """Convert path to safe display name"""
    return Path(name).name
