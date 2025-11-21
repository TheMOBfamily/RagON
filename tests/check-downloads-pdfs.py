#!/usr/bin/env python3
"""
Check PDFs in Downloads against DKM-PDFs by filename matching.
"""

import os
import re
import subprocess
from pathlib import Path

DOWNLOADS_DIR = Path("/home/fong/Downloads")
DKM_PDFS_DIR = Path("/home/fong/Projects/mini-rag/DKM-PDFs")

def extract_author_and_title(filename):
    """Extract author name and core title from filename."""
    # Remove year prefix (e.g., "2024-")
    name = re.sub(r'^\d{4}-', '', filename)
    # Remove extension
    name = re.sub(r'\.(pdf|PDF)$', '', name)
    # Remove emojis and special chars
    name = re.sub(r'[✅✓✔️❌]', '', name)

    # Split by delimiters
    parts = re.split(r'[-_]', name)

    # Try to find author (usually has firstname-lastname pattern)
    author_parts = []
    title_parts = []

    for i, part in enumerate(parts):
        # Collect first 2-3 words as potential title
        if i < 3:
            title_parts.append(part)
        # Look for author pattern (capital letters, common names)
        if any(word in part for word in ['Martin', 'Hunt', 'Thomas', 'Fowler', 'Martin', 'Russell', 'Goodfellow']):
            author_parts.append(part)

    return title_parts[:2], author_parts

def search_in_dkm(title_parts, author_parts):
    """Search for title and author in DKM-PDFs metadata using rg."""
    try:
        # Search by title first (first 2 words)
        if title_parts:
            title_query = ' '.join(title_parts[:2])
            cmd = ['rg', '-i', title_query, str(DKM_PDFS_DIR), '--type', 'json']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if len(result.stdout.splitlines()) > 0:
                return True

        # Search by author
        for author in author_parts:
            if len(author) > 3:  # Skip short words
                cmd = ['rg', '-i', author, str(DKM_PDFS_DIR), '--type', 'json']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if len(result.stdout.splitlines()) > 0:
                    return True

        return False
    except Exception as e:
        return False

def main():
    # Get all PDFs in Downloads
    pdfs = sorted(DOWNLOADS_DIR.glob("*.pdf")) + sorted(DOWNLOADS_DIR.glob("*.PDF"))

    not_found = []
    found = []

    print(f"Checking {len(pdfs)} PDFs in Downloads/...\n")

    for pdf in pdfs:
        filename = pdf.name
        title_parts, author_parts = extract_author_and_title(filename)

        if search_in_dkm(title_parts, author_parts):
            found.append(filename)
            print(f"✅ {filename}")
        else:
            not_found.append(filename)
            print(f"❌ {filename}")

    print(f"\n{'='*80}")
    print(f"Summary:")
    print(f"  Found in DKM-PDFs: {len(found)}")
    print(f"  NOT found in DKM-PDFs: {len(not_found)}")
    print(f"{'='*80}\n")

    if not_found:
        print("Files to move to PDFs/:")
        for f in not_found:
            print(f"  - {f}")

    # Save not_found list to file
    output_file = Path("/home/fong/Projects/mini-rag/pdfs-to-move.txt")
    with open(output_file, 'w') as f:
        for filename in not_found:
            f.write(f"{filename}\n")

    print(f"\nList saved to: {output_file}")

if __name__ == "__main__":
    main()
