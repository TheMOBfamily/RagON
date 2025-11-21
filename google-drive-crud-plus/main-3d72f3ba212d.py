#!/usr/bin/env python3
"""Main entry point for google-drive-crud-plus CLI tool.

This script provides a unified CLI interface for Google Drive operations
via gvfs, including CRUD, checksum, and search functionality.

Usage:
    ./main-3d72f3ba212d.py <command> [options]

Commands:
    list <path>              - List files in directory
    upload <local> <remote>  - Upload file to Drive
    download <remote> <local> - Download file from Drive
    delete <path>            - Delete file/folder
    checksum <path>          - Calculate MD5/SHA256 hash
    search <pattern>         - Search files by name
    pdfs [path]              - List all PDF files

Environment:
    GDRIVE_EMAIL             - Google Drive email (required)
    GDRIVE_LOG_LEVEL         - Logging level (default: INFO)
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from src.config import GDriveConfig
from src.connection import GDriveConnection
from src.crud import GDriveCRUD
from src.checksum import GDriveChecksum
from src.search import GDriveSearch
from src.utils import setup_logging, format_size, get_file_info


# Global logger
logger = None


def setup_file_logging(log_file: Path) -> logging.Logger:
    """Setup logging to both console and file.

    Args:
        log_file: Path to log file.

    Returns:
        Configured logger.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    level_str = os.getenv("GDRIVE_LOG_LEVEL", "INFO")
    level = getattr(logging, level_str.upper(), logging.INFO)

    global logger
    logger = setup_logging(level=level, log_file=str(log_file))

    return logger


def get_config() -> GDriveConfig | None:
    """Get Google Drive config from environment.

    Returns:
        Config instance or None if email not set.
    """
    try:
        config = GDriveConfig.from_env()
        logger.info(f"✅ Configured for: {config.email}")
        return config
    except ValueError:
        logger.error("GDRIVE_EMAIL not set")
        logger.info("Set it with: export GDRIVE_EMAIL='your@gmail.com'")
        logger.info("Or create .env file with: GDRIVE_EMAIL=your@gmail.com")
        return None
    except FileNotFoundError as e:
        logger.error(f"❌ {e}")
        logger.info("\nMount Google Drive first:")
        logger.info("1. Open Nautilus file manager")
        logger.info("2. Click 'Other Locations'")
        logger.info("3. Connect to Google Drive")
        return None


def cmd_list(args: argparse.Namespace) -> int:
    """List files command."""
    config = get_config()
    if not config:
        return 1

    crud = GDriveCRUD(config)
    files = crud.list_files(args.path or "")

    logger.info(f"\n📁 Listing: {args.path or '(root)'}")
    logger.info(f"Found {len(files)} items:\n")

    for item in files:
        info = get_file_info(item)
        icon = "📁" if info.get("is_dir") else "📄"
        logger.info(f"  {icon} {info['name']} - {info['size_formatted']}")

    return 0


def cmd_upload(args: argparse.Namespace) -> int:
    """Upload file command."""
    config = get_config()
    if not config:
        return 1

    crud = GDriveCRUD(config)

    logger.info(f"📤 Uploading: {args.local} → {args.remote}")

    if crud.upload_file(args.local, args.remote):
        logger.info("✅ Upload successful")
        return 0
    else:
        logger.error("❌ Upload failed")
        return 1


def cmd_download(args: argparse.Namespace) -> int:
    """Download file command."""
    config = get_config()
    if not config:
        return 1

    crud = GDriveCRUD(config)

    logger.info(f"📥 Downloading: {args.remote} → {args.local}")

    if crud.download_file(args.remote, args.local):
        logger.info("✅ Download successful")
        return 0
    else:
        logger.error("❌ Download failed")
        return 1


def cmd_delete(args: argparse.Namespace) -> int:
    """Delete file command."""
    config = get_config()
    if not config:
        return 1

    crud = GDriveCRUD(config)

    if not args.force:
        response = input(f"⚠️  Delete '{args.path}'? (yes/no): ")
        if response.lower() not in ["yes", "y"]:
            logger.info("❌ Cancelled")
            return 0

    logger.info(f"🗑️  Deleting: {args.path}")

    if crud.delete_file(args.path):
        logger.info("✅ Delete successful")
        return 0
    else:
        logger.error("❌ Delete failed")
        return 1


