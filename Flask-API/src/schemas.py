"""Pydantic schemas cho RagON API"""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from .settings import DKM_PDF_PATH


class QueryRequest(BaseModel):
    """Request schema cho /query endpoint"""
    pdf_directory: str = DKM_PDF_PATH
    question: str
    top_k: Optional[int] = None


class QueryResponse(BaseModel):
    """Response schema cho /query endpoint"""
    answer: str
    sources: list
    load_time_seconds: float
    retrieval_time_seconds: float
    from_cache: bool
