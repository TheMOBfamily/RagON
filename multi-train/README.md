# Mini-RAG Training System

Hash-based caching system for training PDFs with FAISS vector stores.

## Features

- ✅ **Hash-based Caching**: MD5 hash of PDF content for intelligent caching
- ✅ **Skip Duplicates**: Auto-skip if PDF already trained
- ✅ **Metadata Tracking**: JSON metadata for each trained PDF
- ✅ **Batch Training**: Train all PDFs in directory
- ✅ **Rich CLI**: Progress indicators and summary tables

## Architecture

### Cache Structure
```
DKM-PDFs/
├── .trained/                          # Base cache directory
│   ├── <md5_hash_1>/                  # Cache for PDF 1
│   │   ├── .mini_rag_index/
│   │   │   ├── index.faiss            # FAISS index
│   │   │   ├── index.pkl              # Metadata
│   │   │   └── manifest.json          # Build info
│   │   ├── <original_pdf_name>.pdf    # Copy of PDF
│   │   └── metadata.json              # Training metadata
│   ├── <md5_hash_2>/                  # Cache for PDF 2
│   │   └── ...
│   └── ...
└── *.pdf                              # Source PDFs
```

### Hash-based Caching

**Why MD5 of file content:**
- Same PDF content → Same hash → Reuse cache
- Changed PDF content → Different hash → Rebuild
- Filename doesn't matter (only content)

**Cache Hit Logic:**
```python
def is_trained(pdf_path, cache_base_dir):
    pdf_hash = compute_file_hash(pdf_path)  # MD5 of content
    cache_dir = cache_base_dir / pdf_hash
    
    # Check if both index files exist
    return (
        (cache_dir / ".mini_rag_index/index.faiss").exists() and
        (cache_dir / ".mini_rag_index/index.pkl").exists()
    )
```

## Installation

Uses shared venv with main mini-rag:

```bash
source /home/fong/Projects/mini-rag/venv/bin/activate
```

## Usage

### Train All PDFs (Default)

```bash
./main-train-352179ea6e15.sh
```

### Force Rebuild All

```bash
./main-train-352179ea6e15.sh --force-rebuild
```

### Custom Directories

```bash
./main-train-352179ea6e15.sh \
  --pdf-dir /path/to/pdfs \
  --cache-dir /path/to/cache
```

### List Cached PDFs

```bash
./main-train-352179ea6e15.sh --list-cache
```

### Using Python Directly

```bash
python main-train-352179ea6e15.py --help
python main-train-352179ea6e15.py
python main-train-352179ea6e15.py --force-rebuild
```

### Cleanup Orphaned Folders

**What are orphaned folders?**
When PDFs are deleted/renamed/modified, their old cache folders become orphaned (no matching PDF exists).

**Preview orphaned folders (dry-run):**
```bash
./main-train-352179ea6e15.sh --cleanup-dry-run
```

**Cleanup orphaned folders:**
```bash
./main-train-352179ea6e15.sh --cleanup-orphaned
```

**Train + Auto-cleanup:**
```bash
./main-train-352179ea6e15.sh --cleanup-orphaned
```

## CLI Options

```
--pdf-dir PATH          Directory containing PDFs (default: ../DKM-PDFs)
--cache-dir PATH        Base cache directory (default: ../DKM-PDFs/.trained)
--force-rebuild         Force rebuild even if cached
--list-cache            List all cached PDFs and exit
--cleanup-orphaned      Cleanup orphaned cache folders after training
--cleanup-dry-run       Preview orphaned folders without deleting
```

## Output

### Console Output

```
Mini-RAG Training System
Log file: /path/to/logs/train_20251022_181234.log

Configuration:
  PDF directory: /home/fong/Projects/mini-rag/DKM-PDFs
  Cache directory: /home/fong/Projects/mini-rag/DKM-PDFs/.trained
  Force rebuild: False

Found 5 PDF file(s)

⚡ Cache hit: nasa-P10.pdf
   Using cached: .trained/a1b2c3d4...

🔧 Training: python-data-science-williams.pdf
✓ Trained: python-data-science-williams.pdf (12.34s)
   Cache: .trained/e5f6g7h8...

┌──────────────────────────────────┬────────────┬──────────┐
│ PDF                              │ Status     │ Time (s) │
├──────────────────────────────────┼────────────┼──────────┤
│ nasa-P10.pdf                     │ ⚡ Cached  │     0.05 │
│ python-data-science-williams.pdf │ ✓ Trained  │    12.34 │
│ ...                              │ ...        │      ... │
└──────────────────────────────────┴────────────┴──────────┘

Statistics:
  Cached: 3
  Newly trained: 2
  Failed: 0
  Total time: 45.67s

📄 Results saved to: results/training_20251022_181234.json

🧹 Cleaning up orphaned cache folders...
  📄 Scanning hundreds of PDF files...
  ✓ Found hundreds of unique PDF hashes
  📁 Scanning cache folders...
  ✓ Found 227 cache folders

  ⚠ Found 37 orphaned folders
  Estimated space to free: 1.2 GB

  🗑 Removing 37 orphaned folders...
  ✓ Successfully removed 37 orphaned folders
  ✓ Kept 190 valid cache folders
  ✓ Freed ~1.2 GB of space

🧹 Cleanup Summary:
  Orphaned removed: 37
  Valid kept: 190
```

