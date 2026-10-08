"""Kiểm thử CHỨC NĂNG đăng nhập — sheet 'ChucNang' trong file Excel.

Mỗi hàm test tương ứng 1 test case (TCxx) trong bảng test case.
Chạy trên bản mock login (offline, an toàn).
"""
import pytest

pytestmark = pytest.mark.functional


# ===================== NHÓM 1: Ô NHẬP TRỐNG =====================

def test_TC01_bo_trong_ca_hai_o(login_page, config):
    """TC01: để trống cả username và password -> báo nhập đầy đủ, không đăng nhập."""
    login_page.login("", "")
    assert not login_page.is_logged_in(), "Không được đăng nhập khi bỏ trống"
    assert "đầy đủ" in login_page.get_error_text().lower()


def test_TC02_trong_username(login_page, config):
    """TC02: để trống username, có password -> báo nhập đầy đủ."""
    login_page.login("", config.valid_password)
    assert not login_page.is_logged_in()
    assert login_page.get_error_text() != ""


def test_TC03_trong_password(login_page, config):
    """TC03: có username, để trống password -> báo nhập đầy đủ."""
    login_page.login(config.valid_username, "")
    assert not login_page.is_logged_in()
    assert login_page.get_error_text() != ""


# ===================== NHÓM 2: SAI THÔNG TIN ĐĂNG NHẬP =====================

def test_TC04_dung_ten_sai_matkhau(login_page, config):
    """TC04: đúng username, sai password -> thông báo chung, không vào trang chủ."""
    login_page.login(config.valid_username, "sai_mat_khau")
    assert not login_page.is_logged_in()
    assert "không đúng" in login_page.get_error_text().lower()


def test_TC05_sai_ten_dung_matkhau(login_page, config):
    """TC05: sai username, đúng password -> không đăng nhập."""
    login_page.login("nguoi_la", config.valid_password)
    assert not login_page.is_logged_in()
    assert login_page.get_error_text() != ""


def test_TC06_sai_ca_ten_va_matkhau(login_page, config):
    """TC06: sai cả username lẫn password -> không đăng nhập."""
    login_page.login("nguoi_la", "sai_mat_khau")
    assert not login_page.is_logged_in()
    assert login_page.get_error_text() != ""


def test_TC09_matkhau_phan_biet_hoa_thuong(login_page, config):
    """TC09: password đúng ký tự nhưng sai hoa/thường -> đăng nhập thất bại."""
    login_page.login(config.valid_username, config.valid_password.lower())
    assert not login_page.is_logged_in(), "Mật khẩu phải phân biệt hoa/thường"
