#!/usr/bin/env python3
"""
DKM-PDFs Deduplicator - Find and Organize Duplicate PDFs

SAFETY FEATURES:
  - ⛔ NEVER deletes files - only moves to _backup_duplicates/
  - ✅ Comprehensive logging and reporting
  - 📊 Dry-run mode by default (--execute to perform moves)
  - 🔍 Prioritizes: newer year > text- prefix > non-scanned

Usage:
  # Dry-run (SAFE - no changes)
  python tools/deduplicate-dkm-pdfs.py --dir /path/to/DKM-PDFs

  # Execute (after reviewing dry-run)
  python tools/deduplicate-dkm-pdfs.py --dir /path/to/DKM-PDFs --execute

  # Custom threshold
  python tools/deduplicate-dkm-pdfs.py --dir /path/to/DKM-PDFs --threshold 0.85

Author: AI Assistant + Fong
Date: 2025-11-20
"""

import re
import sys
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Set, List, Tuple, Dict


def normalize_filename(filename: str) -> Tuple[Set[str], List[str], str]:
    """
    Extract meaningful tokens from filename.
    
    Steps:
    1. Remove extension (.pdf, .PDF)
    2. Remove MD5 hash suffix (32 chars)
    3. Remove prefixes (text-, text-scanned-, scanned-, Unknown-)
    4. Extract volume/chapter/book identifiers
    5. Split by separators (-, _, space, .)
    6. Lowercase and filter short tokens (<3 chars)
    
    Args:
        filename: Original filename
    
    Returns:
        Tuple of (token_set, token_list, volume_identifier)
    """
    # Remove extension
    name = re.sub(r'\.(pdf|PDF)$', '', filename)
    
    # Remove hash suffix (32 chars MD5)
    name = re.sub(r'[-_][a-f0-9]{32}$', '', name)
    
    # Remove common prefixes for comparison
    name_for_comparison = re.sub(r'^(text-scanned-|text-|scanned-|Unknown-)', '', name, flags=re.IGNORECASE)
    
    # Extract volume/chapter/book identifiers (e.g., "Volume_2", "Book-5", "Chapter 3")
    # This helps identify different volumes/chapters of the same series
    volume_id = ""
    volume_patterns = [
        r'volume[_\s-]*(\d+)',
        r'vol[_\s-]*(\d+)',
        r'book[_\s-]*(\d+)',
        r'chapter[_\s-]*(\d+)',
        r'part[_\s-]*(\d+)',
        r'edition[_\s-]*(\d+)'
    ]
    
    for pattern in volume_patterns:
        match = re.search(pattern, name_for_comparison.lower())
        if match:
            volume_id = match.group(0)  # e.g., "volume_2"
            break
    
    # Split by separators
    tokens = re.split(r'[-_\s.]+', name_for_comparison.lower())
    
    # Remove empty and very short tokens
    tokens = [t for t in tokens if len(t) > 2]
    
    return set(tokens), tokens, volume_id


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Calculate Jaccard similarity: |intersection| / |union|"""
    if not set1 or not set2:
        return 0.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0


def token_set_ratio(set1: Set[str], set2: Set[str]) -> float:
    """Token Set Ratio: Common tokens / max token count"""
    if not set1 or not set2:
        return 0.0
    
    common = set1 & set2
    max_len = max(len(set1), len(set2))
    
    return len(common) / max_len if max_len > 0 else 0.0


def extract_year(filename: str) -> int:
    """Extract year from filename (YYYY- prefix)"""
    match = re.search(r'^(\d{4})', filename)
    return int(match.group(1)) if match else 0


def has_text_layer_prefix(filename: str) -> bool:
    """Check if filename has text- or Text- prefix (OCR'd PDF)"""
    return bool(re.match(r'^text-', filename, re.IGNORECASE))


def is_scanned(filename: str) -> bool:
    """Check if filename contains 'scanned'"""
    return 'scanned' in filename.lower()


def score_file_quality(filename: str) -> tuple:
    """
    Score file quality for choosing best version.
    
    Priority (descending):
    1. Year (newer is better)
    2. Has text layer prefix (text-* is better)
    3. Not scanned (non-scanned is better)
    4. Shorter filename (simpler is better)
    
    Returns:
        Tuple for sorting: (year, has_text, not_scanned, -len)
    """
    year = extract_year(filename)
    has_text = has_text_layer_prefix(filename)
    not_scanned = not is_scanned(filename)
    
    return (year, has_text, not_scanned, -len(filename))


def find_duplicates(pdf_dir: str, threshold: float = 0.85) -> List[Dict]:
    """
    Find potential duplicate PDFs using token-based similarity.
    
    Args:
        pdf_dir: Directory containing PDFs
        threshold: Similarity threshold (0.0-1.0), default 0.85 for stricter matching
    
    Returns:
        List of duplicate groups with scores
    """
    pdf_path = Path(pdf_dir)
    
    # Find all PDF files
    pdf_files = list(pdf_path.glob('*.pdf')) + list(pdf_path.glob('*.PDF'))
    filenames = [f.name for f in pdf_files]
    
    print(f"📁 Scanning {len(filenames)} PDF files in {pdf_dir}")
    print(f"🎯 Similarity threshold: {threshold}\n")
    
    # Group by year for faster comparison
    by_year = defaultdict(list)
    for fname in filenames:
        year = extract_year(fname)
        by_year[year].append(fname)
    
    # Find potential duplicates
    duplicates = []
    checked = set()
    
    for year, files in by_year.items():
        if year and len(files) > 1:
            for i, file1 in enumerate(files):
                if file1 in checked:
                    continue
                
                tokens1_set, tokens1_list, volume1 = normalize_filename(file1)
                
                for file2 in files[i+1:]:
                    if file2 in checked:
                        continue
                    
                    tokens2_set, tokens2_list, volume2 = normalize_filename(file2)
                    
                    # If both have volume identifiers and they differ, NOT duplicates
                    if volume1 and volume2 and volume1 != volume2:
                        continue  # Skip - different volumes of same series
                    
                    # Calculate similarities
                    jaccard = jaccard_similarity(tokens1_set, tokens2_set)
                    token_score = token_set_ratio(tokens1_set, tokens2_set)
                    
                    # Combined score (max of both)
                    score = max(jaccard, token_score)
                    
                    # If high similarity, it's a potential duplicate
                    if score >= threshold:
                        dup_entry = {
                            'file1': file1,
                            'file2': file2,
                            'score': score,
                            'jaccard': jaccard,
                            'token_score': token_score,
                            'year': year,
                            'volume1': volume1,
                            'volume2': volume2
                        }
                        
                        duplicates.append(dup_entry)
                        checked.add(file2)
    
    # Sort by score (descending)
    duplicates.sort(key=lambda x: x['score'], reverse=True)
    
    return duplicates


def group_duplicates(duplicates: List[Dict]) -> List[List[str]]:
    """
    Group duplicate pairs into clusters.
    
    Example: If A~B and B~C, return [A, B, C] as one group
    """
    # Build adjacency map
    graph = defaultdict(set)
    for dup in duplicates:
        f1, f2 = dup['file1'], dup['file2']
        graph[f1].add(f2)
        graph[f2].add(f1)
    
    # Find connected components (groups)
    visited = set()
    groups = []
    
    def dfs(node, group):
        visited.add(node)
        group.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, group)
    
    for node in graph:
        if node not in visited:
            group = []
            dfs(node, group)
            groups.append(group)
    
    return groups


