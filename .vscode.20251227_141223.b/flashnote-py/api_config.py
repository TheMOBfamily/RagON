#!/usr/bin/env python3
"""
Module cấu hình API cho FlashNote
Cung cấp hàm kiểm tra môi trường development/production
"""

import requests
import os
import socket

# Cấu hình domain mặc định
DEV_DOMAIN = "http://localhost:3000"
PROD_DOMAIN = "https://flashnote.nexiumlab.com"

# Cho phép override thông qua biến môi trường
ENV_DOMAIN = os.environ.get("FLASHNOTE_API_DOMAIN")

# Giảm timeout cho kiểm tra nhanh
SOCKET_TIMEOUT = 0.5  # 500ms là đủ để kiểm tra cổng localhost
CACHE_RESULT = None  # Cache kết quả kiểm tra

def check_server_available(url, timeout=SOCKET_TIMEOUT):
    """
    Kiểm tra nhanh xem server có đang hoạt động không

    Args:
        url (str): URL cần kiểm tra
        timeout (float): Thời gian chờ tối đa (giây)

    Returns:
        bool: True nếu server hoạt động, False nếu không
    """
    # Phân tích URL để lấy host và port
    from urllib.parse import urlparse
    parsed_url = urlparse(url)

    # Kiểm tra chỉ cổng mạng cho localhost
    hostname = parsed_url.hostname
    port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)

    # Nếu là localhost, chỉ kiểm tra socket
    if hostname == 'localhost' or hostname == '127.0.0.1':
        try:
            # Thử kết nối trực tiếp đến cổng - cách nhanh nhất
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((hostname, port))
            s.close()
            return True
        except (socket.timeout, socket.error, ConnectionRefusedError):
            return False

    # Đối với các domain khác, dùng phương thức HEAD
    try:
        response = requests.head(url, timeout=timeout)
        return response.status_code < 400
    except requests.RequestException:
        return False

def get_api_domain():
    """
    Xác định domain API dựa trên tính khả dụng của server development

    Thứ tự ưu tiên:
    1. Biến môi trường FLASHNOTE_API_DOMAIN (nếu được đặt)
    2. Kiểm tra localhost nếu đang chạy
    3. Sử dụng domain production

    Returns:
        str: Domain của API (dev hoặc prod)
    """
    global CACHE_RESULT

    # Sử dụng kết quả cache nếu đã kiểm tra trước đó
    if CACHE_RESULT is not None:
        return CACHE_RESULT

    # Ưu tiên 1: Kiểm tra biến môi trường
    if ENV_DOMAIN:
        CACHE_RESULT = ENV_DOMAIN
        print(f"Sử dụng domain từ biến môi trường: {ENV_DOMAIN}")
        return CACHE_RESULT

    # Ưu tiên 2: Kiểm tra môi trường development (chỉ kiểm tra một lần)
    if check_server_available(DEV_DOMAIN, timeout=SOCKET_TIMEOUT):
        CACHE_RESULT = DEV_DOMAIN
        print("Môi trường development được phát hiện, sử dụng localhost...")
        return CACHE_RESULT

    # Ưu tiên 3: Mặc định sử dụng production
    CACHE_RESULT = PROD_DOMAIN
    print("Môi trường development không khả dụng, sử dụng server production...")
    return CACHE_RESULT

def get_api_endpoint():
    """
    Tạo endpoint đầy đủ từ domain

    Returns:
        str: URL đầy đủ của API endpoint
    """
    domain = get_api_domain()
    return f"{domain}/api/notes"
