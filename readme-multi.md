# Hướng Dẫn Sử Dụng Multi-Query RAG System

## Tổng Quan

Hệ thống Multi-Query RAG cho phép truy vấn song song nhiều nguồn PDF với cơ chế cache thông minh và xử lý JSON-based queries.

### Kiến Trúc Hệ Thống

```
mini-rag/
├── DKM-PDFs/                    # Nơi lưu trữ PDFs và cache
│   ├── *.pdf                    # PDFs gốc
│   └── <md5_hash>/              # Cache cho từng PDF (tự động tạo)
│       ├── index.faiss          # FAISS vector index
│       ├── index.pkl            # Metadata
│       ├── manifest.json        # Build info
│       └── metadata.json        # Training metadata
│
├── multi-train/                 # Hệ thống training PDFs
│   ├── main-train-352179ea6e15.py
│   ├── main-train-352179ea6e15.sh
│   └── src/                     # Training utilities
│
└── multi-query/                 # Hệ thống query song song
    ├── run-multiquery.sh        # ⭐ Script chính - ƯU TIÊN SỬ DỤNG
    ├── main-d1f454371402.py     # Python implementation
    ├── example-queries.json     # Ví dụ JSON queries
    └── src/                     # Query utilities
```

## 🚀 Cách Sử Dụng Nhanh (Recommended)

### ⭐ Ưu Tiên: Dùng Script `run-multiquery.sh` với JSON String

```bash
cd /home/fong/Projects/mini-rag/multi-query

# 1. Query đơn giản
./run-multiquery.sh --json '{"queries":["What is SOLID principle?"]}'

# 2. Multiple queries
./run-multiquery.sh --json '{"queries":["What is SOLID?","Explain DRY principle","What is KISS?"]}'

# 3. Query với external sources
./run-multiquery.sh --json '{"queries":["Laravel best practices"],"external_sources":["/home/fong/Projects/RAGs/laravel-books"]}'

# 4. Sử dụng JSON file
./run-multiquery.sh --json-file example-queries.json
```

### JSON Format

```json
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
```

**Lưu ý quan trọng về queries:**
- ✅ **Queries ngắn gọn**: "What is SOLID?", "Explain DRY principle"
- ✅ **Câu hỏi đơn giản**: Mỗi query tập trung 1 khái niệm
- ❌ **Tránh queries phức tạp**: "Compare SOLID vs DRY and explain how they relate to KISS in context of microservices"
- ❌ **Tránh logic lồng ghép**: Query có nhiều điều kiện hoặc sub-questions
- **Lý do**: Queries đơn giản cho kết quả chính xác và relevant hơn

## 📂 Nơi Chứa PDFs: DKM-PDFs

### Cấu Trúc Thư Mục

```
/home/fong/Projects/mini-rag/DKM-PDFs/
├── Ash Allen - Battle Ready Laravel.pdf
├── data-science-beginners.pdf
├── google-eng-practices.pdf
├── nasa-P10.pdf
├── python-data-science-williams.pdf
│
└── <md5_hash>/                  # Cache tự động (không cần tạo thủ công)
    ├── index.faiss
    ├── index.pkl
    ├── manifest.json
    └── metadata.json
```

### Cơ Chế Cache Thông Minh

Hệ thống tự động tạo cache dựa trên MD5 hash của nội dung PDF:
- **Same content → Same hash → Reuse cache**: Nội dung giống nhau sẽ dùng lại cache
- **Changed content → Different hash → Rebuild**: Nội dung thay đổi sẽ rebuild
- **Filename không quan trọng**: Chỉ nội dung file quyết định cache

**Ví dụ:**
```
DKM-PDFs/
├── nasa-P10.pdf                              # PDF gốc
└── a2d63589ec2fa16130d3dd48319694c5/        # Cache (MD5 hash)
    ├── index.faiss                           # Vector index
    ├── index.pkl                             # Metadata
    ├── manifest.json                         # Build info
    └── metadata.json                         # Training info
```

## 🔧 Multi-Train: Training PDFs

### Khi Nào Cần Training?

- **Lần đầu tiên**: Khi thêm PDF mới vào DKM-PDFs
- **PDF thay đổi**: Khi cập nhật nội dung PDF
- **Force rebuild**: Khi muốn rebuild toàn bộ cache

### Cách Sử Dụng

```bash
cd /home/fong/Projects/mini-rag/multi-train

# 1. Train tất cả PDFs (auto-skip nếu đã trained)
./main-train-352179ea6e15.sh

# 2. Force rebuild tất cả
./main-train-352179ea6e15.sh --force-rebuild

# 3. List cache hiện tại
./main-train-352179ea6e15.sh --list-cache

# 4. Custom directories
./main-train-352179ea6e15.sh \
  --pdf-dir /path/to/pdfs \
  --cache-dir /path/to/cache
```

