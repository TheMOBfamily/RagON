#!/usr/bin/env python3
"""
Script kiểm tra kết nối localhost đơn giản
"""

import sys
import os
import socket
import requests

def check_local_port(port=3000, timeout=2):
    """Kiểm tra cổng localhost có đang mở không"""
    try:
        print(f"Đang kiểm tra cổng localhost:{port}...")
        with socket.create_connection(('localhost', port), timeout=timeout) as sock:
            print(f"✅ THÀNH CÔNG: Cổng {port} đang mở trên localhost")
            return True
    except (socket.timeout, socket.error, ConnectionRefusedError) as e:
        print(f"❌ LỖI: Không kết nối được đến localhost:{port}")
        print(f"Chi tiết lỗi: {str(e)}")
        return False

def check_local_http(port=3000, timeout=2):
    """Kiểm tra HTTP request đến localhost"""
    url = f"http://localhost:{port}"
    try:
        print(f"Đang gửi HTTP GET request đến {url}...")
        response = requests.get(url, timeout=timeout)
        print(f"✅ THÀNH CÔNG: HTTP request đến {url} trả về: {response.status_code}")
        return True
    except requests.RequestException as e:
        print(f"❌ LỖI: HTTP request đến {url} thất bại")
        print(f"Chi tiết lỗi: {str(e)}")
        return False

def main():
    """Hàm chính"""
    print("=== KIỂM TRA MÔI TRƯỜNG DEVELOPMENT ===")

    # Kiểm tra cổng 3000
    port_check = check_local_port(3000)

    # Kiểm tra HTTP request
    http_check = check_local_http(3000)

    # Kết luận
    print("\n=== KẾT LUẬN ===")
    if port_check and http_check:
        print("✅ Môi trường development đang chạy và có thể kết nối được")
        print("✅ Script nên sử dụng localhost:3000")
    elif port_check and not http_check:
        print("⚠️ Cổng 3000 đang mở nhưng không phản hồi HTTP request")
        print("⚠️ Kiểm tra xem ứng dụng có đang chạy đúng cách không")
    else:
        print("❌ Môi trường development không chạy hoặc không thể kết nối")
        print("❌ Script sẽ sử dụng server production")

    print("\nMẹo: Đảm bảo rằng server development đang chạy trước khi chạy script")

if __name__ == "__main__":
    main()
