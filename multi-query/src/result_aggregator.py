from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
from pathlib import Path
import json
from .parallel_query import SourceResult
from .utils import compute_content_hash


@dataclass
class DeduplicatedChunk:
    """A chunk with source tracking"""
    content: str
    sources: List[str]
    content_hash: str
    
    def add_source(self, source: str) -> None:
        if source not in self.sources:
            self.sources.append(source)


@dataclass
class AggregatedResult:
    """Aggregated results from multiple sources"""
    query: str
    chunks: List[DeduplicatedChunk]
    source_results: List[SourceResult]
    total_time: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def successful_sources(self) -> List[SourceResult]:
        return [r for r in self.source_results if r.success]
    
    @property
    def failed_sources(self) -> List[SourceResult]:
        return [r for r in self.source_results if not r.success]
    
    @property
    def total_chunks_before_dedup(self) -> int:
        count = 0
        for result in self.successful_sources:
            count += len(result.context.split('\n---\n'))
        return count
    
    @property
    def duplicates_removed(self) -> int:
        return self.total_chunks_before_dedup - len(self.chunks)


def parse_context_chunks(context: str) -> List[str]:
    """Parse context string into individual chunks"""
    if not context.strip():
        return []
    return [chunk.strip() for chunk in context.split('\n---\n') if chunk.strip()]


def aggregate_results(
    source_results: List[SourceResult],
    query: str,
    total_time: float
) -> AggregatedResult:
    """
    Aggregate and deduplicate results from multiple sources.
    
    Deduplication strategy:
    - Use MD5 hash of normalized content
    - Track which sources contributed each chunk
    - Preserve order from first occurrence
    """
    seen_hashes: Dict[str, DeduplicatedChunk] = {}
    
    for result in source_results:
        if not result.success:
            continue
        
        chunks = parse_context_chunks(result.context)
        
        for chunk in chunks:
            # Normalize and hash
            normalized = chunk.strip()
            if not normalized:
                continue
                
            chunk_hash = compute_content_hash(normalized)
            
            if chunk_hash in seen_hashes:
                # Already seen, add source
                seen_hashes[chunk_hash].add_source(result.source_name)
            else:
                # New chunk
                seen_hashes[chunk_hash] = DeduplicatedChunk(
                    content=normalized,
                    sources=[result.source_name],
                    content_hash=chunk_hash
                )
    
    # Preserve order
    deduplicated_chunks = list(seen_hashes.values())
    
    return AggregatedResult(
        query=query,
        chunks=deduplicated_chunks,
        source_results=source_results,
        total_time=total_time
    )


def _get_pdf_filename_from_hash(hash_path: str) -> str:
    """
    Get actual PDF filename from hash directory by reading manifest.json
    
    Args:
        hash_path: Path like '/path/to/DKM-PDFs/abc123...'
        
    Returns:
        PDF filename or hash if manifest not found
    """
    try:
        manifest_path = Path(hash_path) / "manifest.json"
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
                # manifest format: {"files": {"filename.pdf": {...}}}
                files = manifest.get("files", {})
                if files:
                    # Return first (and usually only) filename
                    return list(files.keys())[0]
    except Exception:
        pass
    
    # Fallback to hash
    return Path(hash_path).name


def format_json_output(result: AggregatedResult) -> dict:
    """
    Format aggregated result as simplified JSON structure.
    
    SIMPLIFIED OUTPUT:
    - NO details per source (removed for brevity)
    - NO rank, sources array, content_hash (removed clutter)
    - Show actual PDF filename instead of hash
    """
    
    # Prepare results: simplified format
    results = []
    for chunk in result.chunks:
        # Get PDF filename from first source hash
        if chunk.sources:
            # Find source path from source_results
            source_hash = chunk.sources[0]
            source_path = None
            for sr in result.source_results:
                if sr.source_name == source_hash:
                    source_path = sr.source_path
                    break
            
            if source_path:
                pdf_filename = _get_pdf_filename_from_hash(source_path)
            else:
                pdf_filename = source_hash
        else:
            pdf_filename = "unknown"
        
        results.append({
            "source": pdf_filename,
            "content": chunk.content
        })
    
    # Build final JSON: simplified structure
    output = {
        "query": result.query,
        "timestamp": result.timestamp,
        "sources": {
            "total": len(result.source_results),
            "successful": len(result.successful_sources),
            "failed": len(result.failed_sources)
        },
        "results": {
            "total_found": len(result.chunks),
            "duplicates_removed": result.duplicates_removed,
            "data": results
        },
        "execution": {
            "total_time_seconds": round(result.total_time, 2)
        }
    }
    
    return output


def format_markdown_output(result: AggregatedResult) -> str:
    """Format aggregated result as markdown (DEPRECATED - use JSON)"""
    lines = [
        "# Multi-RAG Query Results",
        "",
        "## Query",
        result.query,
        "",
        "## Sources Queried",
        ""
    ]
    
    # List sources
    for sr in result.successful_sources:
        lines.append(f"- ✅ **{sr.source_name}** ({sr.time_taken:.2f}s)")
    
    for sr in result.failed_sources:
        lines.append(f"- ❌ **{sr.source_name}** ({sr.time_taken:.2f}s) - {sr.error}")
    
    lines.extend(["", "## Aggregated Results", ""])
    
    if not result.chunks:
        lines.append("*No results found*")
    else:
        for idx, chunk in enumerate(result.chunks, 1):
            lines.append(f"### Result {idx}")
            
            # Show sources
            if len(chunk.sources) == 1:
                lines.append(f"**Source:** {chunk.sources[0]}")
            else:
                sources_str = ", ".join(chunk.sources)
                lines.append(f"**Sources:** {sources_str}")
            
            lines.append("")
            lines.append(chunk.content)
            lines.append("")
    
    # Stats
    lines.extend([
        "## Execution Statistics",
        "",
        f"- **Total time:** {result.total_time:.2f}s",
        f"- **Sources queried:** {len(result.successful_sources)}/{len(result.source_results)}",
        f"- **Results found:** {len(result.chunks)}",
        f"- **Duplicates removed:** {result.duplicates_removed}",
        f"- **Timestamp:** {result.timestamp}",
        ""
    ])
    
    return "\n".join(lines)
