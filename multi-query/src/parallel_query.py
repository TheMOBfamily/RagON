from __future__ import annotations
import sys
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import List
from concurrent.futures import ProcessPoolExecutor, as_completed
from rich.console import Console

# Standalone - NO minirag imports!
from .standalone_loader import load_vectorstore_from_path, get_context_standalone
from .utils import timed, safe_path_name

console = Console()


@dataclass
class SourceResult:
    """Result from querying a single RAG source"""
    source_name: str
    source_path: str
    context: str
    time_taken: float
    error: str | None = None
    
    @property
    def success(self) -> bool:
        return self.error is None


def query_single_source(source_path: str, query: str, top_k: int) -> SourceResult:
    """
    Query a single RAG source (standalone, no minirag).
    Handles both hash-based and traditional FAISS formats.
    """
    import time
    start = time.perf_counter()
    source_name = safe_path_name(source_path)
    
    try:
        # Load vectorstore (standalone)
        store = load_vectorstore_from_path(source_path)
        
        # Get context (standalone)
        context = get_context_standalone(store, query, top_k)
        
        time_taken = time.perf_counter() - start
        
        return SourceResult(
            source_name=source_name,
            source_path=source_path,
            context=context,
            time_taken=time_taken,
            error=None
        )
    except Exception as e:
        time_taken = time.perf_counter() - start
        error_msg = f"{type(e).__name__}: {str(e)}"
        logging.error(f"Error querying source {source_name}: {error_msg}")
        
        return SourceResult(
            source_name=source_name,
            source_path=source_path,
            context="",
            time_taken=time_taken,
            error=error_msg
        )


def query_all_sources_parallel(
    source_paths: List[str],
    query: str,
    max_workers: int = 4,
    timeout: int = 30,
    top_k: int = 4
) -> List[SourceResult]:
    """
    Query multiple RAG sources in parallel using ProcessPoolExecutor.
    
    CRITICAL: Uses ProcessPoolExecutor (not Thread) because PyTorch models
    are NOT thread-safe. Each process gets its own memory space and model instance.
    
    Args:
        source_paths: List of paths to PDF folders
        query: Search query
        max_workers: Max concurrent workers (processes)
        timeout: Timeout per source in seconds
        top_k: Number of results per source
        
    Returns:
        List of SourceResult (includes both success and failures)
    """
    results: List[SourceResult] = []
    
    with timed(f"Parallel query of {len(source_paths)} sources"):
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_source = {
                executor.submit(query_single_source, path, query, top_k): path
                for path in source_paths
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_source, timeout=timeout * len(source_paths)):
                source_path = future_to_source[future]
                try:
                    result = future.result(timeout=timeout)
                    results.append(result)
                    
                    if result.success:
                        console.print(
                            f"[green]✓[/green] {result.source_name} "
                            f"({result.time_taken:.2f}s)"
                        )
                    else:
                        # Technical error - show brief status (details in log)
                        console.print(
                            f"[yellow]○[/yellow] {result.source_name} "
                            f"({result.time_taken:.2f}s) - skipped"
                        )
                        
                except Exception as e:
                    error_msg = f"Timeout or error: {e}"
                    logging.error(f"Failed to get result from {source_path}: {error_msg}")
                    results.append(SourceResult(
                        source_name=safe_path_name(source_path),
                        source_path=source_path,
                        context="",
                        time_taken=timeout,
                        error=error_msg
                    ))
    
    return results
