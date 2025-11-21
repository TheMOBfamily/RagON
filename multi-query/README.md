# Multi-RAG Query System

Parallel querying across multiple PDF sources với ThreadPoolExecutor.

## Features

- ✅ **Parallel Execution**: Query nhiều RAG sources đồng thời với ThreadPoolExecutor
- ✅ **Smart Deduplication**: MD5-based content deduplication across sources
- ✅ **Source Selection**: Chọn sources cụ thể hoặc query tất cả
- ✅ **Error Handling**: Graceful handling of partial failures
- ✅ **Result Aggregation**: Merge và track sources cho mỗi result
- ✅ **Rich CLI**: Interactive interface với rich console output
- ✅ **Token Optimization**: Optimized JSON format tiết kiệm 21.76% tokens (~35K chars)

## Architecture

### Directory Structure
```
multi-query/
├── main-d1f454371402.py       # CLI entry point
├── src/
│   ├── __init__.py
│   ├── config.py               # Settings & configuration
│   ├── source_manager.py       # Source discovery & selection
│   ├── parallel_query.py       # ThreadPoolExecutor logic
│   ├── result_aggregator.py    # Deduplication & aggregation
│   └── utils.py                # Common utilities
└── README.md                   # This file
```

### Design Principles

- **KISS**: Simple, straightforward implementation
- **DRY**: Re-use modules from main mini-rag
- **SOLID**: Each file has single responsibility
- **SSoT**: Centralized config in config.py
- **Small**: Each file < 150 LOC

## Installation

Sử dụng shared venv với main mini-rag:

```bash
source /home/fong/Projects/mini-rag/venv/bin/activate
```

Dependencies đã có sẵn:
- langchain
- faiss-cpu
- sentence-transformers
- rich
- pypdf

## Usage

### ⚠️ BEST PRACTICES - Query Strategy (CRITICAL)

**MANDATORY RULES:**
1. **List trước khi chạy** - ALWAYS run `--list-sources` để xem sources có sẵn
2. **Tối đa 9 cuốn sách** - Không query quá 9 sources trong 1 lần  
3. **Tối đa 3 queries** - Không quá 3 câu hỏi trong 1 JSON request
4. **Query ngắn gọn** - Mỗi query nên ngắn và trọng tâm (< 15 từ)
5. **2-5 lệnh/topic** - Thực hiện 2-5 lệnh tìm kiếm để đủ chiều sâu

### List Available PDFs (MANDATORY FIRST STEP - OPTIMIZED)

**NEW: Optimized JSON format tiết kiệm 21.76% tokens (~35K chars)**

```bash
# List all PDFs with hash mapping (RECOMMENDED)
./run-multiquery.sh --list-pdfs

# Output format (optimized):
{
  "notice": "⚠️ IMPORTANT NOTICE ⚠️\n\nRandom order...",
  "books": {
    "abc123hash...": "book1.pdf",
    "def456hash...": "book2.pdf",
    ...
  }
}
```

**Benefits:**
- ✅ 21.76% token reduction (161K → 126K chars)
- ✅ O(1) hash lookup instead of O(n) array search
- ✅ JSON native, dễ parse với jq
- ✅ Semantic rõ ràng: hash → filename mapping

### List Available Sources (Alternative - Table View)

```bash
python main-d1f454371402.py --list-sources

# Or use helper script
cd /home/fong/Projects/mini-rag/multi-query
./run-multiquery.sh --list-sources
```

Output shows:
- Source number (for selection)
- Source name (filename or hash)
- PDF count
- Full path with hash ID

**Example output:**
```
┌─────┬────────────────────────────────────────────────────────┬───────┬───────────────────────────────────────────────────┓
│ No. │ Source Name                                            │ Count │ Path                                              │
├─────┼────────────────────────────────────────────────────────┼───────┼───────────────────────────────────────────────────┤
│   1 │ 2019- David M. Kroenke, Randall J. Boyle - Using MIS   │     1 │ /home/fong/Projects/mini-rag/DKM-PDFs/5d2b78154c…│
│   2 │ 2022-Laudon_Management Information Systems (17)        │     1 │ /home/fong/Projects/mini-rag/DKM-PDFs/c36ae55cd1…│
│   5 │ AI-ML-Business.pdf                                     │     1 │ /home/fong/Projects/mini-rag/DKM-PDFs/9665bc5b38…│
└─────┴────────────────────────────────────────────────────────┴───────┴───────────────────────────────────────────────────┘
Total sources found: 151
```

**Analyze và chọn tối đa 9 sources phù hợp với topic của bạn.**

### Query with JSON (Recommended - Tối đa 3 queries)

