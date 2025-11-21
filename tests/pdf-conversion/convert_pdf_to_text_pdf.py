#!/usr/bin/env python3
"""Convert PDF to text and then to new PDF with text-* prefix."""

import sys
from pathlib import Path
from pypdf import PdfReader
from fpdf import FPDF
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract all text from PDF file."""
    console.print(f"\n[cyan]Reading PDF: {pdf_path.name}[/cyan]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Extracting text...", total=None)

        reader = PdfReader(str(pdf_path))
        text_parts = []
        total_pages = len(reader.pages)

        for i, page in enumerate(reader.pages, 1):
            progress.update(task, description=f"Extracting page {i}/{total_pages}")
            text = page.extract_text()
            if text.strip():
                text_parts.append(text)

        progress.update(task, description=f"Extracted {total_pages} pages")

    return "\n\n".join(text_parts)


def save_text_to_file(text: str, output_path: Path) -> None:
    """Save extracted text to .txt file."""
    console.print(f"\n[cyan]Saving text to: {output_path}[/cyan]")
    output_path.write_text(text, encoding='utf-8')
    console.print(f"[green]✓ Saved {len(text):,} characters[/green]")


def convert_text_to_pdf(text: str, output_path: Path) -> None:
    """Convert text to PDF using fpdf2."""
    console.print(f"\n[cyan]Creating PDF: {output_path}[/cyan]")

    # Create PDF document
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Courier", size=10)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Building PDF...", total=None)

        # Split text into lines
        lines = text.split('\n')

        for i, line in enumerate(lines, 1):
            if i % 1000 == 0:
                progress.update(task, description=f"Processing line {i:,}/{len(lines):,}")

            # fpdf2 handles Unicode text well
            if line.strip():
                try:
                    pdf.multi_cell(0, 5, line, align='L')
                except Exception:
                    # Skip lines that cause encoding issues
                    pdf.multi_cell(0, 5, "[line with encoding issue]", align='L')
            else:
                pdf.ln(5)  # Add spacing for empty lines

        progress.update(task, description="Saving PDF...")
        pdf.output(str(output_path))

    console.print(f"[green]✓ PDF created successfully[/green]")


def main():
    source_pdf = Path("/home/fong/Projects/mini-rag/PDFs/2018-Reinforcement-Learning_-An-Introduction-Adaptive-Computation-and-Machine-Learning-Richard-S-Sutton_-Andrew-G-Barto-MIT-Press.PDF")

    if not source_pdf.exists():
        console.print(f"[red]Error: Source PDF not found: {source_pdf}[/red]")
        sys.exit(1)

    # Define output paths
    base_name = source_pdf.stem
    output_dir = source_pdf.parent

    txt_output = output_dir / f"{base_name}.txt"
    pdf_output = output_dir / f"text-{base_name}.pdf"

    console.print(f"\n[bold cyan]PDF to Text to PDF Conversion[/bold cyan]")
    console.print(f"Source: {source_pdf.name}")
    console.print(f"Text output: {txt_output.name}")
    console.print(f"PDF output: {pdf_output.name}")

    # Step 1: Extract text
    text = extract_text_from_pdf(source_pdf)

    # Step 2: Save to text file
    save_text_to_file(text, txt_output)

    # Step 3: Convert to PDF
    convert_text_to_pdf(text, pdf_output)

    console.print(f"\n[bold green]✓ Conversion complete![/bold green]")
    console.print(f"Text file: {txt_output}")
    console.print(f"PDF file: {pdf_output}")


if __name__ == "__main__":
    main()
