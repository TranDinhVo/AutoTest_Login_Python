"""Kiểm thử ĐỘ BỀN đăng nhập — sheet 'DoBen' trong file Excel.

Kiểm tra hệ thống phản ứng ổn định với dữ liệu bất thường. Chạy trên mock.

Lưu ý về DoS/DDoS: file này KHÔNG chứa script tấn công từ chối dịch vụ.
ROB01 chỉ thử SỐ LẦN RẤT NHỎ (5 lần) để minh hoạ thiết kế test khoá tài khoản
/ chống brute-force, không phải để làm quá tải. Việc đánh giá tải thật phải
dùng công cụ load test trên môi trường được cấp phép.
"""
import pytest

pytestmark = pytest.mark.robustness


def test_ROB01_brute_force_nhieu_lan_sai(login_page, config):
    """ROB01: đăng nhập sai 5 lần liên tiếp -> luôn báo lỗi chung, không bị lộ thông tin.

    (Hệ thống thật nên khoá tạm/thêm CAPTCHA sau N lần sai — kiểm tra thủ công
    trên môi trường thật; mock không mô phỏng khoá nên ở đây chỉ xác minh
    mỗi lần sai đều bị từ chối một cách nhất quán.)
    """
    for lan in range(5):
        login_page.open()
        login_page.login(config.valid_username, "sai_mat_khau")
        assert not login_page.is_logged_in(), f"Lần {lan+1}: không được đăng nhập"
        assert login_page.get_error_text() != "", f"Lần {lan+1}: phải có thông báo lỗi"


def test_ROB02_input_rat_dai(login_page, config):
    """ROB02: nhập chuỗi ~10.000 ký tự -> trang không crash, báo lỗi bình thường."""
    chuoi_dai = "A" * 10000
    login_page.login(chuoi_dai, chuoi_dai)
    assert not login_page.is_logged_in()
    # Trang vẫn còn sống: lấy được URL hiện tại mà không văng lỗi
    assert login_page.current_url() != ""


def test_ROB03_ky_tu_unicode_dac_biet(login_page, config):
    """ROB03: username có dấu tiếng Việt + ký tự đặc biệt -> xử lý UTF-8 đúng, không lỗi.

    (Dùng ký tự trong BMP vì ChromeDriver.send_keys không hỗ trợ ký tự ngoài BMP
    như emoji. Bộ ký tự này vẫn kiểm tra được mã hoá UTF-8 và ký tự đặc biệt.)
    """
    login_page.login("Nguyễn_Văn_Á@#$%^&*()", "mật_khẩu_Đặc_Biệt_123")
    assert not login_page.is_logged_in()
    assert login_page.get_error_text() != ""
