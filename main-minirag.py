#!/usr/bin/env python
from __future__ import annotations
import argparse
import sys
import logging
import uuid
from datetime import datetime
from pathlib import Path
from rich.console import Console

# Ensure src/ on path for direct script execution without install
SRC_PATH = Path(__file__).parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from minirag.loader import load_pdfs  # type: ignore  # noqa: E402
from minirag.splitter import split_documents  # type: ignore  # noqa: E402
from minirag.vectorstore import build_or_load_vectorstore  # type: ignore  # noqa: E402
from minirag.pipeline import answer_question  # type: ignore  # noqa: E402
from minirag.utils import timed  # type: ignore  # noqa: E402
from minirag.config import get_settings  # type: ignore  # noqa: E402

console = Console()


def setup_logging() -> str:
    """Setup logging to file trong logs/ folder"""
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"minirag_{timestamp}.log"
    
    logging.getLogger().handlers.clear()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file)
        ]
    )
    return str(log_file)


def save_results(question: str, answer: str, pdf_dir: str) -> str:
    """Save query results to timestamped markdown file in results/ folder"""
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_id = str(uuid.uuid4())[:8]
    filename = f"{timestamp}-{file_id}.md"
    output_file = results_dir / filename
    
    # Extract document chunks with metadata for markdown
    lines = answer.split('\n---\n')
    formatted_chunks = []
    
    for line in lines:
        if line.strip():
            # Extract document name from [document.pdf] format
            if line.startswith('[') and ']' in line:
                end_bracket = line.find(']')
                doc_name = line[1:end_bracket]
                content = line[end_bracket+1:].strip()
                formatted_chunks.append(f"**Source**: `{doc_name}`\n\n{content}")
            else:
                formatted_chunks.append(line)
    
    # Create markdown content
    markdown_content = f"""# Mini-RAG Query Results

## Query
{question}

## PDF Directory
{pdf_dir}

## Retrieved Context

{chr(10).join([f"### Chunk {i+1}{chr(10)}{chunk}{chr(10)}" for i, chunk in enumerate(formatted_chunks)])}

## Metadata
- **Timestamp**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **File ID**: {file_id}
- **Results saved to**: {output_file}
"""
    
    output_file.write_text(markdown_content, encoding='utf-8')
    return str(output_file)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mini RAG - hỏi đáp trên thư mục PDF")
    parser.add_argument("question", help="Câu hỏi cần trả lời")
    parser.add_argument("pdf_dir", help="Đường dẫn tuyệt đối tới thư mục chứa PDF")
    parser.add_argument(
        "--force-rebuild",
        action="store_true",
        help="Force rebuild vector store even if no changes detected"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Number of chunks to retrieve (default: 5, from config/env)"
    )
    return parser.parse_args()


def main() -> int:
    log_file = setup_logging()
    
    args = parse_args()
    pdf_dir = Path(args.pdf_dir)
    
    logging.info(f"Mini-RAG started - Question: {args.question}")
    logging.info(f"PDF Directory: {pdf_dir}")
    logging.info(f"Log file: {log_file}")
    
    if not pdf_dir.is_absolute():
        error_msg = "Vui lòng cung cấp đường dẫn tuyệt đối tới thư mục PDF"
        console.print(f"[red]{error_msg}")
        logging.error(error_msg)
        return 1

    try:
        # Get settings and override TOP_K if specified
        settings = get_settings()
        if args.top_k is not None:
            settings.top_k = args.top_k
            logging.info(f"TOP_K override from args: {args.top_k}")

        logging.info(f"Using TOP_K={settings.top_k} chunks for retrieval")

        with timed("Xây / nạp vector store"):
            store = build_or_load_vectorstore(str(pdf_dir), force_rebuild=args.force_rebuild)
            logging.info("Vector store ready")

        with timed("Truy xuất & sinh câu trả lời"):
            answer = answer_question(store, args.question, top_k=settings.top_k)
            logging.info("Answer generated successfully")

        console.print("\n[bold yellow]Câu trả lời:\n")
        console.print(answer)
        
        # Save results to file
        output_file = save_results(args.question, answer, str(pdf_dir))
        
        logging.info("Process completed successfully")
        console.print(f"\n[bold green]📄 Results saved to: {output_file}")
        console.print(f"[dim]Log file: {log_file}")
        return 0
        
    except Exception as e:
        error_msg = f"Error during processing: {e}"
        console.print(f"[red]{error_msg}")
        logging.error(error_msg, exc_info=True)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
