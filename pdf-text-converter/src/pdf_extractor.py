"""Extract text from PDFs with text layer using PyPDF."""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Optional
from pypdf import PdfReader


logger = logging.getLogger("pdf_converter.extractor")


def extract_text_from_pdf(pdf_path: Path) -> Optional[str]:
    """Extract text from PDF file with text layer.
    
    Args:
        pdf_path: Path to PDF file
    
    Returns:
        Extracted text as string, or None if no text found
    """
    try:
        reader = PdfReader(str(pdf_path))
        logger.info(f"Reading PDF: {pdf_path.name} ({len(reader.pages)} pages)")
        
        text_parts = []
        pages_with_text = 0
        
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            
            if page_text and page_text.strip():
                text_parts.append(f"--- Page {i + 1} ---\n{page_text.strip()}\n")
                pages_with_text += 1
        
        if pages_with_text == 0:
            logger.warning(f"No text found in PDF (might be scanned): {pdf_path.name}")
            return None
        
        logger.info(f"Extracted text from {pages_with_text}/{len(reader.pages)} pages")
        return "\n".join(text_parts)
    
    except Exception as e:
        logger.error(f"Failed to extract text from {pdf_path.name}: {e}")
        return None


def has_text_layer(pdf_path: Path) -> bool:
    """Check if PDF has text layer by testing first few pages.
    
    Args:
        pdf_path: Path to PDF file
    
    Returns:
        True if PDF has text layer, False otherwise
    """
    try:
        reader = PdfReader(str(pdf_path))
        
        # Check first 3 pages (or all if less than 3)
        pages_to_check = min(3, len(reader.pages))
        
        for i in range(pages_to_check):
            page_text = reader.pages[i].extract_text()
            
            # If any page has text (>50 chars), consider it has text layer
            if page_text and len(page_text.strip()) > 50:
                return True
        
        return False
    
    except Exception as e:
        logger.error(f"Error checking text layer: {e}")
        return False
