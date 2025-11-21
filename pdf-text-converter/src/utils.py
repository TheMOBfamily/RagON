"""Utility functions for PDF text converter."""
from __future__ import annotations
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """Setup logging configuration."""
    Path(log_dir).mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/pdf_converter_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("pdf_converter")


def validate_pdf_path(pdf_path: str) -> Path:
    """Validate PDF file path exists and is a PDF."""
    p = Path(pdf_path)
    
    if not p.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    if not p.is_file():
        raise ValueError(f"Path is not a file: {pdf_path}")
    
    if p.suffix.lower() != ".pdf":
        raise ValueError(f"File is not a PDF: {pdf_path}")
    
    return p


def create_output_path(input_path: Path, output_dir: Optional[str] = None, 
                       suffix: str = "_text") -> Path:
    """Create output file path for converted PDF.
    
    Args:
        input_path: Original PDF path
        output_dir: Optional output directory (default: same as input)
        suffix: Suffix to add to filename (default: "_text")
    
    Returns:
        Path object for output file
    """
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = input_path.parent
    
    # Create output filename: original_name_text.pdf
    output_name = f"{input_path.stem}{suffix}.pdf"
    return out_dir / output_name


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"
