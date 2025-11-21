#!/usr/bin/env python3
"""Build per-PDF table of contents artifacts and a merged 0-index.pdf.

Strategy (coarse → fine):
1. Try PDF outlines/bookmarks (fast, structured).
2. Regex scan first N pages (default 12) for TOC-like lines:
   - Dot leaders:  Title .... 123
   - Section numbers: 1.2.3 Title  45
   - Trailing page number with some spacing.
3. Keep all raw candidate lines (broad recall). Refinement can be added later.

Artifacts:
- DKM-PDFs/toc_manifest.json : metadata & cached MD5 to skip unchanged files.
- DKM-PDFs/<md5hash>/index.md : human-readable TOC dump (raw).
- DKM-PDFs/0-index.pdf : merged PDF containing all TOCs.

Idempotent & incremental: only re-extract when file MD5 changed or missing entry.
"""
from __future__ import annotations
import re, json, hashlib, sys, time
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from pypdf import PdfReader
from fpdf import FPDF

# Load environment from .env (portable)
import os, sys
from pathlib import Path


def _load_env_from_ragon_root() -> None:
    """Load .env from RAGON_ROOT."""
    current = Path(__file__).resolve().parent
    for _ in range(3):
        env_file = current / ".env"
        if env_file.exists():
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        key, _, value = line.partition("=")
                        os.environ.setdefault(key.strip(), value.strip().strip('"'))
            break
        current = current.parent


_load_env_from_ragon_root()

VENV_PATH = os.getenv("VENV_PATH", "")
VENV_PY = f"{VENV_PATH}/bin/python" if VENV_PATH else ""
if VENV_PY and os.path.exists(VENV_PY) and os.path.realpath(sys.executable) != os.path.realpath(VENV_PY):
    os.execv(VENV_PY, [VENV_PY, __file__, *sys.argv[1:]])

DKM_PDF_PATH = os.getenv("DKM_PDF_PATH", "")
ROOT = Path(DKM_PDF_PATH) if DKM_PDF_PATH else Path(__file__).resolve().parent.parent / "DKM-PDFs"
MANIFEST_PATH = ROOT / "toc_manifest.json"
PAGES_SCAN = 30  # pages to scan for regex extraction (expanded from 12)

dot_leader_re = re.compile(r"^(.{4,}?)(?:\.{2,}|\s)\s*(\d{1,4})$")
section_number_re = re.compile(r"^(\d+(?:\.\d+)*)([ \t]+)(.{2,}?)[ \t]{2,}(\d{1,4})$")
trailing_page_re = re.compile(r"^(.{4,}?)[ \t]{3,}(\d{1,4})$")

@dataclass
class TocLine:
    title: str
    page: Optional[int]
    source: str  # outline|regex

    def to_dict(self):
        return {"title": self.title, "page": self.page, "source": self.source}


def md5_file(p: Path) -> str:
    h = hashlib.md5()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def load_manifest() -> Dict[str, Any]:
    if MANIFEST_PATH.exists():
        try:
            return json.loads(MANIFEST_PATH.read_text("utf-8"))
        except Exception:
            pass
    return {"version": 1, "generated_at": None, "pdfs": {}}


def save_manifest(data: Dict[str, Any]):
    data["generated_at"] = time.strftime('%Y-%m-%dT%H:%M:%S')
    MANIFEST_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")


def extract_outline(reader: PdfReader) -> List[TocLine]:
    lines: List[TocLine] = []
    try:
        outlines = getattr(reader, 'outlines', None)
        if not outlines:
            return []
        # outlines can be nested; flatten
        def walk(items):
            for it in items:
                if isinstance(it, list):
                    yield from walk(it)
                else:
                    title = getattr(it, 'title', '') or str(it)
                    try:
                        page_obj = reader.get_destination_page_number(it)  # type: ignore
                    except Exception:
                        page_obj = None
                    lines.append(TocLine(title=title.strip(), page=page_obj + 1 if page_obj is not None else None, source="outline"))
        walk(outlines)
    except Exception:
        return []
    return lines


