"""RagON - RAG Persistent Service
FastAPI service giữ FAISS index trong RAM để query <1s
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# Thêm RagON và Flask-API/src vào path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))  # Flask-API/src for settings

from fastapi import FastAPI, HTTPException, Header, Depends, Request
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
import ipaddress

# Import từ RagON
from minirag.vectorstore import build_or_load_vectorstore
from minirag.config import get_settings

# API Key from settings
from settings import RAGON_API_KEY

app = FastAPI(
    title="RagON",
    description="RAG Persistent Service - FAISS index trong RAM",
    version="1.0.0"
)


def is_local_or_lan(client_ip: str) -> bool:
    """Check if client is localhost or LAN (private network)"""
    try:
        ip = ipaddress.ip_address(client_ip)
        # Localhost
        if ip.is_loopback:
            return True
        # Private networks (LAN): 10.x.x.x, 172.16-31.x.x, 192.168.x.x
        if ip.is_private:
            return True
        return False
    except ValueError:
        return False


def verify_api_key(request: Request, x_api_key: str = Header(None)):
    """Verify API key - skip for localhost/LAN, require for external"""
    client_ip = request.client.host

    # Skip API check for localhost and LAN
    if is_local_or_lan(client_ip):
        return None

    # Require API key for external clients
    if x_api_key != RAGON_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return x_api_key

# In-memory cache: {pdf_dir: {index: FAISS, loaded_at: datetime}}
INDEX_CACHE: Dict[str, Dict[str, any]] = {}


from settings import DKM_PDF_PATH

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = None


class QueryResponse(BaseModel):
    answer: str
    sources: list
    load_time_seconds: float
    retrieval_time_seconds: float
    from_cache: bool


@app.on_event("startup")
async def startup_event():
    """Load DKM-PDFs vào cache khi start"""
    print("🚀 RagON Starting...")
    print("📦 Preloading DKM-PDFs...")

    dkm_path = DKM_PDF_PATH
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


@app.get("/")
async def root():
    return {
        "service": "RagON",
        "status": "running",
        "cached_indices": len(INDEX_CACHE),
        "paths": list(INDEX_CACHE.keys())
    }


@app.get("/cache/stats")
async def cache_stats():
    """Thống kê cache"""
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


@app.post("/query", response_model=QueryResponse)
async def query_rag(req: QueryRequest, api_key: str = Depends(verify_api_key)):
    """Query RAG với FAISS index trong RAM - yêu cầu API key"""
    pdf_path = Path(DKM_PDF_PATH).resolve()
    pdf_dir_str = str(pdf_path)

    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"DKM_PDF_PATH not found: {DKM_PDF_PATH}")

    # Check cache
    from_cache = pdf_dir_str in INDEX_CACHE
    load_start = time.time()

    if from_cache:
        print(f"🔥 Cache HIT: {pdf_dir_str}")
        index = INDEX_CACHE[pdf_dir_str]["index"]
        load_time = 0.0
    else:
        print(f"⏳ Loading index: {pdf_dir_str}")
        index = build_or_load_vectorstore(pdf_dir_str, force_rebuild=False)
        load_time = time.time() - load_start

        # Cache it
        INDEX_CACHE[pdf_dir_str] = {
            "index": index,
            "loaded_at": datetime.now()
        }
        print(f"✅ Loaded in {load_time:.2f}s")

    # Query
    retrieval_start = time.time()
    settings = get_settings()
    top_k = req.top_k if req.top_k else settings.top_k

    docs = index.similarity_search(req.question, k=top_k)
    retrieval_time = time.time() - retrieval_start

    # Format response
    sources = []
    for doc in docs:
        sources.append({
            "content": doc.page_content,
            "metadata": doc.metadata
        })

    # Simple answer (concatenate top results)
    answer = "\n\n".join([
        f"[{doc.metadata.get('source', 'unknown')}] Page {doc.metadata.get('page', 'N/A')}:\n{doc.page_content}"
        for doc in docs
    ])

    return QueryResponse(
        answer=answer,
        sources=sources,
        load_time_seconds=load_time,
        retrieval_time_seconds=retrieval_time,
        from_cache=from_cache
    )


@app.delete("/cache/{path:path}")
async def clear_cache_path(path: str):
    """Xóa 1 path khỏi cache"""
    if path in INDEX_CACHE:
        del INDEX_CACHE[path]
        return {"message": f"Cleared cache for {path}"}
    else:
        raise HTTPException(status_code=404, detail="Path not in cache")


@app.delete("/cache")
async def clear_all_cache():
    """Xóa toàn bộ cache"""
    count = len(INDEX_CACHE)
    INDEX_CACHE.clear()
    return {"message": f"Cleared {count} cached indices"}


if __name__ == "__main__":
    import uvicorn
    from src.settings import PORT, HOST
    uvicorn.run(app, host=HOST, port=PORT)
