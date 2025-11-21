# 🔍 Phân Tích Kiến Trúc: run-multiquery.sh vs run.sh

**Date:** 2025-11-20
**Mục đích:** Giải thích logic query theo hash và so sánh với run.sh

---

## 📊 Kết Quả Test Thực Tế (MCP NewRAG)

| Test Case | Time | Delta vs 1-hash | Sources | Chunks |
|-----------|------|-----------------|---------|--------|
| **1 hash** | 5.4s | baseline | 1/1 | 3 |
| **9 hash** | 6.67s | +1.27s (+23.5%) | 9/9 | 27 |
| **30 hash** | 6.8s | +1.4s (+25.9%) | 30/30 | 90 |

### 📈 Phát Hiện Quan Trọng:

**✅ ĐÚNG như em nói:**
- Load 30 books CHỈ CHẬM HƠN 1 book khoảng **1.4 giây**!
- **KHÔNG phải 30× slower** như trước khi optimize
- Tốc độ GẦN NHƯ TUYẾN TÍNH (linear scaling)

**Nhưng có khác biệt với benchmark lúc trước:**
- Benchmark shell script: 1 hash (2.969s), 30 hash (3.067s) → delta **0.098s**
- MCP NewRAG: 1 hash (5.4s), 30 hash (6.8s) → delta **1.4s**

→ **Tại sao?** Đọc tiếp phần kiến trúc bên dưới.

---

## 🏗️ Kiến Trúc: run-multiquery.sh

### Flow Execution:

```
run-multiquery.sh
  ↓
main-d1f454371402.py
  ↓
filter_sources_by_hashes()  [line 298-306]
  ↓ (filter N hash IDs)
query_all_sources_parallel()  [line 332]
  ↓
ProcessPoolExecutor (max_workers=4)  [parallel_query.py:96]
  ↓
[Process 1]  [Process 2]  [Process 3]  [Process 4]
    ↓            ↓            ↓            ↓
query_single_source()  (mỗi process 1 source)
    ↓
load_vectorstore_from_path()
    ↓
- Load embeddings (5.6s RIÊNG từng process!)
- Load FAISS index (0.022s)
    ↓
get_context_standalone()
```

### ⚠️ Vấn Đề Với ProcessPoolExecutor:

**Mỗi process có memory space RIÊNG:**
- Process 1: Load embeddings (5.6s) → Query source 1
- Process 2: Load embeddings (5.6s) → Query source 2  ← KHÔNG reuse được!
- Process 3: Load embeddings (5.6s) → Query source 3
- Process 4: Load embeddings (5.6s) → Query source 4

**Embeddings singleton CHỈ work TRONG process!**

→ **max_workers=4** → Tối đa 4 processes load embeddings song song
→ **30 sources** → Chia làm 8 batch (30/4 = 7.5)
→ Mỗi batch load embeddings → Tổng ~8× embeddings load

---

## 🔄 So Sánh: run-multiquery.sh vs run.sh

### A. run.sh (Single Folder Query)

**Use case:** Query 1 folder chứa nhiều PDFs (đã merge thành 1 FAISS index)

```
run.sh "Question" /path/to/DKM-PDFs
  ↓
RagON API (persistent service)
  ↓
Load embeddings 1 LẦN (persist trong service)
  ↓
Load FAISS index đã MERGE (1 file lớn)
  ↓
Query 1 lần → Return
```

**Đặc điểm:**
- ✅ **1 merged index** (tất cả PDFs gộp thành 1)
- ✅ **Embeddings loaded 1 lần** (persistent service)
- ✅ **Query 1 lần duy nhất**
- ⚠️ **Phải merge trước** (time-consuming)

### B. run-multiquery.sh (Multi-Hash Query)

**Use case:** Query nhiều hashes (mỗi hash = 1 PDF riêng biệt với FAISS index riêng)

```
run-multiquery.sh --source-hashes "hash1,hash2,...,hash30"
  ↓
ProcessPoolExecutor (4 workers)
  ↓
[Process 1]     [Process 2]     [Process 3]     [Process 4]
Query hash1     Query hash5     Query hash9     Query hash13
Query hash2     Query hash6     Query hash10    Query hash14
Query hash3     Query hash7     Query hash11    Query hash15
Query hash4     Query hash8     Query hash12    Query hash16
...             ...             ...             ...
```

**Đặc điểm:**
- ✅ **N separate indices** (mỗi PDF = 1 index riêng)
- ⚠️ **Embeddings loaded nhiều lần** (mỗi process load riêng)
- ✅ **Query parallel** (4 workers song song)
- ✅ **KHÔNG cần merge** (query trực tiếp)