def extract_regex(reader: PdfReader, pages: int) -> List[TocLine]:
    lines: List[TocLine] = []
    max_pages = min(pages, len(reader.pages))
    for i in range(max_pages):
        try:
            text = reader.pages[i].extract_text() or ''
        except Exception:
            continue
        for raw_line in text.splitlines():
            l = raw_line.strip()
            if not l or len(l) < 4:
                continue
            # Avoid huge paragraphs
            if len(l) > 180:
                continue
            m = dot_leader_re.match(l)
            if m:
                title, pg = m.groups()
                lines.append(TocLine(title=title.strip(), page=int(pg), source="regex"))
                continue
            m = section_number_re.match(l)
            if m:
                num, _, rest, pg = m.groups()
                title = f"{num} {rest.strip()}"
                lines.append(TocLine(title=title.strip(), page=int(pg), source="regex"))
                continue
            m = trailing_page_re.match(l)
            if m:
                title, pg = m.groups()
                # Heuristic: ignore if title ends with too many digits (likely false positive)
                if re.search(r"\d{3,}$", title):
                    continue
                lines.append(TocLine(title=title.strip(), page=int(pg), source="regex"))
    # Deduplicate by (title,page)
    uniq = {}
    for tl in lines:
        key = (tl.title, tl.page)
        if key not in uniq:
            uniq[key] = tl
    return list(uniq.values())


def detect_toc_pages(reader: PdfReader, pages: int) -> List[int]:
    """Detect pages likely containing TOC; return zero-based indices and add one extra page after the last block."""
    max_pages = min(pages, len(reader.pages))
    toc_pages: List[int] = []
    for i in range(max_pages):
        try:
            text = reader.pages[i].extract_text() or ''
        except Exception:
            continue
        low = text.lower()
        keyword_hit = ("mục lục" in low) or ("table of contents" in low) or ("contents" in low)
        matches = 0
        for raw_line in text.splitlines():
            l = raw_line.strip()
            if not l or len(l) < 4 or len(l) > 180:
                continue
            if dot_leader_re.match(l) or section_number_re.match(l) or trailing_page_re.match(l):
                matches += 1
        if keyword_hit or matches >= 3:
            toc_pages.append(i)
    # Add spillover: include the page right after the last detected contiguous block
    if toc_pages:
        extra: List[int] = []
        last = None
        for idx in toc_pages:
            if last is not None and idx != last + 1:
                # new block; add spillover for previous block
                spill = last + 1
                if spill < len(reader.pages):
                    extra.append(spill)
            last = idx
        # spill for final block
        if last is not None:
            spill = last + 1
            if spill < len(reader.pages):
                extra.append(spill)
        toc_pages = sorted(set(toc_pages + extra))
    return toc_pages


def collect_page_texts(reader: PdfReader, page_indices: List[int]) -> List[tuple[int, str]]:
    out: List[tuple[int, str]] = []
    for i in sorted(set(page_indices)):
        try:
            txt = reader.pages[i].extract_text() or ''
        except Exception:
            txt = ''
        out.append((i, txt))
    return out


def write_index_md(hash_id: str, pdf_name: str, toc: List[TocLine], page_texts: Optional[List[tuple[int, str]]] = None):
    folder = ROOT / hash_id
    folder.mkdir(exist_ok=True)
    md_path = folder / "index.md"
    lines = [
        f"# TOC: {pdf_name}",
        f"Hash: {hash_id}",
        f"Total lines: {len(toc)}",
        "",
        "| # | Page | Source | Title |",
        "|---|------|--------|-------|",
    ]
    for idx, tl in enumerate(toc, 1):
        page = tl.page if tl.page is not None else ''
        # Escape pipe
        title = tl.title.replace('|', '\\|')
        lines.append(f"| {idx} | {page} | {tl.source} | {title} |")
    if page_texts:
        lines.append("")
        lines.append("## TOC pages content (+ a bit extra)")
        for pg_idx, txt in page_texts:
            lines.append("")
            lines.append(f"### Page {pg_idx + 1}")
            lines.append("")
            lines.append(txt or "")
    md_path.write_text('\n'.join(lines), 'utf-8')


