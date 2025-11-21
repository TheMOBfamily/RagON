from __future__ import annotations
import shutil
from pathlib import Path
from typing import Set, Tuple
from rich.console import Console
from rich.table import Table

try:
    from .hash_utils import compute_file_hash
except ImportError:
    from hash_utils import compute_file_hash

console = Console()


def find_all_current_pdf_hashes(pdf_dir: Path) -> Set[str]:
    """
    Compute MD5 hash của tất cả PDF files hiện tại.

    Args:
        pdf_dir: Directory chứa PDF files

    Returns:
        Set of MD5 hashes (valid hashes)
    """
    # Support both .pdf and .PDF extensions
    pdf_files_lower = list(pdf_dir.glob("*.pdf"))
    pdf_files_upper = list(pdf_dir.glob("*.PDF"))
    pdf_files = sorted(set(pdf_files_lower + pdf_files_upper))

    valid_hashes = set()

    console.print(f"[cyan]📄 Scanning {len(pdf_files)} PDF files...[/cyan]")

    for pdf_path in pdf_files:
        try:
            pdf_hash = compute_file_hash(pdf_path)
            valid_hashes.add(pdf_hash)
        except Exception as e:
            console.print(f"[yellow]⚠ Warning: Failed to hash {pdf_path.name}: {e}[/yellow]")

    console.print(f"[green]✓ Found {len(valid_hashes)} unique PDF hashes[/green]")
    return valid_hashes


def find_all_cache_folders(cache_base_dir: Path) -> Set[str]:
    """
    Find all hash folders in cache directory.

    Args:
        cache_base_dir: Base cache directory

    Returns:
        Set of folder names (MD5 hashes)
    """
    if not cache_base_dir.exists():
        return set()

    cache_folders = set()

    for item in cache_base_dir.iterdir():
        if not item.is_dir():
            continue

        # Check if folder name looks like MD5 hash (32 hex chars)
        if len(item.name) == 32 and all(c in '0123456789abcdef' for c in item.name):
            cache_folders.add(item.name)

    return cache_folders


def identify_orphaned_folders(
    valid_hashes: Set[str],
    cache_folders: Set[str]
) -> Set[str]:
    """
    Identify orphaned cache folders.

    Args:
        valid_hashes: Set of valid PDF hashes
        cache_folders: Set of existing cache folder hashes

    Returns:
        Set of orphaned folder hashes
    """
    orphaned = cache_folders - valid_hashes
    return orphaned


def cleanup_orphaned_folders(
    cache_base_dir: Path,
    pdf_dir: Path | None = None,
    dry_run: bool = False,
    require_confirmation: bool = True
) -> Tuple[int, int]:
    """
    Cleanup orphaned cache folders.

    Args:
        cache_base_dir: Base cache directory
        pdf_dir: PDF directory (defaults to cache_base_dir)
        dry_run: Preview only, don't delete
        require_confirmation: Ask before deleting if orphaned > 10

    Returns:
        (removed_count, kept_count)
    """
    if pdf_dir is None:
        pdf_dir = cache_base_dir

    console.print("\n[bold cyan]🧹 Orphaned Cache Cleanup[/bold cyan]\n")

    # Step 1: Find current PDF hashes
    valid_hashes = find_all_current_pdf_hashes(pdf_dir)

    # Step 2: Find cache folders
    console.print(f"[cyan]📁 Scanning cache folders...[/cyan]")
    cache_folders = find_all_cache_folders(cache_base_dir)
    console.print(f"[green]✓ Found {len(cache_folders)} cache folders[/green]\n")

    # Step 3: Identify orphaned
    orphaned = identify_orphaned_folders(valid_hashes, cache_folders)

    if not orphaned:
        console.print("[green]✨ No orphaned folders found! All caches are valid.[/green]")
        return 0, len(cache_folders)

    # Step 4: Display orphaned folders
    console.print(f"[yellow]⚠ Found {len(orphaned)} orphaned folders:[/yellow]\n")

    table = Table(title="Orphaned Cache Folders")
    table.add_column("Hash", style="dim")
    table.add_column("Path", style="yellow")

    orphaned_list = sorted(orphaned)[:20]  # Show first 20
    for folder_hash in orphaned_list:
        folder_path = cache_base_dir / folder_hash
        table.add_row(
            folder_hash[:16] + "...",
            str(folder_path.relative_to(cache_base_dir.parent))
        )

    if len(orphaned) > 20:
        table.add_row("...", f"(and {len(orphaned) - 20} more)")

    console.print(table)
    console.print()

    # Calculate space
    total_size = 0
    for folder_hash in orphaned:
        folder_path = cache_base_dir / folder_hash
        if folder_path.exists():
            # Estimate size
            for file in folder_path.rglob("*"):
                if file.is_file():
                    total_size += file.stat().st_size

    size_mb = total_size / (1024 * 1024)
    console.print(f"[dim]Estimated space to free: {size_mb:.1f} MB[/dim]\n")

    # Dry-run mode
    if dry_run:
        console.print("[yellow]🔍 DRY-RUN MODE: No folders will be deleted[/yellow]")
        return 0, len(cache_folders)

    # Confirmation
    if require_confirmation and len(orphaned) > 10:
        console.print(f"[bold red]⚠ About to delete {len(orphaned)} folders![/bold red]")
        response = input("Continue? (yes/no): ").lower().strip()
        if response not in ["yes", "y"]:
            console.print("[yellow]Cleanup cancelled by user[/yellow]")
            return 0, len(cache_folders)

    # Step 5: Delete orphaned folders
    console.print(f"[cyan]🗑 Removing {len(orphaned)} orphaned folders...[/cyan]")

    removed_count = 0
    for folder_hash in orphaned:
        folder_path = cache_base_dir / folder_hash
        try:
            if folder_path.exists():
                shutil.rmtree(folder_path)
                removed_count += 1
        except Exception as e:
            console.print(f"[red]✗ Failed to remove {folder_hash}: {e}[/red]")

    kept_count = len(cache_folders) - removed_count

    console.print(f"[green]✓ Successfully removed {removed_count} orphaned folders[/green]")
    console.print(f"[green]✓ Kept {kept_count} valid cache folders[/green]")
    console.print(f"[green]✓ Freed ~{size_mb:.1f} MB of space[/green]\n")

    return removed_count, kept_count