### Output Example

```
Mini-RAG Training System
Log file: /path/to/logs/train_20251022_181234.log

Configuration:
  PDF directory: /home/fong/Projects/mini-rag/DKM-PDFs
  Cache directory: /home/fong/Projects/mini-rag/DKM-PDFs
  Force rebuild: False

Found 5 PDF file(s)

⚡ Cache hit: nasa-P10.pdf (0.05s)
🔧 Training: python-data-science-williams.pdf
✓ Trained: python-data-science-williams.pdf (12.34s)

┌──────────────────────────────────┬───────────┬──────────┐
│ PDF                              │ Status    │ Time (s) │
├──────────────────────────────────┼───────────┼──────────┤
│ nasa-P10.pdf                     │ ⚡ Cached │     0.05 │
│ python-data-science-williams.pdf │ ✓ Trained │    12.34 │
└──────────────────────────────────┴───────────┴──────────┘

Statistics:
  Cached: 3
  Newly trained: 2
  Failed: 0
  Total time: 45.67s
```

### Performance

| Scenario | Lần Đầu | Lần Sau (Cached) | Speedup |
|----------|---------|------------------|---------|
| 5 PDFs   | 67.89s  | 0.25s           | 271x    |
| 1 PDF    | 13.58s  | 0.05s           | 271x    |

## 🔍 Multi-Query: Query Song Song

### ⭐ Ưu Tiên Sử Dụng: `run-multiquery.sh` với JSON

```bash
cd /home/fong/Projects/mini-rag/multi-query
```

#### 1. List Available Sources

```bash
./run-multiquery.sh --list-sources

# Output:
┌────┬─────────────────────┬───────────┬──────────────────────────┐
│No. │ Source Name         │ PDF Count │ Path                     │
├────┼─────────────────────┼───────────┼──────────────────────────┤
│  1 │ DKM-PDFs-cache1     │         1 │ /path/to/cache1          │
│  2 │ DKM-PDFs-cache2     │         1 │ /path/to/cache2          │
└────┴─────────────────────┴───────────┴──────────────────────────┘
```

#### 2. Query với JSON String (Recommended)

```bash
# Query đơn giản
./run-multiquery.sh --json '{"queries":["What is SOLID principle?"]}'

# Multiple queries
./run-multiquery.sh --json '{"queries":["What is SOLID?","Explain DRY","What is KISS?"]}'

# Với external sources
./run-multiquery.sh --json '{
  "queries":["Laravel best practices"],
  "external_sources":["/home/fong/Projects/RAGs/laravel-books"]
}'
```

#### 3. Query với JSON File

```bash
# Tạo file queries.json
cat > my-queries.json << 'EOF'
{
  "queries": [
    "What is SOLID principle?",
    "Explain clean code practices",
    "What are design patterns?"
  ],
  "external_sources": [
    "/home/fong/Projects/RAGs/laravel-books",
    "/home/fong/Projects/RAGs/python-cleancode"
  ]
}
EOF

# Sử dụng file
./run-multiquery.sh --json-file my-queries.json
```

#### 4. Advanced Options

```bash
# Tăng số workers và timeout
./run-multiquery.sh \
  --json '{"queries":["Complex question?"]}' \
  --max-workers 8 \
  --timeout 60 \
  --top-k 6

# Custom output location
./run-multiquery.sh \
  --json '{"queries":["Question?"]}' \
  --output /path/to/custom_output.md
```

### Query Examples

#### ✅ Good Queries (Ngắn gọn, đơn giản)

```json
{
  "queries": [
    "What is SOLID principle?",
    "Explain DRY principle",
    "What is KISS principle?",
    "What are design patterns?",
    "How to implement repository pattern?",
    "What is dependency injection?"
  ]
}
```

#### ❌ Bad Queries (Phức tạp, lồng ghép logic)

```json
{
  "queries": [
    "Compare SOLID vs DRY and explain how they relate to KISS principle in context of microservices architecture with examples from Laravel and Django",
    "What are the differences between factory pattern, abstract factory, and builder pattern, and when should I use each one in a RESTful API?",
    "Explain how dependency injection works in Laravel compared to Symfony and discuss pros/cons of each approach"
  ]
}
```

**Tại sao nên tránh queries phức tạp?**
- Retrieval system có thể không tìm được relevant contexts
- Kết quả bị fragmented và không focused
- LLM khó tổng hợp thông tin từ nhiều nguồn khác nhau
- Accuracy giảm đi đáng kể

**Giải pháp:**
- Break down thành nhiều queries đơn giản
- Mỗi query tập trung 1 khái niệm/vấn đề
- Tổng hợp kết quả sau khi có answers riêng lẻ