def build_merged_pdf(entries: List[Dict[str, Any]], output: Path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    for entry in entries:
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 14)
        try:
            pdf.cell(0, 10, entry['filename'], ln=1)
            pdf.set_font('Helvetica', '', 10)
            pdf.cell(0, 6, f"Hash: {entry['hash']} | Lines: {len(entry['toc_lines'])} | Strategy: {entry['strategy']}", ln=1)
            pdf.ln(2)
            pdf.set_font('Helvetica', '', 9)
            for i, tl in enumerate(entry['toc_lines'], 1):
                page = tl.get('page') or ''
                source = tl.get('source')
                line = f"{i:03d}. [{page}] ({source}) {tl['title']}"
                # Wrap manually with safe width
                max_w = 150
                while len(line) > 0:
                    segment = line[:max_w]
                    line = line[max_w:]
                    pdf.multi_cell(0, 5, segment)
        except Exception:
            # Skip problematic entries to avoid aborting the whole build
            continue
    try:
        pdf.output(str(output))
    except Exception:
        pass


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build TOC index artifacts")
    parser.add_argument('--force-rebuild', action='store_true', help='Force re-extraction even if hash unchanged')
    parser.add_argument('--pages', type=int, default=30, help='Number of leading pages to scan for TOC')
    args = parser.parse_args()
    global PAGES_SCAN
    PAGES_SCAN = int(args.pages)
    force_rebuild = bool(args.force_rebuild)
    manifest = load_manifest()
    pdf_entries = manifest.setdefault('pdfs', {})
    changed: List[Dict[str, Any]] = []
    all_processed_entries: List[Dict[str, Any]] = []
    pdf_files = sorted([p for p in ROOT.glob('*.pdf')] + [p for p in ROOT.glob('*.PDF')])
    if not pdf_files:
        print("No PDFs found in DKM-PDFs root.")
        return
    for pdf_path in pdf_files:
        try:
            file_hash = md5_file(pdf_path)
        except Exception as e:
            print(f"[SKIP] {pdf_path.name}: hash error {e}")
            continue
        entry = pdf_entries.get(pdf_path.name)
        if entry and entry.get('hash') == file_hash and not force_rebuild:
            # Reuse cached lines but regenerate index.md with full TOC pages content
            try:
                reader = PdfReader(str(pdf_path))
            except Exception:
                reader = None
            toc_dicts = entry.get('toc_lines', [])
            toc_objs = [TocLine(title=d.get('title',''), page=d.get('page'), source=d.get('source','cached')) for d in toc_dicts]
            page_texts = None
            if reader is not None:
                toc_pages = detect_toc_pages(reader, PAGES_SCAN)
                page_texts = collect_page_texts(reader, toc_pages)
            write_index_md(file_hash, pdf_path.name, toc_objs, page_texts)
            # Cleanup old timestamped index files
            for extra in (ROOT / file_hash).glob('index-*.md'):
                if extra.name != 'index.md':
                    try: extra.unlink()
                    except Exception: pass
            # Reuse cached lines
            all_processed_entries.append({
                'filename': pdf_path.name,
                'hash': file_hash,
                'toc_lines': entry['toc_lines'],
                'strategy': entry.get('extraction_strategy', 'cached')
            })
            continue
        # Extract fresh
        try:
            reader = PdfReader(str(pdf_path))
        except Exception as e:
            print(f"[SKIP] {pdf_path.name}: open error {e}")
            continue
        outline_lines = extract_outline(reader)
        regex_lines = extract_regex(reader, PAGES_SCAN)
        combined: List[TocLine] = []
        used_sources = []
        if outline_lines:
            combined.extend(outline_lines)
            used_sources.append('outline')
        if regex_lines:
            combined.extend(regex_lines)
            used_sources.append('regex')
        # Fallback: if nothing, store empty placeholder
        extraction_strategy = '+'.join(used_sources) if used_sources else 'none'
        dict_lines = [tl.to_dict() for tl in combined]
        pdf_entries[pdf_path.name] = {
            'hash': file_hash,
            'updated_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'outline_used': bool(outline_lines),
            'toc_lines': dict_lines,
            'raw_sample_pages': list(range(1, min(PAGES_SCAN, len(reader.pages)) + 1)),
            'extraction_strategy': extraction_strategy,
            'version': 1
        }
        toc_pages = detect_toc_pages(reader, PAGES_SCAN)
        page_texts = collect_page_texts(reader, toc_pages)
        write_index_md(file_hash, pdf_path.name, combined, page_texts)
        # Cleanup old timestamped index files
        for extra in (ROOT / file_hash).glob('index-*.md'):
            if extra.name != 'index.md':
                try: extra.unlink()
                except Exception: pass
        all_processed_entries.append({
            'filename': pdf_path.name,
            'hash': file_hash,
            'toc_lines': dict_lines,
            'strategy': extraction_strategy
        })
        changed.append(pdf_entries[pdf_path.name])
        print(f"[OK] {pdf_path.name}: {len(dict_lines)} lines ({extraction_strategy}); TOC pages: {','.join(str(p+1) for p in toc_pages) if toc_pages else 'none'}")
    save_manifest(manifest)
    try:
        build_merged_pdf(all_processed_entries, ROOT / '0-index.pdf')
        print(f"Generated 0-index.pdf with {len(all_processed_entries)} documents.")
    except Exception:
        print("Merged PDF generation skipped due to rendering errors.")

if __name__ == '__main__':
    main()