def choose_best_file(files: List[str]) -> Tuple[str, List[str]]:
    """
    Choose the best file from a duplicate group.
    
    Returns:
        (best_file, files_to_move)
    """
    # Sort by quality score (descending)
    sorted_files = sorted(files, key=score_file_quality, reverse=True)
    
    best = sorted_files[0]
    to_move = sorted_files[1:]
    
    return best, to_move


def print_duplicate_report(duplicates: List[Dict], groups: List[List[str]]):
    """Print duplicate detection report"""
    print("=" * 100)
    print("🔍 DUPLICATE DETECTION REPORT")
    print(f"Found {len(duplicates)} duplicate pairs")
    print(f"Grouped into {len(groups)} duplicate clusters")
    print("=" * 100)
    
    if not groups:
        print("\n✅ No duplicates found! Your DKM-PDFs is clean.\n")
        return
    
    print(f"\n📊 DUPLICATE GROUPS:\n")
    
    total_to_move = 0
    
    for i, group in enumerate(groups, 1):
        best, to_move = choose_best_file(group)
        total_to_move += len(to_move)
        
        print(f"{i}. Group of {len(group)} files:")
        print(f"   ✅ KEEP:  {best}")
        
        # Show quality score breakdown
        year, has_text, not_scanned, neg_len = score_file_quality(best)
        print(f"      └─ Score: year={year}, text_layer={has_text}, not_scanned={not_scanned}")
        
        for file in to_move:
            year, has_text, not_scanned, neg_len = score_file_quality(file)
            print(f"   ❌ MOVE:  {file}")
            print(f"      └─ Score: year={year}, text_layer={has_text}, not_scanned={not_scanned}")
        print()
    
    print("=" * 100)
    print(f"\n📈 SUMMARY:")
    print(f"   Total duplicate groups: {len(groups)}")
    print(f"   Files to keep: {len(groups)}")
    print(f"   Files to move: {total_to_move}")
    print("=" * 100)


