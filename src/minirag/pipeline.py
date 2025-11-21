from __future__ import annotations
from typing import List
from langchain.docstore.document import Document
from .config import get_settings


def _format_docs(docs: List[Document]) -> str:
    """Format retrieved documents for AI pipeline consumption"""
    out = []
    for d in docs:
        src = d.metadata.get("source_file", "unknown")
        page = d.metadata.get("page")  # 0-indexed or None

        # Format with page number if available (1-indexed for humans)
        if page is not None:
            header = f"[{src}] Page {page + 1}"
        else:
            header = f"[{src}]"  # Fallback to old format

        out.append(f"{header}: {d.page_content.strip()}")
    return "\n---\n".join(out)


def get_context(store, query: str, top_k: int | None = None) -> str:
    """
    Retrieve relevant context for AI pipeline consumption.

    This is pure retrieval - no LLM generation.
    Output is structured text suitable for feeding into AI models.

    Args:
        store: FAISS vector store
        query: Search query (can be natural language, keywords, or structured)
        top_k: Number of chunks to retrieve (overrides config default if provided)

    Returns:
        Formatted context string with document sources
    """
    settings = get_settings()
    k = top_k if top_k is not None else settings.top_k
    retriever = store.as_retriever(search_kwargs={"k": k})

    # Get relevant documents via semantic search (LangChain invoke API with fallback)
    try:
        docs = retriever.invoke(query)  # LangChain 0.1.46+
    except AttributeError:
        docs = retriever.get_relevant_documents(query)
    if isinstance(docs, Document):
        docs = [docs]

    # Return formatted context for AI consumption
    return _format_docs(docs)


# Legacy compatibility function
def answer_question(store, question: str, top_k: int | None = None) -> str:
    """Legacy compatibility wrapper - returns pure context"""
    return get_context(store, question, top_k=top_k)
