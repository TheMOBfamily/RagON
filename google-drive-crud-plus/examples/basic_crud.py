#!/usr/bin/env python3
"""Basic CRUD operations example for google-drive-crud-plus."""

from __future__ import annotations

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import GDriveConfig
from src.connection import GDriveConnection
from src.crud import GDriveCRUD
from src.utils import setup_logging, get_file_info


def main() -> None:
    """Run basic CRUD examples."""
    # Setup logging
    logger = setup_logging()

    # Configure (replace with your email)
    email = "limpaul.fin@gmail.com"
    config = GDriveConfig(email=email)

    logger.info(f"Configured for: {email}")
    logger.info(f"Mount path: {config.mount_path}")

    # Check connection
    connection = GDriveConnection(config)

    if not connection.is_mounted():
        logger.warning("Google Drive not mounted. Attempting to mount...")
        if connection.mount():
            logger.info("Successfully mounted Google Drive")
        else:
            logger.error("Failed to mount Google Drive")
            return

    # Initialize CRUD operations
    crud = GDriveCRUD(config)

    # Example 1: List files in root
    logger.info("\n=== Listing files in Drive root ===")
    files = crud.list_files()
    for file_path in files[:10]:  # Show first 10
        info = get_file_info(file_path)
        logger.info(f"  {info['name']} - {info['size_formatted']}")

    # Example 2: Create a test folder
    logger.info("\n=== Creating test folder ===")
    test_folder = "test-crud-plus"
    if crud.create_folder(test_folder):
        logger.info(f"Created folder: {test_folder}")
    else:
        logger.warning(f"Folder may already exist: {test_folder}")

    # Example 3: Upload a test file
    logger.info("\n=== Uploading test file ===")
    test_content = b"Hello from google-drive-crud-plus!"
    local_test_file = Path("/tmp/test-upload.txt")
    local_test_file.write_bytes(test_content)

    if crud.upload_file(local_test_file, f"{test_folder}/test-upload.txt"):
        logger.info("File uploaded successfully")
    else:
        logger.error("File upload failed")

    # Example 4: Read file back
    logger.info("\n=== Reading file back ===")
    content = crud.read_file(f"{test_folder}/test-upload.txt")
    if content:
        logger.info(f"File content: {content.decode()}")
    else:
        logger.error("Failed to read file")

    # Example 5: Check if file exists
    logger.info("\n=== Checking file existence ===")
    exists = crud.file_exists(f"{test_folder}/test-upload.txt")
    logger.info(f"File exists: {exists}")

    # Cleanup
    local_test_file.unlink()
    logger.info("\nExample completed!")


if __name__ == "__main__":
    main()
