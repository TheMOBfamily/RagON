# Multi-RAG Quick Start Guide

## Installation

```bash
cd /home/fong/Projects/mini-rag/multi-query
source /home/fong/Projects/mini-rag/venv/bin/activate
```

## Basic Usage

### 1. List Available Sources
```bash
python main-d1f454371402.py --list-sources
```

### 2. Query All Sources
```bash
python main-d1f454371402.py "Your question here"
```

### 3. Query Specific Sources
```bash
# Query sources 1, 2, and 3
python main-d1f454371402.py "Your question" --sources 1,2,3
```

### 4. Using Helper Script
```bash
./run-multiquery.sh "Your question"
./run-multiquery.sh --list-sources
```

## Configuration

### Environment Variables
```bash
export MULTI_RAG_BASE_DIR="/path/to/pdf/collections"
export MULTI_RAG_WORKERS=8        # Parallel workers (default: 4)
export MULTI_RAG_TOP_K=6          # Results per source (default: 4)
export MULTI_RAG_TIMEOUT=60       # Timeout per source (default: 30)
```

### CLI Options
```bash
python main-d1f454371402.py "Question" \
  --base-dir /path/to/pdfs \
  --max-workers 8 \
  --top-k 6 \
  --timeout 60 \
  --output custom_output.md
```

## Examples

### Example 1: Python Clean Code Books
```bash
python main-d1f454371402.py \
  --base-dir /home/fong/Projects/hub-thay-vinh-python-nang-cao-2025-09-29/python-cleancode-books \
  "What is SOLID principle?"
```

### Example 2: Multiple Collections
```bash
# First, list sources
python main-d1f454371402.py --list-sources

# Then select specific ones
python main-d1f454371402.py "Code review best practices" --sources 1,3,5
```

### Example 3: High Concurrency
```bash
python main-d1f454371402.py \
  --max-workers 8 \
  --timeout 60 \
  "Machine learning fundamentals"
```

## Output

Results saved to: `/home/fong/Projects/mini-rag/results/multirag_YYYYMMDD_HHMMSS.md`

Logs saved to: `/home/fong/Projects/mini-rag/logs/multirag_YYYYMMDD_HHMMSS.log`

## Architecture

- **Parallel execution:** ThreadPoolExecutor with configurable workers
- **Deduplication:** MD5-based content matching across sources
- **Error handling:** Graceful partial failures
- **Re-use:** minirag vectorstore and pipeline modules

## Troubleshooting

### No sources found
```bash
# Check base directory
ls -la /path/to/base/

# Verify PDFs exist
find /path/to/base/ -name "*.pdf"
```

### Timeout errors
```bash
# Increase timeout
python main-d1f454371402.py "Query" --timeout 60
```

### Import errors
```bash
# Ensure venv is activated
which python
# Should output: /home/fong/Projects/mini-rag/venv/bin/python

# Check dependencies
pip list | grep -E "langchain|faiss|sentence-transformers|rich"
```

## Full Documentation

See: `/home/fong/Projects/mini-rag/multi-query/README.md`
