#!/usr/bin/env python
"""
Vectorstore loader for merge operations - NO CACHE (direct disk load)

Author: AI Assistant
Date: 2025-11-20
Purpose: Load FAISS indexes for merge WITHOUT caching to RAM
"""
from __future__ import annotations
from pathlib import Path
from typing import Any

# CRITICAL: Import sentence_transformers BEFORE faiss to avoid meta tensor errors
try:
    from langchain_huggingface import HuggingFaceEmbeddings  # noqa: F401
except ImportError:
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings  # noqa: F401
    except ImportError:
        pass

# Now safe to import FAISS
from langchain_community.vectorstores import FAISS


def get_embeddings_no_cache() -> Any:
    """Get HuggingFace embeddings (no cache)"""
    import os
    model_name = os.getenv("HF_EMBEDDINGS_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=model_name)
    except ImportError:
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(model_name=model_name)
        except Exception as e:
            raise RuntimeError(f"Cannot load HuggingFace embeddings: {e}")


def load_vectorstore_no_cache(source_path: str) -> FAISS:
    """
    Load FAISS vectorstore from path WITHOUT cache (for merge only).

    Supports 2 formats:
    1. Hash-based: <hash>/index.faiss (DKM-PDFs trained format)
    2. Traditional: <path>/.mini_rag_index/index.faiss (test-pdf format)

    Args:
        source_path: Path to folder containing index

    Returns:
        FAISS vectorstore
    """
    source_path_obj = Path(source_path)

    if not source_path_obj.exists():
        raise FileNotFoundError(f"Source path not found: {source_path}")

    # Detect format and find index location
    index_dir = None

    # Check hash-based format: index.faiss directly in folder
    if (source_path_obj / "index.faiss").exists():
        index_dir = source_path_obj
    # Check traditional format: .mini_rag_index subfolder
    elif (source_path_obj / ".mini_rag_index" / "index.faiss").exists():
        index_dir = source_path_obj / ".mini_rag_index"
    else:
        raise FileNotFoundError(f"No FAISS index found in {source_path}")

    # Verify both required files exist
    if not (index_dir / "index.faiss").exists():
        raise FileNotFoundError(f"Missing index.faiss in {index_dir}")
    if not (index_dir / "index.pkl").exists():
        raise FileNotFoundError(f"Missing index.pkl in {index_dir}")

    # Load embeddings
    embeddings = get_embeddings_no_cache()

    # Load FAISS index from disk - NO CACHE
    print(f"💾 Loading from disk (no cache): {source_path_obj.name}")
    store = FAISS.load_local(
        str(index_dir),
        embeddings,
        allow_dangerous_deserialization=True
    )

    # NO cache.save() here - this is the key difference!
    return store
