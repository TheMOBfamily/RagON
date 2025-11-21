# Tool: Update PDF Metadata

Update `manifest.json` và `metadata.json` sau khi rename PDF files.

## Usage

```bash
cd /home/fong/Projects/mini-rag/tool-update-pdf-metadata
python3 update_pdf_metadata.py
```

**That's it.** No parameters needed. Script auto-scans `/home/fong/Projects/mini-rag/DKM-PDFs/`

## What it does

1. Scans all PDFs in `DKM-PDFs/`
2. For each PDF: calculates MD5 → finds hash folder → updates manifest.json + metadata.json
3. Skips if filename unchanged

## Example

Rename: `Advanced-Machine-Learning.pdf` → `2016-Advanced-Machine-Learning-John-Hearty-Packt.PDF`

Run: `python3 update_pdf_metadata.py`

Result:
- `manifest.json` key updated
- `metadata.json` filename updated

Done.
