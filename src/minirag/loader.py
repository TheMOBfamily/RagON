from __future__ import annotations
import os
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.docstore.document import Document


def load_pdfs(pdf_dir: str) -> List[Document]:
    """Load all PDF files from a directory into Documents.
    Simple sequential loader (can be optimized with concurrency later).
    """
    p = Path(pdf_dir)
    if not p.exists() or not p.is_dir():
        raise FileNotFoundError(f"PDF directory not found: {pdf_dir}")

    pdf_files = sorted([f for f in p.iterdir() if f.suffix.lower() == ".pdf"])
    if not pdf_files:
        raise ValueError(f"No PDF files found in directory: {pdf_dir}")

    docs: List[Document] = []
    for pdf in pdf_files:
        loader = PyPDFLoader(str(pdf))
        pages = loader.load()
        # store original file path in metadata
        for d in pages:
            d.metadata["source_file"] = pdf.name
        docs.extend(pages)
    return docs
