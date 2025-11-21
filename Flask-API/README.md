# RagON - RAG Persistent Service

RagON (RAG ON-memory) là FastAPI service giữ FAISS index trong RAM để query cực nhanh (<1s).

## 🎯 Vấn đề giải quyết

**Trước đây (Legacy mode):**
- Mỗi lần query phải load FAISS index từ disk → **15-25 giây**
- Không thể tái sử dụng index đã load
- Không hiệu quả cho multiple queries

**Giờ đây (RagON API mode):**
- Load index 1 lần vào RAM → giữ persistent
- Query tiếp theo: **<1 giây** (cache hit)
- Hỗ trợ multiple PDF directories cùng lúc
- Auto-preload DKM-PDFs khi start

## 🏗️ Kiến trúc

```
┌─────────────────┐
│   Client        │
│  (run.sh)       │
└────────┬────────┘
         │ HTTP POST /query
         ▼
┌─────────────────────────────────┐
│   RagON FastAPI Service         │
│   Port: 2011                    │
├─────────────────────────────────┤
│  In-Memory Cache:               │
│  ┌───────────────────────────┐  │
│  │ INDEX_CACHE               │  │
│  │ {                         │  │
│  │   "/path/to/pdfs": {      │  │
│  │     index: FAISS,         │  │
│  │     loaded_at: datetime   │  │
│  │   }                       │  │
│  │ }                         │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   FAISS VectorStore (disk)      │
│   .mini_rag_index/              │
└─────────────────────────────────┘
```

## 🚀 Cách start service

### 1. Start thủ công

```bash
cd /home/fong/Projects/mini-rag/RagON
./Start-RAG-persistent-service.sh [PORT]
```

Mặc định port: `2011`

### 2. Auto-start (khuyến nghị)

Sử dụng `run.sh` từ project root - service sẽ tự động start nếu chưa chạy:

```bash
cd /home/fong/Projects/mini-rag
./run.sh "câu hỏi của bạn" /path/to/pdfs
```

**Logic auto-start:**
1. Kiểm tra service có đang chạy không (`curl http://localhost:1411`)
2. Nếu không → tự động start service
3. Đợi tối đa 30 giây cho service ready
4. Tiếp tục query

## 📡 API Endpoints

### GET `/`
Kiểm tra service status

**Response:**
```json
{
  "service": "RagON",
  "status": "running",
  "cached_indices": 1,
  "paths": ["/home/fong/Projects/mini-rag/DKM-PDFs"]
}
```

### GET `/cache/stats`
Thống kê cache

**Response:**
```json
{
  "total_cached": 1,
  "indices": [
    {
      "path": "/home/fong/Projects/mini-rag/DKM-PDFs",
      "loaded_at": "2025-11-20T00:45:00.123456",
      "docs_count": 1234
    }
  ]
}
```

### POST `/query`
Query RAG với caching

**Request:**
```json
{
  "pdf_directory": "/home/fong/Projects/mini-rag/DKM-PDFs",
  "question": "SOLID principles là gì?",
  "top_k": 4
}
```

**Response:**
```json
{
  "answer": "[source.pdf] Page 10:\nSOLID principles...",
  "sources": [
    {
      "content": "SOLID principles...",
      "metadata": {
        "source": "source.pdf",
        "page": 10
      }
    }
  ],
  "load_time_seconds": 0.0,
  "retrieval_time_seconds": 0.09,
  "from_cache": true
}
```

### DELETE `/cache/{path}`
Xóa 1 path khỏi cache

```bash
curl -X DELETE http://localhost:1411/cache//home/fong/Projects/mini-rag/example
```

### DELETE `/cache`
Xóa toàn bộ cache

```bash
curl -X DELETE http://localhost:1411/cache
```

## 💾 Cache Mechanism

### Preloading (Startup)
Service tự động load DKM-PDFs vào cache khi start:

