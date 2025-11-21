#!/usr/bin/env python3
"""Search operations example for google-drive-crud-plus."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import GDriveConfig
from src.search import GDriveSearch
from src.utils import setup_logging, format_size


def main() -> None:
    """Run search examples."""
    logger = setup_logging()

    # Configure (replace with your email)
    email = "limpaul.fin@gmail.com"
    config = GDriveConfig(email=email)

    search = GDriveSearch(config)

    # Example 1: Search all PDFs
    logger.info("=== Searching for all PDF files ===\n")
    pdf_files = search.pdfs_only()

    logger.info(f"Found {len(pdf_files)} PDF files")
    for pdf in pdf_files[:10]:  # Show first 10
        size = pdf.stat().st_size if pdf.exists() else 0
        logger.info(f"  {pdf.name} - {format_size(size)}")

    # Example 2: Search by name pattern
    logger.info("\n=== Searching files with 'python' in name ===\n")
    python_files = search.by_name("*python*", case_sensitive=False)

    logger.info(f"Found {len(python_files)} files")
    for file in python_files[:5]:
        logger.info(f"  {file.name}")

    # Example 3: Search by size range (10MB to 100MB)
    logger.info("\n=== Searching files between 10MB and 100MB ===\n")
    size_filtered = search.by_size(
        min_size=10 * 1024 * 1024,  # 10MB
        max_size=100 * 1024 * 1024,  # 100MB
    )

    logger.info(f"Found {len(size_filtered)} files")
    for file in size_filtered[:5]:
        if file.is_file():
            size = file.stat().st_size
            logger.info(f"  {file.name} - {format_size(size)}")

    # Example 4: Search by specific extension
    logger.info("\n=== Searching for .txt files ===\n")
    txt_files = search.by_extension(".txt")

    logger.info(f"Found {len(txt_files)} .txt files")
    for txt_file in txt_files[:5]:
        logger.info(f"  {txt_file.name}")

    logger.info("\nExample completed!")


if __name__ == "__main__":
    main()