```bash
# Basic query (1-3 queries only)
./run-multiquery.sh --json '{
  "queries":[
    "What is SOLID?",
    "Clean functions",
    "Code review"
  ]
}'

# Query specific sources by hash (Chọn 9 sources phù hợp)
./run-multiquery.sh --json '{
  "queries":["SOLID principles"]
}' --source-hashes "5d2b78154c,c36ae55cd1,9665bc5b38,f4a9966c46,20ca0b4146"

# Query with external sources
./run-multiquery.sh --json '{
  "queries":["Laravel best practices"],
  "external_sources":["/path/to/other/rag"]
}'
```

Output:
```
┌────┬─────────────┬───────────┬──────────────────┐
│No. │ Source Name │ PDF Count │ Path             │
├────┼─────────────┼───────────┼──────────────────┤
│  1 │ folder1     │         5 │ /path/to/folder1 │
│  2 │ folder2     │        12 │ /path/to/folder2 │
└────┴─────────────┴───────────┴──────────────────┘
```

### Workflow chuẩn (2-5 lệnh để tìm kiếm đủ chiều)

**Example: Research SOLID principles**

```bash
# STEP 1: List sources (MANDATORY)
./run-multiquery.sh --list-sources

# STEP 2: Lệnh 1 - Overview  
./run-multiquery.sh --json '{
  "queries":["SOLID principles overview"]
}' --source-hashes "hash1,hash2,hash3,hash4,hash5,hash6,hash7,hash8,hash9"

# STEP 3: Lệnh 2 - Deep dive
./run-multiquery.sh --json '{
  "queries":[
    "single responsibility principle",
    "open closed principle"
  ]
}' --source-hashes "..."

# STEP 4: Lệnh 3 - Examples
./run-multiquery.sh --json '{
  "queries":["SOLID examples Python code"]
}' --source-hashes "..."

# STEP 5: Lệnh 4 - Common mistakes
./run-multiquery.sh --json '{
  "queries":["SOLID violations antipatterns"]
}' --source-hashes "..."

# STEP 6 (optional): Lệnh 5 - Best practices
./run-multiquery.sh --json '{
  "queries":["SOLID refactoring best practices"]
}' --source-hashes "..."
```

**Tại sao 2-5 lệnh?**
- ✅ 1 lệnh: Không đủ chiều sâu
- ✅ 2-3 lệnh: Basic coverage  
- ✅ 4-5 lệnh: Deep dive complete
- ✅ >5 lệnh: Diminishing returns

### Query All Sources (Default)

**⚠️ NOT RECOMMENDED** - Query all hundreds of sources cùng lúc sẽ:
- Tốn thời gian (~15-30s)
- Results quá nhiều, khó review
- Context bị loãng, độ chính xác giảm

**Chỉ dùng khi:**
- Không chắc sources nào chứa info
- Cần broad search across all books
- Topic rất general

```bash
# Query tất cả sources (hundreds of books)
python main-d1f454371402.py --json '{"queries":["What is SOLID principle?"]}'
```

### Query Specific Sources (RECOMMENDED)

**Best practice: Chọn 3-9 sources phù hợp với topic**

```bash
# Chọn sources 1, 2, và 5
python main-d1f454371402.py "What is SOLID?" --sources 1,2,5
```

### Custom Configuration

```bash
python main-d1f454371402.py "Query" \
  --max-workers 8 \
  --top-k 6 \
  --timeout 60
```

### Specify Base Directory

```bash
python main-d1f454371402.py "Question" \
  --base-dir /path/to/pdf/collections
```

### Custom Output Path

```bash
python main-d1f454371402.py "Question" \
  --output /path/to/custom_output.md
```

## Configuration

### Environment Variables

```bash
export MULTI_RAG_BASE_DIR="/home/fong/Projects/mini-rag/test-pdf"
export MULTI_RAG_WORKERS=4
export MULTI_RAG_TOP_K=4
export MULTI_RAG_TIMEOUT=30
export CHUNK_SIZE=1200
export CHUNK_OVERLAP=150
```

### Config File

Settings are in `src/config.py`:

```python
@dataclass
class MultiRAGSettings:
    base_rag_dir: str = "/home/fong/Projects/mini-rag/test-pdf"
    max_workers: int = 4           # Parallel workers
    top_k_per_source: int = 4      # Results per source
    timeout_per_source: int = 30   # Timeout in seconds
    chunk_size: int = 1200
    chunk_overlap: int = 150
```

## How It Works

### 1. Source Discovery

- Scan base directory for folders containing PDFs
- Each folder = 1 RAG source
- Display numbered list for selection

