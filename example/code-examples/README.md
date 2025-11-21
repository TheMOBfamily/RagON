# Mini-RAG Code Examples

Thư mục này chứa các example scripts để demonstrate cách sử dụng Mini-RAG system.

## Files

- `run_minirag_example.py`: Script Python để chạy main-minirag.py với PDF documents
- `README.txt`: Hướng dẫn cơ bản (legacy)

## Usage

### Chạy với câu hỏi cụ thể:
```bash
python run_minirag_example.py "Nội dung chính của các tài liệu là gì?"
```

### Chạy interactive mode:
```bash
python run_minirag_example.py
```

## How it works

Script sẽ:
1. Tự động tìm đường dẫn đến `main-minirag.py` (ở parent directory)
2. Sử dụng `../pdf-documents/` làm PDF source directory  
3. Chạy main-minirag.py với question và absolute path
4. Hiển thị kết quả trả về

## Requirements

- Python 3.8+
- Đã setup virtual environment và install requirements.txt
- Có ít nhất 1 PDF file trong `../pdf-documents/`

## Notes

- Script tự động convert relative paths thành absolute paths
- Vector store và manifest.json sẽ được tạo trong pdf-documents folder
- Caching mechanism sẽ hoạt động tự động based on file changes