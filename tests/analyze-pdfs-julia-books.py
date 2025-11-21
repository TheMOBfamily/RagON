#!/usr/bin/env python3
"""
Analyze and rename PDF files in Julia-books-nang-cao folder
following year-first naming convention
"""

import os
import re
from pathlib import Path
import PyPDF2

def read_pdf_first_pages(pdf_path, num_pages=5):
    """Extract text from first N pages of PDF"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = min(num_pages, len(reader.pages))

            text = ""
            for i in range(total_pages):
                page = reader.pages[i]
                text += page.extract_text() + "\n\n"

            return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_year_from_filename(filename):
    """Extract year from Anna's Archive format"""
    # Format: Title -- Author -- Edition, Location, Year -- Publisher
    parts = filename.split(' -- ')
    if len(parts) >= 3:
        # Year is in the 3rd part
        year_match = re.search(r'\b(19|20)\d{2}\b', parts[2])
        if year_match:
            return year_match.group(0)
    return None

def extract_year_from_text(text):
    """Extract publication year from PDF text (first pages)"""
    # Look for copyright year, publication year, etc.
    patterns = [
        (r'Copyright\s*©?\s*(19|20)\d{2}', 'Copyright'),  # Copyright 2023 or Copyright © 2023
        (r'©\s*(19|20)\d{2}', 'Copyright symbol'),  # © 2023
        (r'Published.*?(19|20)\d{2}', 'Published'),  # Published 2023
        (r'May\s+\d+,\s+(19|20)\d{2}', 'Date'),  # May 10, 2013
        (r'\b(19|20)\d{2}\b', 'Generic 4-digit'),  # Any 4-digit year
    ]

    for pattern, label in patterns:
        matches = re.findall(pattern, text[:5000], re.IGNORECASE)  # Search first 5000 chars
        if matches:
            # Return most recent year found
            years = []
            for m in matches:
                if isinstance(m, tuple):
                    year = m[0] + m[1] if len(m) == 2 else ''.join(m)
                else:
                    year = m
                if len(year) == 4 and year.isdigit():
                    years.append(year)

            if years:
                most_recent = max(years)
                print(f"  Found year {most_recent} from pattern: {label}")
                return most_recent

    return None

def main():
    folder = Path("/home/fong/Dropbox/PDFs/Julia-books-nang-cao")

    print("=" * 80)
    print("ANALYZING PDF FILES FOR RENAMING")
    print("=" * 80)
    print()

    # Get all PDF files (not EPUB, exclude already renamed)
    pdf_files = [f for f in folder.glob("*.pdf")
                 if not re.match(r'^\d{4}-', f.name)]

    for idx, pdf_file in enumerate(pdf_files, 1):
        print(f"\n{'='*80}")
        print(f"FILE {idx}: {pdf_file.name}")
        print(f"{'='*80}")

        # Extract year from filename first
        year_from_filename = extract_year_from_filename(pdf_file.name)
        print(f"Year from filename: {year_from_filename or 'Not found'}")

        # Read first pages
        print(f"\nReading first 5 pages...")
        text = read_pdf_first_pages(pdf_file, num_pages=5)

        if text.startswith("Error"):
            print(f"❌ {text}")
            continue

        # Extract year from text
        year_from_text = extract_year_from_text(text)
        print(f"Year from PDF content: {year_from_text or 'Not found'}")

        # Show first 500 chars for context
        print(f"\nFirst 500 chars of PDF:")
        print("-" * 80)
        print(text[:500].strip())
        print("-" * 80)

        # Determine final year
        final_year = year_from_filename or year_from_text or "Unknown"
        print(f"\n✅ Final year to use: {final_year}")

        # Show current filename structure
        if " -- " in pdf_file.name:
            parts = pdf_file.name.split(' -- ')
            print(f"\nCurrent structure:")
            print(f"  Title: {parts[0] if len(parts) > 0 else 'N/A'}")
            print(f"  Author: {parts[1] if len(parts) > 1 else 'N/A'}")
            print(f"  Edition/Year: {parts[2] if len(parts) > 2 else 'N/A'}")
            print(f"  Publisher: {parts[3] if len(parts) > 3 else 'N/A'}")

if __name__ == '__main__':
    main()
