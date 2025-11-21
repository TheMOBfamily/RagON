from __future__ import annotations
import json
import hashlib
from pathlib import Path
from typing import List, Dict
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from .embedder import get_embeddings
from .shm_cache import SharedMemoryCache

INDEX_DIR_NAME = ".mini_rag_index"
MANIFEST_FILE = "manifest.json"


def _hash_file(p: Path, chunk_size: int = 1024 * 1024) -> str:
    """Return md5 hex digest of a file (streaming)."""
    h = hashlib.md5()
    with p.open("rb") as f:
        while True:
            block = f.read(chunk_size)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def _current_pdf_state(
    pdf_dir: Path,
    previous: Dict[str, Dict[str, float]] | None = None,
    *,
    hash_files: bool = True,
) -> Dict[str, Dict[str, float]]:
    state: Dict[str, Dict[str, float]] = {}
    previous = previous or {}
    for f in sorted(pdf_dir.iterdir()):
        if f.is_file() and f.suffix.lower() == ".pdf":
            stat = f.stat()
            state[f.name] = {
                "size": stat.st_size,
                "mtime": stat.st_mtime,
            }
            prev_meta = previous.get(f.name)
            if not hash_files:
                state[f.name]["md5"] = prev_meta.get("md5") if prev_meta else ""
            elif (
                prev_meta
                and prev_meta.get("size") == state[f.name]["size"]
                and prev_meta.get("mtime") == state[f.name]["mtime"]
                and "md5" in prev_meta
            ):
                # Reuse stored hash when size + mtime unchanged
                state[f.name]["md5"] = prev_meta["md5"]
            else:
                state[f.name]["md5"] = _hash_file(f)
    return state


def _load_manifest(path: Path) -> Dict[str, Dict[str, float]]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
        return data.get("files", {}) if isinstance(data, dict) else {}
    except Exception:
        return {}


def _write_manifest(path: Path, files: Dict[str, Dict[str, float]]) -> None:
    payload = {"version": 1, "files": files}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def _needs_rebuild(manifest_files: Dict[str, Dict[str, float]], current: Dict[str, Dict[str, float]]) -> bool:
    if not manifest_files:
        return True
    if manifest_files.keys() != current.keys():
        return True
    # Check any hash change
    for name, meta in current.items():
        if meta.get("md5") != manifest_files.get(name, {}).get("md5"):
            return True
    return False


def build_or_load_vectorstore(pdf_dir: str, force_rebuild: bool = False) -> FAISS:
    """Build or load FAISS vector store.

    Structure:
    - manifest.json: pdf_dir/manifest.json (root level)
    - vector files: pdf_dir/.mini_rag_index/ (subfolder)

    Rebuild triggers:
    - No index / manifest
    - Set of PDF files changed (added/removed)
    - MD5 hash of any PDF changed
    - force_rebuild=True

    Blacklist protection:
    - Directories in Settings.no_train_dirs are NEVER rebuilt
    - force_rebuild is automatically set to False for blacklisted directories
    """
    from .config import get_settings

    pdf_path = Path(pdf_dir).resolve()  # Normalize to absolute path
    settings = get_settings()

    # ── NEW: Shared Memory Cache (/tmp/) ──
    # Check cache FIRST - survives process death
    shm_cache = SharedMemoryCache(str(pdf_path))

    if not force_rebuild and shm_cache.is_cached():
        print("🔥 Cache HIT - Loading from /tmp/")
        cached_index = shm_cache.load()
        if cached_index is not None:
            return cached_index
        else:
            print("⚠️  Cache corrupted, rebuilding...")

    # ── EXISTING CODE ──
    # Check if directory is blacklisted
    is_blacklisted = any(
        pdf_path == Path(no_train_dir).resolve()
        for no_train_dir in settings.no_train_dirs
    )

    if is_blacklisted:
        if force_rebuild:
            print(f"🚫 BLOCKED: Directory '{pdf_dir}' is in NO_TRAIN blacklist")
            print("   This directory cannot be rebuilt (read-only mode)")
            print("   Forcing force_rebuild=False")
        force_rebuild = False

    index_path = pdf_path / INDEX_DIR_NAME
    index_path.mkdir(exist_ok=True)

    embeddings = get_embeddings()
    faiss_index_file = index_path / "index.faiss"
    store_pkl_file = index_path / "index.pkl"

    if is_blacklisted:
        if not faiss_index_file.exists() or not store_pkl_file.exists():
            print("❌ ERROR: No existing vector store found for blacklisted directory. Cannot proceed without rebuild.")
            raise FileNotFoundError("Vector store not found for blacklisted directory")
        print("✅ Using cached vector store (blacklisted directory)")
        store = FAISS.load_local(str(index_path), embeddings, allow_dangerous_deserialization=True)

        # Save to /tmp/ for next queries
        shm_cache.save(store)

        return store

    # manifest.json ở root level của pdf_dir
    manifest_path = pdf_path / MANIFEST_FILE
    previous = _load_manifest(manifest_path)
    current = _current_pdf_state(pdf_path, previous, hash_files=True)

    rebuild_needed = _needs_rebuild(previous, current)
    
    # If index doesn't exist, must rebuild
    if not faiss_index_file.exists() or not store_pkl_file.exists():
        rebuild_needed = True
        force_rebuild = True  # Force rebuild when index missing
    
    # If rebuild needed but not forced, warn and use existing
    if rebuild_needed and not force_rebuild:
        prev_files = set(previous.keys())
        curr_files = set(current.keys())

        added = curr_files - prev_files
        removed = prev_files - curr_files
        modified = [
            name
            for name in curr_files & prev_files
            if current[name].get("md5") != previous.get(name, {}).get("md5")
        ]

        parts = []
        if added:
            parts.append(f"{len(added)} added")
        if removed:
            parts.append(f"{len(removed)} removed")
        if modified:
            parts.append(f"{len(modified)} modified")

        summary = ", ".join(parts) if parts else "detected"
        print(f"⚠️  WARNING: PDF files changed ({summary}). Using existing vector store; rerun with --force-rebuild to rebuild.")
        
        # Load existing if available
        if faiss_index_file.exists() and store_pkl_file.exists():
            store = FAISS.load_local(str(index_path), embeddings, allow_dangerous_deserialization=True)

            # Save to /tmp/ for next queries
            shm_cache.save(store)

            return store
        else:
            print("❌ ERROR: No existing vector store found. Cannot proceed without rebuild.")
            raise FileNotFoundError("No vector store exists and rebuild not authorized")
    
    # If no rebuild needed and index exists, use cached
    if not rebuild_needed and faiss_index_file.exists() and store_pkl_file.exists():
        print("✅ Using cached vector store")
        store = FAISS.load_local(str(index_path), embeddings, allow_dangerous_deserialization=True)

        # Save to /tmp/ for next queries
        shm_cache.save(store)

        return store

    # Rebuild index - load and split documents only now
    print("📄 Loading PDFs for rebuild...")
    from .loader import load_pdfs
    from .splitter import split_documents
    
    docs = load_pdfs(pdf_dir)
    print(f"📄 Loaded {len(docs)} documents") 
    
    chunks = split_documents(docs)
    print(f"✂️ Split into {len(chunks)} chunks")
    
    print(f"🔄 Building vector store...")
    store = FAISS.from_documents(chunks, embeddings)
    store.save_local(str(index_path))
    _write_manifest(manifest_path, current)
    print(f"✅ Vector store saved to {index_path}")

    # Save to /tmp/ for next queries
    shm_cache.save(store)

    return store
