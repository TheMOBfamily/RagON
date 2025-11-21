#!/usr/bin/env python3
"""
Rename PDF files to year-first format:
{year}-{title}-{author-optional}-{publisher-optional}.PDF
"""

import os
import re
from pathlib import Path

def clean_component(text):
    """Remove ALL special chars, keep only alphanumeric, dash, underscore"""
    # Replace & with 'and' before cleaning
    text = text.replace('&', 'and')
    # Replace apostrophe variants with empty string
    text = text.replace("'", '').replace("'", '')  # ASCII and curly quote
    # Replace all spaces with dash
    text = re.sub(r'\s+', '-', text)
    # Remove ALL special characters - keep only: A-Z, a-z, 0-9, -, _
    text = re.sub(r'[^A-Za-z0-9\-_]', '', text)
    # Remove multiple consecutive dashes
    text = re.sub(r'-+', '-', text)
    # Strip leading/trailing dashes
    text = text.strip('-')
    return text

def parse_annas_archive_filename(filename):
    """
    Parse Anna's Archive format:
    Title -- Author -- Edition, Location, Year -- Publisher -- ISBN -- Hash -- Anna's Archive.pdf

    Returns: (year, title, author, publisher)
    """
    parts = filename.split(' -- ')

    if len(parts) < 3:
        return None, None, None, None

    # Extract title
    title = clean_component(parts[0])

    # Extract author
    author = clean_component(parts[1]) if len(parts) > 1 else ""
    # Multiple authors separated by comma or semicolon
    if ',' in author or ';' in author:
        authors = [a.strip() for a in re.split(r'[,;]', author)]
        author = '_'.join([clean_component(a) for a in authors[:3]])  # Max 3 authors

    # Extract year from edition field (parts[2])
    year = "Unknown"
    if len(parts) > 2:
        year_match = re.search(r'\b(19|20)\d{2}\b', parts[2])
        if year_match:
            year = year_match.group(0)

    # Extract publisher
    publisher = ""
    if len(parts) > 3:
        pub = parts[3].split(',')[0]  # Get first part before comma
        publisher = clean_component(pub)

    return year, title, author, publisher

def rename_pdf(old_path, dry_run=True):
    """Rename PDF file to year-first format"""
    old_name = old_path.name

    # Skip if already renamed
    if re.match(r'^\d{4}-', old_name) or re.match(r'^Unknown-', old_name):
        print(f"⏭️  Skip (already renamed): {old_name}")
        return False

    # Parse filename
    year, title, author, publisher = parse_annas_archive_filename(old_name)

    if not title:
        print(f"❌ Cannot parse: {old_name}")
        return False

    # Build new filename
    components = [year, title]
    if author:
        components.append(author)
    if publisher:
        components.append(publisher)

    new_name = '-'.join(components) + '.PDF'
    new_path = old_path.parent / new_name

    # Check if target exists
    if new_path.exists():
        print(f"⚠️  Target exists: {new_name}")
        return False

    if dry_run:
        print(f"🔍 Would rename:")
        print(f"   Old: {old_name}")
        print(f"   New: {new_name}")
    else:
        old_path.rename(new_path)
        print(f"✅ Renamed:")
        print(f"   Old: {old_name}")
        print(f"   New: {new_name}")

    return True

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python rename-pdfs-year-first.py <folder> [--execute]")
        sys.exit(1)

    folder = Path(sys.argv[1])
    dry_run = '--execute' not in sys.argv

    if not folder.is_dir():
        print(f"Error: {folder} is not a directory")
        sys.exit(1)

    # Scan both .pdf and .PDF extensions (Linux is case-sensitive)
    pdf_files = sorted(list(folder.glob('*.pdf')) + list(folder.glob('*.PDF')))

    if not pdf_files:
        print(f"No PDF files found in {folder}")
        sys.exit(0)

    print(f"Found {len(pdf_files)} PDF files")
    print(f"Mode: {'DRY RUN (preview only)' if dry_run else 'EXECUTE (will rename)'}")
    print("-" * 80)

    renamed = 0
    for pdf_file in pdf_files:
        if rename_pdf(pdf_file, dry_run):
            renamed += 1

    print("-" * 80)
    print(f"Summary: {renamed}/{len(pdf_files)} files {'would be' if dry_run else 'were'} renamed")

    if dry_run and renamed > 0:
        print("\n⚠️  This was a DRY RUN. Run with --execute to actually rename files.")

if __name__ == '__main__':
    main()
