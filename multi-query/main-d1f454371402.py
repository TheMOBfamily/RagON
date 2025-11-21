#!/usr/bin/env python
from __future__ import annotations
import argparse
import sys
import time
import logging
from pathlib import Path
from rich.console import Console

# Setup path
PROJECT_ROOT = Path(__file__).parent.parent
SRC_PATH = Path(__file__).parent / "src"
MINIRAG_SRC = PROJECT_ROOT / "src"

for path in [SRC_PATH, MINIRAG_SRC]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from src.config import get_settings  # type: ignore
from src.source_manager import (  # type: ignore
    list_sources, 
    select_sources, 
    discover_sources,
    list_pdfs_metadata,
    filter_sources_by_hashes
)
from src.parallel_query import query_all_sources_parallel  # type: ignore
from src.result_aggregator import aggregate_results, format_json_output  # type: ignore
from src.utils import setup_logging  # type: ignore
from src.messages import THINK_ULTRA_NOTICE, PDF_LIST_NOTICE  # centralized notices

console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Multi-RAG Query - JSON-based parallel querying across multiple sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
JSON Format:
{
  "queries": [
    "What is SOLID principle?",
    "Explain clean code practices",
    "What are Laravel best practices?"
  ],
  "external_sources": [
    "/home/fong/Projects/RAGs/laravel-books",
    "/home/fong/Projects/RAGs/nasa-google-cleancode"
  ]
}

Usage Examples:

  1. List available sources with full hash (32 chars):
     %(prog)s --list-pdfs

  2. List available sources in discovery order (no randomization):
     %(prog)s --list-pdfs --no-sort

  3. Query with JSON string + specific sources (RECOMMENDED):
     %(prog)s --json '{"queries":["What is SOLID?"]}' --source-hashes "838cc6ac8cb0d8ddb98fdb1ae0c8a443,41d80961ba66da6a1294aa9624cea15d"

  4. Query with JSON string (multiple queries, max 3):
     %(prog)s --json '{"queries":["Q1","Q2","Q3"]}' --source-hashes "hash1,hash2,hash3"

  5. Query with JSON string + external sources:
     %(prog)s --json '{"queries":["Q1"],"external_sources":["/path/to/rag"]}'

  6. Query with JSON file (absolute path):
     %(prog)s --json-file /home/fong/Projects/mini-rag/multi-query/example-queries.json

  7. List sources including external in discovery order:
     %(prog)s --json-file example-queries.json --list-sources --no-sort

CRITICAL LIMITATIONS:
  ⚠️  DO NOT query all hundreds of sources without --source-hashes filter
  ⚠️  Maximum 9 sources per query (use --source-hashes with full 32-char MD5 hash)
  ⚠️  Maximum 3 queries per request
  ⚠️  Querying all sources is VERY SLOW (>2 minutes) and resource-intensive
  ✅  ALWAYS use --list-pdfs to get full hash, then filter specific sources

