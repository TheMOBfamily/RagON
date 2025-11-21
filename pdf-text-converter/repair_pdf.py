#!/usr/bin/env python3
"""
PDF Repair Utility - Fix problematic PDFs before OCR
Handles Ghostscript errors like 'rangecheck in setscreen'
"""

import sys
import subprocess
from pathlib import Path
import tempfile
import shutil
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def repair_pdf_with_ghostscript(input_pdf: Path, output_pdf: Path) -> bool:
    """
    Repair PDF using Ghostscript by rasterizing and rebuilding.
    This normalizes the PDF and removes problematic operators and metadata.

    Args:
        input_pdf: Path to problematic PDF
        output_pdf: Path to save repaired PDF

    Returns:
        True if successful, False otherwise
    """
    try:
        # Method 1: Direct PDF to PDF conversion with safer settings
        logger.info(f"Attempting repair with Ghostscript (method 1: direct conversion)...")
        gs_cmd = [
            'gs',
            '-dSAFER',
            '-dBATCH',
            '-dNOPAUSE',
            '-dNOCACHE',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',  # PDF 1.4 for better compatibility
            '-dPDFSETTINGS=/prepress',   # High quality
            '-dEmbedAllFonts=true',
            '-dSubsetFonts=false',
            '-dAutoRotatePages=/None',
            '-dColorConversionStrategy=/LeaveColorUnchanged',
            '-dDownsampleMonoImages=false',
            '-dDownsampleGrayImages=false',
            '-dDownsampleColorImages=false',
            '-dFIXEDMEDIA',  # Ignore page size in PDF
            '-dPDFFitPage',  # Fit pages
            f'-sOutputFile={output_pdf}',
            str(input_pdf)
        ]

        result = subprocess.run(gs_cmd, capture_output=True, text=True)

        if result.returncode == 0 and output_pdf.exists() and output_pdf.stat().st_size > 0:
            # Verify it can be rasterized
            if verify_pdf_can_rasterize(output_pdf):
                logger.info(f"✓ Method 1 succeeded: {output_pdf}")
                return True
            else:
                logger.warning("Method 1 produced PDF but it still can't rasterize")

        # Method 2: Rasterize to images and rebuild (aggressive fix)
        logger.info(f"Trying method 2 (rasterize → rebuild)...")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)

            # Step 1: Rasterize all pages to high-res PNGs (300 DPI)
            logger.info("  Step 1: Rasterizing to images at 300 DPI...")
            png_pattern = temp_dir_path / "page_%03d.png"

            rasterize_cmd = [
                'gs',
                '-dSAFER',
                '-dBATCH',
                '-dNOPAUSE',
                '-sDEVICE=png16m',
                '-r300',  # 300 DPI for good quality
                '-dTextAlphaBits=4',
                '-dGraphicsAlphaBits=4',
                f'-sOutputFile={png_pattern}',
                str(input_pdf)
            ]

            result = subprocess.run(rasterize_cmd, capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                logger.error(f"Rasterization failed: {result.stderr}")
                return False

            # Count generated PNGs
            png_files = sorted(temp_dir_path.glob("page_*.png"))
            logger.info(f"  Generated {len(png_files)} PNG images")

            if not png_files:
                logger.error("No images generated!")
                return False

            # Step 2: Rebuild PDF from images
            logger.info("  Step 2: Rebuilding PDF from images...")
            rebuild_cmd = [
                'gs',
                '-dSAFER',
                '-dBATCH',
                '-dNOPAUSE',
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.4',
                '-dPDFSETTINGS=/prepress',
                '-sColorConversionStrategy=RGB',
                '-dAutoRotatePages=/None',
                f'-sOutputFile={output_pdf}'
            ] + [str(f) for f in png_files]

            result = subprocess.run(rebuild_cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0 and output_pdf.exists() and output_pdf.stat().st_size > 0:
                logger.info(f"✓ Method 2 succeeded: {output_pdf}")
                return True
            else:
                logger.error(f"Rebuild failed: {result.stderr}")
                return False

    except Exception as e:
        logger.error(f"Repair failed with exception: {e}")
        return False


def verify_pdf_can_rasterize(pdf_path: Path) -> bool:
    """
    Verify if PDF can be rasterized at high resolution (300 DPI).

    Returns:
        True if rasterization succeeds, False otherwise
    """
    try:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_png:
            temp_png_path = Path(temp_png.name)

        try:
            test_cmd = [
                'gs',
                '-dSAFER',
                '-dBATCH',
                '-dNOPAUSE',
                '-sDEVICE=png16m',
                '-dFirstPage=1',
                '-dLastPage=1',
                '-r300',  # Test at OCR resolution
                f'-sOutputFile={temp_png_path}',
                str(pdf_path)
            ]

            result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=10)
            return result.returncode == 0

        finally:
            temp_png_path.unlink(missing_ok=True)

    except Exception:
        return False


def check_pdf_needs_repair(pdf_path: Path) -> bool:
    """
    Quick test if PDF can be rasterized by Ghostscript at OCR resolution.

    Returns:
        True if PDF needs repair, False if it's OK
    """
    try:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_png:
            temp_png_path = Path(temp_png.name)

        try:
            # Try to rasterize first page at 300 DPI (OCR resolution)
            test_cmd = [
                'gs',
                '-dSAFER',
                '-dBATCH',
                '-dNOPAUSE',
                '-sDEVICE=png16m',
                '-dFirstPage=1',
                '-dLastPage=1',
                '-r300',  # Test at OCR resolution
                f'-sOutputFile={temp_png_path}',
                str(pdf_path)
            ]

            result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                logger.info("✓ PDF is OK, no repair needed")
                return False
            else:
                logger.warning(f"✗ PDF has issues: {result.stderr[:200]}")
                return True

        finally:
            temp_png_path.unlink(missing_ok=True)

    except Exception as e:
        logger.warning(f"Check failed, assuming repair needed: {e}")
        return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python repair_pdf.py <input.pdf> [output.pdf]")
        print("       If output not specified, creates '<input>-repaired.pdf'")
        sys.exit(1)

    input_pdf = Path(sys.argv[1]).resolve()

    if not input_pdf.exists():
        logger.error(f"File not found: {input_pdf}")
        sys.exit(1)

    # Determine output path
    if len(sys.argv) >= 3:
        output_pdf = Path(sys.argv[2]).resolve()
    else:
        output_pdf = input_pdf.parent / f"{input_pdf.stem}-repaired.pdf"

    logger.info(f"Input:  {input_pdf}")
    logger.info(f"Output: {output_pdf}")
    logger.info(f"Size:   {input_pdf.stat().st_size / 1024 / 1024:.2f} MB")

    # Check if repair is needed
    logger.info("\n=== Checking if repair is needed ===")
    needs_repair = check_pdf_needs_repair(input_pdf)

    if not needs_repair:
        logger.info("PDF is already compatible, copying to output...")
        shutil.copy2(input_pdf, output_pdf)
        logger.info(f"✓ Done: {output_pdf}")
        sys.exit(0)

    # Perform repair
    logger.info("\n=== Starting repair ===")
    success = repair_pdf_with_ghostscript(input_pdf, output_pdf)

    if success:
        original_size = input_pdf.stat().st_size / 1024 / 1024
        repaired_size = output_pdf.stat().st_size / 1024 / 1024
        logger.info(f"\n✓ SUCCESS!")
        logger.info(f"  Original: {original_size:.2f} MB")
        logger.info(f"  Repaired: {repaired_size:.2f} MB")
        logger.info(f"  Saved to: {output_pdf}")
        sys.exit(0)
    else:
        logger.error(f"\n✗ FAILED to repair {input_pdf}")
        sys.exit(1)


if __name__ == "__main__":
    main()
