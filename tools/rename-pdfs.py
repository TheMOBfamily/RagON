#!/usr/bin/env python3
"""Rename PDF files từ Anna's Archive format sang naming convention chuẩn"""

import os
import re
import sys
from pathlib import Path


def clean_title(title: str) -> str:
    """Clean và format title theo naming convention"""
    # Remove special chars
    title = re.sub(r'[/:*?"<>|]', '', title)
    # Replace underscores and multiple spaces with single space
    title = re.sub(r'[_]+', ' ', title)
    title = re.sub(r'\s+', ' ', title).strip()
    # Replace spaces with dash
    title = title.replace(' ', '-')
    # Remove multiple dashes
    title = re.sub(r'-+', '-', title)
    return title


def clean_author(author: str) -> str:
    """Clean và format author theo naming convention"""
    # Remove trailing commas
    author = author.rstrip(', ')
    # Replace &, and, und with _
    author = re.sub(r'\s*(&|and|und)\s*', '_', author)
    # Replace ; with _
    author = author.replace(';', '_')
    # Replace , with _ for multiple authors
    author = re.sub(r',\s*', '_', author)
    # Replace spaces with dash
    author = author.replace(' ', '-')
    # Remove multiple dashes/underscores
    author = re.sub(r'-+', '-', author)
    author = re.sub(r'_+', '_', author)
    return author.strip('_-')


def clean_publisher(publisher: str) -> str:
    """Clean và format publisher theo naming convention"""
    # Remove extra info after comma
    if ',' in publisher:
        publisher = publisher.split(',')[0]
    # Remove special chars
    publisher = re.sub(r'[/:*?"<>|]', '', publisher)
    # Replace spaces with dash
    publisher = publisher.replace(' ', '-')
    # Remove multiple dashes
    publisher = re.sub(r'-+', '-', publisher)
    return publisher.strip('-')


def extract_year(edition_year: str) -> str:
    """Extract year from edition/year field"""
    # Try to find 4-digit year
    match = re.search(r'\b(19|20)\d{2}\b', edition_year)
    if match:
        return match.group(0)

    # If not found, try to extract from date format
    match = re.search(r'\b(19|20)\d{2}-\d{2}-\d{2}\b', edition_year)
    if match:
        return match.group(0)[:4]

    return 'Unknown'


def parse_anna_archive_filename(filename: str) -> dict:
    """Parse Anna's Archive filename format

    Format: Title -- Author -- Edition/Year -- Publisher -- ISBN -- Hash -- Anna's Archive.pdf
    """
    # Remove .pdf extension
    name = filename.replace('.pdf', '')

    # Split by --
    parts = [p.strip() for p in name.split(' -- ')]

    result = {
        'title': 'Unknown',
        'author': 'Unknown',
        'publisher': 'Unknown',
        'year': 'Unknown'
    }

    if len(parts) >= 4:
        result['title'] = parts[0]
        result['author'] = parts[1]
        result['year'] = extract_year(parts[2])
        result['publisher'] = parts[3]
    elif len(parts) >= 3:
        result['title'] = parts[0]
        result['author'] = parts[1]
        result['publisher'] = parts[2]

    return result


def generate_new_filename(metadata: dict) -> str:
    """Generate new filename theo naming convention

    Format: Title - Author - Publisher - Year.pdf
    """
    title = clean_title(metadata['title'])
    author = clean_author(metadata['author'])
    publisher = clean_publisher(metadata['publisher'])
    year = metadata['year']

    return f"{title} - {author} - {publisher} - {year}.pdf"


def rename_pdfs_in_folder(folder_path: str, dry_run: bool = True):
    """Rename all PDF files in folder"""
    folder = Path(folder_path)

    if not folder.exists():
        print(f"Error: Folder không tồn tại: {folder_path}")
        return

    pdf_files = list(folder.glob('*.pdf'))

    if not pdf_files:
        print(f"Không tìm thấy PDF files trong: {folder_path}")
        return

    print(f"\nFound {len(pdf_files)} PDF files trong {folder_path}\n")

    for pdf_file in pdf_files:
        old_name = pdf_file.name

        # Skip if already renamed (không có Anna's Archive pattern)
        if ' -- ' not in old_name and '-' in old_name:
            print(f"⊘ Skip (already renamed): {old_name}")
            continue

        # Parse metadata
        metadata = parse_anna_archive_filename(old_name)
        new_name = generate_new_filename(metadata)

        # Check if new name is different
        if old_name == new_name:
            print(f"⊘ Skip (same name): {old_name}")
            continue

        print(f"→ {old_name}")
        print(f"  {new_name}\n")

        if not dry_run:
            new_path = pdf_file.parent / new_name
            # Check if target exists
            if new_path.exists():
                print(f"  ⚠ Warning: Target file already exists, skipping\n")
                continue
            pdf_file.rename(new_path)
            print(f"  ✓ Renamed\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python rename-pdfs.py <folder_path> [--execute]")
        print("\n  --execute: Actually rename files (default is dry-run)")
        sys.exit(1)

    folder_path = sys.argv[1]
    dry_run = '--execute' not in sys.argv

    if dry_run:
        print("=== DRY RUN MODE (preview only) ===")
        print("Use --execute to actually rename files\n")
    else:
        print("=== EXECUTE MODE (will rename files) ===\n")

    rename_pdfs_in_folder(folder_path, dry_run=dry_run)


if __name__ == '__main__':
    main()
