#!/usr/bin/env python3
"""Convert PDF to clean PDF by extracting text and recreating PDF.

This fixes font encoding issues that cause embedding errors.

Usage:
    python convert-pdf-clean.py <input.pdf>
"""
from __future__ import annotations
import sys
from pathlib import Path
from pypdf import PdfReader
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT
import tempfile
import time

sys.path.insert(0, str(Path(__file__).parent / "src"))
from utils import setup_logging, format_file_size


def extract_text_from_pdf(pdf_path: Path, logger) -> list[tuple[int, str]]:
    """Extract text from PDF page by page.
    
    Returns:
        List of (page_num, text) tuples
    """
    logger.info(f"Extracting text from: {pdf_path.name}")
    
    reader = PdfReader(str(pdf_path))
    pages_text = []
    
    for page_num, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
            # Clean text: remove null bytes and other problematic chars
            text = text.replace('\x00', '').replace('\ufffd', '')
            text = ''.join(char for char in text if char.isprintable() or char in '\n\r\t')
            
            if text.strip():
                pages_text.append((page_num, text))
                logger.info(f"  Page {page_num}: {len(text)} chars")
            else:
                logger.warning(f"  Page {page_num}: No text")
        except Exception as e:
            logger.error(f"  Page {page_num}: Error - {e}")
            continue
    
    total_chars = sum(len(text) for _, text in pages_text)
    logger.info(f"Total extracted: {total_chars:,} characters from {len(pages_text)} pages\n")
    
    return pages_text


def create_clean_pdf(pages_text: list[tuple[int, str]], output_path: Path, logger) -> bool:
    """Create clean PDF from extracted text using reportlab.
    
    Args:
        pages_text: List of (page_num, text) tuples
        output_path: Output PDF path
    
    Returns:
        True if successful
    """
    logger.info(f"Creating clean PDF: {output_path.name}")
    
    try:
        # Create PDF with SimpleDocTemplate for better text handling
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Styles
        styles = getSampleStyleSheet()
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            alignment=TA_LEFT,
            wordWrap='CJK'  # Better word wrapping
        )
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading2'],
            fontSize=12,
            leading=16,
            spaceAfter=12,
            textColor='darkblue'
        )
        
        # Build content
        story = []
        
        for page_num, text in pages_text:
            # Add page header
            page_title = Paragraph(f"<b>Page {page_num}</b>", title_style)
            story.append(page_title)
            story.append(Spacer(1, 0.2*inch))
            
            # Split text into paragraphs
            paragraphs = text.split('\n\n')
            
            for para_text in paragraphs:
                if not para_text.strip():
                    continue
                
                # Clean and escape special chars for reportlab
                para_text = para_text.strip()
                para_text = para_text.replace('&', '&amp;')
                para_text = para_text.replace('<', '&lt;')
                para_text = para_text.replace('>', '&gt;')
                
                # Replace line breaks with <br/>
                para_text = para_text.replace('\n', '<br/>')
                
                try:
                    para = Paragraph(para_text, normal_style)
                    story.append(para)
                    story.append(Spacer(1, 0.1*inch))
                except Exception as e:
                    logger.warning(f"    Skipped problematic paragraph: {str(e)[:50]}")
                    continue
            
            # Page break between pages
            story.append(PageBreak())
            logger.info(f"  Added page {page_num}")
        
        # Build PDF
        doc.build(story)
        
        logger.info(f"✅ Clean PDF created successfully")
        logger.info(f"   Output: {output_path}")
        logger.info(f"   Size: {format_file_size(output_path.stat().st_size)}")
        
        # Verify
        reader_verify = PdfReader(str(output_path))
        logger.info(f"   Pages: {len(reader_verify.pages)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to create PDF: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def process_pdf(pdf_path: Path, logger) -> Path | None:
    """Process a PDF file: extract text and create clean PDF.
    
    Returns:
        Path to output PDF if successful, None otherwise
    """
    start_time = time.time()
    
    logger.info("="*60)
    logger.info(f"Processing: {pdf_path}")
    logger.info(f"Size: {format_file_size(pdf_path.stat().st_size)}")
    logger.info("="*60 + "\n")
    
    # Extract text
    pages_text = extract_text_from_pdf(pdf_path, logger)
    
    if not pages_text:
        logger.error("No text extracted from PDF!")
        return None
    
    # Output path: same directory, prefixed with "clean-"
    output_path = pdf_path.parent / f"clean-{pdf_path.name}"
    
    # Create clean PDF
    success = create_clean_pdf(pages_text, output_path, logger)
    
    if success:
        elapsed = time.time() - start_time
        logger.info(f"\n✅ COMPLETED in {elapsed:.1f}s")
        logger.info(f"   Original: {pdf_path.name}")
        logger.info(f"   Clean: {output_path.name}")
        return output_path
    
    return None


def main():
    logger = setup_logging(log_dir=str(Path(__file__).parent / "logs"))
    
    if len(sys.argv) < 2:
        print("Usage: python convert-pdf-clean.py <input.pdf>")
        print("\nThis tool converts a PDF to clean PDF by:")
        print("  1. Extracting text from original PDF")
        print("  2. Creating new PDF with clean fonts")
        print("  3. Output: clean-<original_name>.pdf")
        sys.exit(1)
    
    try:
        pdf_path = Path(sys.argv[1]).resolve()
        
        if not pdf_path.exists():
            logger.error(f"File not found: {pdf_path}")
            sys.exit(1)
        
        if not pdf_path.suffix.lower() == '.pdf':
            logger.error(f"Not a PDF file: {pdf_path}")
            sys.exit(1)
        
        output_path = process_pdf(pdf_path, logger)
        
        if output_path:
            print(f"\n✅ Success! Clean PDF created:")
            print(f"   {output_path}")
            sys.exit(0)
        else:
            print("\n❌ Failed to create clean PDF")
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.info("\n⚠ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
