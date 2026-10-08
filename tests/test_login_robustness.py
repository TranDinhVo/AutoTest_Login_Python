"""Kiểm thử ĐỘ BỀN đăng nhập — sheet 'DoBen' trong file Excel.

Lưu ý DoS/DDoS: file này KHÔNG chứa script tấn công. ROB01 chỉ thử SỐ LẦN RẤT
NHỎ (5 lần) để minh hoạ thiết kế test chống brute-force, không làm quá tải.
"""
import pytest

from base.base_test import BaseTest

pytestmark = pytest.mark.robustness


class TestLoginRobustness(BaseTest):

    def test_ROB01_brute_force_nhieu_lan_sai(self):
        """ROB01: đăng nhập sai 5 lần liên tiếp -> luôn bị từ chối nhất quán."""
        for lan in range(5):
            self.login_page.open()
            self.login_page.login_as(self.config.valid_username, "sai_mat_khau")
            assert not self.login_page.logged_in(), f"Lần {lan+1}: không được đăng nhập"
            assert self.login_page.error_message() != "", f"Lần {lan+1}: phải có thông báo lỗi"

    def test_ROB02_input_rat_dai(self):
        """ROB02: nhập chuỗi ~10.000 ký tự -> trang không crash."""
        chuoi_dai = "A" * 10000
        self.login_page.login_as(chuoi_dai, chuoi_dai)
        assert not self.login_page.logged_in()
        assert self.driver.current_url != ""

    def test_ROB03_ky_tu_unicode_dac_biet(self):
        """ROB03: username có dấu tiếng Việt + ký tự đặc biệt (BMP) -> xử lý UTF-8 đúng.

        (Dùng ký tự trong BMP vì ChromeDriver.send_keys không hỗ trợ ký tự ngoài
        BMP như emoji.)
        """
        self.login_page.login_as("Nguyễn_Văn_Á@#$%^&*()", "mật_khẩu_Đặc_Biệt_123")
        assert not self.login_page.logged_in()
        assert self.login_page.error_message() != ""
