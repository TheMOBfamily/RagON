#!/usr/bin/env python3
"""Convert text file to PDF using fpdf2."""

import os
import re
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
from rich.progress import Progress, SpinnerColumn, TextColumn

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


def convert_text_to_pdf(text_path: Path, pdf_path: Path) -> None:
    """Convert text file to PDF."""
    console.print(f"\n[cyan]Reading text file: {text_path.name}[/cyan]")

    # Read text file
    text = text_path.read_text(encoding='utf-8')
    console.print(f"[green]Read {len(text):,} characters[/green]")

    # Clean text
    console.print(f"[cyan]Cleaning special characters...[/cyan]")
    text = clean_text(text)
    console.print(f"[green]Cleaned {len(text):,} characters[/green]")

    console.print(f"\n[cyan]Creating PDF: {pdf_path.name}[/cyan]")

    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Courier", size=7)  # Smaller font to fit more content

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Building PDF...", total=None)

        lines = text.split('\n')
        total_lines = len(lines)

        for i, line in enumerate(lines, 1):
            if i % 500 == 0:
                progress.update(task, description=f"Processing {i:,}/{total_lines:,} lines")

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
                except Exception as e:
                    # Skip problematic lines silently
                    pass
            else:
                pdf.ln(3.5)

        progress.update(task, description="Saving PDF...")
        pdf.output(str(pdf_path))

    pdf_size = pdf_path.stat().st_size / (1024 * 1024)
    console.print(f"\n[bold green]✓ PDF created successfully![/bold green]")
    console.print(f"Size: {pdf_size:.1f} MB")


def main():
    # Use env var for path
    pdf_dir = Path(RAGON_ROOT) / "PDFs"
    txt_file = pdf_dir / "2018-Reinforcement-Learning_-An-Introduction-Adaptive-Computation-and-Machine-Learning-Richard-S-Sutton_-Andrew-G-Barto-MIT-Press.txt"

    if not txt_file.exists():
        console.print(f"[red]Error: Text file not found: {txt_file}[/red]")
        return

    # Output PDF with 'text-' prefix
    pdf_file = txt_file.parent / f"text-{txt_file.stem}.pdf"

    console.print(f"\n[bold cyan]Text to PDF Conversion[/bold cyan]")
    console.print(f"Input: {txt_file.name}")
    console.print(f"Output: {pdf_file.name}")

    convert_text_to_pdf(txt_file, pdf_file)

    console.print(f"\n[bold green]Done![/bold green]")
    console.print(f"Output file: {pdf_file}")


if __name__ == "__main__":
    main()
