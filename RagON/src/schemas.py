"""Pydantic schemas cho RagON API"""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class QueryRequest(BaseModel):
    """Request schema cho /query endpoint"""
    pdf_directory: str = "/home/fong/Projects/mini-rag/DKM-PDFs"
    question: str
    top_k: Optional[int] = None


class QueryResponse(BaseModel):
    """Response schema cho /query endpoint"""
    answer: str
    sources: list
    load_time_seconds: float
    retrieval_time_seconds: float
    from_cache: bool
