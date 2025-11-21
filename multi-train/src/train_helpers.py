from __future__ import annotations
from typing import List, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from .train_config import get_settings


def split_documents(docs: List[Document]) -> List[Document]:
    """Split documents into chunks (standalone, copied from minirag)"""
    settings = get_settings()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " "]
    )
    return splitter.split_documents(docs)


def get_embeddings() -> Any:
    """Get HuggingFace embeddings (standalone, copied from minirag)"""
    settings = get_settings()
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=settings.hf_embeddings_model)
    except ImportError:
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            return HuggingFaceEmbeddings(model_name=settings.hf_embeddings_model)
        except Exception as e:
            raise RuntimeError(f"Cannot load HuggingFace embeddings: {e}")
