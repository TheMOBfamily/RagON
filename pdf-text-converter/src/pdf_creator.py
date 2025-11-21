"""Create text-only PDF from extracted text."""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Optional
from fpdf import FPDF
from pypdf import PdfWriter, PdfReader
import tempfile


logger = logging.getLogger("pdf_converter.creator")


class TextPDF(FPDF):
    """Custom PDF class for text-only output."""
    
    def header(self):
        """PDF header (empty for text-only)."""
        pass
    
    def footer(self):
        """PDF footer with page number."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def create_text_pdf(text: str, output_path: Path) -> bool:
    """Create text-only PDF from extracted text.
    
    Args:
        text: Extracted text content
        output_path: Path to save output PDF
    
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"Creating text-only PDF: {output_path.name}")
        
        pdf = TextPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Split text into lines and add to PDF
        lines = text.split('\n')
        
        for line in lines:
            # Handle special characters and encoding
            try:
                # Clean line and encode for PDF
                clean_line = line.encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 10, clean_line)
            except Exception as e:
                logger.debug(f"Skipping line with encoding issue: {e}")
                continue
        
        # Save PDF
        pdf.output(str(output_path))
        
        file_size = output_path.stat().st_size
        logger.info(f"Created PDF: {output_path.name} ({file_size} bytes)")
        
        return True
    
    except Exception as e:
        logger.error(f"Failed to create PDF: {e}")
        return False


def create_text_pdf_from_text(text: str, original_name: str = "") -> Optional[Path]:
    """Create a temporary PDF from text.
    
    Args:
        text: Extracted text content
        original_name: Original PDF filename for metadata
    
    Returns:
        Path to temporary PDF file, or None if failed
    """
    try:
        # Create temp PDF
        pdf = TextPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Set metadata
        pdf.set_title(f"Text Version: {original_name}")
        pdf.set_author("PDF Text Converter")
        pdf.set_creator("mini-rag/pdf-text-converter")
        
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        
        # Add content
        lines = text.split('\n')
        for line in lines:
            try:
                clean_line = line.encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 8, clean_line)
            except Exception:
                continue
        
        # Save to temp file
        temp_fd, temp_path = tempfile.mkstemp(suffix='.pdf')
        import os
        os.close(temp_fd)
        
        pdf.output(temp_path)
        return Path(temp_path)
    
    except Exception as e:
        logger.error(f"Failed to create temp PDF: {e}")
        return None


def merge_pdfs(existing_pdf: Path, new_pdf: Path, output_path: Path) -> bool:
    """Merge new PDF into existing PDF.
    
    Args:
        existing_pdf: Existing PDF file path (may not exist on first batch)
        new_pdf: New PDF to append
        output_path: Output path for merged PDF
    
    Returns:
        True if successful, False otherwise
    """
    try:
        writer = PdfWriter()
        
        # Add pages from existing PDF if it exists
        if existing_pdf.exists():
            logger.info(f"  Merging with existing PDF ({existing_pdf.stat().st_size} bytes)")
            reader = PdfReader(str(existing_pdf))
            existing_pages = len(reader.pages)
            logger.info(f"  Existing pages: {existing_pages}")
            for page in reader.pages:
                writer.add_page(page)
        else:
            logger.info("  First batch - creating new PDF")
        
        # Add pages from new PDF
        logger.info(f"  Adding new batch PDF ({new_pdf.stat().st_size} bytes)")
        reader = PdfReader(str(new_pdf))
        new_pages = len(reader.pages)
        logger.info(f"  New pages: {new_pages}")
        for page in reader.pages:
            writer.add_page(page)
        
        # Write merged PDF
        logger.info(f"  Writing merged PDF to {output_path}")
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        logger.info(f"  ✓ Merge complete: {output_path.stat().st_size} bytes")
        return True
    
    except Exception as e:
        logger.error(f"Failed to merge PDFs: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False
