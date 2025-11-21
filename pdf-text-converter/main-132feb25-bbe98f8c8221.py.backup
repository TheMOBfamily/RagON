#!/usr/bin/env python3
"""PDF Text Converter - Batch processing with text layer detection

Automatically detects if PDF has text layer:
- If text layer exists → extract directly (fast, no OCR)
- If scanned → OCR with batch processing

Usage:
    ./main-convert-scanned-pdf-text-pdf-bbe98f8c8221.sh [input.pdf|folder]
    Default folder: /home/fong/Projects/mini-rag/PDFs/scanned/
"""
from __future__ import annotations
import sys
import ocrmypdf
from pathlib import Path
from pypdf import PdfReader, PdfWriter
import tempfile
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import hashlib

sys.path.insert(0, str(Path(__file__).parent / "src"))
from utils import setup_logging, format_file_size
from pdf_sanitizer import try_remove_pdf_annotations


def safe_filename(filename: str, max_length: int = 200) -> str:
    """Truncate filename to safe length, preserve extension + hash for uniqueness.

    Linux filesystem limit: 255 bytes
    Safety buffer: use 200 to leave room for prefix "text-"

    Example:
        Input:  "Unknown-scanned-How-To-Write-Your-First-Thesis-...-scann.PDF" (250 chars)
        Output: "Unknown-scanned-How-To-Write-Your-First-The...-a1b2c3d4.PDF" (200 chars)

    Args:
        filename: Original filename
        max_length: Max safe length (default 200)

    Returns:
        Truncated filename with hash
    """
    if len(filename) <= max_length:
        return filename

    # Split name and extension
    stem = Path(filename).stem  # "file.tar.gz" -> "file.tar"
    ext = "".join(Path(filename).suffixes)  # ".tar.gz"

    # Calculate hash of original name (for uniqueness)
    file_hash = hashlib.md5(filename.encode()).hexdigest()[:8]

    # Reserve space for: extension + hash + separator
    reserved = len(ext) + 8 + 4  # ".PDF" + "-" + "a1b2c3d4" + "..."
    available = max_length - reserved

    # Truncate stem and add hash
    truncated = stem[:available] + "...-" + file_hash + ext

    return truncated


def has_text_layer(pdf_path: Path, logger, sample_pages: int = 3) -> bool:
    """Check if PDF has extractable text layer.

    Samples first N pages and checks if text content is sufficient.
    Threshold: >50 chars per page on average → has text layer

    Args:
        pdf_path: Input PDF
        sample_pages: Number of pages to sample (default 3)

    Returns:
        True if PDF has text layer, False if scanned
    """
    try:
        reader = PdfReader(str(pdf_path))
        total_pages = len(reader.pages)
        check_pages = min(sample_pages, total_pages)

        total_chars = 0
        for i in range(check_pages):
            text = reader.pages[i].extract_text() or ""
            total_chars += len(text.strip())

        avg_chars = total_chars / check_pages
        has_text = avg_chars > 50  # Threshold: >50 chars/page

        logger.info(f"  Text layer check: {total_chars} chars in {check_pages} pages")
        logger.info(f"  Average: {avg_chars:.0f} chars/page → {'✓ HAS TEXT' if has_text else '✗ SCANNED'}")

        return has_text

    except Exception as e:
        logger.warning(f"  Text layer check failed: {e}")
        return False  # Assume scanned if check fails


def extract_text_only(pdf_path: Path, logger) -> str:
    """Extract text from PDF with text layer (no OCR needed).

    Args:
        pdf_path: Input PDF

    Returns:
        Extracted text
    """
    reader = PdfReader(str(pdf_path))
    texts = []
    errors = 0

    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
            if text.strip():
                texts.append(f"=== Page {i} ===\n\n{text}\n\n")
        except Exception as e:
            errors += 1
            logger.warning(f"  ⚠️ Page {i} extract failed: {e}, skipping...")
            continue
    
    if errors > 0:
        logger.info(f"  ⚠️ Skipped {errors} corrupted pages, extracted {len(texts)} pages successfully")

    return "".join(texts)


