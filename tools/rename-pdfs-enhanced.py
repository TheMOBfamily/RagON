#!/usr/bin/env python3
"""
Enhanced PDF renamer supporting multiple filename formats.
Converts to year-first format: {year}-{title}-{author-optional}-{publisher-optional}.PDF
"""

import os
import re
from pathlib import Path

def clean_component(text):
    """Remove ALL special chars, keep only alphanumeric, dash, underscore"""
    text = text.replace('&', 'and')
    text = text.replace("'", '').replace("'", '').replace("'", '')
    text = text.replace('✅', '').strip()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^A-Za-z0-9\-_]', '', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text

def extract_year(text):
    """Extract 4-digit year from text within reasonable bounds"""
    matches = re.findall(r'((?:19|20)\d{2})', text)
    for candidate in matches:
        year_int = int(candidate)
        if 1900 <= year_int <= 2025:
            return candidate
    return None

def parse_filename(filename):
    """
    Parse various filename formats and extract: year, title, author, publisher

    Supports:
    1. Anna's Archive: Title -- Author -- Edition, Year -- Publisher -- ...
    2. Author - Title format: "Author - Title-Publisher (Year).pdf"
    3. Title - Author format: "Title - Author - Publisher - Year.pdf"
    4. Year at end: "Title-Author-Year.pdf"
    5. Simple format: "Title.pdf" (no year)
    """
    name_without_ext = filename.replace('.pdf', '').replace('.PDF', '')

    # Pattern 1: Anna's Archive format (Title -- Author -- Edition, Year -- Publisher)
    if ' -- ' in name_without_ext:
        parts = name_without_ext.split(' -- ')
        title = clean_component(parts[0])
        author = clean_component(parts[1]) if len(parts) > 1 else ""
        year = extract_year(parts[2]) if len(parts) > 2 else "Unknown"
        publisher = clean_component(parts[3].split(',')[0]) if len(parts) > 3 else ""

        # Handle multiple authors
        if ',' in author or ';' in author:
            authors = [a.strip() for a in re.split(r'[,;]', author)]
            author = '_'.join([clean_component(a) for a in authors[:3]])

        return year, title, author, publisher

    # Pattern 2: "Author - Title-Publisher (Year).pdf" or similar
    if name_without_ext.count(' - ') >= 1:
        parts = name_without_ext.split(' - ')

        # Try to identify year in last part
        year = extract_year(parts[-1]) or "Unknown"

        # Try to identify publisher (usually has "Press", "Publishing", etc.)
        publisher = ""
        for i in range(len(parts)-1, -1, -1):
            if any(pub_word in parts[i] for pub_word in ['Press', 'Publishing', 'OReilly', 'Packt', 'Manning', 'Wiley', 'Springer']):
                publisher = clean_component(parts[i].split('(')[0].split('-')[0])
                break

        # First part is usually author or title
        if len(parts) >= 2:
            # Heuristic: if first part is short (<30 chars), likely author
            if len(parts[0]) < 30 and len(parts) >= 3:
                author = clean_component(parts[0])
                title = clean_component(parts[1])
            else:
                title = clean_component(parts[0])
                author = clean_component(parts[1]) if len(parts) > 1 else ""
        else:
            title = clean_component(parts[0])
            author = ""

        return year, title, author, publisher

    # Pattern 3: Year at beginning (already renamed format)
    year_match = re.match(r'^(\d{4}|Unknown)-', name_without_ext)
    if year_match:
        return None, None, None, None  # Skip already renamed

    # Pattern 4: Simple filename - extract year if present, use filename as title
    year = extract_year(name_without_ext) or "Unknown"
    title = clean_component(name_without_ext)

    return year, title, "", ""

def rename_pdf(old_path, dry_run=True):
    """Rename PDF file to year-first format"""
    old_name = old_path.name

    # Skip non-PDF files
    if not old_name.lower().endswith('.pdf'):
        print(f"⏭️  Skip (not PDF): {old_name}")
        return False

    # Skip already-correct year-first names, but allow Unknown-* to be reprocessed
    if re.match(r'^\d{4}-', old_name):
        print(f"⏭️  Skip (already renamed): {old_name}")
        return False

    name_for_parsing = old_name
    unknown_prefixed = False
    if re.match(r'^Unknown-', old_name):
        unknown_prefixed = True
        name_for_parsing = old_name[len('Unknown-'):]

    # Parse filename
    year, title, author, publisher = parse_filename(name_for_parsing)

    if year is None or not title:
        print(f"⏭️  Skip (already in correct format): {old_name}")
        return False

    # If we started with Unknown-* and still couldn't find a year, keep as-is
    if unknown_prefixed and year == "Unknown":
        print(f"⏭️  Skip (still no year found): {old_name}")
        return False

    # Build new filename
    components = [year, title]
    if author:
        components.append(author)
    if publisher:
        components.append(publisher)

    new_name = '-'.join(components) + '.PDF'

    # Truncate if too long (max 255 chars)
    if len(new_name) > 255:
        new_name = new_name[:251] + '.PDF'

    new_path = old_path.parent / new_name

    # Check if target exists
    if new_path.exists() and new_path != old_path:
        print(f"⚠️  Target exists: {new_name}")
        return False

    if dry_run:
        print(f"🔍 Would rename:")
        print(f"   Old: {old_name}")
        print(f"   New: {new_name}")
        print()
    else:
        try:
            old_path.rename(new_path)
            print(f"✅ Renamed:")
            print(f"   Old: {old_name}")
            print(f"   New: {new_name}")
            print()
        except Exception as e:
            print(f"❌ Error renaming {old_name}: {e}")
            return False

    return True

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python rename-pdfs-enhanced.py <folder> [--execute]")
        sys.exit(1)

    folder = Path(sys.argv[1])
    dry_run = '--execute' not in sys.argv

    if not folder.is_dir():
        print(f"Error: {folder} is not a directory")
        sys.exit(1)

    # Find all PDF files (case-insensitive)
    pdf_files = sorted(folder.glob('*.pdf')) + sorted(folder.glob('*.PDF'))
    pdf_files = list(set(pdf_files))  # Remove duplicates

    if not pdf_files:
        print(f"No PDF files found in {folder}")
        sys.exit(0)

    print(f"Found {len(pdf_files)} PDF files")
    print(f"Mode: {'DRY RUN (preview only)' if dry_run else 'EXECUTE (will rename)'}")
    print("-" * 80)
    print()

    renamed = 0
    skipped = 0
    errors = 0

    for pdf_file in pdf_files:
        result = rename_pdf(pdf_file, dry_run)
        if result:
            renamed += 1
        elif result is False:
            skipped += 1

    print("-" * 80)
    print(f"Summary:")
    print(f"  Total files: {len(pdf_files)}")
    print(f"  {'Would be' if dry_run else 'Were'} renamed: {renamed}")
    print(f"  Skipped: {skipped}")

    if dry_run and renamed > 0:
        print()
        print("⚠️  This was a DRY RUN. Run with --execute to actually rename files.")

if __name__ == '__main__':
    main()