def execute_deduplication(pdf_dir: str, groups: List[List[str]], dry_run: bool = True):
    """
    Execute deduplication by moving duplicate files to backup folder.
    
    Args:
        pdf_dir: Directory containing PDFs
        groups: List of duplicate groups
        dry_run: If True, only print what would be done
    """
    pdf_path = Path(pdf_dir)
    backup_dir = pdf_path / "_backup_duplicates"
    
    if not groups:
        print("\n✅ Nothing to do - no duplicates found.\n")
        return
    
    if dry_run:
        print("\n" + "=" * 100)
        print("🔍 DRY RUN MODE - No files will be moved")
        print("=" * 100)
        print(f"\nBackup directory: {backup_dir}")
        print("\nFiles that WOULD be moved:\n")
    else:
        # Create backup directory
        backup_dir.mkdir(exist_ok=True)
        print("\n" + "=" * 100)
        print("🚀 EXECUTING DEDUPLICATION")
        print("=" * 100)
        print(f"\nBackup directory: {backup_dir}")
        print("\nMoving files:\n")
    
    moved_count = 0
    
    for i, group in enumerate(groups, 1):
        best, to_move = choose_best_file(group)
        
        for file in to_move:
            src = pdf_path / file
            dst = backup_dir / file
            
            if dry_run:
                print(f"  [{i}] {file} → _backup_duplicates/")
            else:
                # Check if destination exists
                if dst.exists():
                    print(f"  ⚠️  SKIP (already exists): {file}")
                else:
                    src.rename(dst)
                    print(f"  ✅ MOVED: {file}")
                    moved_count += 1
    
    print("\n" + "=" * 100)
    if dry_run:
        print(f"🔍 DRY RUN COMPLETE - {len([f for g in groups for f in choose_best_file(g)[1]])} files would be moved")
        print(f"\n💡 To execute, run with --execute flag")
    else:
        print(f"✅ DEDUPLICATION COMPLETE - {moved_count} files moved to backup")
        print(f"\n💡 Review backup folder before deleting: {backup_dir}")
    print("=" * 100 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="DKM-PDFs Deduplicator - Find and organize duplicate PDFs safely",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry-run (safe - no changes)
  python tools/deduplicate-dkm-pdfs.py --dir /home/fong/Projects/mini-rag/DKM-PDFs
  
  # Execute deduplication
  python tools/deduplicate-dkm-pdfs.py --dir /home/fong/Projects/mini-rag/DKM-PDFs --execute
  
  # Custom threshold
  python tools/deduplicate-dkm-pdfs.py --dir /path/to/DKM-PDFs --threshold 0.90
        """
    )
    
    parser.add_argument(
        '--dir',
        required=True,
        help='Directory containing DKM-PDFs to deduplicate'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.85,
        help='Similarity threshold (0.0-1.0, default: 0.85 for stricter matching)'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Execute file moves (default is dry-run)'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not Path(args.dir).exists():
        print(f"❌ Error: Directory not found: {args.dir}")
        sys.exit(1)
    
    if not 0.0 <= args.threshold <= 1.0:
        print(f"❌ Error: Threshold must be between 0.0 and 1.0")
        sys.exit(1)
    
    # Find duplicates
    duplicates = find_duplicates(args.dir, args.threshold)
    
    # Group duplicates
    groups = group_duplicates(duplicates)
    
    # Print report
    print_duplicate_report(duplicates, groups)
    
    # Execute deduplication
    execute_deduplication(args.dir, groups, dry_run=not args.execute)


if __name__ == '__main__':
    main()
