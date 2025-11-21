#!/usr/bin/env python
from __future__ import annotations
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add src to path
SRC_PATH = Path(__file__).parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from src.hash_utils import (  # type: ignore
    compute_file_hash,
    get_cache_dir,
    is_trained,
    create_pdf_metadata
)
from src.train_config import get_settings  # type: ignore
from src.train_helpers import split_documents, get_embeddings  # type: ignore
from src.cleanup_utils import cleanup_orphaned_folders  # type: ignore

console = Console()


def setup_logging(log_dir: Path) -> str:
    """Setup logging to file and console"""
    log_dir.mkdir(exist_ok=True, parents=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"train_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return str(log_file)


def train_single_pdf(
    pdf_path: Path,
    cache_base_dir: Path,
    force_rebuild: bool = False
) -> dict:
    """
    Train a single PDF with hash-based caching.
    KISS: Cache directly in <hash>/ folder with index files.
    
    Args:
        pdf_path: Path to PDF file
        cache_base_dir: Base directory (DKM-PDFs)
        force_rebuild: Force rebuild even if cached
        
    Returns:
        Training result metadata
    """
    import time
    import shutil
    
    start_time = time.perf_counter()
    
    # Check if already trained
    trained, cache_dir = is_trained(pdf_path, cache_base_dir)
    
    if trained and not force_rebuild:
        console.print(f"[yellow]⚡ Cache hit:[/yellow] {pdf_path.name}")
        console.print(f"   [dim]Hash: {cache_dir.name}[/dim]")
        
        elapsed = time.perf_counter() - start_time
        return {
            "pdf": pdf_path.name,
            "status": "cached",
            "cache_dir": str(cache_dir),
            "hash": cache_dir.name,
            "time_taken": elapsed
        }
    
    # Train PDF
    console.print(f"[cyan]🔧 Training:[/cyan] {pdf_path.name}")
    console.print(f"   [dim]Hash: {compute_file_hash(pdf_path)}[/dim]")
    
    # Create cache directory
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Build vector store (standalone, no minirag dependency)
    try:
        from langchain_community.document_loaders import PyPDFLoader
        from langchain_community.vectorstores import FAISS
        
        # Load PDF directly
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        
        # Add metadata
        for doc in docs:
            doc.metadata["source_file"] = pdf_path.name
        
        # Split documents
        chunks = split_documents(docs)
        console.print(f"   [dim]Chunks: {len(chunks)}[/dim]")
        
        # Filter invalid chunks (must have valid string content)
        valid_chunks = []
        for chunk in chunks:
            if (hasattr(chunk, 'page_content') and 
                chunk.page_content and 
                isinstance(chunk.page_content, str) and
                chunk.page_content.strip()):
                valid_chunks.append(chunk)
        
        if len(valid_chunks) < len(chunks):
            console.print(f"   [yellow]⚠ Filtered {len(chunks) - len(valid_chunks)} invalid chunks[/yellow]")
        
        if not valid_chunks:
            raise ValueError("No valid chunks found after filtering")
        
        console.print(f"   [dim]Valid chunks: {len(valid_chunks)}[/dim]")
        
        # Build FAISS index
        embeddings = get_embeddings()
        store = FAISS.from_documents(valid_chunks, embeddings)
        
        # Save directly to cache_dir (creates index.faiss and index.pkl)
        store.save_local(str(cache_dir))
        
        # Create manifest
        manifest = {
            "files": {
                pdf_path.name: {
                    "md5": compute_file_hash(pdf_path),
                    "size": pdf_path.stat().st_size,
                    "mtime": pdf_path.stat().st_mtime
                }
            }
        }
        (cache_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
        
        # Create metadata
        metadata = create_pdf_metadata(pdf_path, cache_dir)
        (cache_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
        
        elapsed = time.perf_counter() - start_time
        
        console.print(f"[green]✓ Trained:[/green] {pdf_path.name} ({elapsed:.2f}s)")
        
        return {
            "pdf": pdf_path.name,
            "status": "trained",
            "cache_dir": str(cache_dir),
            "hash": cache_dir.name,
            "chunks": len(chunks),
            "time_taken": elapsed,
            "metadata": metadata
        }
        
    except Exception as e:
        elapsed = time.perf_counter() - start_time
        console.print(f"[red]✗ Failed:[/red] {pdf_path.name}")
        console.print(f"   [red]Error: {e}[/red]")
        logging.error(f"Failed to train {pdf_path.name}: {e}", exc_info=True)
        
        return {
            "pdf": pdf_path.name,
            "status": "failed",
            "error": str(e),
            "time_taken": elapsed
        }


def train_all_pdfs(
    pdf_dir: Path,
    cache_base_dir: Path,
    force_rebuild: bool = False
) -> list[dict]:
    """
    Train all PDFs in a directory.

    Args:
        pdf_dir: Directory containing PDFs
        cache_base_dir: Base directory for caches
        force_rebuild: Force rebuild all

    Returns:
        List of training results
    """
    # Find all PDFs (case-insensitive: both .pdf and .PDF)
    pdf_files_lower = list(pdf_dir.glob("*.pdf"))
    pdf_files_upper = list(pdf_dir.glob("*.PDF"))
    pdf_files = sorted(set(pdf_files_lower + pdf_files_upper))
    
    if not pdf_files:
        console.print(f"[red]No PDF files found in {pdf_dir}")
        return []
    
    console.print(f"\n[bold]Found {len(pdf_files)} PDF file(s)[/bold]\n")
    
    results = []
    for pdf_path in pdf_files:
        result = train_single_pdf(pdf_path, cache_base_dir, force_rebuild)
        results.append(result)
        console.print()  # Empty line
    
    return results


def print_summary(results: list[dict]) -> None:
    """Print training summary"""
    from rich.table import Table
    
    table = Table(title="Training Summary")
    table.add_column("PDF", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Time (s)", justify="right", style="magenta")
    
    total_time = 0
    cached_count = 0
    trained_count = 0
    failed_count = 0
    
    for result in results:
        status = result["status"]
        if status == "cached":
            status_display = "⚡ Cached"
            cached_count += 1
        elif status == "trained":
            status_display = "✓ Trained"
            trained_count += 1
        else:
            status_display = "✗ Failed"
            failed_count += 1
        
        table.add_row(
            result["pdf"],
            status_display,
            f"{result['time_taken']:.2f}"
        )
        total_time += result["time_taken"]
    
    console.print("\n")
    console.print(table)
    console.print(f"\n[bold]Statistics:[/bold]")
    console.print(f"  Cached: {cached_count}")
    console.print(f"  Newly trained: {trained_count}")
    console.print(f"  Failed: {failed_count}")
    console.print(f"  Total time: {total_time:.2f}s")


def parse_args() -> argparse.Namespace:
    settings = get_settings()  # Get defaults
    
    parser = argparse.ArgumentParser(
        description="Train PDFs with hash-based caching",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Train all PDFs in default directory
  %(prog)s
  
  # Force rebuild all
  %(prog)s --force-rebuild
  
  # Custom directories
  %(prog)s --pdf-dir /path/to/pdfs --cache-dir /path/to/cache
        """
    )
    
    parser.add_argument(
        "--pdf-dir",
        type=str,
        default=settings.pdf_dir,
        help=f"Directory containing PDFs (default: {settings.pdf_dir})"
    )
    
    parser.add_argument(
        "--cache-dir",
        type=str,
        default=settings.cache_dir,
        help=f"Base cache directory (default: {settings.cache_dir})"
    )
    
    parser.add_argument(
        "--force-rebuild",
        action="store_true",
        help="Force rebuild even if cached"
    )
    
    parser.add_argument(
        "--list-cache",
        action="store_true",
        help="List cached PDFs and exit"
    )

    parser.add_argument(
        "--cleanup-orphaned",
        action="store_true",
        help="Cleanup orphaned cache folders after training"
    )

    parser.add_argument(
        "--cleanup-dry-run",
        action="store_true",
        help="Preview orphaned folders without deleting (implies --cleanup-orphaned)"
    )

    return parser.parse_args()


def list_cached_pdfs(cache_base_dir: Path) -> None:
    """List all cached PDFs"""
    from rich.table import Table
    
    if not cache_base_dir.exists():
        console.print(f"[yellow]No cache directory found: {cache_base_dir}")
        return
    
    table = Table(title="Cached PDFs")
    table.add_column("Hash", style="cyan")
    table.add_column("PDF Name", style="green")
    table.add_column("Trained At", style="dim")
    
    cached_count = 0
    
    for cache_dir in cache_base_dir.iterdir():
        if not cache_dir.is_dir():
            continue
        
        metadata_file = cache_dir / "metadata.json"
        if metadata_file.exists():
            metadata = json.loads(metadata_file.read_text())
            table.add_row(
                cache_dir.name[:16] + "...",
                metadata.get("filename", "unknown"),
                metadata.get("trained_at", "unknown")
            )
            cached_count += 1
    
    console.print(table)
    console.print(f"\n[bold]Total cached:[/bold] {cached_count}")


def main() -> int:
    args = parse_args()
    
    pdf_dir = Path(args.pdf_dir)
    cache_base_dir = Path(args.cache_dir)
    
    # Setup logging
    PROJECT_ROOT = Path(__file__).parent.parent
    log_dir = PROJECT_ROOT / "logs"
    log_file = setup_logging(log_dir)
    
    console.print("[bold]Mini-RAG Training System[/bold]")
    console.print(f"[dim]Log file: {log_file}[/dim]\n")
    
    # List cache mode
    if args.list_cache:
        list_cached_pdfs(cache_base_dir)
        return 0
    
    # Validate directories
    if not pdf_dir.exists():
        console.print(f"[red]Error: PDF directory not found: {pdf_dir}")
        return 1
    
    cache_base_dir.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[bold]Configuration:[/bold]")
    console.print(f"  PDF directory: {pdf_dir}")
    console.print(f"  Cache directory: {cache_base_dir}")
    console.print(f"  Force rebuild: {args.force_rebuild}")
    console.print(f"  Cleanup orphaned: {args.cleanup_orphaned or args.cleanup_dry_run}")
    
    # Train PDFs
    try:
        results = train_all_pdfs(pdf_dir, cache_base_dir, args.force_rebuild)
        
        if not results:
            return 1
        
        # Print summary
        print_summary(results)
        
        # Save results
        results_dir = PROJECT_ROOT / "results"
        results_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"training_{timestamp}.json"
        results_file.write_text(json.dumps(results, indent=2))
        
        console.print(f"\n[bold]📄 Results saved to:[/bold] {results_file}")

        # Cleanup orphaned folders if requested
        if args.cleanup_orphaned or args.cleanup_dry_run:
            try:
                removed, kept = cleanup_orphaned_folders(
                    cache_base_dir=cache_base_dir,
                    pdf_dir=pdf_dir,
                    dry_run=args.cleanup_dry_run,
                    require_confirmation=not args.cleanup_dry_run  # Auto-confirm in dry-run
                )

                console.print(f"\n[bold]🧹 Cleanup Summary:[/bold]")
                console.print(f"  Orphaned removed: {removed}")
                console.print(f"  Valid kept: {kept}")

            except Exception as e:
                console.print(f"\n[red]Warning: Cleanup failed: {e}[/red]")
                logging.error(f"Cleanup failed: {e}", exc_info=True)

        # Check if any failed
        failed = [r for r in results if r["status"] == "failed"]
        return 1 if failed else 0
        
    except Exception as e:
        console.print(f"\n[red]Error: {e}")
        logging.error(f"Training failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
