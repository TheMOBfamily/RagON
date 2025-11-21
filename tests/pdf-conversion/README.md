# PDF to Text to PDF Conversion Utilities

Convert PDFs to plain text and back to clean text-only PDFs with `text-*` prefix.

## Quick Start

```bash
# 1. Edit PDF list in batch script
nano tests/pdf-conversion/batch_convert_pdfs.py

# 2. Run conversion
source venv/bin/activate
python tests/pdf-conversion/batch_convert_pdfs.py

# 3. Check outputs in PDFs/ directory
ls -lh PDFs/text-*.pdf
```

## Scripts

### batch_convert_pdfs.py (Main Script)
Batch process multiple PDFs with progress tracking and summary.

**Features**:
- Fast extraction using `pdftotext`
- Progress bar with Rich
- Summary table
- Error handling per file

### txt_to_pdf.py
Convert single text file to PDF.

### convert_pdf_to_text_pdf.py
All-in-one PDF → text → PDF pipeline.

## Text Cleaning

Removes problematic characters:
- Form feed (␌) → newline
- Control characters → removed
- Long lines (>150 chars) → auto-split

## Dependencies

**Python**: `pypdf`, `fpdf2`, `rich`
**System**: `pdftotext` (install: `sudo apt install poppler-utils`)

## Output Format

- Font: Courier 7pt
- Text-only (no images/formatting)
- Prefix: `text-*`
- Very small file size (~99% compression)

## Example Results

| Original | Text   | Output | Ratio  |
|----------|--------|--------|--------|
| 70 MB    | 1.6 MB | 154 KB | 99.8%  |
| 22 MB    | 1.8 MB | 193 KB | 99.1%  |

## Use Cases

- RAG/embedding systems (clean text input)
- Text analysis (remove visual noise)
- Archival (minimal storage)

## See Also

- Detailed docs: `.memory` file in this directory
- Main RAG project: `../../CLAUDE.md`