```
🚀 RagON Starting...
📦 Preloading DKM-PDFs...
✅ DKM-PDFs loaded in 15.06s
🔥 Cache ready - queries will be <1s
```

### On-demand Loading
Khi query PDF directory mới:

```
⏳ Loading index: /path/to/new/pdfs
✅ Loaded in 18.32s
```

### Cache Hit
Query tiếp theo trên cùng directory:

```
🔥 Cache HIT: /path/to/pdfs
⏱️  Load time: 0.00s
⏱️  Retrieval time: 0.09s
```

## 📊 Performance

| Scenario | Load Time | Retrieval Time | Total |
|----------|-----------|----------------|-------|
| **Cold Start** (lần đầu) | 15-25s | 0.1s | ~15-25s |
| **Cache Hit** (lần sau) | 0.0s | 0.1s | **~0.1s** |

**Tăng tốc: 150-250x** 🚀

## 🛠️ Troubleshooting

### Service không start được

**Lỗi:** `venv not found`
```bash
# Tạo venv
cd /home/fong/Projects/mini-rag
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Lỗi:** `Address already in use`
```bash
# Kill process cũ
ps aux | grep uvicorn | grep 2011 | awk '{print $2}' | xargs kill -9
```

### Cache không hit

**Nguyên nhân:** Path khác nhau (relative vs absolute)

**Giải pháp:**
- Luôn dùng absolute path: `/home/fong/Projects/mini-rag/DKM-PDFs`
- KHÔNG dùng relative path: `./DKM-PDFs` hay `~/Projects/mini-rag/DKM-PDFs`

### Query chậm

**Kiểm tra cache:**
```bash
curl http://localhost:1411/cache/stats
```

**Reload cache:**
```bash
# Xóa cache cũ
curl -X DELETE http://localhost:1411/cache

# Service sẽ reload tự động
```

### Memory cao

RagON giữ FAISS index trong RAM → RAM usage cao là bình thường.

**Ước tính RAM:**
- DKM-PDFs (hundreds of books): ~4-6 GB
- Smaller collections: ~500 MB - 2 GB

**Giải pháp nếu hết RAM:**
```bash
# Xóa cache không dùng
curl -X DELETE http://localhost:1411/cache/path/to/unused/pdfs
```

## 🔗 Integration

### Với run.sh (Khuyến nghị)

```bash
./run.sh "câu hỏi" /path/to/pdfs
```

Auto-start + query + response formatting

### Với curl (Manual)

```bash
# Query (pdf_directory optional - defaults to DKM_PDF_PATH from .env)
curl -X POST http://localhost:1411/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "SOLID principles",
    "top_k": 4
  }' | jq
```

### Với Python

```python
import requests

# pdf_directory optional - defaults to DKM_PDF_PATH from .env
response = requests.post(
    "http://localhost:1411/query",
    json={
        "question": "SOLID principles",
        "top_k": 4
    }
)

result = response.json()
print(f"Answer: {result['answer']}")
print(f"From cache: {result['from_cache']}")
print(f"Time: {result['retrieval_time_seconds']:.2f}s")
```

## 📝 Development

### Structure

```
RagON/
├── src/
│   └── server.py          # FastAPI service
├── Start-RAG-persistent-service.sh
└── README.md
```

### Dependencies

- FastAPI
- uvicorn[standard]
- langchain-community
- Kế thừa từ mini-rag: `src/minirag/`

### Logs

Service chạy với `--reload` → tự động restart khi code thay đổi.

**Xem logs:**
```bash
# Nếu chạy foreground
# Output trực tiếp ra terminal

# Nếu chạy background
tail -f logs/service.log
```

## 🎯 Roadmap

- [ ] WebSocket support cho streaming responses
- [ ] Multi-GPU support cho large collections
- [ ] Cache eviction policy (LRU)
- [ ] Metrics & monitoring (Prometheus)
- [ ] Docker container

## 📄 License

Inherits from mini-rag project.