def ocr_pdf_pages(pdf_path: Path, start_page: int, end_page: int, logger) -> str:
    """OCR specific page range.
    
    Args:
        pdf_path: Input PDF
        start_page: Start page (1-indexed)
        end_page: End page (1-indexed)
    
    Returns:
        Extracted text
    """
    logger.info(f"  OCR pages {start_page}-{end_page}...")
    
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_in:
        temp_input = Path(tmp_in.name)
    
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_out:
        temp_output = Path(tmp_out.name)
    
    # Extract page range to temp PDF
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    
    for i in range(start_page - 1, min(end_page, len(reader.pages))):
        writer.add_page(reader.pages[i])
    
    with open(temp_input, 'wb') as f:
        writer.write(f)
    
    # Sanitize PDF trước OCR (xóa annotations/bookmarks hỏng)
    sanitized_input = try_remove_pdf_annotations(temp_input, logger)
    
    # OCR the batch (skip if text layer exists)
    # Add oversample=300 to force consistent DPI and avoid metadata issues
    # skip_text=True → auto-skip pages with text layer (for hybrid PDFs)
    try:
        ocrmypdf.ocr(sanitized_input, temp_output, language="eng",
                    progress_bar=False, deskew=False,
                    skip_text=True,  # ← Skip pages with text layer (no error if text exists)
                    oversample=300,  # Force 300 DPI resolution to avoid DPI detection issues
                    pdfa_image_compression='lossless')
    except Exception as e:
        # Fallback: skip PDF/A conversion nếu Ghostscript lỗi
        logger.warning(f"  ⚠️ PDF/A conversion failed, trying without PDF/A...")
        ocrmypdf.ocr(sanitized_input, temp_output, language="eng",
                    progress_bar=False, deskew=False,
                    skip_text=True,
                    oversample=300,
                    output_type='pdf')  # Plain PDF, không dùng PDF/A
    finally:
        # Cleanup sanitized temp file
        if sanitized_input != temp_input:
            sanitized_input.unlink(missing_ok=True)
    
    # Extract text
    reader2 = PdfReader(str(temp_output))
    texts = []
    for i, page in enumerate(reader2.pages):
        text = page.extract_text() or ""
        if text.strip():
            texts.append(f"=== Page {start_page + i} ===\n\n{text}\n\n")
    
    # Cleanup
    temp_input.unlink(missing_ok=True)
    temp_output.unlink(missing_ok=True)
    
    return "".join(texts)


def create_text_pdf_batch(text: str, output_path: Path, append: bool = False) -> bool:
    """Create or append text to PDF file.
    
    Args:
        text: Text to add
        output_path: Output PDF path
        append: If True, merge with existing PDF
    """
    # Create temp PDF with this batch's text
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        temp_pdf = Path(tmp.name)
    
    c = canvas.Canvas(str(temp_pdf), pagesize=letter)
    c.setFont("Helvetica", 9)
    
    width, height = letter
    y = height - inch
    
    for line in text.split('\n'):
        if y < inch:
            c.showPage()
            c.setFont("Helvetica", 9)
            y = height - inch
        
        c.drawString(50, y, line.strip())
        y -= 12
    
    c.save()
    
    # Merge or copy
    if append and output_path.exists():
        # Merge with existing
        writer = PdfWriter()
        
        # Add existing pages
        reader_existing = PdfReader(str(output_path))
        for page in reader_existing.pages:
            writer.add_page(page)
        
        # Add new pages
        reader_new = PdfReader(str(temp_pdf))
        for page in reader_new.pages:
            writer.add_page(page)
        
        # Save merged
        with open(output_path, 'wb') as f:
            writer.write(f)
    else:
        # First batch - just copy
        import shutil
        shutil.copy(temp_pdf, output_path)
    
    temp_pdf.unlink(missing_ok=True)
    return True


