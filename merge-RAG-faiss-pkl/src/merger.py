#!/usr/bin/env python
"""
FAISS index merger with CRUD-aware incremental updates

Author: AI Assistant
Date: 2025-10-26
LOC: ~95 (< 100)
"""
from __future__ import annotations
import sys
import time
import shutil
from pathlib import Path
from datetime import datetime
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn

from .config import (
    MULTI_QUERY_SRC, MANIFEST_PATH, MERGED_INDEX_DIR,
    ATOMIC_WRITE_ENABLED, BATCH_THRESHOLD, BATCH_SIZE_DEFAULT
)
from .manifest import load_manifest, update_manifest, save_manifest
from .utils import console, print_header, print_info, print_success, print_warning
from .atomic_writer import create_temp_merge_dir, atomic_replace, cleanup_temp_dir
from .batch_merger import batch_merge_all

# Add multi-query to path
sys.path.insert(0, str(MULTI_QUERY_SRC))


def merge_indexes(
    base_dir: Path,
    output_dir: Path,
    limit: int | None = None,
    dry_run: bool = False,
    atomic: bool = ATOMIC_WRITE_ENABLED,  # Use config.py default
    batch_size: int | None = None
):
    """
    Merge FAISS indexes with CRUD detection and safety features

    Features:
    - CRUD detection: Only merge when concatenated hash changes
    - Atomic write: Merge to temp dir → atomic replace (zero data loss)
    - Batch mode: Split into batches for large-scale (>500 books)

    Args:
        base_dir: Base directory containing source indexes
        output_dir: Output directory for merged index
        limit: Limit number of sources (for testing)
        dry_run: Preview only, no files modified
        atomic: Use atomic write pattern (default: True)
        batch_size: Enable batch mode with specified batch size (default: None)
    """
    from source_manager import list_sources  # type: ignore
    from standalone_loader import get_embeddings_standalone, load_vectorstore_from_path  # type: ignore

    manifest_path = MANIFEST_PATH
    manifest = load_manifest(manifest_path)

    # Get sources
    sources = list_sources(str(base_dir))
    total = len(sources)

    if limit:
        sources = sources[:limit]
        print_warning(f"🧪 TEST MODE: Limiting to {len(sources)}/{total} PDFs")

    source_paths = [Path(s.path) for s in sources]

    # Update manifest + check concat hash
    manifest, indexes_changed, concat_changed = update_manifest(manifest, source_paths)

    print_header("Manifest Check")
    console.print(f"  Total indexes tracked: {len(manifest['merge_tracking']['indexes'])}")
    console.print(f"  Indexes changed: {indexes_changed}")
    console.print(f"  Concatenated hash changed: {concat_changed}")
    console.print(f"  Current concat MD5: {manifest['merge_tracking']['concat_md5']}")

    # Decide if merge needed
    need_merge = concat_changed or not output_dir.exists()

    if not need_merge:
        print_success("\n✅ No CRUD detected - skipping merge")
        save_manifest(manifest_path, manifest, dry_run)
        return

    if concat_changed:
        print_warning("\n🔄 CRUD detected - merge required!")
    else:
        print_info("\n🆕 First merge - creating index...")

    if dry_run:
        print_warning("\nDRY RUN MODE - No files modified")
        save_manifest(manifest_path, manifest, dry_run=True)
        return

    # Auto-detect batch mode (use config.py constants)
    if batch_size is None and len(source_paths) > BATCH_THRESHOLD:
        batch_size = BATCH_SIZE_DEFAULT
        print_info(f"🎯 Auto-enabled batch mode: {len(source_paths)} sources > {BATCH_THRESHOLD} threshold")

    use_batch_mode = batch_size is not None and batch_size > 0
    if use_batch_mode:
        print_info(f"📦 Batch mode: {len(source_paths)} sources, batch_size={batch_size}")

    # Create temp dir for atomic write (if atomic=True)
    temp_dir = None
    merge_target_dir = output_dir

    if atomic:
        temp_dir = create_temp_merge_dir()
        merge_target_dir = temp_dir
        print_info(f"⚛️  Atomic mode: Merging to temp dir first")

    try:
        # Execute merge (batch or normal)
        start = time.perf_counter()

        if use_batch_mode:
            # Batch merge
            success = batch_merge_all(source_paths, merge_target_dir, batch_size, keep_batches=False)
            if not success:
                raise RuntimeError("Batch merge failed")
        else:
            # Normal merge (legacy)
            print_header(f"Merging {len(source_paths)} indexes")
            console.print(f"Output: {merge_target_dir}")

            print_info("\nLoading embeddings model...")
            embeddings = get_embeddings_standalone()

            base_index = None
            successful = 0
            failed = 0

            with Progress(SpinnerColumn(), *Progress.get_default_columns(), TimeElapsedColumn()) as progress:
                task = progress.add_task("[cyan]Merging...", total=len(source_paths))

                for idx, source_path in enumerate(source_paths, start=1):
                    try:
                        console.print(f"[cyan]Merging {idx}/{len(source_paths)}:[/cyan] {source_path.name}")
                        index = load_vectorstore_from_path(source_path)
                        if base_index is None:
                            base_index = index
                        else:
                            base_index.merge_from(index)
                        successful += 1
                        console.print(f"[green]✓[/green] {source_path.name}")
                    except Exception as e:
                        console.print(f"[red]✗[/red] {source_path.name}: {e}")
                        failed += 1
                    finally:
                        progress.update(task, advance=1)

            # Save merged index
            if base_index:
                print_info("\nSaving merged index...")
                merge_target_dir.mkdir(parents=True, exist_ok=True)
                base_index.save_local(str(merge_target_dir))

                console.print(f"Successful: {successful}/{len(source_paths)}")
                console.print(f"Failed: {failed}/{len(source_paths)}")
            else:
                raise RuntimeError("No index created - all merges failed")

        elapsed = time.perf_counter() - start

        # Atomic replace (if atomic=True)
        if atomic and temp_dir:
            if atomic_replace(temp_dir, output_dir, backup=True):
                print_success(f"⚛️  Atomic replace successful!")
            else:
                raise RuntimeError("Atomic replace failed")

        # Update manifest
        manifest["merge_tracking"]["last_merged_at"] = datetime.now().isoformat()
        save_manifest(manifest_path, manifest, dry_run=False)

        print_success(f"\n✅ Merge complete! ({elapsed:.2f}s)")

    except Exception as e:
        console.print(f"[red]❌ Merge failed: {e}[/red]")
        # Cleanup temp dir on failure
        if atomic and temp_dir:
            cleanup_temp_dir(temp_dir, force=True)
        raise

    finally:
        # Cleanup temp dir if atomic mode succeeded (temp_dir already moved)
        if atomic and temp_dir and not temp_dir.exists():
            console.print("[dim]✅ Temp dir auto-cleaned (moved to target)[/dim]")
