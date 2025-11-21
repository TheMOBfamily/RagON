#!/usr/bin/env python
"""
Configuration for merge-RAG-faiss-pkl
Centralized paths and constants

Author: AI Assistant
Date: 2025-10-26
LOC: ~40 (< 100)
"""
from __future__ import annotations
import os
from pathlib import Path


def _load_env_from_ragon_root() -> None:
    """Load .env from RAGON_ROOT (portable)."""
    current = Path(__file__).resolve().parent
    for _ in range(4):  # Search up to 4 levels
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


# Project root
PROJECT_ROOT = Path(os.getenv("RAGON_ROOT", Path(__file__).parent.parent.parent))

# Source directories
MULTI_QUERY_SRC = PROJECT_ROOT / "multi-query" / "src"
DKM_PDFS_DIR = Path(os.getenv("DKM_PDF_PATH", PROJECT_ROOT / "DKM-PDFs"))

# Output directories
MERGED_INDEX_DIR = DKM_PDFS_DIR / ".mini_rag_index"
MANIFEST_PATH = DKM_PDFS_DIR / "manifest.json"

# Backup paths
MANIFEST_BACKUP_SUFFIX = ".json.backup"

# Manifest schema version
MANIFEST_VERSION = 1

# Merge settings
DEFAULT_TEST_LIMIT = 5  # Test với 5 PDFs
HASH_CHUNK_SIZE = 8192  # 8KB chunks for file hashing

# Atomic merge settings (SSOT)
# Based on DKM RAG research: external sort batch optimization
ATOMIC_WRITE_ENABLED = True  # Always use atomic write (zero data loss)
BATCH_THRESHOLD = 500  # Auto-enable batch mode when sources > threshold
BATCH_SIZE_DEFAULT = 100  # Sources per batch (optimal for ~770KB/PDF)
# Rationale: 100 PDFs × 770KB ≈ 77MB RAM/batch (safe for 4GB+ systems)
# Compare: 1000 PDFs × 770KB ≈ 770MB + metadata ≈ 2-3GB (OOM risk)

# Temp directory settings
TEMP_BASE_DIR = Path("/tmp")  # Force /tmp/ instead of /dev/shm/ (avoid RAM disk crash)
TEMP_DIR_PREFIX = "faiss-merge-"  # Prefix for secure temp directories
ATOMIC_BACKUP_ENABLED = True  # Create backup before atomic replace

# Console colors (for rich)
COLOR_INFO = "cyan"
COLOR_SUCCESS = "green"
COLOR_WARNING = "yellow"
COLOR_ERROR = "red"
COLOR_HEADER = "blue"
