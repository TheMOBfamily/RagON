#!/usr/bin/env python3
"""
Compare PDFs between two folders using fuzzy string matching.
Find duplicates and identify files that need to be copied.

⚠️ IMPORTANT: This script ONLY generates reports. It does NOT copy/move any files.

Usage:
    # Basic usage (threshold 80%)
    source venv/bin/activate
    python tools/compare-pdfs-fuzzy.py \\
        --source /path/to/source/folder \\
        --dest $DKM_PDF_PATH

    # Custom threshold (85%)
    python tools/compare-pdfs-fuzzy.py \\
        --source /path/to/source \\
        --dest /path/to/dest \\
        --threshold 85

Output:
    - ✅ MATCHED FILES: Already exist in destination (skip copy)
    - ⚠️ MANUAL REVIEW: Matches with score < 90% (potential false positives)
    - ❌ NOT MATCHED: Need to copy to destination

Recommendation:
    - Use threshold 80-85% for broader matching
    - Manually review matches < 90% before deciding
    - Copy only "NOT MATCHED" files to avoid duplicates
"""

import os
import re
import argparse
from pathlib import Path
from rapidfuzz import fuzz, process


def normalize_filename(filename):
    """
    Normalize PDF filename for fuzzy matching.

    Example:
        2024-Book-Title-Author-Publisher.PDF
        -> "2024 book title author publisher"

    Args:
        filename: PDF filename (with or without extension)

    Returns:
        Normalized string for comparison
    """
    # Remove extension
    name = Path(filename).stem

    # Remove special prefixes
    name = re.sub(r'^(scanned-|text-scanned-|Unknown-)', '', name, flags=re.IGNORECASE)

    # Replace separators with spaces
    name = name.replace('-', ' ').replace('_', ' ')

    # Remove special characters, keep alphanumeric and spaces
    name = re.sub(r'[^A-Za-z0-9\s]', '', name)

    # Normalize whitespace and lowercase
    name = ' '.join(name.split()).lower()

    return name


def find_pdfs(folder_path):
    """
    Find all PDF files in folder (case-insensitive).

    Args:
        folder_path: Path to folder

    Returns:
        List of PDF filenames (basename only)
    """
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    pdfs = []
    # Check both .PDF and .pdf extensions
    for pattern in ['*.PDF', '*.pdf']:
        pdfs.extend([f.name for f in folder.rglob(pattern)])

    return sorted(set(pdfs))  # Remove duplicates and sort


def fuzzy_match_pdfs(source_files, dest_files, threshold=80):
    """
    Match PDFs from source to destination using fuzzy matching.

    Args:
        source_files: List of source PDF filenames
        dest_files: List of destination PDF filenames
        threshold: Minimum similarity score (0-100)

    Returns:
        Tuple of (matched, not_matched):
        - matched: List of (source_file, dest_file, score)
        - not_matched: List of source files with no match
    """
    # Normalize destination files for matching
    dest_normalized = {normalize_filename(f): f for f in dest_files}
    dest_choices = list(dest_normalized.keys())

    matched = []
    not_matched = []

    for src_file in source_files:
        src_norm = normalize_filename(src_file)

        # Find best match in destination
        if dest_choices:
            # Use token_set_ratio for better matching (ignores word order)
            results = process.extract(
                src_norm,
                dest_choices,
                scorer=fuzz.token_set_ratio,
                limit=1
            )

            if results and results[0][1] >= threshold:
                best_match_norm, score, _ = results[0]
                best_match_file = dest_normalized[best_match_norm]
                matched.append((src_file, best_match_file, score))
            else:
                not_matched.append(src_file)
        else:
            not_matched.append(src_file)

    return matched, not_matched


def print_report(matched, not_matched, source_folder, dest_folder):
    """Print comparison report."""
    print(f"\n{'='*80}")
    print("PDF FUZZY MATCHING REPORT")
    print(f"{'='*80}")
    print(f"Source: {source_folder}")
    print(f"Destination: {dest_folder}")
    print(f"⚠️  This script ONLY reports. It does NOT copy/move any files.")
    print(f"{'='*80}\n")

    # Separate matched files into high confidence and manual review
    high_confidence = [(s, d, sc) for s, d, sc in matched if sc >= 90]
    manual_review = [(s, d, sc) for s, d, sc in matched if sc < 90]

    # High confidence matches
    if high_confidence:
        print(f"✅ MATCHED FILES - HIGH CONFIDENCE ({len(high_confidence)}):")
        print(f"{'-'*80}")
        for src, dst, score in sorted(high_confidence, key=lambda x: -x[2]):
            print(f"[{score:>3.0f}%] {src}")
            print(f"       ↔ {dst}")
            print()

    # Manual review needed
    if manual_review:
        print(f"\n⚠️  MANUAL REVIEW NEEDED - POTENTIAL FALSE POSITIVES ({len(manual_review)}):")
        print(f"{'-'*80}")
        print("These matches have score < 90%. Please verify manually:")
        print()
        for src, dst, score in sorted(manual_review, key=lambda x: -x[2]):
            print(f"[{score:>3.0f}%] Score below 90% - verify if same book:")
            print(f"  SOURCE: {src}")
            print(f"  DEST:   {dst}")
            print()

    # Not matched files
    if not_matched:
        print(f"\n❌ NOT MATCHED - RECOMMEND TO COPY ({len(not_matched)}):")
        print(f"{'-'*80}")
        for src in sorted(not_matched):
            print(f"  • {src}")

    # Summary
    print(f"\n{'='*80}")
    print(f"SUMMARY:")
    print(f"  ✅ High confidence matches (≥90%): {len(high_confidence)}")
    print(f"  ⚠️  Manual review needed (<90%): {len(manual_review)}")
    print(f"  ❌ Not matched (recommend copy): {len(not_matched)}")
    print(f"  📊 Total source files: {len(matched) + len(not_matched)}")
    print(f"{'='*80}")
    print(f"\n💡 RECOMMENDATION:")
    print(f"  1. Review {len(manual_review)} manual review cases above")
    print(f"  2. Copy {len(not_matched)} not-matched files to destination")
    print(f"  3. Skip {len(high_confidence)} already-existing files")
    print(f"{'='*80}\n")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Compare PDFs using fuzzy matching to find duplicates"
    )
    parser.add_argument(
        '--source',
        required=True,
        help='Source folder containing PDFs to check'
    )
    parser.add_argument(
        '--dest',
        required=True,
        help='Destination folder to compare against'
    )
    parser.add_argument(
        '--threshold',
        type=int,
        default=80,
        help='Minimum similarity threshold (0-100, default: 80)'
    )

    args = parser.parse_args()

    # Validate threshold
    if not 0 <= args.threshold <= 100:
        print("Error: Threshold must be between 0 and 100")
        return 1

    # Find PDFs in both folders
    print("Scanning folders...")
    source_files = find_pdfs(args.source)
    dest_files = find_pdfs(args.dest)

    print(f"Found {len(source_files)} PDFs in source folder")
    print(f"Found {len(dest_files)} PDFs in destination folder")

    # Perform fuzzy matching
    print(f"\nMatching with threshold {args.threshold}%...")
    matched, not_matched = fuzzy_match_pdfs(source_files, dest_files, args.threshold)

    # Print report
    print_report(matched, not_matched, args.source, args.dest)

    return 0


if __name__ == '__main__':
    exit(main())