### Output Format

Kết quả được lưu tại: `/home/fong/Projects/mini-rag/results/multirag_YYYYMMDD_HHMMSS.md`

```markdown
# Multi-RAG Query Results

## Query 1: What is SOLID principle?

### Sources Queried
- ✅ **DKM-PDFs-cache1** (2.34s)
- ✅ **DKM-PDFs-cache2** (3.12s)
- ✅ **laravel-books** (2.89s)

### Aggregated Results

#### Result 1
**Sources:** DKM-PDFs-cache1, laravel-books
**Content:**
[Retrieved content về SOLID principle...]

#### Result 2
**Source:** DKM-PDFs-cache2
**Content:**
[More content về SOLID...]

### Answer
[LLM-generated answer dựa trên aggregated results]

---

## Query 2: Explain clean code practices

[Similar structure for each query...]

---

## Execution Statistics
- **Total queries:** 3
- **Total time:** 15.67s
- **Sources queried:** 5
- **Results found:** 24
- **Duplicates removed:** 6
```

### Configuration Options

#### Environment Variables

```bash
export MULTI_RAG_BASE_DIR="/home/fong/Projects/mini-rag/DKM-PDFs"
export MULTI_RAG_WORKERS=4        # Parallel workers
export MULTI_RAG_TOP_K=4          # Results per source
export MULTI_RAG_TIMEOUT=30       # Timeout per source (seconds)
export CHUNK_SIZE=1200            # Chunk size for splitting
export CHUNK_OVERLAP=150          # Overlap between chunks
```

#### CLI Options

```bash
--json STRING              # JSON string với queries
--json-file PATH          # Path to JSON file
--list-sources            # List available sources
--base-dir PATH           # Base directory cho PDFs
--max-workers N           # Number of parallel workers (default: 4)
--top-k N                 # Top K results per source (default: 4)
--timeout N               # Timeout per source in seconds (default: 30)
--output PATH             # Output file path
```

## 🎯 Best Practices

### 1. Query Design

**DO ✅:**
- Viết queries ngắn gọn, tập trung 1 concept
- Sử dụng câu hỏi đơn giản, rõ ràng
- Break down complex questions thành nhiều queries đơn giản
- Dùng proper terminology trong domain

**DON'T ❌:**
- Queries quá dài (>15 words)
- Lồng ghép nhiều sub-questions trong 1 query
- So sánh/contrast nhiều concepts cùng lúc
- Queries với nhiều điều kiện IF/ELSE logic

### 2. Source Management

**Training:**
- Train PDFs trước khi query lần đầu
- Reuse cache cho queries tiếp theo
- Force rebuild khi PDF content thay đổi

**Organization:**
- Group related PDFs trong cùng folder
- Sử dụng external_sources cho RAG systems khác
- Maintain clear naming convention

### 3. Performance Optimization

**Parallel Workers:**
- Default: 4 workers (good for most cases)
- CPU-bound: Tăng lên 6-8 workers
- I/O-bound: Có thể tăng lên 10-12 workers

**Timeouts:**
- Default: 30 seconds (sufficient cho most PDFs)
- Large PDFs (>100MB): Tăng lên 60-90 seconds
- Many sources: Set timeout cao hơn để tránh partial failures

**Top-K:**
- Default: 4 results per source (balanced)
- Simple queries: 2-3 results
- Complex queries: 6-8 results (but keep queries simple!)

### 4. Troubleshooting

#### No sources found
```bash
# Check directory
ls -la /home/fong/Projects/mini-rag/DKM-PDFs/

# Verify cache structure
find /home/fong/Projects/mini-rag/DKM-PDFs/ -name "index.faiss"
```

#### Timeout errors
```bash
# Increase timeout
./run-multiquery.sh --json '{"queries":["Q?"]}' --timeout 60

# Reduce workers (less contention)
./run-multiquery.sh --json '{"queries":["Q?"]}' --max-workers 2
```

#### Import errors
```bash
# Verify venv
which python
# Should be: /home/fong/Projects/mini-rag/venv/bin/python

# Check dependencies
pip list | grep -E "langchain|faiss|sentence-transformers"
```

#### Poor results quality
- **Simplify queries**: Break down complex questions
- **Increase top-k**: Get more contexts
- **Check PDF content**: Verify PDFs contain relevant info
- **Retrain PDFs**: Force rebuild cache

## 📊 Complete Workflow Example

### Scenario: Query Laravel Best Practices