def process_pdf(pdf_path: Path, output_dir: Path, logger, batch_size: int = 30) -> bool:
    """Process PDF - auto-detect text layer and choose extraction method."""
    try:
        # ✅ Fix 1: Validate file exists BEFORE processing (NON-FATAL, just skip)
        if not pdf_path.exists():
            logger.warning(f"⚠️  SKIP: File not found: {pdf_path.name}")
            logger.warning(f"   (Non-fatal error, continuing with next file...)\n")
            return False  # Skip this file, but continue batch processing

        logger.info(f"Processing: {pdf_path.name}")
        logger.info(f"Size: {format_file_size(pdf_path.stat().st_size)}")

        # Get page count
        reader = PdfReader(str(pdf_path))
        total_pages = len(reader.pages)
        logger.info(f"Total pages: {total_pages}")

        # ✅ Fix 2: Truncate long filename BEFORE creating output path
        safe_name = safe_filename(pdf_path.name, max_length=200)
        output_filename = f"text-{safe_name}"
        output_path = output_dir / output_filename

        # Log if filename was truncated (NON-FATAL, just warn)
        if safe_name != pdf_path.name:
            logger.warning(f"  ⚠️  Filename too long ({len(pdf_path.name)} chars)")
            logger.warning(f"     Auto-truncated to: {safe_name}")

        # Remove old output if exists (now safe, path length validated)
        try:
            output_path.unlink(missing_ok=True)
        except OSError as e:
            logger.warning(f"  ⚠️  Cannot delete old output: {e} (continuing anyway...)")

        # Check if PDF has text layer
        if has_text_layer(pdf_path, logger):
            logger.info("📄 PDF has text layer → Direct extraction (no OCR)\n")

            # Fast path: direct text extraction
            start_time = time.time()
            extracted_text = extract_text_only(pdf_path, logger)

            if not extracted_text.strip():
                logger.warning("No text extracted, falling back to OCR")
                # Fall through to OCR path below
            else:
                # Create PDF from extracted text
                create_text_pdf_batch(extracted_text, output_path, append=False)

                elapsed = time.time() - start_time
                logger.info(f"✅ SUCCESS (Direct extraction in {elapsed:.1f}s)")
                logger.info(f"   Output: {output_path.name}")
                logger.info(f"   Size: {format_file_size(output_path.stat().st_size)}")
                logger.info(f"   Text: {len(extracted_text):,} characters")
                return True

        # OCR path (for scanned PDFs)
        logger.info("🔍 Scanned PDF detected → OCR processing")
        logger.info(f"Batch size: {batch_size} pages\n")
        
        # Process in batches
        for start in range(1, total_pages + 1, batch_size):
            end = min(start + batch_size - 1, total_pages)
            
            logger.info(f"Batch {start}-{end}/{total_pages}:")
            
            # Step 1: OCR this batch
            start_time = time.time()
            batch_text = ocr_pdf_pages(pdf_path, start, end, logger)
            
            if not batch_text.strip():
                logger.warning(f"  No text in batch {start}-{end}")
                continue
            
            logger.info(f"  Extracted: {len(batch_text)} chars")
            
            # Step 2: Append to PDF
            is_first = (start == 1)
            create_text_pdf_batch(batch_text, output_path, append=not is_first)
            
            elapsed = time.time() - start_time
            current_size = output_path.stat().st_size if output_path.exists() else 0
            
            logger.info(f"  ✓ Saved (batch took {elapsed:.1f}s)")
            logger.info(f"  ✓ Current PDF: {format_file_size(current_size)}\n")
        
        # Final verification
        if output_path.exists():
            reader_final = PdfReader(str(output_path))
            total_chars = sum(len(p.extract_text() or "") for p in reader_final.pages)
            
            logger.info(f"✅ SUCCESS!")
            logger.info(f"   Output: {output_path.name}")
            logger.info(f"   Size: {format_file_size(output_path.stat().st_size)}")
            logger.info(f"   Pages: {len(reader_final.pages)}")
            logger.info(f"   Text: {total_chars:,} characters")
            return True
        
        return False

    except Exception as e:
        # ✅ NON-FATAL: Catch all errors, log and continue with next file
        logger.error(f"❌ Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        logger.warning(f"⚠️  Skipping this file, continuing batch processing...\n")
        return False  # Mark as failed, but don't crash the entire batch


def main():
    logger = setup_logging(log_dir=str(Path(__file__).parent / "logs"))

    # Default folder if no argument provided
    default_folder = Path("/home/fong/Projects/mini-rag/PDFs/scanned")

    try:
        if len(sys.argv) < 2:
            # Use default folder
            input_path = default_folder
            logger.info(f"No argument provided, using default folder:")
            logger.info(f"  {input_path}\n")
        else:
            input_path = Path(sys.argv[1]).resolve()

        if not input_path.exists():
            logger.error(f"Not found: {input_path}")
            sys.exit(1)

        # Check if input is folder or single file
        if input_path.is_dir():
            # Folder mode: process all PDFs
            pdf_files = sorted(input_path.glob("*.pdf")) + sorted(input_path.glob("*.PDF"))

            if not pdf_files:
                logger.warning(f"No PDF files found in: {input_path}")
                sys.exit(1)

            logger.info(f"Found {len(pdf_files)} PDF files in folder\n")
            logger.info("=" * 70)

            output_dir = input_path / "output-text-pdfs"
            output_dir.mkdir(exist_ok=True)

            success_count = 0
            failed_files = []

            for idx, pdf_path in enumerate(pdf_files, start=1):
                logger.info(f"\n[{idx}/{len(pdf_files)}] Processing: {pdf_path.name}")
                logger.info("=" * 70)

                if process_pdf(pdf_path, output_dir, logger):
                    success_count += 1
                else:
                    failed_files.append(pdf_path.name)

            # Summary
            logger.info("\n" + "=" * 70)
            logger.info("BATCH PROCESSING SUMMARY")
            logger.info("=" * 70)
            logger.info(f"Total files: {len(pdf_files)}")
            logger.info(f"✅ Success: {success_count}")
            logger.info(f"❌ Failed: {len(failed_files)}")

            if failed_files:
                logger.info("\n⚠️  Failed files (non-fatal, skipped):")
                for fname in failed_files:
                    logger.info(f"  - {fname}")
                logger.info("\nNote: Failed files were skipped, batch processing completed.")

            # Exit 0 if all success, exit 1 if some failed (for CI/CD awareness)
            sys.exit(0 if len(failed_files) == 0 else 1)

        else:
            # Single file mode
            output_dir = input_path.parent / "output-text-pdfs"
            output_dir.mkdir(exist_ok=True)

            if process_pdf(input_path, output_dir, logger):
                sys.exit(0)
            else:
                sys.exit(1)

    except Exception as e:
        logger.error(f"Fatal: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
