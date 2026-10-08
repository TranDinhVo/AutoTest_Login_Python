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
    # --- Nhóm cơ bản ---
    "SEC01_or_1_eq_1_username":  ("' OR '1'='1", "x"),
    "SEC02_comment_bypass":      ("admin'--", "x"),
    "SEC03_or_1_eq_1_password":  ("student", "' OR '1'='1"),
    "SEC04_drop_table":          ("'; DROP TABLE users;--", "x"),
    # --- Nhóm bổ sung ---
    "SEC08_or_1_eq_1_comment":   ("' OR 1=1--", "x"),         # điều kiện luôn đúng + chú thích
    "SEC09_admin_hash_comment":  ("admin'#", "x"),            # chú thích kiểu MySQL (#)
    "SEC10_union_select":        ("' UNION SELECT 1,2,3--", "x"),  # UNION-based
    "SEC11_quote_empty_eq":      ("' OR ''='", "x"),          # so sánh rỗng = rỗng
    "SEC12_paren_bypass":        ('") OR ("1"="1', "x"),      # thoát dấu ngoặc
    "SEC13_double_quote_pass":   ("student", '" OR ""="'),    # payload ở password dùng nháy kép
    "SEC14_time_based_blind":    ("'; WAITFOR DELAY '0:0:5'--", "x"),  # time-based blind
    "SEC15_stacked_update":      ("x'; UPDATE users SET pass='1'--", "x"),  # stacked query
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


# ===================== XSS (Cross-Site Scripting) =====================

XSS_PAYLOADS = {
    "SEC05_script_tag":   "<script>alert(1)</script>",
    "SEC06_img_onerror":  '"><img src=x onerror=alert(1)>',
}


@pytest.mark.parametrize("case", list(XSS_PAYLOADS), ids=list(XSS_PAYLOADS))
def test_xss_khong_thuc_thi_ma(login_page, config, case):
    """SEC05-SEC06: payload XSS KHÔNG được chạy (không có alert), không đăng nhập."""
    payload = XSS_PAYLOADS[case]
    login_page.login(payload, "x")

    # 1) Không có hộp alert bật lên -> mã JS không được thực thi
    assert _no_alert(login_page.driver), (
        f"[{case}] Payload XSS đã thực thi (xuất hiện alert)!"
    )
    # 2) Không được đăng nhập bằng payload
    assert not login_page.is_logged_in()
