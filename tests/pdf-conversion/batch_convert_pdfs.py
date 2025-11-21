#!/usr/bin/env python3
"""Batch convert PDFs to text and then to new PDFs with 'text-*' prefix."""

import os
import subprocess
from pathlib import Path

# Load .env from RagON root
def _load_env():
    current = Path(__file__).resolve().parent
    for _ in range(4):
        env_file = current / ".env"
        if env_file.exists():
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        os.environ.setdefault(k.strip(), v.strip().strip('"'))
            break
        current = current.parent

_load_env()
RAGON_ROOT = os.getenv("RAGON_ROOT", "/home/fong/Projects/RagON")
from fpdf import FPDF
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table

console = Console()


def clean_text(text: str) -> str:
    """Remove special characters that may cause issues in PDF."""
    # Remove form feed and other problematic control characters
    text = text.replace('\f', '\n')  # Form feed ␌ -> newline
    text = text.replace('\v', '\n')  # Vertical tab -> newline
    text = text.replace('\r\n', '\n')  # Windows line endings
    text = text.replace('\r', '\n')  # Old Mac line endings

    # Remove other control characters except newline and tab
    # Keep printable chars + \n + \t
    text = ''.join(char for char in text if char == '\n' or char == '\t' or (ord(char) >= 32 and ord(char) < 127) or ord(char) >= 128)

    return text


def extract_text_from_pdf(pdf_path: Path) -> Path:
    """Extract text from PDF using pdftotext command."""
    txt_path = pdf_path.with_suffix('.txt')

    console.print(f"[cyan]Extracting text: {pdf_path.name}[/cyan]")

    # Use pdftotext command
    result = subprocess.run(
        ['pdftotext', str(pdf_path), str(txt_path)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        console.print(f"[red]Error extracting {pdf_path.name}[/red]")
        return None

    if txt_path.exists():
        size_mb = txt_path.stat().st_size / (1024 * 1024)
        console.print(f"[green]✓ Extracted {size_mb:.1f} MB[/green]")
        return txt_path

    return None


def convert_text_to_pdf(text_path: Path) -> Path:
    """Convert text file to PDF."""
    # Output PDF with 'text-' prefix
    pdf_path = text_path.parent / f"text-{text_path.stem}.pdf"

    console.print(f"[cyan]Converting to PDF: {text_path.name}[/cyan]")

    # Read and clean text
    text = text_path.read_text(encoding='utf-8', errors='ignore')
    text = clean_text(text)

    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Courier", size=7)

    lines = text.split('\n')

    for line in lines:
        if line.strip():
            try:
                # Limit line length to prevent issues
                max_line_len = 150
                if len(line) > max_line_len:
                    # Split long lines
                    for j in range(0, len(line), max_line_len):
                        chunk = line[j:j+max_line_len]
                        pdf.multi_cell(0, 3.5, chunk, align='L')
                else:
                    pdf.multi_cell(0, 3.5, line, align='L')
            except Exception:
                # Skip problematic lines silently
                pass
        else:
            pdf.ln(3.5)

    pdf.output(str(pdf_path))

    if pdf_path.exists():
        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        console.print(f"[green]✓ Created PDF {size_mb:.1f} MB[/green]")
        return pdf_path

    return None


def main():
    # List of PDFs to process (using env var)
    pdf_dir = Path(RAGON_ROOT) / "PDFs"
    pdf_files = [
        pdf_dir / "2019-Hands-On-Machine-Learning-with-Scikit-Learn-Keras-and-TensorFlow_-Concepts-Tools-and-Techniques-to-Build-Intelligent-Systems-Aurélien-Géron-OReilly.PDF",
        pdf_dir / "2022-Natural-Language-Processing-with-Transformers_-Building-Language-Applications-with-Hugging-Face-Lewis-Tunstall-Leandro-von-Werra-Thomas-Wolf.PDF",
        pdf_dir / "2023-Generative-Deep-Learning_-Teaching-Machines-To-Paint-Write-Compose-and-Play-David-Foster-OReilly.PDF",
    ]

    console.print("\n[bold cyan]Batch PDF to Text to PDF Conversion[/bold cyan]")
    console.print(f"Processing {len(pdf_files)} files\n")

    results = []

    for i, pdf_path in enumerate(pdf_files, 1):
        console.print(f"\n[bold yellow]═══ File {i}/{len(pdf_files)} ═══[/bold yellow]")
        console.print(f"Source: {pdf_path.name}\n")

        if not pdf_path.exists():
            console.print(f"[red]✗ File not found: {pdf_path}[/red]")
            results.append({
                'file': pdf_path.name,
                'status': 'Not found',
                'txt_size': '-',
                'pdf_size': '-'
            })
            continue

        # Extract text
        txt_path = extract_text_from_pdf(pdf_path)
        if not txt_path:
            results.append({
                'file': pdf_path.name,
                'status': 'Extract failed',
                'txt_size': '-',
                'pdf_size': '-'
            })
            continue

        # Convert to PDF
        output_pdf = convert_text_to_pdf(txt_path)
        if not output_pdf:
            results.append({
                'file': pdf_path.name,
                'status': 'Convert failed',
                'txt_size': f"{txt_path.stat().st_size / (1024*1024):.1f} MB",
                'pdf_size': '-'
            })
            continue

        results.append({
            'file': pdf_path.name,
            'status': 'Success',
            'txt_size': f"{txt_path.stat().st_size / (1024*1024):.1f} MB",
            'pdf_size': f"{output_pdf.stat().st_size / (1024*1024):.1f} MB"
        })

    # Display summary table
    console.print("\n[bold cyan]═══ Summary ═══[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("File", style="cyan", no_wrap=False, max_width=50)
    table.add_column("Status", style="green")
    table.add_column("Text Size", justify="right")
    table.add_column("PDF Size", justify="right")

    for result in results:
        status_style = "green" if result['status'] == 'Success' else "red"
        table.add_row(
            result['file'],
            f"[{status_style}]{result['status']}[/{status_style}]",
            result['txt_size'],
            result['pdf_size']
        )

    console.print(table)
    console.print("\n[bold green]✓ Batch conversion complete![/bold green]\n")


if __name__ == "__main__":
    main()
