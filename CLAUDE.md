# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Mô tả dự án

Mini RAG (Retrieval Augmented Generation) - hệ thống hỏi đáp trên tài liệu PDF sử dụng LangChain, FAISS và OpenAI/HuggingFace.

## Cấu trúc kiến trúc

### Kiến trúc modular theo pipeline:
- **loader.py**: Nạp PDF từ thư mục bằng PyPDFLoader
- **splitter.py**: Chia tài liệu thành chunks với RecursiveCharacterTextSplitter
- **embedder.py**: Xử lý embeddings (OpenAI hoặc HuggingFace)
- **vectorstore.py**: Quản lý FAISS vector store với persistence thông minh
- **pipeline.py**: Chain cuối cùng từ retrieval đến answer generation
- **config.py**: Centralized settings với env vars
- **utils.py**: Utilities (timing, logging, etc.)

### Cache mechanism thông minh:
Vector store được cache trong `.mini_rag_index/` với manifest.json tracking MD5 hashes. Chỉ rebuild khi:
- PDF thêm/xóa
- MD5 hash thay đổi  
- Index/manifest bị thiếu

## Lệnh thường dùng

### Setup môi trường:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Chạy ứng dụng:
```bash
python main-minirag.py "Câu hỏi?" /absolute/path/to/pdf_folder
```

### Test với example folder:
```bash
python main-minirag.py "Nội dung chính là gì?" $(pwd)/example
```

## Biến môi trường

Tham khảo `.env.example`:
- `EMBEDDINGS_MODEL`: "openai" hoặc "huggingface" (default: huggingface)
- `OPENAI_API_KEY`: Bắt buộc nếu dùng OpenAI
- `HUGGINGFACEHUB_API_TOKEN`: Cho HuggingFace models
- `HF_EMBEDDINGS_MODEL_NAME`: Default "sentence-transformers/all-MiniLM-L6-v2"
- `OPENAI_MODEL_NAME`: Default "gpt-4o-mini"
- `CHUNK_SIZE`: Default 1200
- `CHUNK_OVERLAP`: Default 150
- `TOP_K`: Default 4

## Patterns quan trọng

### Error handling:
- Fallback offline mode khi không có OPENAI_API_KEY
- Graceful validation trong config.py
- Path validation (requires absolute paths)

### Metadata tracking:
- `source_file` trong Document metadata
- File state tracking với md5, size, mtime
- Version tracking trong manifest

### Performance optimization:
- Streaming file hashing
- Intelligent cache invalidation
- Lazy loading vector store

## Nguyên tắc phát triển

- Mỗi module < 150 dòng code
- Type hints với `from __future__ import annotations`
- Rich console output cho UX tốt hơn
- Tách biệt concerns: loading → splitting → embedding → retrieval → generation