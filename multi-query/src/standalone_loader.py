"""Standalone vectorstore loader for multi-query (no minirag dependency)"""
from __future__ import annotations
from pathlib import Path
from typing import Any
import sys

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

# Import SharedMemoryCache from minirag package
MINIRAG_SRC = Path(__file__).parent.parent.parent / "src"
if str(MINIRAG_SRC) not in sys.path:
    sys.path.insert(0, str(MINIRAG_SRC))

from minirag.shm_cache import SharedMemoryCache


def get_embeddings_standalone() -> Any:
    """Get HuggingFace embeddings (standalone)"""
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


def load_vectorstore_from_path(source_path: str) -> FAISS:
    """
    Load FAISS vectorstore from path with /dev/shm/ cache (standalone).
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

    # ── NEW: Shared Memory Cache ──
    cache = SharedMemoryCache(str(source_path_obj))

    # Check cache FIRST
    if cache.is_cached():
        print(f"🔥 Cache HIT: {source_path_obj.name}")
        cached = cache.load()
        if cached is not None:
            return cached
        # Cache corrupted, continue to reload

    # ── EXISTING: Detect format and find index location ──
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
    embeddings = get_embeddings_standalone()

    # Load FAISS index from disk
    print(f"💾 Loading from disk: {source_path_obj.name}")
    store = FAISS.load_local(
        str(index_dir),
        embeddings,
        allow_dangerous_deserialization=True
    )

    # ── NEW: Save to /dev/shm/ cache ──
    cache.save(store)

    return store


def get_context_standalone(store: FAISS, query: str, top_k: int = 4) -> str:
    """
    Retrieve context from vectorstore (standalone, copied from minirag).
    
    Args:
        store: FAISS vectorstore
        query: Search query
        top_k: Number of chunks to retrieve
        
    Returns:
        Formatted context string
    """
    import os
    
    # Get top_k from env or use parameter
    top_k = int(os.getenv("TOP_K", str(top_k)))
    
    # Create retriever
    retriever = store.as_retriever(search_kwargs={"k": top_k})
    
    # Get relevant documents
    from langchain.schema import Document
    docs: list[Document] = retriever.invoke(query)
    
    if not docs:
        return ""
    
    # Format context with page number
    context_parts = []
    for doc in docs:
        content = doc.page_content.strip()
        source = doc.metadata.get("source_file", "unknown")
        page = doc.metadata.get("page")  # 0-indexed or None

        # Format with page number if available (1-indexed for humans)
        if page is not None:
            header = f"[Source: {source}] Page {page + 1}"
        else:
            header = f"[Source: {source}]"

        context_parts.append(f"{header}:\n{content}")

    return "\n---\n".join(context_parts)