### Metadata File

Each trained PDF has a `metadata.json`:

```json
{
  "filename": "python-data-science-williams.pdf",
  "file_hash": "e5f6g7h8a9b0c1d2e3f4g5h6i7j8k9l0",
  "file_size": 12345678,
  "trained_at": "2025-10-22T18:12:34.567890",
  "cache_dir": "/home/fong/Projects/mini-rag/DKM-PDFs/.trained/e5f6g7h8..."
}
```

## How It Works

### 1. Hash Computation

```python
import hashlib

def compute_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
```

**Streaming approach:**
- Read file in 8KB chunks
- Memory efficient for large PDFs
- Fast computation

### 2. Cache Check

Before training each PDF:
1. Compute MD5 hash of content
2. Check if `cache_dir/<hash>/.mini_rag_index/` exists
3. If exists → Skip training (cache hit)
4. If not exists → Train and cache

### 3. Training Process

```python
1. Create cache directory: .trained/<md5_hash>/
2. Copy PDF to cache directory
3. Build vector store using minirag.vectorstore
4. Vector store creates .mini_rag_index/ inside cache dir
5. Save metadata.json with training info
```

### 4. Vector Store Re-use

To query a trained PDF:

```python
from minirag.vectorstore import build_or_load_vectorstore

# Load from cache
cache_dir = ".trained/<md5_hash>"
store = build_or_load_vectorstore(cache_dir, force_rebuild=False)

# Query
results = store.similarity_search("your question", k=4)
```

## Examples

### Example 1: First Training Run

```bash
$ ./main-train-352179ea6e15.sh

Found 5 PDF file(s)

🔧 Training: Ash Allen - Battle Ready Laravel.pdf
✓ Trained: Ash Allen - Battle Ready Laravel.pdf (15.23s)

🔧 Training: google-eng-practices.pdf
✓ Trained: google-eng-practices.pdf (8.45s)

# ... train all 5 PDFs
# Total time: 67.89s
```

### Example 2: Second Run (All Cached)

```bash
$ ./main-train-352179ea6e15.sh

Found 5 PDF file(s)

⚡ Cache hit: Ash Allen - Battle Ready Laravel.pdf
⚡ Cache hit: google-eng-practices.pdf
⚡ Cache hit: nasa-P10.pdf
⚡ Cache hit: data-science-beginners.pdf
⚡ Cache hit: python-data-science-williams.pdf

Statistics:
  Cached: 5
  Newly trained: 0
  Failed: 0
  Total time: 0.25s  # Ultra fast!
```

### Example 3: Force Rebuild

```bash
$ ./main-train-352179ea6e15.sh --force-rebuild

# Rebuilds all, even if cached
```

## Performance

### Caching Benefits

| Scenario | Without Cache | With Cache | Speedup |
|----------|--------------|------------|---------|
| 5 PDFs (first run) | 67.89s | 67.89s | 1x |
| 5 PDFs (second run) | 67.89s | 0.25s | 271x |
| 1 changed PDF | 13.58s | 0.20s | 67x |

### Hash Computation Speed

- Small PDF (100KB): ~5ms
- Medium PDF (5MB): ~50ms
- Large PDF (50MB): ~500ms

Much faster than rebuilding vector store!

## Integration with Multi-Query

Trained PDFs can be queried with multi-query system:

```bash
# Train PDFs first
cd /home/fong/Projects/mini-rag/train
./main-train-352179ea6e15.sh

# Query using multi-query
cd /home/fong/Projects/mini-rag/multi-query
python main-d1f454371402.py "Question" \
  --base-dir /home/fong/Projects/mini-rag/DKM-PDFs/.trained
```

## Troubleshooting

### Cache directory not found

```bash
# Check if cache directory exists
ls -la /home/fong/Projects/mini-rag/DKM-PDFs/.trained/

# Create if missing
mkdir -p /home/fong/Projects/mini-rag/DKM-PDFs/.trained
```

### Hash mismatch

If PDF content changes but hash stays same:
- File was edited but not saved
- File system caching issue

Solution: Use `--force-rebuild`

### Memory issues with large PDFs

Training uses streaming, but FAISS indexing needs memory:
- Small PDFs (<10MB): ~100MB RAM
- Large PDFs (>100MB): ~1GB RAM

## Files

- `main-train-352179ea6e15.py`: Python training script
- `main-train-352179ea6e15.sh`: Bash wrapper
- `src/hash_utils.py`: Hash computation and caching logic
- `src/__init__.py`: Module init

## Dependencies

Same as mini-rag (from shared venv):
- langchain
- faiss-cpu
- sentence-transformers
- rich
- pypdf

## Credits

- Built on mini-rag architecture
- Uses MD5 for content-based caching
- Follows clean code principles

## License

Same as mini-rag project.
