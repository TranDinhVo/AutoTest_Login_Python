"""Kiểm thử CHỨC NĂNG đăng nhập — sheet 'ChucNang' trong file Excel.

Lớp test kế thừa BaseTest (tự khởi tạo WebDriver + mở trang login).
Mỗi method test tương ứng 1 test case (TCxx). Chạy trên mock (offline, an toàn).
"""
import pytest

from base.base_test import BaseTest

pytestmark = pytest.mark.functional


class TestLoginFunctional(BaseTest):

    # ===================== NHÓM 1: Ô NHẬP TRỐNG =====================

    def test_TC01_bo_trong_ca_hai_o(self):
        """TC01: để trống cả username và password -> báo nhập đầy đủ, không đăng nhập."""
        self.login_page.login_as("", "")
        assert not self.login_page.logged_in()
        assert "đầy đủ" in self.login_page.error_message().lower()

    def test_TC02_trong_username(self):
        """TC02: để trống username, có password -> báo nhập đầy đủ."""
        self.login_page.login_as("", self.config.valid_password)
        assert not self.login_page.logged_in()
        assert self.login_page.error_message() != ""

    def test_TC03_trong_password(self):
        """TC03: có username, để trống password -> báo nhập đầy đủ."""
        self.login_page.login_as(self.config.valid_username, "")
        assert not self.login_page.logged_in()
        assert self.login_page.error_message() != ""

    # ===================== NHÓM 2: SAI THÔNG TIN =====================

    def test_TC04_dung_ten_sai_matkhau(self):
        """TC04: đúng username, sai password -> thông báo chung, vẫn ở trang login."""
        self.login_page.login_as(self.config.valid_username, "sai_mat_khau")
        assert self.login_page.is_on_login_page()
        assert "không đúng" in self.login_page.error_message().lower()

    def test_TC05_sai_ten_dung_matkhau(self):
        """TC05: sai username, đúng password -> không đăng nhập."""
        self.login_page.login_as("nguoi_la", self.config.valid_password)
        assert not self.login_page.logged_in()
        assert self.login_page.error_message() != ""

    def test_TC06_sai_ca_ten_va_matkhau(self):
        """TC06: sai cả username lẫn password -> không đăng nhập."""
        self.login_page.login_as("nguoi_la", "sai_mat_khau")
        assert not self.login_page.logged_in()
        assert self.login_page.error_message() != ""

    def test_TC09_matkhau_phan_biet_hoa_thuong(self):
        """TC09: password đúng ký tự nhưng sai hoa/thường -> thất bại."""
        self.login_page.login_as(self.config.valid_username, self.config.valid_password.lower())
        assert not self.login_page.logged_in()

    # ============== NHÓM 3: ĐĂNG NHẬP THÀNH CÔNG & GIỮ ĐĂNG NHẬP ==============

    def test_TC07_dang_nhap_dung_khong_giu_dang_nhap(self):
        """TC07: đăng nhập đúng, KHÔNG giữ đăng nhập -> vào trang chủ;
        mở lại trình duyệt phải đăng nhập lại."""
        dashboard = self.login_page.login_as(
            self.config.valid_username, self.config.valid_password, remember=False)
        assert dashboard.is_loaded(), "Phải vào được trang chủ"

        self.login_page.reopen()
        assert not self.login_page.logged_in(), "Không giữ đăng nhập thì phải đăng nhập lại"

    def test_TC08_dang_nhap_dung_co_giu_dang_nhap(self):
        """TC08: đăng nhập đúng, CÓ giữ đăng nhập -> vào trang chủ;
        mở lại trình duyệt vào thẳng trang chủ."""
        dashboard = self.login_page.login_as(
            self.config.valid_username, self.config.valid_password, remember=True)
        assert dashboard.is_loaded(), "Phải vào được trang chủ"

        self.login_page.reopen()
        assert self.login_page.logged_in(), "Giữ đăng nhập thì không phải đăng nhập lại"

    def test_TC10_username_co_khoang_trang_thua(self):
        """TC10: username có khoảng trắng thừa đầu/cuối -> mock so khớp chính xác, thất bại."""
        self.login_page.login_as("  " + self.config.valid_username + "  ",
                                  self.config.valid_password)
        assert not self.login_page.logged_in()
