#!/usr/bin/env python3
"""Convert PDF to TXT - Extract text from PDF with text layer

Usage:
    python convert-pdf-to-txt.py <input.pdf> [output.txt]
    
If output.txt not specified, saves as <input-basename>.txt in same directory.
"""
from __future__ import annotations
import sys
from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: Path, output_path: Path | None = None) -> bool:
    """Extract text from PDF and save to TXT file.
    
    Args:
        pdf_path: Input PDF file path
        output_path: Output TXT file path (optional)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Determine output path
        if output_path is None:
            output_path = pdf_path.parent / f"{pdf_path.stem}.txt"
        
        print(f"📄 Reading PDF: {pdf_path.name}")
        print(f"   Size: {pdf_path.stat().st_size / (1024*1024):.2f} MB")
        
        # Read PDF
        reader = PdfReader(str(pdf_path))
        total_pages = len(reader.pages)
        print(f"   Pages: {total_pages}")
        
        # Extract text from all pages
        all_text = []
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                all_text.append(f"{'='*60}\n")
                all_text.append(f"Page {i}/{total_pages}\n")
                all_text.append(f"{'='*60}\n\n")
                all_text.append(text)
                all_text.append("\n\n")
                print(f"   ✓ Page {i}/{total_pages}: {len(text)} chars")
            else:
                print(f"   ⚠ Page {i}/{total_pages}: No text found")
        
        # Save to file
        full_text = "".join(all_text)
        output_path.write_text(full_text, encoding="utf-8")
        
        print(f"\n✅ SUCCESS!")
        print(f"   Output: {output_path}")
        print(f"   Size: {output_path.stat().st_size / 1024:.2f} KB")
        print(f"   Characters: {len(full_text):,}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert-pdf-to-txt.py <input.pdf> [output.txt]")
        print("\nExample:")
        print("  python convert-pdf-to-txt.py document.pdf")
        print("  python convert-pdf-to-txt.py document.pdf output.txt")
        sys.exit(1)
    
    # Get input PDF path
    pdf_path = Path(sys.argv[1]).resolve()
    if not pdf_path.exists():
        print(f"❌ ERROR: File not found: {pdf_path}")
        sys.exit(1)
    
    if not pdf_path.suffix.lower() == ".pdf":
        print(f"❌ ERROR: Not a PDF file: {pdf_path}")
        sys.exit(1)
    
    # Get output TXT path (optional)
    output_path = None
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2]).resolve()
    
    # Extract text
    if extract_text_from_pdf(pdf_path, output_path):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
