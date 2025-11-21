#!/usr/bin/env python3
"""Checksum operations example for google-drive-crud-plus."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import GDriveConfig
from src.checksum import GDriveChecksum
from src.utils import setup_logging


def main() -> None:
    """Run checksum examples."""
    logger = setup_logging()

    # Configure (replace with your email)
    email = "limpaul.fin@gmail.com"
    config = GDriveConfig(email=email)

    checksum = GDriveChecksum(config)

    # Example folder with PDFs (replace with your folder)
    pdf_folder = "0ABc5fJDyNr1wUk9PVA/1n0RWhHyNgACVQtcqIilIe1roFjQTvkeB"

    logger.info(f"=== Calculating checksums for PDFs in: {pdf_folder} ===\n")

    # Get the full path
    full_path = config.get_full_path(pdf_folder)

    if not full_path.exists():
        logger.error(f"Folder not found: {full_path}")
        logger.info("\nMake sure you:")
        logger.info("1. Have Google Drive mounted in Nautilus")
        logger.info("2. Have access to the folder")
        logger.info("3. Correct folder path (can get from Nautilus)")
        return

    # List PDF files
    pdf_files = list(full_path.glob("*.pdf")) + list(full_path.glob("*.PDF"))

    logger.info(f"Found {len(pdf_files)} PDF files\n")

    # Calculate checksums for each PDF
    for pdf_file in pdf_files[:5]:  # Show first 5 files
        relative_path = str(pdf_file.relative_to(config.mount_path))

        logger.info(f"File: {pdf_file.name}")

        # MD5
        md5_hash = checksum.md5(relative_path)
        if md5_hash:
            logger.info(f"  MD5:    {md5_hash}")

        # SHA256
        sha256_hash = checksum.sha256(relative_path)
        if sha256_hash:
            logger.info(f"  SHA256: {sha256_hash}")

        logger.info("")

    logger.info("\nExample completed!")


if __name__ == "__main__":
    main()
