# PDF Text Converter ✅

Convert scanned PDFs to **pure text-only PDFs** (no images, no background).

**RECOMMENDED SCRIPT:** `main-ocrmypdf-reportlab.sh`

## Features

- ✅ **OCR with Tesseract:** Industry-standard English OCR
- ✅ **Pure text-only PDF:** No images, no background (2-3 KB output)
- ✅ **Fast:** ~5-6 seconds per page
- ✅ **Accurate:** Tesseract quality extraction
- ✅ **ReportLab rendering:** Reliable text-to-PDF conversion

## Installation

### 1. Install dependencies

```bash
cd /home/fong/Projects/mini-rag
source venv/bin/activate
pip install paddleocr pdf2image
```

**System dependencies for pdf2image:**
```bash
sudo apt-get install poppler-utils  # Ubuntu/Debian
```

### 2. Verify installation

```bash
python -c "import paddleocr; print('PaddleOCR OK')"
python -c "from pdf2image import convert_from_path; print('pdf2image OK')"
```

## Usage

### Basic usage (run from anywhere):

```bash
# Process single PDF - creates text-only PDF (no images!)
./main-ocrmypdf-reportlab.sh /path/to/scanned.pdf

# Output: /path/to/output-text-pdfs/text-scanned.pdf
```

**What you get:**
- Input: `scanned.pdf` (with images, ~10 MB)
- Output: `text-scanned.pdf` (text-only, ~2-3 KB) ✅

### Direct Python usage:

```bash
cd /home/fong/Projects/mini-rag/pdf-text-converter
source ../venv/bin/activate
python main132feb25-bbe98f8c8221.py input.pdf [output_dir]
```

## Architecture

```
pdf-text-converter/
├── main132feb25-bbe98f8c8221.py    # Main entry point
├── main132feb25-bbe98f8c8221.sh    # Shell wrapper (venv activation)
├── src/
│   ├── utils.py              # Logging, validation (79 LOC)
│   ├── pdf_extractor.py      # Extract text from PDFs (69 LOC)
│   ├── ocr_processor.py      # OCR for scanned PDFs (89 LOC)
│   └── pdf_creator.py        # Create text-only PDFs (95 LOC)
├── logs/                     # Execution logs
└── README.md
```

## Technical Details

### PDF Processing Pipeline

```
Input PDF
    ↓
[Check Text Layer]
    ↓
    ├─ Has Text → Extract Text (PyPDF)
    └─ No Text  → Convert to Images → OCR (PaddleOCR)
    ↓
Create Text-Only PDF (FPDF2)
    ↓
Output PDF (searchable)
```

### OCR Engine

**PaddleOCR** (Recommended for English):
- State-of-the-art accuracy
- Very fast processing
- Lightweight (< 20MB model)
- Optimized for batch processing

### Dependencies

**Core:**
- `pypdf` - PDF text extraction
- `fpdf2` - PDF creation
- `paddleocr` - OCR engine
- `pdf2image` - PDF to image conversion

**Already in requirements.txt:**
- `langchain`, `faiss-cpu`, `tqdm`, `python-dotenv`, `rich`

## Examples

### Convert scanned PDF:

```bash
./main132feb25-bbe98f8c8221.sh scanned_document.pdf
# Output: scanned_document_text.pdf
```

### Convert PDF with text layer:

```bash
./main132feb25-bbe98f8c8221.sh regular_pdf.pdf output/
# Output: output/regular_pdf_text.pdf
```

## Logs

Execution logs saved to: `pdf-text-converter/logs/pdf_converter_YYYYMMDD_HHMMSS.log`

## Performance

| File Type | Size | Processing Time |
|-----------|------|----------------|
| Text PDF (50 pages) | 2MB | ~2-3 seconds |
| Scanned PDF (50 pages) | 10MB | ~30-60 seconds |

**Note:** OCR time depends on image quality and page count.

## Troubleshooting

### Issue: "PaddleOCR not installed"
```bash
pip install paddleocr
```

### Issue: "pdf2image conversion failed"
```bash
sudo apt-get install poppler-utils
```

### Issue: "No text extracted"
- Check if PDF is corrupted
- Try increasing OCR DPI (edit `ocr_processor.py`, line 32)

## Future Enhancements

- [ ] Batch processing (folder input)
- [ ] Vietnamese language support
- [ ] Multiple OCR engines (Tesseract fallback)
- [ ] GUI interface
- [ ] Progress bar for large files

## Author

Created: 2025-10-24  
Project: mini-rag  
Dependencies: PaddleOCR, PyPDF, FPDF2
