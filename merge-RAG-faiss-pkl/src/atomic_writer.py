#!/usr/bin/env python
"""
Atomic write operations for FAISS merge to prevent data loss

Design:
1. Merge to temp dir first
2. Verify merge success
3. Atomic replace old index with new one
4. Auto-cleanup on failure

Author: AI Assistant
Date: 2025-11-19
LOC: ~80 (< 100)
"""
from __future__ import annotations
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Optional

from .config import TEMP_DIR_PREFIX, TEMP_BASE_DIR, ATOMIC_BACKUP_ENABLED
from .utils import console, print_info, print_success, print_warning, print_error


def create_temp_merge_dir(prefix: str = TEMP_DIR_PREFIX) -> Path:
    """
    Create secure temporary directory for merge operations

    Uses tempfile.mkdtemp() for security (0700 permissions)
    Dir persists until explicitly cleaned up

    Args:
        prefix: Prefix for temp dir name (default: "faiss-merge-")

    Returns:
        Path: Temporary directory path
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    temp_dir = Path(tempfile.mkdtemp(prefix=f"{prefix}{timestamp}-", dir=str(TEMP_BASE_DIR)))

    print_info(f"📁 Created temp merge dir: {temp_dir}")
    return temp_dir


def atomic_replace(temp_dir: Path, target_dir: Path, backup: bool = ATOMIC_BACKUP_ENABLED) -> bool:
    """
    Atomically replace target_dir with temp_dir + PERMANENT backup

    NEW Strategy (Zero Data Loss):
    1. Create backups/{timestamp}/ folder
    2. MOVE old files → backups/{timestamp}/ (NEVER delete)
    3. Move temp_dir → target_dir (atomic on same filesystem)
    4. Rollback from backup if move fails

    Args:
        temp_dir: Source temporary directory (merged index)
        target_dir: Target directory to replace
        backup: Create backup before replace (default: True)

    Returns:
        bool: True if successful, False otherwise
    """
    if not temp_dir.exists():
        print_error(f"❌ Temp dir not found: {temp_dir}")
        return False

    # Verify temp dir has required files
    if not (temp_dir / "index.faiss").exists() or not (temp_dir / "index.pkl").exists():
        print_error(f"❌ Temp dir missing FAISS files: {temp_dir}")
        return False

    backup_dir: Optional[Path] = None

    try:
        # Step 1: Create PERMANENT backup folder structure
        if target_dir.exists() and backup:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            backups_root = target_dir.parent / f"{target_dir.name}.backups"
            backup_dir = backups_root / timestamp
            backup_dir.mkdir(parents=True, exist_ok=True)

            print_info(f"💾 Backing up old index: {target_dir.name}/ → {target_dir.name}.backups/{timestamp}/")

            # Move old files to backup folder (NOT whole dir)
            for file in target_dir.iterdir():
                dest = backup_dir / file.name
                shutil.move(str(file), str(dest))
                console.print(f"[dim]  • {file.name} → backups/{timestamp}/{file.name}[/dim]")

            # Remove now-empty target dir
            target_dir.rmdir()

        # Step 2: Atomic move (rename on same filesystem)
        print_info(f"⚡ Atomic move: {temp_dir.name}/ → {target_dir.name}/")
        shutil.move(str(temp_dir), str(target_dir))

        # Step 3: KEEP backup (NEVER delete)
        if backup_dir and backup_dir.exists():
            print_success(f"✅ Backup preserved: {backup_dir.relative_to(target_dir.parent.parent)}")

        print_success(f"✅ Atomic replace successful: {target_dir}")
        return True

    except Exception as e:
        print_error(f"❌ Atomic replace failed: {e}")

        # Step 4: Rollback - restore backup if available
        if backup_dir and backup_dir.exists():
            print_warning(f"🔙 Rolling back: backups/{backup_dir.name}/ → {target_dir.name}/")
            try:
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                target_dir.mkdir(parents=True)
                for file in backup_dir.iterdir():
                    shutil.move(str(file), str(target_dir / file.name))
                print_success("✅ Rollback successful - old index restored")
            except Exception as rollback_error:
                print_error(f"❌ Rollback failed: {rollback_error}")

        return False


def cleanup_temp_dir(temp_dir: Path, force: bool = False) -> None:
    """
    Cleanup temporary directory

    Args:
        temp_dir: Temporary directory to cleanup
        force: Force cleanup even if dir has content (default: False)
    """
    if not temp_dir.exists():
        return

    try:
        if force or not any(temp_dir.iterdir()):
            shutil.rmtree(temp_dir)
            console.print(f"[dim]🗑️  Cleaned up temp dir: {temp_dir}[/dim]")
        else:
            print_warning(f"⚠️  Temp dir not empty, skipping cleanup: {temp_dir}")
    except Exception as e:
        print_warning(f"⚠️  Cleanup failed: {e}")
