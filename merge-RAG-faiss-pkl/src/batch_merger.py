#!/usr/bin/env python
"""
Batch merge strategy for large-scale FAISS index merging

Strategy: Divide & Conquer
1. Split N sources into M batches (batch_size each)
2. Merge each batch → batch_index_1, batch_index_2, ..., batch_index_M
3. Merge M batch_indexes → final_index

Benefits:
- Controlled RAM usage: max(batch_size * vector_size)
- Scalable to 1000+ books without OOM
- Intermediate batch indexes for debugging

Author: AI Assistant
Date: 2025-11-19
LOC: ~145 (< 150)
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
from typing import List
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn

from .config import MULTI_QUERY_SRC
from .utils import console, print_header, print_info, print_success, print_warning

# Add multi-query to path
sys.path.insert(0, str(MULTI_QUERY_SRC))


def split_into_batches(items: List[Path], batch_size: int) -> List[List[Path]]:
    """
    Split list into batches of fixed size

    Args:
        items: List of items to split
        batch_size: Maximum items per batch

    Returns:
        List of batches (each batch is a list of items)
    """
    batches = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batches.append(batch)

    print_info(f"📦 Split {len(items)} items into {len(batches)} batches (size={batch_size})")
    return batches


def merge_single_batch(
    batch_sources: List[Path],
    batch_id: int,
    output_dir: Path
) -> Path | None:
    """
    Merge a single batch of source indexes

    Args:
        batch_sources: List of source index paths for this batch
        batch_id: Batch number (for naming)
        output_dir: Output directory for batch index

    Returns:
        Path to merged batch index, or None if failed
    """
    from standalone_loader import get_embeddings_standalone, load_vectorstore_from_path  # type: ignore

    print_header(f"Batch {batch_id}: Merging {len(batch_sources)} indexes")

    base_index = None
    successful = 0
    failed = 0

    with Progress(SpinnerColumn(), *Progress.get_default_columns(), TimeElapsedColumn()) as progress:
        task = progress.add_task(f"[cyan]Batch {batch_id}...", total=len(batch_sources))

        for idx, source_path in enumerate(batch_sources, start=1):
            try:
                index = load_vectorstore_from_path(source_path)
                if base_index is None:
                    base_index = index
                else:
                    base_index.merge_from(index)
                successful += 1
                console.print(f"[green]✓[/green] [{idx}/{len(batch_sources)}] {source_path.name}")
            except Exception as e:
                console.print(f"[red]✗[/red] [{idx}/{len(batch_sources)}] {source_path.name}: {e}")
                failed += 1
            finally:
                progress.update(task, advance=1)

    # Save batch index
    if base_index:
        batch_dir = output_dir / f"batch_{batch_id:03d}"
        batch_dir.mkdir(parents=True, exist_ok=True)

        print_info(f"💾 Saving batch {batch_id} index: {batch_dir}")
        base_index.save_local(str(batch_dir))

        console.print(f"[green]✓[/green] Batch {batch_id}: {successful}/{len(batch_sources)} successful, {failed} failed")
        return batch_dir
    else:
        print_warning(f"⚠️  Batch {batch_id}: No index created (all failed)")
        return None


def merge_batch_indexes(batch_dirs: List[Path], output_dir: Path) -> bool:
    """
    Merge pre-computed batch indexes into final index

    Args:
        batch_dirs: List of batch index directories
        output_dir: Output directory for final merged index

    Returns:
        bool: True if successful, False otherwise
    """
    from standalone_loader import get_embeddings_standalone, load_vectorstore_from_path  # type: ignore

    print_header(f"Final Merge: Combining {len(batch_dirs)} batch indexes")

    embeddings = get_embeddings_standalone()
    base_index = None
    successful = 0
    failed = 0

    with Progress(SpinnerColumn(), *Progress.get_default_columns(), TimeElapsedColumn()) as progress:
        task = progress.add_task("[cyan]Merging batch indexes...", total=len(batch_dirs))

        for idx, batch_dir in enumerate(batch_dirs, start=1):
            try:
                console.print(f"[cyan]Merging batch {idx}/{len(batch_dirs)}:[/cyan] {batch_dir.name}")
                index = load_vectorstore_from_path(batch_dir)
                if base_index is None:
                    base_index = index
                else:
                    base_index.merge_from(index)
                successful += 1
                console.print(f"[green]✓[/green] {batch_dir.name}")
            except Exception as e:
                console.print(f"[red]✗[/red] {batch_dir.name}: {e}")
                failed += 1
            finally:
                progress.update(task, advance=1)

    # Save final index
    if base_index:
        print_info(f"💾 Saving final merged index: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)
        base_index.save_local(str(output_dir))

        print_success(f"✅ Final merge complete: {successful}/{len(batch_dirs)} batches merged")
        return True
    else:
        print_warning("⚠️  Final merge failed: No index created")
        return False


def batch_merge_all(
    source_paths: List[Path],
    output_dir: Path,
    batch_size: int = 100,
    keep_batches: bool = False
) -> bool:
    """
    Batch merge entry point - orchestrates the entire batch merge process

    Args:
        source_paths: List of source index paths
        output_dir: Final output directory
        batch_size: Sources per batch (default: 100)
        keep_batches: Keep intermediate batch indexes (default: False)

    Returns:
        bool: True if successful, False otherwise
    """
    start = time.perf_counter()

    # Step 1: Split into batches
    batches = split_into_batches(source_paths, batch_size)

    # Step 2: Merge each batch
    batch_output_dir = output_dir.parent / f"{output_dir.name}.batches"
    batch_output_dir.mkdir(parents=True, exist_ok=True)

    batch_dirs = []
    for batch_id, batch_sources in enumerate(batches, start=1):
        batch_dir = merge_single_batch(batch_sources, batch_id, batch_output_dir)
        if batch_dir:
            batch_dirs.append(batch_dir)

    if not batch_dirs:
        print_warning("⚠️  No batch indexes created - merge failed")
        return False

    # Step 3: Merge batch indexes into final index
    success = merge_batch_indexes(batch_dirs, output_dir)

    # Step 4: Cleanup intermediate batches (optional)
    if success and not keep_batches:
        print_info(f"🗑️  Cleaning up {len(batch_dirs)} batch indexes")
        import shutil
        shutil.rmtree(batch_output_dir)

    elapsed = time.perf_counter() - start
    if success:
        print_success(f"✅ Batch merge complete! ({elapsed:.2f}s)")

    return success