```bash
# Step 1: Ensure PDFs are trained
cd /home/fong/Projects/mini-rag/multi-train
./main-train-352179ea6e15.sh

# Step 2: List available sources
cd /home/fong/Projects/mini-rag/multi-query
./run-multiquery.sh --list-sources

# Step 3: Create queries file
cat > laravel-queries.json << 'EOF'
{
  "queries": [
    "What is repository pattern in Laravel?",
    "How to implement service layer in Laravel?",
    "What are Laravel naming conventions?",
    "How to structure large Laravel applications?"
  ],
  "external_sources": [
    "/home/fong/Projects/RAGs/laravel-books"
  ]
}
EOF

# Step 4: Run queries
./run-multiquery.sh --json-file laravel-queries.json

# Step 5: Check results
ls -lh /home/fong/Projects/mini-rag/results/multirag_*.md
cat /home/fong/Projects/mini-rag/results/multirag_$(date +%Y%m%d)_*.md
```

## 🔗 Integration với External RAG Systems

### Sử dụng External Sources

External sources phải có cấu trúc `.mini_rag_index/`:

```
/home/fong/Projects/RAGs/laravel-books/
├── *.pdf                        # PDFs (optional)
└── .mini_rag_index/            # Required!
    ├── index.faiss
    ├── index.pkl
    └── manifest.json
```

### Example với Multiple External Sources

```bash
./run-multiquery.sh --json '{
  "queries": [
    "What is clean code?",
    "What are SOLID principles?",
    "What is dependency injection?"
  ],
  "external_sources": [
    "/home/fong/Projects/RAGs/python-cleancode",
    "/home/fong/Projects/RAGs/java-design-patterns",
    "/home/fong/Projects/RAGs/laravel-books"
  ]
}'
```

## 📈 Performance Benchmarks

### Training Performance (multi-train)

| PDFs | Size | First Run | Cached | Speedup |
|------|------|-----------|--------|---------|
| 5    | ~50MB | 67.89s   | 0.25s  | 271x   |
| 10   | ~100MB | 135.34s  | 0.48s  | 281x   |
| 20   | ~200MB | 278.12s  | 0.92s  | 302x   |

### Query Performance (multi-query)

| Sources | Workers | Query Time | Results |
|---------|---------|------------|---------|
| 3       | 4       | 5.67s     | 12      |
| 5       | 4       | 8.34s     | 20      |
| 5       | 8       | 5.12s     | 20      |
| 10      | 8       | 12.45s    | 40      |

## 🛠 Technical Details

### Architecture

- **Training**: Hash-based caching với MD5
- **Query**: ThreadPoolExecutor parallel execution
- **Deduplication**: MD5-based content matching
- **Vector Store**: FAISS với sentence-transformers
- **LLM**: OpenAI GPT-4o-mini (hoặc offline mode)

### Dependencies

```
langchain
faiss-cpu
sentence-transformers
rich
pypdf
openai (optional)
```

### Shared Virtual Environment

Both `multi-train` và `multi-query` share cùng venv:

```
/home/fong/Projects/mini-rag/venv/
```

## 📝 Summary

### Quick Commands

```bash
# Training
cd /home/fong/Projects/mini-rag/multi-train
./main-train-352179ea6e15.sh

# List sources
cd /home/fong/Projects/mini-rag/multi-query
./run-multiquery.sh --list-sources

# Query (JSON string - RECOMMENDED)
./run-multiquery.sh --json '{"queries":["What is SOLID?"]}'

# Query (JSON file)
./run-multiquery.sh --json-file example-queries.json

# Query with options
./run-multiquery.sh \
  --json '{"queries":["Question?"]}' \
  --max-workers 8 \
  --timeout 60
```

### Key Points

1. **Always use JSON format** for queries (JSON string hoặc JSON file)
2. **Keep queries simple** - ngắn gọn, 1 concept per query
3. **Avoid complex queries** - no nested logic, no comparisons
4. **Prioritize `run-multiquery.sh`** - wrapper script handles venv
5. **Cache is automatic** - based on PDF content MD5 hash
6. **PDFs location**: `/home/fong/Projects/mini-rag/DKM-PDFs/`
7. **Results location**: `/home/fong/Projects/mini-rag/results/`
8. **Logs location**: `/home/fong/Projects/mini-rag/logs/`

## 🆘 Support

### Documentation

- Multi-query: `/home/fong/Projects/mini-rag/multi-query/README.md`
- Multi-train: `/home/fong/Projects/mini-rag/multi-train/README.md`
- Main project: `/home/fong/Projects/mini-rag/README.md`

### Common Issues

1. **No sources found**: Check DKM-PDFs structure, run training first
2. **Timeout errors**: Increase `--timeout`, reduce `--max-workers`
3. **Poor results**: Simplify queries, increase `--top-k`
4. **Import errors**: Verify venv activation

### Contact

Check project documentation in `/home/fong/Projects/mini-rag/` for more details.
