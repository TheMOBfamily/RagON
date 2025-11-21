#!/usr/bin/env python3
"""
Check scanned PDFs against DKM-PDFs collection
Move duplicates to pools folder, keep new ones for OCR
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Set

# Paths
SCANNED_DIR = Path("/home/fong/Projects/mini-rag/PDFs/scanned")
TARGET_DIR = Path("/home/fong/Projects/mini-rag/DKM-PDFs")
POOLS_DIR = Path("/home/fong/Projects/mini-rag/PDFs/pools")

def normalize_filename(filename: str) -> Set[str]:
    """Normalize filename to token set for comparison"""
    # Remove extension
    name = filename.replace('.PDF', '').replace('.pdf', '')

    # Remove prefixes
    for prefix in ['scanned-', 'text-scanned-', 'text-', 'Unknown-scanned-', 'Unknown-']:
        if name.startswith(prefix):
            name = name[len(prefix):]

    # Remove MD5 hash suffix (32 chars)
    if len(name) > 32 and name[-32:].replace('-', '').replace('_', '').isalnum():
        name = name[:-32].rstrip('-_')

    # Split by separators
    tokens = re.split(r'[-_\s.]+', name.lower())

    # Filter short tokens and return set
    return set(t for t in tokens if len(t) > 2)

def calculate_similarity(tokens1: Set[str], tokens2: Set[str]) -> float:
    """Calculate Jaccard similarity + Token Set Ratio, return max"""
    if not tokens1 or not tokens2:
        return 0.0

    intersection = tokens1 & tokens2
    union = tokens1 | tokens2

    # Jaccard similarity
    jaccard = len(intersection) / len(union) if union else 0.0

    # Token Set Ratio
    token_ratio = len(intersection) / max(len(tokens1), len(tokens2))

    return max(jaccard, token_ratio)

def find_similar_in_target(source_file: str, target_files: List[str], threshold: float = 0.7) -> List[Tuple[str, float]]:
    """Find similar files in target directory"""
    source_tokens = normalize_filename(source_file)
    matches = []

    for target_file in target_files:
        target_tokens = normalize_filename(target_file)
        score = calculate_similarity(source_tokens, target_tokens)

        if score >= threshold:
            matches.append((target_file, score))

    # Sort by score descending
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches

def main():
    print("🔍 Scanned PDFs Duplicate Check")
    print("=" * 70)

    # Ensure pools directory exists
    POOLS_DIR.mkdir(parents=True, exist_ok=True)

    # Get file lists
    scanned_files = sorted([f.name for f in SCANNED_DIR.glob("*.PDF")] +
                          [f.name for f in SCANNED_DIR.glob("*.pdf")])
    target_files = sorted([f.name for f in TARGET_DIR.glob("*.PDF")] +
                         [f.name for f in TARGET_DIR.glob("*.pdf")])

    print(f"\n📁 Scanned: {len(scanned_files)} PDFs in {SCANNED_DIR}")
    print(f"📁 Target: {len(target_files)} PDFs in {TARGET_DIR}")
    print(f"📁 Pools: {POOLS_DIR}")
    print()

    results = {
        'duplicates': [],     # Already in DKM-PDFs → move to pools
        'new': [],           # Not in DKM-PDFs → keep for OCR
        'case_dups': []      # Same file with different case
    }

    # Find case duplicates first
    seen_lower = {}
    for f in scanned_files:
        lower = f.lower()
        if lower in seen_lower:
            print(f"⚠️  Case duplicate: {f} ≈ {seen_lower[lower]}")
            results['case_dups'].append(f)
        else:
            seen_lower[lower] = f

    # Process each unique file
    processed = set()
    for idx, scanned_file in enumerate(scanned_files, 1):
        # Skip case duplicates
        if scanned_file in results['case_dups']:
            continue

        # Skip if already processed (case duplicate)
        if scanned_file.lower() in processed:
            continue
        processed.add(scanned_file.lower())

        print(f"\n[{idx}/{len(scanned_files)}] {scanned_file}")

        # Check for duplicates in target
        matches = find_similar_in_target(scanned_file, target_files, threshold=0.7)

        if matches:
            print(f"  🔄 Found {len(matches)} similar file(s) in DKM-PDFs:")
            for match_file, score in matches[:3]:  # Show top 3
                print(f"     - {match_file} (score: {score:.2f})")
            results['duplicates'].append((scanned_file, matches))
        else:
            print(f"  ✨ NEW - not in DKM-PDFs → keep for OCR")
            results['new'].append(scanned_file)

    # Print summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)

    print(f"\n🔄 Duplicates (already in DKM-PDFs) → move to pools: {len(results['duplicates'])}")
    for source, matches in results['duplicates']:
        top_match = matches[0] if matches else ("N/A", 0)
        print(f"   - {source}")
        print(f"     ≈ {top_match[0]} ({top_match[1]:.2f})")

    print(f"\n✨ NEW (not in DKM-PDFs) → keep for OCR: {len(results['new'])}")
    for f in results['new']:
        print(f"   - {f}")

    if results['case_dups']:
        print(f"\n⚠️  Case duplicates (keep one, remove other): {len(results['case_dups'])}")
        for f in results['case_dups']:
            print(f"   - {f}")

    # Generate move commands
    print("\n" + "=" * 70)
    print("🚚 NEXT STEPS:")
    print("=" * 70)

    if results['duplicates']:
        print(f"\nMoving {len(results['duplicates'])} duplicates to pools folder:")
        print("```bash")
        for source, _ in results['duplicates']:
            print(f'mv "{SCANNED_DIR}/{source}" "{POOLS_DIR}/"')
        print("```")

    if results['case_dups']:
        print(f"\nRemoving {len(results['case_dups'])} case duplicates:")
        print("```bash")
        for f in results['case_dups']:
            print(f'rm "{SCANNED_DIR}/{f}"')
        print("```")

    print(f"\n✅ Will keep {len(results['new'])} files for OCR in {SCANNED_DIR}")

    return results

if __name__ == '__main__':
    main()
