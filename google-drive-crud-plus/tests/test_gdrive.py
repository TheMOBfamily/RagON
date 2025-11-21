#!/usr/bin/env python3
"""Test script for google-drive-crud-plus with actual Google Drive folder."""

from __future__ import annotations

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import GDriveConfig
from src.connection import GDriveConnection
from src.crud import GDriveCRUD
from src.checksum import GDriveChecksum
from src.search import GDriveSearch
from src.utils import setup_logging, format_size


def test_connection(email: str) -> GDriveConfig | None:
    """Test Google Drive connection.

    Args:
        email: Google Drive email.

    Returns:
        Config if successful, None otherwise.
    """
    logger = setup_logging()

    try:
        config = GDriveConfig(email=email)
        logger.info(f"✅ Config created for: {email}")
        logger.info(f"   Mount path: {config.mount_path}")

        connection = GDriveConnection(config)

        if connection.is_mounted():
            logger.info("✅ Google Drive is mounted")
            return config
        else:
            logger.warning("⚠️  Google Drive not mounted")
            logger.info("\nTo mount Google Drive:")
            logger.info("1. Open Nautilus file manager")
            logger.info("2. Click 'Other Locations'")
            logger.info("3. Connect to Google Drive")
            logger.info("4. Log in with your Google account")
            return None

    except FileNotFoundError as e:
        logger.error(f"❌ Error: {e}")
        logger.info("\nMake sure:")
        logger.info("- You're using GNOME/Ubuntu with gvfs")
        logger.info("- Google Drive is mounted in Nautilus")
        return None


def test_crud(config: GDriveConfig) -> None:
    """Test CRUD operations."""
    logger = setup_logging()
    crud = GDriveCRUD(config)

    logger.info("\n=== Testing CRUD Operations ===")

    # List root files
    logger.info("\n📁 Listing root files:")
    files = crud.list_files()
    logger.info(f"   Found {len(files)} items in root")

    for item in files[:5]:
        icon = "📁" if item.is_dir() else "📄"
        logger.info(f"   {icon} {item.name}")


def test_search_pdfs(config: GDriveConfig, folder: str) -> None:
    """Test PDF search in specific folder."""
    logger = setup_logging()
    search = GDriveSearch(config)

    logger.info(f"\n=== Searching PDFs in: {folder} ===")

    # Get full path to check if exists
    full_path = config.get_full_path(folder)

    if not full_path.exists():
        logger.error(f"❌ Folder not found: {folder}")
        logger.info("\nTip: Get correct path from Nautilus:")
        logger.info("1. Navigate to folder in Nautilus")
        logger.info("2. Right-click → Properties")
        logger.info("3. Copy the location path")
        return

    # Search for PDFs
    logger.info("🔍 Searching for PDF files...")
    pdf_files = search.by_extension(".pdf", folder)
    pdf_files_upper = search.by_extension(".PDF", folder)
    all_pdfs = pdf_files + pdf_files_upper

    logger.info(f"   Found {len(all_pdfs)} PDF files")

    # Show first 10 PDFs
    for pdf in all_pdfs[:10]:
        if pdf.exists():
            size = pdf.stat().st_size
            logger.info(f"   📄 {pdf.name} ({format_size(size)})")


def test_checksums(config: GDriveConfig, folder: str) -> None:
    """Test checksum calculations."""
    logger = setup_logging()
    search = GDriveSearch(config)
    checksum = GDriveChecksum(config)

    logger.info(f"\n=== Calculating Checksums for PDFs ===")

    # Find PDFs
    full_path = config.get_full_path(folder)
    if not full_path.exists():
        logger.error(f"❌ Folder not found: {folder}")
        return

    pdf_files = search.by_extension(".pdf", folder)
    if not pdf_files:
        logger.warning("⚠️  No PDF files found")
        return

    # Calculate checksums for first 3 PDFs
    logger.info(f"\nCalculating checksums for first 3 PDFs...\n")

    for pdf in pdf_files[:3]:
        relative_path = str(pdf.relative_to(config.mount_path))

        logger.info(f"📄 {pdf.name}")

        md5 = checksum.md5(relative_path)
        if md5:
            logger.info(f"   MD5:    {md5}")

        sha256 = checksum.sha256(relative_path)
        if sha256:
            logger.info(f"   SHA256: {sha256}")

        logger.info("")


def main() -> None:
    """Run all tests."""
    logger = setup_logging()

    logger.info("=" * 60)
    logger.info("  Google Drive CRUD Plus - Test Suite")
    logger.info("=" * 60)

    # Configure with your email
    email = "limpaul.fin@gmail.com"

    # Test connection
    config = test_connection(email)

    if not config:
        logger.error("\n❌ Cannot proceed without valid Google Drive connection")
        return

    # Test basic CRUD
    test_crud(config)

    # Test with specific PDF folder (from google-drive:// URI)
    # Format: folder ID from URI
    pdf_folder = "0ABc5fJDyNr1wUk9PVA/1n0RWhHyNgACVQtcqIilIe1roFjQTvkeB"

    # Test search
    test_search_pdfs(config, pdf_folder)

    # Test checksums
    test_checksums(config, pdf_folder)

    logger.info("\n" + "=" * 60)
    logger.info("  ✅ Test suite completed!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