---

## 📐 Logic Query Theo Hash

### Câu Hỏi: Có GỘP index không?

**❌ KHÔNG GỘP!** Mỗi hash query RIÊNG LẺ:

```python
# Không có merge, chỉ có filter
all_sources = discover_sources(base_dir)  # Find all indices
all_sources = filter_sources_by_hashes(all_sources, hash_list)  # Filter by hash

# Query mỗi source RIÊNG (parallel)
for source in all_sources:
    query_single_source(source, query, top_k)
```

### Câu Hỏi: Tương tự run.sh cho từng folder?

**⚠️ KHÁC NHAU:**

| Aspect | run.sh | run-multiquery.sh |
|--------|--------|-------------------|
| **Index structure** | 1 merged index | N separate indices |
| **Embeddings load** | 1 lần (persistent) | N lần (per process) |
| **Query strategy** | 1 query trên merged index | N queries parallel |
| **Speed (1 source)** | Fast (persistent embeddings) | Slower (load embeddings) |
| **Speed (30 sources)** | N/A (phải merge 30 sources trước) | ~6.8s (parallel) |
| **Use case** | Query tập trung trên 1 collection | Query rải rác nhiều books |

**Analogy:**
- `run.sh`: Đọc 1 cuốn ENCYCLOPEDIA lớn (merged)
- `run-multiquery.sh`: Đọc 30 cuốn sách NHỎ song song (separate)

---

## 🧪 Tại Sao Benchmark Khác Với MCP NewRAG?

### Benchmark shell script lúc trước:
```bash
# Direct execution trong cùng shell
test-optimization.sh
  ↓
run-multiquery.sh (gọi 3 lần tuần tự)
  ↓
1 hash: 2.969s
9 hash: 3.043s  (+0.074s)
30 hash: 3.067s (+0.098s)
```

→ **Tại sao nhanh?** Có thể do:
1. OS page cache đã warm lên sau lần 1
2. Python processes được reuse
3. Embeddings model được cache bởi OS

### MCP NewRAG (qua Node.js server):
```
MCP call → Node.js server → Python subprocess → ProcessPoolExecutor
  ↓
1 hash: 5.4s
9 hash: 6.67s  (+1.27s)
30 hash: 6.8s  (+1.4s)
```

→ **Tại sao chậm hơn?**
1. Overhead từ Node.js → Python
2. Subprocess spawning time
3. ProcessPoolExecutor khởi tạo workers
4. Embeddings load nhiều lần (không share giữa processes)

---

## ✅ Kết Luận

### 1. Logic Query Theo Hash:
- ❌ **KHÔNG gộp index** - mỗi hash query riêng
- ✅ **Query SONG SONG** - ProcessPoolExecutor (4 workers)
- ⚠️ **Embeddings load NHIỀU lần** - mỗi process riêng

### 2. So Sánh Với run.sh:
- `run.sh`: 1 merged index, embeddings persistent, query 1 lần
- `run-multiquery.sh`: N separate indices, embeddings reload, query N lần parallel

### 3. Performance Thực Tế:
- ✅ **Đúng như em nói**: 30 books chỉ chậm hơn 1 book ~1.4s
- ✅ **Linear scaling**: Không phải exponential
- ⚠️ **Bottleneck**: Embeddings load (giải quyết bằng persistent service)

### 4. Embeddings Service Optimization:
- ✅ **Work TRONG process**: Singleton pattern hiệu quả
- ❌ **Không work GIỮA processes**: ProcessPoolExecutor không share memory
- 💡 **Giải pháp**: Chuyển sang persistent service (như RagON) để reuse embeddings

---

## 🚀 Đề Xuất Tối Ưu Hóa Tiếp

### Short-term (Quick win):
1. **Tăng max_workers** → Giảm số batch → Ít embeddings reload hơn
2. **Pre-warm embeddings** → Load trước khi fork processes

### Long-term (Architecture change):
1. **Persistent embeddings service** → Load embeddings 1 lần, reuse cho mọi query
2. **Shared memory embeddings** → Use mmap hoặc shared memory
3. **ThreadPoolExecutor** → Share embeddings (nếu thread-safe)

---

**Tóm tắt:** `run-multiquery.sh` KHÔNG gộp index, query từng hash RIÊNG SONG SONG qua ProcessPoolExecutor. Performance tốt (30 books ~6.8s) nhưng vẫn có overhead từ embeddings reload nhiều lần do multi-process architecture.
