#!/usr/bin/env python
"""
Merge DKM-PDFs FAISS indexes - CLI entry point
Hash ID: 4f63f059 (merge-RAG-faiss-pkl)

Usage:
  python main-4f63f059.py --test      # Test với 5 PDFs
  python main-4f63f059.py --merge     # Merge tất cả
  python main-4f63f059.py --dry-run   # Preview only

Author: AI Assistant
Date: 2025-10-26
LOC: ~50 (< 100)
"""
from __future__ import annotations
import argparse
from pathlib import Path
from src.config import DKM_PDFS_DIR, MERGED_INDEX_DIR, DEFAULT_TEST_LIMIT
from src.merger import merge_indexes
from src.utils import print_header, print_info


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Merge DKM-PDFs FAISS indexes with CRUD detection",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--dry-run", action="store_true", help="Preview only (safe)")
    parser.add_argument("--test", action="store_true", help="Test with 5 PDFs")
    parser.add_argument("--merge", action="store_true", help="Merge all (skip if no CRUD)")
    parser.add_argument("--base-dir", type=Path, default=DKM_PDFS_DIR, help="Base directory")
    parser.add_argument("--output", type=Path, default=MERGED_INDEX_DIR, help="Output directory")
    parser.add_argument("--no-atomic", action="store_true", help="Disable atomic write (unsafe)")
    parser.add_argument("--batch-size", type=int, default=None, help="Enable batch mode (e.g. 100)")

    args = parser.parse_args()

    print_header("DKM-PDFs FAISS Merge Tool")
    print_info(f"Base dir: {args.base_dir}")
    print_info(f"Output dir: {args.output}")
    print_info(f"Atomic mode: {not args.no_atomic}")
    if args.batch_size:
        print_info(f"Batch mode: enabled (batch_size={args.batch_size})")

    # Merge options
    merge_opts = {
        "atomic": not args.no_atomic,
        "batch_size": args.batch_size
    }

    # Execute
    if args.test:
        merge_indexes(args.base_dir, args.output, limit=DEFAULT_TEST_LIMIT, dry_run=False, **merge_opts)
    elif args.merge:
        merge_indexes(args.base_dir, args.output, limit=None, dry_run=False, **merge_opts)
    else:
        # Default: dry run
        merge_indexes(args.base_dir, args.output, limit=DEFAULT_TEST_LIMIT, dry_run=True, **merge_opts)


if __name__ == "__main__":
    main()
