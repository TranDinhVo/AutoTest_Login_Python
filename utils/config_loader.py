"""Đọc cấu hình từ config.ini và tính ra URL trang login cần kiểm thử."""
import configparser
import os
from pathlib import Path
from urllib.parse import urlparse

# Thư mục gốc dự án (chứa config.ini, mock_login/, ...)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    def __init__(self, path=None):
        path = path or os.path.join(ROOT_DIR, "config.ini")
        parser = configparser.ConfigParser()
        parser.read(path, encoding="utf-8")
        t = parser["target"]

        self.base_url_raw = t.get("base_url", "MOCK").strip()
        self.valid_username = t.get("valid_username", "student")
        self.valid_password = t.get("valid_password", "Password123")

        self.username_id = t.get("username_id", "username")
        self.password_id = t.get("password_id", "password")
        self.remember_id = t.get("remember_id", "remember")
        self.submit_id = t.get("submit_id", "submit")
        self.error_id = t.get("error_id", "error")

        self.success_url_contains = t.get("success_url_contains", "logged-in-successfully")
        self.headless = t.getboolean("headless", fallback=True)
        self.browser = t.get("browser", "chrome").strip().lower()

        hosts = t.get("security_allowed_hosts", "MOCK,localhost,127.0.0.1")
        self.security_allowed_hosts = [h.strip() for h in hosts.split(",") if h.strip()]

    @property
    def is_mock(self):
        return self.base_url_raw.upper() == "MOCK"

    @property
    def login_url(self):
        """URL thật dùng cho driver.get(). MOCK -> file:// tới mock_login/login.html."""
        if self.is_mock:
            page = os.path.join(ROOT_DIR, "mock_login", "login.html")
            # as_uri() tạo URL file:// đúng chuẩn trên cả Windows và Linux (CI)
            return Path(page).as_uri()
        return self.base_url_raw

    @property
    def target_host(self):
        """Host dùng để kiểm tra chốt an toàn cho test bảo mật."""
        if self.is_mock:
            return "MOCK"
        return urlparse(self.base_url_raw).hostname or ""

    @property
    def security_tests_allowed(self):
        """True nếu được phép chạy test SQLi/XSS trên mục tiêu hiện tại."""
        return self.target_host in self.security_allowed_hosts