### 2. Parallel Query Execution

```python
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(query_source, src) for src in sources]
    results = [f.result(timeout=30) for f in as_completed(futures)]
```

### 3. Result Aggregation

- Parse context chunks from each source
- Compute MD5 hash for deduplication
- Track which sources contributed each chunk
- Sort and format results

### 4. Output Generation

Markdown format with:
- Query info
- Source statistics
- Deduplicated results with source tracking
- Execution stats

## Output Format

```markdown
# Multi-RAG Query Results

## Query
What is SOLID principle?

## Sources Queried
- ✅ **source1** (2.34s)
- ✅ **source2** (3.12s)
- ❌ **source3** (1.23s) - Timeout error

## Aggregated Results

### Result 1
**Sources:** source1, source2
[Content here...]

### Result 2
**Source:** source1
[Content here...]

## Execution Statistics
- **Total time:** 5.67s
- **Sources queried:** 2/3
- **Results found:** 12
- **Duplicates removed:** 3
```

## Performance

### ThreadPoolExecutor vs asyncio

**Chọn ThreadPoolExecutor vì:**
- ✅ I/O-bound tasks (FAISS similarity search)
- ✅ Simple integration với sync APIs
- ✅ Python GIL không ảnh hưởng I/O operations
- ✅ No need to wrap blocking calls

**asyncio would require:**
- Wrapping FAISS calls in `run_in_executor`
- More complex error handling
- Less straightforward debugging

### Optimization Tips

1. **Adjust max_workers**: Default 4, tune based on CPU cores
2. **Set timeouts**: Prevent slow sources from blocking
3. **Cache vector stores**: FAISS auto-caches in `.mini_rag_index/`
4. **Batch queries**: Reduce overhead for multiple questions

## Error Handling

### Partial Failures

System continues when some sources fail:

```python
results = await gather(*tasks, return_exceptions=True)
for result in results:
    if isinstance(result, Exception):
        log_error(result)
        continue
    process(result)
```

### Timeout Handling

Each source has individual timeout:

```python
future.result(timeout=30)  # Per-source timeout
```

### Validation

- Check base_dir exists before discovery
- Validate source selections (1 <= idx <= len(sources))
- Handle empty results gracefully

## Logging

Logs saved to: `/home/fong/Projects/mini-rag/logs/multirag_YYYYMMDD_HHMMSS.log`

Format:
```
2025-10-22 10:45:23 - INFO - Discovering sources in /path/to/base
2025-10-22 10:45:24 - INFO - Found 3 sources
2025-10-22 10:45:25 - INFO - Parallel query of 3 sources: 5.67s
2025-10-22 10:45:25 - ERROR - Error querying source2: Timeout
```

## Examples

### Example 1: Query Python Clean Code Books

```bash
python main-d1f454371402.py \
  --base-dir /home/fong/Projects/hub-thay-vinh-python-nang-cao-2025-09-29/python-cleancode-books \
  "What is SOLID principle?"
```

### Example 2: Compare Multiple Sources

```bash
python main-d1f454371402.py \
  --base-dir /home/fong/Projects/RAGs \
  --sources 1,2 \
  "Best practices for code review"
```

### Example 3: High Concurrency

```bash
python main-d1f454371402.py \
  --max-workers 8 \
  --timeout 60 \
  "Machine learning fundamentals"
```

## Troubleshooting

### No sources found

```bash
# Check base directory
ls -la /path/to/base/

# Verify PDF files exist
find /path/to/base/ -name "*.pdf"
```

### Timeout errors

```bash
# Increase timeout
python main-d1f454371402.py "Query" --timeout 60
```

### Import errors

```bash
# Verify venv activation
which python
# Should be: /home/fong/Projects/mini-rag/venv/bin/python

# Check sys.path in main script
python -c "import sys; print('\n'.join(sys.path))"
```

## Comparison with main-minirag

| Feature | main-minirag | multi-query |
|---------|--------------|-------------|
| Sources | Single folder | Multiple folders |
| Execution | Sequential | Parallel |
| Deduplication | N/A | MD5-based |
| Source tracking | Single source | Multi-source tracking |
| CLI | Simple | Rich with --list-sources |

## Future Enhancements

- [ ] Result scoring/ranking across sources
- [ ] Async support with asyncio
- [ ] Source weighting (prioritize certain sources)
- [ ] Query caching for repeated queries
- [ ] JSON output format
- [ ] Interactive source selection (TUI)

## Credits

- Built on mini-rag architecture
- Uses LangChain + FAISS + sentence-transformers
- Follows clean code principles from init-prompt.json

## License

Same as mini-rag project.
