"""Kiểm thử BẢO MẬT đăng nhập — sheet 'BaoMat' trong file Excel.

Đây là kiểm thử INPUT-VALIDATION (phòng thủ): nhập các payload SQLi/XSS và
xác minh trang xử lý chúng như CHUỖI THƯỜNG — không bị bypass đăng nhập,
không thực thi mã. KHÔNG phải tấn công.

CHỐT AN TOÀN: các test này chỉ chạy khi mục tiêu (base_url) nằm trong
security_allowed_hosts (mock/localhost/demo). Nếu trỏ vào server thật của
trường, toàn bộ test trong file này sẽ tự động bị SKIP.
"""
import pytest
from selenium.common.exceptions import NoAlertPresentException

pytestmark = pytest.mark.security


@pytest.fixture(autouse=True)
def _guard_allowed_target(config):
    """Bỏ qua test bảo mật nếu mục tiêu không nằm trong danh sách được phép."""
    if not config.security_tests_allowed:
        pytest.skip(
            f"Mục tiêu '{config.target_host}' không được phép chạy test bảo mật. "
            f"Chỉ chạy trên: {config.security_allowed_hosts}"
        )


def _no_alert(driver):
    """True nếu KHÔNG có hộp alert (tức payload XSS không chạy)."""
    try:
        driver.switch_to.alert  # noqa: B018 - truy cập để kiểm tra tồn tại
        return False
    except NoAlertPresentException:
        return True


# ===================== SQL INJECTION =====================

SQLI_PAYLOADS = {
    "SEC01_or_1_eq_1_username": ("' OR '1'='1", "x"),
    "SEC02_comment_bypass":     ("admin'--", "x"),
    "SEC03_or_1_eq_1_password": ("student", "' OR '1'='1"),
    "SEC04_drop_table":         ("'; DROP TABLE users;--", "x"),
}


@pytest.mark.parametrize("case", list(SQLI_PAYLOADS), ids=list(SQLI_PAYLOADS))
def test_sql_injection_khong_bypass(login_page, config, case):
    """SEC01-SEC04: payload SQLi KHÔNG được phép đăng nhập thành công."""
    username, password = SQLI_PAYLOADS[case]
    login_page.login(username, password)

    assert not login_page.is_logged_in(), (
        f"[{case}] Payload SQLi KHÔNG được phép bypass đăng nhập!"
    )
    # Vẫn phải có thông báo lỗi bình thường (không lộ lỗi hệ thống/stacktrace)
    assert login_page.get_error_text() != ""
