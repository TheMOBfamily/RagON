#!/usr/bin/env python3
"""Convert TXT to PDF - Create PDF from text file

Usage:
    python convert-txt-to-pdf.py <input.txt> [output.pdf]
    
If output.pdf not specified, saves as <input-basename>.pdf in same directory.
"""
from __future__ import annotations
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def create_pdf_from_text(txt_path: Path, output_path: Path | None = None) -> bool:
    """Create PDF from text file.
    
    Args:
        txt_path: Input TXT file path
        output_path: Output PDF file path (optional)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Determine output path
        if output_path is None:
            output_path = txt_path.parent / f"{txt_path.stem}.pdf"
        
        print(f"📄 Reading TXT: {txt_path.name}")
        print(f"   Size: {txt_path.stat().st_size / 1024:.2f} KB")
        
        # Read text
        text = txt_path.read_text(encoding="utf-8")
        lines = text.split('\n')
        print(f"   Lines: {len(lines):,}")
        print(f"   Characters: {len(text):,}")
        
        # Create PDF
        print(f"\n📝 Creating PDF...")
        c = canvas.Canvas(str(output_path), pagesize=letter)
        
        # Page dimensions
        width, height = letter
        margin_left = 0.75 * inch
        margin_right = width - 0.75 * inch
        margin_top = height - 0.75 * inch
        margin_bottom = 0.75 * inch
        
        # Text settings
        font_name = "Helvetica"
        font_size = 10
        line_height = 12
        
        c.setFont(font_name, font_size)
        
        # Current position
        y = margin_top
        page_count = 1
        
        # Process each line
        for i, line in enumerate(lines, start=1):
            # Check if need new page
            if y < margin_bottom:
                c.showPage()
                c.setFont(font_name, font_size)
                y = margin_top
                page_count += 1
            
            # Handle long lines (word wrap)
            line = line.rstrip()
            if not line:
                # Empty line - just add space
                y -= line_height
                continue
            
            # Simple word wrap
            words = line.split()
            current_line = ""
            
            for word in words:
                test_line = f"{current_line} {word}".strip()
                
                # Estimate width (rough approximation)
                char_width = font_size * 0.5
                estimated_width = len(test_line) * char_width
                max_width = margin_right - margin_left
                
                if estimated_width <= max_width:
                    current_line = test_line
                else:
                    # Draw current line and start new one
                    if current_line:
                        c.drawString(margin_left, y, current_line)
                        y -= line_height
                        
                        # Check page break
                        if y < margin_bottom:
                            c.showPage()
                            c.setFont(font_name, font_size)
                            y = margin_top
                            page_count += 1
                    
                    current_line = word
            
            # Draw remaining text
            if current_line:
                c.drawString(margin_left, y, current_line)
                y -= line_height
            
            # Progress indicator
            if i % 500 == 0:
                print(f"   Processed {i:,}/{len(lines):,} lines...")
        
        # Save PDF
        c.save()
        
        print(f"\n✅ SUCCESS!")
        print(f"   Output: {output_path}")
        print(f"   Size: {output_path.stat().st_size / 1024:.2f} KB")
        print(f"   Pages: {page_count}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert-txt-to-pdf.py <input.txt> [output.pdf]")
        print("\nExample:")
        print("  python convert-txt-to-pdf.py document.txt")
        print("  python convert-txt-to-pdf.py document.txt output.pdf")
        sys.exit(1)
    
    # Get input TXT path
    txt_path = Path(sys.argv[1]).resolve()
    if not txt_path.exists():
        print(f"❌ ERROR: File not found: {txt_path}")
        sys.exit(1)
    
    if not txt_path.suffix.lower() == ".txt":
        print(f"❌ ERROR: Not a TXT file: {txt_path}")
        sys.exit(1)
    
    # Get output PDF path (optional)
    output_path = None
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2]).resolve()
    
    # Create PDF
    if create_pdf_from_text(txt_path, output_path):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
