#!/usr/bin/env python
"""
Manifest CRUD operations
Track index states with concatenated hash for CRUD detection

Author: AI Assistant
Date: 2025-10-26
LOC: ~95 (< 100)
"""
from __future__ import annotations
import json
import shutil
from pathlib import Path
from datetime import datetime
from .config import MANIFEST_VERSION, MANIFEST_BACKUP_SUFFIX
from .hash_utils import compute_index_hash, compute_concatenated_hash
from .utils import console, print_info, print_warning


def load_manifest(manifest_path: Path) -> dict:
    """Load or create manifest with schema v1"""
    if manifest_path.exists():
        print_info(f"Loading manifest from {manifest_path}")
        with open(manifest_path, "r") as f:
            data = json.load(f)

        # Migrate old schema if needed
        if "indexes" in data and "merge_tracking" not in data:
            print_warning("⚠️  Migrating old schema to v1...")
            data = _migrate_to_v1(data)

        # Ensure merge_tracking exists
        if "merge_tracking" not in data:
            data["merge_tracking"] = _empty_tracking()

        return data

    print_info("Creating new manifest")
    return _create_manifest()


def update_manifest(manifest: dict, source_paths: list[Path]) -> tuple[dict, bool, bool]:
    """
    Update manifest with current index states + concatenated hash
    Returns: (updated_manifest, indexes_changed, concat_hash_changed)
    """
    indexes_changed = False
    hash_ids = []

    for source_path in source_paths:
        hash_id = source_path.name
        current_hash = compute_index_hash(source_path)

        if not current_hash:
            print_warning(f"⚠️  Skipping {hash_id} (no index files)")
            continue

        hash_ids.append(hash_id)

        # Check if changed
        existing = manifest["merge_tracking"]["indexes"].get(hash_id, {})
        old_hash = existing.get("index_hash", "")

        if old_hash != current_hash:
            indexes_changed = True

        # Update (not delete!)
        manifest["merge_tracking"]["indexes"][hash_id] = {
            "source_path": str(source_path),
            "index_hash": current_hash,
            "last_checked": datetime.now().isoformat()
        }

    # Compute concatenated hash
    new_concat = "".join(sorted(hash_ids))
    new_concat_md5 = compute_concatenated_hash(hash_ids)
    old_concat_md5 = manifest["merge_tracking"].get("concat_md5", "")
    concat_changed = (new_concat_md5 != old_concat_md5)

    # Update
    manifest["merge_tracking"]["all_hashes_concatenated"] = new_concat
    manifest["merge_tracking"]["concat_md5"] = new_concat_md5
    manifest["updated_at"] = datetime.now().isoformat()

    return manifest, indexes_changed, concat_changed


def save_manifest(manifest_path: Path, manifest: dict, dry_run: bool = False):
    """Save manifest with backup"""
    if dry_run:
        return

    # Backup existing
    if manifest_path.exists():
        backup_path = manifest_path.with_suffix(MANIFEST_BACKUP_SUFFIX)
        shutil.copy2(manifest_path, backup_path)

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)


def _create_manifest() -> dict:
    """Create new manifest v1"""
    now = datetime.now().isoformat()
    return {
        "version": MANIFEST_VERSION,
        "created_at": now,
        "updated_at": now,
        "merge_tracking": _empty_tracking()
    }


def _empty_tracking() -> dict:
    """Empty merge tracking structure"""
    return {
        "indexes": {},
        "all_hashes_concatenated": "",
        "concat_md5": "",
        "last_merged_at": None
    }


def _migrate_to_v1(old_data: dict) -> dict:
    """Migrate old schema to v1"""
    return {
        "version": MANIFEST_VERSION,
        "created_at": old_data.get("created_at", datetime.now().isoformat()),
        "updated_at": datetime.now().isoformat(),
        "merge_tracking": {
            "indexes": old_data.get("indexes", {}),
            "all_hashes_concatenated": "",
            "concat_md5": "",
            "last_merged_at": None
        }
    }
