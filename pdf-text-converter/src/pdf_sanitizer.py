#!/usr/bin/env python3
"""PDF Sanitizer - Remove problematic annotations/bookmarks before OCR

Xử lý các vấn đề:
- Annotations trỏ tới trang không tồn tại
- Bookmarks/outline bị hỏng
- Metadata gây lỗi Ghostscript

SOLID: Single Responsibility - chỉ làm sạch PDF trước OCR
"""
from __future__ import annotations
from pathlib import Path
from pypdf import PdfReader, PdfWriter
import tempfile


def sanitize_pdf(input_path: Path, logger) -> Path:
    """Loại bỏ annotations/bookmarks có thể gây lỗi Ghostscript.
    
    Args:
        input_path: PDF gốc
        logger: Logger instance
        
    Returns:
        Path tới PDF đã sanitize (temp file)
    """
    try:
        reader = PdfReader(str(input_path))
        writer = PdfWriter()
        
        # Copy pages (không copy annotations)
        for page in reader.pages:
            new_page = writer.add_page(page)
            # Xóa annotations nếu có
            if '/Annots' in new_page:
                del new_page['/Annots']
        
        # Không copy outline/bookmarks (tự động skip)
        # Không copy metadata form fields
        
        # Ghi ra temp file
        temp_fd, temp_path = tempfile.mkstemp(suffix='.pdf', prefix='sanitized_')
        with open(temp_path, 'wb') as f:
            writer.write(f)
        
        logger.info(f"  🧹 Sanitized PDF → {Path(temp_path).name}")
        return Path(temp_path)
        
    except Exception as e:
        logger.warning(f"  ⚠️ Sanitize failed: {e}, using original")
        return input_path


def try_remove_pdf_annotations(pdf_path: Path, logger) -> Path:
    """Wrapper với error handling.
    
    Returns original path nếu sanitize thất bại.
    """
    try:
        return sanitize_pdf(pdf_path, logger)
    except Exception:
        return pdf_path
