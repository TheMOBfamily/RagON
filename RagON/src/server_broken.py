"""RagON - RAG Persistent Service
FastAPI service giữ FAISS index trong RAM để query <1s
"""
from __future__ import annotations
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException

from src.schemas import QueryRequest, QueryResponse
from src.cache_manager import (
    get_cache_stats, clear_cache_by_path, clear_all_cache,
    load_index, reload_index, preload_default_index, INDEX_CACHE
)
from minirag.config import get_settings

app = FastAPI(
    title="RagON",
    description="RAG Persistent Service - FAISS index trong RAM",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Preload DKM-PDFs vào cache khi start"""
    preload_default_index()


@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "RagON",
        "status": "running",
        "cached_indices": len(INDEX_CACHE),
        "paths": list(INDEX_CACHE.keys())
    }


@app.get("/cache/stats")
async def cache_stats():
    """Thống kê cache"""
    return get_cache_stats()


@app.post("/query", response_model=QueryResponse)
async def query_rag(req: QueryRequest):
    """Query RAG với FAISS index trong RAM"""
    pdf_path = Path(req.pdf_directory).resolve()
    pdf_dir_str = str(pdf_path)

    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"Directory not found: {req.pdf_directory}")

    # Load index (từ cache hoặc disk)
    index, load_time, from_cache = load_index(pdf_dir_str)

    # Query
    retrieval_start = time.time()
    settings = get_settings()
    top_k = req.top_k if req.top_k else settings.top_k

    docs = index.similarity_search(req.question, k=top_k)
    retrieval_time = time.time() - retrieval_start

    # Format response
    sources = [
        {"content": doc.page_content, "metadata": doc.metadata}
        for doc in docs
    ]

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
    if clear_cache_by_path(path):
        return {"message": f"Cleared cache for {path}"}
    else:
        raise HTTPException(status_code=404, detail="Path not in cache")


@app.delete("/cache")
async def clear_all():
    """Xóa toàn bộ cache"""
    count = clear_all_cache()
    return {"message": f"Cleared {count} cached indices"}


@app.post("/cache/reload/{path:path}")
async def reload_cache_path(path: str):
    """Reload 1 path (clear + load lại từ disk)"""
    try:
        _, load_time, docs_count = reload_index(path)
        return {
            "message": f"Reloaded index for {path}",
            "load_time_seconds": load_time,
            "docs_count": docs_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload: {str(e)}")


@app.post("/cache/reload")
async def reload_all():
    """Reload toàn bộ cache (DKM-PDFs mặc định)"""
    dkm_path = "/home/fong/Projects/mini-rag/DKM-PDFs"
    clear_all_cache()

    try:
        _, load_time, docs_count = reload_index(dkm_path)
        return {
            "message": "Reloaded all cache (DKM-PDFs)",
            "load_time_seconds": load_time,
            "docs_count": docs_count,
            "cached_paths": list(INDEX_CACHE.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=2011)