def cmd_checksum(args: argparse.Namespace) -> int:
    """Checksum calculation command."""
    config = get_config()
    if not config:
        return 1

    checksum = GDriveChecksum(config)

    logger.info(f"🔐 Calculating checksums for: {args.path}\n")

    md5_hash = checksum.md5(args.path)
    sha256_hash = checksum.sha256(args.path)

    if md5_hash:
        logger.info(f"MD5:    {md5_hash}")
    if sha256_hash:
        logger.info(f"SHA256: {sha256_hash}")

    if not md5_hash and not sha256_hash:
        logger.error("❌ Failed to calculate checksums")
        return 1

    return 0


def cmd_search(args: argparse.Namespace) -> int:
    """Search files command."""
    config = get_config()
    if not config:
        return 1

    search = GDriveSearch(config)

    logger.info(f"🔍 Searching for: {args.pattern}\n")

    results = search.by_name(args.pattern, case_sensitive=args.case_sensitive)

    logger.info(f"Found {len(results)} matches:\n")

    for result in results[:args.limit]:
        info = get_file_info(result)
        icon = "📁" if info.get("is_dir") else "📄"
        logger.info(f"  {icon} {result.name} - {info['size_formatted']}")

    if len(results) > args.limit:
        logger.info(f"\n... and {len(results) - args.limit} more")

    return 0


def cmd_pdfs(args: argparse.Namespace) -> int:
    """List PDF files command."""
    config = get_config()
    if not config:
        return 1

    search = GDriveSearch(config)

    logger.info(f"📚 Searching for PDF files in: {args.path or '(root)'}\n")

    pdfs = search.pdfs_only(args.path or "")

    logger.info(f"Found {len(pdfs)} PDF files:\n")

    for pdf in pdfs[:args.limit]:
        if pdf.exists():
            size = pdf.stat().st_size
            logger.info(f"  📄 {pdf.name} ({format_size(size)})")

    if len(pdfs) > args.limit:
        logger.info(f"\n... and {len(pdfs) - args.limit} more")

    return 0


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Google Drive CRUD Plus - CLI tool for Google Drive operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List files in directory")
    list_parser.add_argument("path", nargs="?", default="", help="Path to list (default: root)")

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload file to Drive")
    upload_parser.add_argument("local", help="Local file path")
    upload_parser.add_argument("remote", help="Remote Drive path")

    # Download command
    download_parser = subparsers.add_parser("download", help="Download file from Drive")
    download_parser.add_argument("remote", help="Remote Drive path")
    download_parser.add_argument("local", help="Local file path")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete file/folder")
    delete_parser.add_argument("path", help="Path to delete")
    delete_parser.add_argument("-f", "--force", action="store_true", help="Skip confirmation")

    # Checksum command
    checksum_parser = subparsers.add_parser("checksum", help="Calculate file checksum")
    checksum_parser.add_argument("path", help="File path")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search files by pattern")
    search_parser.add_argument("pattern", help="Search pattern")
    search_parser.add_argument("-c", "--case-sensitive", action="store_true", help="Case sensitive")
    search_parser.add_argument("-l", "--limit", type=int, default=20, help="Max results (default: 20)")

    # PDFs command
    pdfs_parser = subparsers.add_parser("pdfs", help="List all PDF files")
    pdfs_parser.add_argument("path", nargs="?", default="", help="Path to search (default: root)")
    pdfs_parser.add_argument("-l", "--limit", type=int, default=50, help="Max results (default: 50)")

    args = parser.parse_args()

    # Setup logging
    log_file = SCRIPT_DIR / "log" / "debug.log"
    setup_file_logging(log_file)

    logger.info("=" * 60)
    logger.info(f"Google Drive CRUD Plus - {datetime.now().isoformat()}")
    logger.info("=" * 60)

    # Dispatch to command handler
    commands = {
        "list": cmd_list,
        "upload": cmd_upload,
        "download": cmd_download,
        "delete": cmd_delete,
        "checksum": cmd_checksum,
        "search": cmd_search,
        "pdfs": cmd_pdfs,
    }

    handler = commands.get(args.command)
    if not handler:
        logger.error(f"Unknown command: {args.command}")
        return 1

    try:
        return handler(args)
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        logger.exception(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
