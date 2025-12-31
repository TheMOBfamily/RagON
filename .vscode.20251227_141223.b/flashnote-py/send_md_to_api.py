#!/usr/bin/env python3
r"""
Script để đọc file markdown và gửi nội dung lên API FlashNote
Usage: python send_md_to_api.py "<đường_dẫn_file.md>"

Lưu ý: Đặt đường dẫn trong dấu ngoặc kép nếu có khoảng trắng hoặc ký tự đặc biệt
Ví dụ: python send_md_to_api.py "G:\My Drive\file có dấu.md"
"""

import sys
import json
import requests
import webbrowser
import os
from pathlib import Path
import urllib.parse
import shlex

# Đảm bảo tìm được module api_config trong cùng thư mục với script này
script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

# Import từ module cấu hình API
try:
    from api_config import get_api_domain, get_api_endpoint
    # Sử dụng cấu hình từ module
    API_DOMAIN = get_api_domain()
    API_ENDPOINT = get_api_endpoint()
except ImportError:
    # Fallback nếu không import được module
    print("Cảnh báo: Không thể import module api_config. Sử dụng cấu hình mặc định.")
    # ===== CẤU HÌNH MẶC ĐỊNH =====
    API_DOMAIN = "https://flashnote.nexiumlab.com"  # Mặc định sử dụng production
    API_ENDPOINT = f"{API_DOMAIN}/api/notes"
    # =============================

def normalize_path(file_path):
    """Chuẩn hóa đường dẫn file để xử lý các ký tự đặc biệt và khoảng trắng"""
    try:
        # Xử lý đường dẫn từ command line
        if os.name == 'nt':  # Windows
            # Loại bỏ dấu ngoặc kép nếu có
            file_path = file_path.strip('"')
            # Thay thế dấu \ bằng / để tránh lỗi escape sequence
            file_path = file_path.replace('\\', '/')

        # Chuyển đổi đường dẫn thành Path object
        path = Path(file_path).resolve()
        # Encode URL cho các ký tự đặc biệt nếu cần
        encoded_path = urllib.parse.quote(str(path))
        return path, encoded_path
    except Exception as e:
        print(f"Lỗi khi chuẩn hóa đường dẫn: {e}")
        return None, None

def send_md_to_api(file_path):
    """Đọc nội dung file markdown và gửi lên API"""
    try:
        # Chuẩn hóa đường dẫn
        path_obj, encoded_path = normalize_path(file_path)
        if not path_obj:
            print(f"Lỗi: Không thể xử lý đường dẫn file {file_path}")
            return

        if not path_obj.exists():
            print(f"Lỗi: File {path_obj} không tồn tại.")
            print("Hãy đảm bảo đường dẫn được đặt trong dấu ngoặc kép nếu có khoảng trắng.")
            print('Ví dụ: python send_md_to_api.py "G:/My Drive/file.md"')
            return

        # Đọc nội dung file với encoding UTF-8
        try:
            with open(path_obj, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            # Thử lại với encoding khác nếu UTF-8 thất bại
            with open(path_obj, 'r', encoding='cp1252') as file:
                content = file.read()

        # Chuẩn bị dữ liệu
        payload = {
            'content': content,
            'source_path': str(path_obj)  # Thêm thông tin về nguồn file
        }

        # `Headers`
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }

        # Gửi request
        print(f"Đang gửi nội dung lên API ({API_ENDPOINT})...")
        response = requests.post(API_ENDPOINT, data=json.dumps(payload), headers=headers)

        # Xử lý kết quả
        if response.status_code == 201:
            result = response.json()
            print("Đã tạo note thành công!")
            print(f"ID: {result.get('id')}")

            # Lấy URL từ response hoặc tạo URL từ ID
            note_url = result.get('url') if 'url' in result else f"{API_DOMAIN}/{result.get('id')}"
            print(f"URL: {note_url}")
            print(f"Hết hạn: {result.get('expiresAt')}")

            # Thêm key vào URL nếu chưa có
            if 'key=' not in note_url:
                if '?' in note_url:
                    note_url += '&key=fong'
                else:
                    note_url += '?key=fong'

            # Mở URL trong trình duyệt mặc định
            print("Đang mở URL trong trình duyệt...")
            webbrowser.open(note_url)

            return result
        else:
            print(f"Lỗi: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        return None

def main():
    """Hàm chính"""
    if len(sys.argv) != 2:
        print('Sử dụng: python send_md_to_api.py "<đường_dẫn_file.md>"')
        print('Lưu ý: Đặt đường dẫn trong dấu ngoặc kép nếu có khoảng trắng')
        print('Ví dụ: python send_md_to_api.py "G:/My Drive/file.md"')
        sys.exit(1)

    file_path = sys.argv[1]
    send_md_to_api(file_path)

if __name__ == "__main__":
    main()
