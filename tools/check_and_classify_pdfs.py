#!/usr/bin/env python3
"""
Check PDF duplicates and classify by text layer (scanned vs native)
Based on instructions from .fong/instructions/customs/instructions-pdf-batch-processing-workflow/
"""

from __future__ import annotations
import os
import subprocess
import re
from pathlib import Path
from typing import List, Tuple, Set


def _load_env_from_ragon_root() -> None:
    """Load .env from RAGON_ROOT."""
    current = Path(__file__).resolve().parent
    for _ in range(3):
        env_file = current / ".env"
        if env_file.exists():
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, _, value = line.partition("=")
                        os.environ.setdefault(key.strip(), value.strip().strip('"'))
            break
        current = current.parent


_load_env_from_ragon_root()

# Paths from .env
DKM_PDF_PATH = os.getenv("DKM_PDF_PATH", "")
RAGON_ROOT = os.getenv("RAGON_ROOT", "")

SOURCE_DIR = Path(RAGON_ROOT) / "PDFs" if RAGON_ROOT else Path("PDFs")
TARGET_DIR = Path(DKM_PDF_PATH) if DKM_PDF_PATH else Path("DKM-PDFs")
SCANNED_DIR = Path(RAGON_ROOT) / "PDFs" / "scanned" if RAGON_ROOT else Path("PDFs/scanned")

def normalize_filename(filename: str) -> Set[str]:
    """
    Normalize filename to token set for comparison
    Based on Jaccard + Token Set Ratio algorithm
    """
    # Remove extension
    name = filename.replace('.PDF', '').replace('.pdf', '')

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

def check_text_layer(pdf_path: Path, pages_to_check: List[int] = [1, 5, 10, 20]) -> Tuple[bool, int]:
    """
    Check if PDF has text layer (native) or is scanned
    Returns: (has_text_layer, max_chars_found)
    Based on workflow step 4: scanned detection
    """
    max_chars = 0

    for page in pages_to_check:
        try:
            result = subprocess.run(
                ['pdftotext', '-f', str(page), '-l', str(page), str(pdf_path), '-'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                char_count = len(result.stdout)
                max_chars = max(max_chars, char_count)

                # Early exit if we found significant text
                if max_chars >= 100:
                    return (True, max_chars)
        except Exception as e:
            print(f"  ⚠️  Error checking page {page}: {e}")
            continue

    # Decision: < 100 chars = SCANNED
    return (max_chars >= 100, max_chars)

def main():
    print("🔍 PDF Classification & Duplicate Check")
    print("=" * 70)

    # Ensure directories exist
    SCANNED_DIR.mkdir(exist_ok=True)

    # Get file lists
    source_files = sorted([f.name for f in SOURCE_DIR.glob("*.PDF")] +
                         [f.name for f in SOURCE_DIR.glob("*.pdf")])
    target_files = sorted([f.name for f in TARGET_DIR.glob("*.PDF")] +
                         [f.name for f in TARGET_DIR.glob("*.pdf")])

    print(f"\n📁 Source: {len(source_files)} PDFs in {SOURCE_DIR}")
    print(f"📁 Target: {len(target_files)} PDFs in {TARGET_DIR}")
    print(f"📁 Scanned: {SCANNED_DIR}")
    print()

    results = {
        'new_native': [],        # New PDFs with text layer → move to DKM-PDFs
        'new_scanned': [],       # New scanned PDFs → move to PDFs/scanned
        'duplicates': [],        # Already in DKM-PDFs
        'errors': []            # Errors during processing
    }

    # Process each source file
    for idx, source_file in enumerate(source_files, 1):
        print(f"\n[{idx}/{len(source_files)}] {source_file}")

        source_path = SOURCE_DIR / source_file

        # Skip if already has scanned- prefix
        if source_file.startswith('scanned-'):
            print(f"  📸 Already marked as scanned")
            results['new_scanned'].append(source_file)
            continue

        # Check for duplicates in target
        matches = find_similar_in_target(source_file, target_files, threshold=0.7)

        if matches:
            print(f"  🔄 Found {len(matches)} similar file(s) in DKM-PDFs:")
            for match_file, score in matches[:3]:  # Show top 3
                print(f"     - {match_file} (score: {score:.2f})")
            results['duplicates'].append((source_file, matches))
            continue

        # Check text layer
        print(f"  🔍 Checking text layer...")
        try:
            has_text, max_chars = check_text_layer(source_path)

            if has_text:
                print(f"  ✅ Native PDF (max chars: {max_chars}) → DKM-PDFs")
                results['new_native'].append(source_file)
            else:
                print(f"  📸 Scanned PDF (max chars: {max_chars}) → PDFs/scanned")
                results['new_scanned'].append(source_file)
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results['errors'].append((source_file, str(e)))

    # Print summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"\n✅ New native PDFs (→ DKM-PDFs): {len(results['new_native'])}")
    for f in results['new_native']:
        print(f"   - {f}")

    print(f"\n📸 New scanned PDFs (→ PDFs/scanned): {len(results['new_scanned'])}")
    for f in results['new_scanned']:
        print(f"   - {f}")

    print(f"\n🔄 Duplicates (already in DKM-PDFs): {len(results['duplicates'])}")
    for source, matches in results['duplicates']:
        top_match = matches[0] if matches else ("N/A", 0)
        print(f"   - {source} ≈ {top_match[0]} ({top_match[1]:.2f})")

    if results['errors']:
        print(f"\n❌ Errors: {len(results['errors'])}")
        for f, err in results['errors']:
            print(f"   - {f}: {err}")

    # Ask for confirmation before moving
    print("\n" + "=" * 70)
    print("🚚 NEXT STEPS:")
    print("=" * 70)

    if results['new_native']:
        print(f"\nTo move {len(results['new_native'])} native PDFs to DKM-PDFs:")
        print("```bash")
        for f in results['new_native']:
            print(f'mv "{SOURCE_DIR}/{f}" "{TARGET_DIR}/"')
        print("```")

    if results['new_scanned']:
        print(f"\nTo move {len(results['new_scanned'])} scanned PDFs to PDFs/scanned:")
        print("```bash")
        for f in results['new_scanned']:
            dest_name = f if f.startswith('scanned-') else f'scanned-{f}'
            print(f'mv "{SOURCE_DIR}/{f}" "{SCANNED_DIR}/{dest_name}"')
        print("```")

    print("\n✅ Done! Review the results above before executing moves.")

if __name__ == '__main__':
    main()
