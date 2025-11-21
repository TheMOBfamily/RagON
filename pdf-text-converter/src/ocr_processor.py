"""OCR processing for scanned PDFs using PaddleOCR."""
from __future__ import annotations
import logging
from pathlib import Path
from typing import Optional, List, Tuple
import tempfile
import os


logger = logging.getLogger("pdf_converter.ocr")


def get_pdf_page_count(pdf_path: Path) -> int:
    """Get total page count of PDF.
    
    Args:
        pdf_path: Path to PDF file
    
    Returns:
        Number of pages
    """
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))
        return len(reader.pages)
    except Exception as e:
        logger.error(f"Failed to get page count: {e}")
        return 0


def convert_pdf_pages_batch(pdf_path: Path, output_dir: Path, 
                            first_page: int, last_page: int) -> List[Path]:
    """Convert a batch of PDF pages to images.
    
    Args:
        pdf_path: Path to PDF file
        output_dir: Directory to save images
        first_page: First page number (1-indexed)
        last_page: Last page number (1-indexed)
    
    Returns:
        List of image file paths for this batch
    """
    try:
        from pdf2image import convert_from_path
        
        logger.info(f"Converting pages {first_page}-{last_page} to images")
        
        # Convert specific page range (300 DPI for good OCR quality)
        images = convert_from_path(
            str(pdf_path), 
            dpi=300,
            first_page=first_page,
            last_page=last_page
        )
        
        image_paths = []
        for i, image in enumerate(images, start=first_page):
            img_path = output_dir / f"page_{i:04d}.png"
            image.save(str(img_path), "PNG")
            image_paths.append(img_path)
        
        return image_paths
    
    except ImportError:
        logger.error("pdf2image not installed. Install: pip install pdf2image")
        raise
    except Exception as e:
        logger.error(f"Failed to convert pages {first_page}-{last_page}: {e}")
        raise


def ocr_batch_paddleocr(image_paths: List[Path], start_page: int) -> Optional[str]:
    """Perform OCR on a batch of images using PaddleOCR.
    
    Args:
        image_paths: List of image file paths (small batch)
        start_page: Starting page number for logging
    
    Returns:
        Extracted text as string, or None if OCR failed
    """
    try:
        from paddleocr import PaddleOCR
        
        # Initialize PaddleOCR (English only, no angle classification)
        ocr = PaddleOCR(use_angle_cls=False, lang='en')
        
        text_parts = []
        
        for i, img_path in enumerate(image_paths):
            page_num = start_page + i
            logger.info(f"  OCR page {page_num}")
            
            # Note: API changed in newer versions - no cls parameter
            result = ocr.ocr(str(img_path))
            
            if result and result[0]:
                # Extract text from OCR results
                page_text = "\n".join([line[1][0] for line in result[0]])
                text_parts.append(f"--- Page {page_num} ---\n{page_text.strip()}\n")
            else:
                text_parts.append(f"--- Page {page_num} ---\n[No text detected]\n")
        
        if not text_parts:
            return None
        
        return "\n".join(text_parts)
    
    except ImportError:
        logger.error("PaddleOCR not installed. Install: pip install paddleocr")
        raise
    except Exception as e:
        logger.error(f"OCR batch processing failed: {e}")
        return None
