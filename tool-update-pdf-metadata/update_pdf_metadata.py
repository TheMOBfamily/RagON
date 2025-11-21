#!/usr/bin/env python3
"""
Script để update manifest.json và metadata.json khi rename file PDF
Chỉ update theo chuẩn, không sửa xóa gì thư mục

Usage:
    python update_pdf_metadata.py

Hoặc chạy với file cụ thể:
    python update_pdf_metadata.py <path_to_pdf>
"""

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional


def calculate_md5(file_path: Path) -> str:
    """Tính MD5 hash của file PDF"""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        # Đọc file theo chunks để xử lý file lớn
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def find_hash_folder(base_dir: Path, file_hash: str) -> Optional[Path]:
    """Tìm folder hash tương ứng với file hash"""
    hash_folder = base_dir / file_hash
    if hash_folder.exists() and hash_folder.is_dir():
        return hash_folder
    return None


def update_manifest_json(manifest_path: Path, old_filename: str, new_filename: str) -> bool:
    """Update manifest.json với tên file mới"""
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # Tìm entry cũ bằng hash matching
        files = manifest.get('files', {})
        file_data = None
        
        # Tìm entry với hash khớp (vì tên file có thể đã thay đổi)
        for filename, data in files.items():
            # Nếu tìm thấy entry cũ
            if filename == old_filename:
                file_data = data
                del files[filename]
                break
        
        if file_data is None:
            # Nếu không tìm thấy old_filename, có thể đã được update rồi
            # hoặc chưa có trong manifest
            return False
        
        # Thêm entry mới với tên file mới
        files[new_filename] = file_data
        manifest['files'] = files
        
        # Ghi lại file
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"❌ Lỗi update manifest.json: {e}")
        return False


def update_metadata_json(metadata_path: Path, new_filename: str) -> bool:
    """Update metadata.json với tên file mới"""
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Update filename
        metadata['filename'] = new_filename
        
        # Ghi lại file
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"❌ Lỗi update metadata.json: {e}")
        return False


def get_old_filename_from_metadata(metadata_path: Path) -> Optional[str]:
    """Lấy tên file cũ từ metadata.json"""
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        return metadata.get('filename')
    except Exception as e:
        print(f"❌ Lỗi đọc metadata.json: {e}")
        return None


def process_pdf_file(pdf_path: Path, base_dir: Path) -> bool:
    """Xử lý một file PDF"""
    print(f"\n🔍 Xử lý: {pdf_path.name}")
    
    # 1. Tính MD5 hash
    print("  ⏳ Đang tính MD5 hash...")
    file_hash = calculate_md5(pdf_path)
    print(f"  ✓ Hash: {file_hash}")
    
    # 2. Tìm folder hash
    hash_folder = find_hash_folder(base_dir, file_hash)
    if not hash_folder:
        print(f"  ⚠️  Không tìm thấy folder hash: {file_hash}")
        return False
    
    print(f"  ✓ Tìm thấy folder: {hash_folder.name}")
    
    # 3. Đọc tên file cũ từ metadata
    metadata_path = hash_folder / "metadata.json"
    manifest_path = hash_folder / "manifest.json"
    
    if not metadata_path.exists():
        print(f"  ⚠️  Không tìm thấy metadata.json")
        return False
    
    old_filename = get_old_filename_from_metadata(metadata_path)
    if not old_filename:
        print(f"  ⚠️  Không đọc được tên file cũ")
        return False
    
    new_filename = pdf_path.name
    
    # Kiểm tra xem có thay đổi không
    if old_filename == new_filename:
        print(f"  ℹ️  Tên file không đổi, bỏ qua")
        return True
    
    print(f"  📝 Tên cũ: {old_filename}")
    print(f"  📝 Tên mới: {new_filename}")
    
    # 4. Update manifest.json
    if manifest_path.exists():
        print("  ⏳ Đang update manifest.json...")
        if update_manifest_json(manifest_path, old_filename, new_filename):
            print("  ✓ Đã update manifest.json")
        else:
            print("  ⚠️  Không update được manifest.json")
    else:
        print("  ⚠️  Không tìm thấy manifest.json")
    
    # 5. Update metadata.json
    print("  ⏳ Đang update metadata.json...")
    if update_metadata_json(metadata_path, new_filename):
        print("  ✓ Đã update metadata.json")
    else:
        print("  ⚠️  Không update được metadata.json")
        return False
    
    print(f"  ✅ Hoàn thành update cho: {new_filename}")
    return True


def process_all_pdfs(base_dir: Path):
    """Xử lý tất cả file PDF trong thư mục"""
    # Support both .pdf and .PDF extensions
    pdf_files = list(base_dir.glob("*.pdf")) + list(base_dir.glob("*.PDF"))

    if not pdf_files:
        print("⚠️  Không tìm thấy file PDF nào trong thư mục")
        return
    
    print(f"📚 Tìm thấy {len(pdf_files)} file PDF")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for pdf_path in pdf_files:
        try:
            result = process_pdf_file(pdf_path, base_dir)
            if result:
                success_count += 1
            else:
                skip_count += 1
        except Exception as e:
            print(f"❌ Lỗi xử lý {pdf_path.name}: {e}")
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"📊 Tổng kết:")
    print(f"  ✅ Thành công: {success_count}")
    print(f"  ⚠️  Bỏ qua: {skip_count}")
    print(f"  ❌ Lỗi: {error_count}")
    print(f"{'='*60}")


def main():
    """Main function"""
    # Xác định thư mục base - ALWAYS use absolute path
    base_dir = Path("/home/fong/Projects/mini-rag/DKM-PDFs")

    print(f"📂 Thư mục làm việc: {base_dir}")
    
    # Kiểm tra xem có truyền file cụ thể không
    if len(sys.argv) > 1:
        pdf_path = Path(sys.argv[1])
        if not pdf_path.exists():
            print(f"❌ File không tồn tại: {pdf_path}")
            sys.exit(1)
        
        if not pdf_path.suffix.lower() == '.pdf':
            print(f"❌ File không phải PDF: {pdf_path}")
            sys.exit(1)
        
        # Xử lý file cụ thể
        process_pdf_file(pdf_path, base_dir)
    else:
        # Xử lý tất cả file PDF
        process_all_pdfs(base_dir)


if __name__ == "__main__":
    main()