Note: Always use JSON format. No plain text queries allowed.
      External sources must have .mini_rag_index/ structure.
      Hash IDs must be full 32-character MD5 (e.g., 838cc6ac8cb0d8ddb98fdb1ae0c8a443)
        """
    )
    
    parser.add_argument(
        "--json",
        type=str,
        help="JSON string with queries and external sources"
    )
    
    parser.add_argument(
        "--json-file",
        type=str,
        help="Path to JSON file (absolute path recommended)"
    )
    
    parser.add_argument(
        "--list-sources",
        action="store_true",
        help="List available RAG sources and exit"
    )
    
    parser.add_argument(
        "--list-pdfs",
        action="store_true",
        help="List all PDFs with metadata (filename + file_hash) as JSON"
    )

    parser.add_argument(
        "--source-hashes",
        type=str,
        help="Comma-separated list of hash IDs to filter sources (e.g., 'aa4a4de3...,bb5c7ef8...')"
    )
    
    parser.add_argument(
        "--base-dir",
        type=str,
        help="Base directory (default: from config)"
    )
    
    parser.add_argument(
        "--max-workers",
        type=int,
        help="Maximum parallel workers (default: from config)"
    )
    
    parser.add_argument(
        "--top-k",
        type=int,
        help="Top K results per source (default: from config)"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        help="Timeout per source in seconds (default: from config)"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: results/multirag_<timestamp>.md)"
    )

    parser.add_argument(
        "--no-sort",
        action="store_true",
        help="Do not sort results (show in discovery order)"
    )

    return parser.parse_args()


def main() -> int:
    import json
    from datetime import datetime
    
    args = parse_args()
    settings = get_settings()
    
    # Override settings from args
    base_dir = args.base_dir or settings.base_rag_dir
    max_workers = args.max_workers or settings.max_workers
    top_k = args.top_k or settings.top_k_per_source
    timeout = args.timeout or settings.timeout_per_source
    
    # Setup logging
    log_dir = PROJECT_ROOT / "logs"
    log_file = setup_logging(log_dir)
    
    # Log file path (logged only, not printed to console)
    logging.info(f"Log file: {log_file}")
    
    # Load JSON if provided
    json_data = {}
    external_sources = []
    
    if args.json or args.json_file:
        try:
            if args.json:
                # Direct JSON string input
                json_data = json.loads(args.json)
                logging.info(f"JSON mode (direct): Loaded {len(json_data.get('queries', []))} queries")
            elif args.json_file:
                # JSON file input (absolute path)
                json_file_path = Path(args.json_file)
                if not json_file_path.is_absolute():
                    console.print(f"[yellow]Warning: Relative path detected. Converting to absolute...[/yellow]")
                    json_file_path = json_file_path.resolve()
                
                if not json_file_path.exists():
                    console.print(f"[red]Error: JSON file not found: {json_file_path}")
                    return 1
                
                with open(json_file_path, "r") as f:
                    json_data = json.load(f)
                
                logging.info(f"JSON mode (file): {json_file_path}")
                logging.info(f"Loaded {len(json_data.get('queries', []))} queries")
            
            external_sources = json_data.get("external_sources", [])
            if external_sources:
                logging.info(f"External sources: {len(external_sources)}")
        except json.JSONDecodeError as e:
            console.print(f"[red]Error parsing JSON: {e}")
            return 1
        except Exception as e:
            console.print(f"[red]Error loading JSON: {e}")
            return 1
    
    # List PDFs mode
    if args.list_pdfs:
        try:
            pdfs = list_pdfs_metadata(base_dir, no_sort=args.no_sort)
            if not pdfs:
                console.print("[yellow]No PDFs found")
                return 1

            # Optimized output format: dict with notice + books (23.87% token savings)
            full_output = {
                "notice": PDF_LIST_NOTICE,
                "books": pdfs
            }

            # Output as JSON (required by MCP server)
            import json as json_module
            print(json_module.dumps(full_output, indent=2, ensure_ascii=False))
            return 0
        except Exception as e:
            console.print(f"[red]Error: {e}")
            logging.error(f"Failed to list PDFs: {e}", exc_info=True)
            return 1

    # List sources mode
    if args.list_sources:
        try:
            list_sources(base_dir, external_sources, no_sort=args.no_sort)
            return 0
        except Exception as e:
            console.print(f"[red]Error: {e}")
            return 1
    
    # Determine queries (JSON is MANDATORY)
    queries = []
    if (args.json or args.json_file) and "queries" in json_data:
        queries = json_data["queries"]
        
        # Require --source-hashes when querying
        if not args.source_hashes:
            console.print("[red]Error: --source-hashes is REQUIRED when querying!")
            console.print("[yellow]Querying all sources is very slow and resource-intensive.")
            console.print("[yellow]Use --list-pdfs to see available sources, then specify --source-hashes")
            console.print()
            console.print("[cyan]Listing available PDFs:[/cyan]")
            try:
                pdfs = list_pdfs_metadata(base_dir, no_sort=args.no_sort)
                if pdfs:
                    import json as json_module
                    # Consistent output format with --list-pdfs
                    full_output = {
                        "notice": PDF_LIST_NOTICE,
                        "books": pdfs
                    }
                    print(json_module.dumps(full_output, indent=2, ensure_ascii=False))
                else:
                    console.print("[yellow]No PDFs found")
            except Exception as e:
                console.print(f"[red]Error listing PDFs: {e}")
            return 1
    else:
        # No JSON input provided - show warning and list available sources
        console.print("[red]Error: JSON input is required!")
        console.print("[yellow]Use: --json 'JSON_STRING' OR --json-file /path/to/file.json")
        console.print("Run with --help for examples")
        console.print()
        console.print("[cyan]Available sources:[/cyan]")
        try:
            list_sources(base_dir, external_sources, no_sort=args.no_sort)
        except Exception as e:
            console.print(f"[red]Error listing sources: {e}")
        return 1

    try:
        # Discover and select sources
        logging.info("Discovering sources...")
        all_sources = discover_sources(base_dir, external_sources, no_sort=args.no_sort)
        
        if not all_sources:
            logging.error("No RAG sources found")
            return 1
        
        # Filter by hash IDs if provided
        if args.source_hashes:
            hash_list = [h.strip() for h in args.source_hashes.split(",")]
            logging.info(f"Filtering by {len(hash_list)} hash ID(s)")
            all_sources = filter_sources_by_hashes(all_sources, hash_list)
            
            if not all_sources:
                console.print("[red]Error: No sources match the provided hash IDs")
                return 1
            
            logging.info(f"Filtered to {len(all_sources)} source(s)")
        
        # Select all sources (no --sources option in JSON mode)
        selected = all_sources
        
        if not selected:
            logging.error("No valid sources selected")
            return 1
        
        logging.info(f"Selected {len(selected)} source(s)")
        
        # Setup output directory
        results_dir = PROJECT_ROOT / "results"
        results_dir.mkdir(exist_ok=True)
        
        # Query each query string
        for query_idx, query in enumerate(queries, 1):
            if len(queries) > 1:
                logging.info(f"Query {query_idx}/{len(queries)}")
            
            logging.info(f"Query: {query}")
            
            # Parallel query
            start_time = time.perf_counter()
            
            source_paths = [src.path for src in selected]
            results = query_all_sources_parallel(
                source_paths=source_paths,
                query=query,
                max_workers=max_workers,
                timeout=timeout,
                top_k=top_k
            )
            
            total_time = time.perf_counter() - start_time
            
            # Aggregate results
            logging.info("Aggregating results...")
            aggregated = aggregate_results(results, query, total_time)
            
            # Format as JSON
            json_output = format_json_output(aggregated)
            
            # Save to JSON file (use hash of query as filename)
            import hashlib
            query_hash = hashlib.md5(query.encode()).hexdigest()[:12]
            
            if args.output and len(queries) == 1:
                output_path = Path(args.output)
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                if len(queries) > 1:
                    output_path = results_dir / f"{query_hash}_q{query_idx}_{timestamp}.json"
                else:
                    output_path = results_dir / f"{query_hash}_{timestamp}.json"
            
            # Ensure .json extension
            if not str(output_path).endswith('.json'):
                output_path = output_path.with_suffix('.json')
            
            # Write JSON to file
            output_path.write_text(json.dumps(json_output, indent=2, ensure_ascii=False), encoding='utf-8')
            
            # Print results to console (simplified JSON output)
            import json as json_module
            
            # Only print results data (source + content)
            results_data = json_output.get("results", {}).get("data", [])
            
            if results_data:
                # Print as pretty JSON array
                print(json_module.dumps(results_data, indent=2, ensure_ascii=False))
            
            # Print summary to console
            abs_output_path = output_path.resolve()
            print(f"\n✓ Query {query_idx}/{len(queries)} completed")
            print(f"📁 Output: {abs_output_path}")
            print(f"📊 Sources: {len(aggregated.successful_sources)}/{len(aggregated.source_results)} successful")
            print(f"📝 Results: {len(aggregated.chunks)} chunks")
            print(f"⏱️  Time: {total_time:.2f}s")

            # Also log for record
            logging.info(f"Query {query_idx} completed")
            logging.info(f"Output: {abs_output_path}")
            logging.info(f"Sources: {len(aggregated.successful_sources)}/{len(aggregated.source_results)} successful")
            logging.info(f"Results: {len(aggregated.chunks)} chunks")
            logging.info(f"Time: {total_time:.2f}s")
            
            if query_idx < len(queries):
                print("\n" + "="*70 + "\n")
        
        logging.info(f"Query completed successfully: {len(queries)} queries")
        return 0
        
    except Exception as e:
        console.print(f"\n[red]Error: {e}")
        logging.error(f"Query failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
