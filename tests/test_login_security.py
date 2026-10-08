"""Kiểm thử BẢO MẬT đăng nhập — sheet 'BaoMat' trong file Excel.

Kiểm thử INPUT-VALIDATION (phòng thủ): nhập payload SQLi/XSS và xác minh trang
xử lý như CHUỖI THƯỜNG — không bypass đăng nhập, không thực thi mã.

CHỐT AN TOÀN: lớp đặt REQUIRE_SECURITY_ALLOWED = True nên BaseTest sẽ tự SKIP
nếu mục tiêu không nằm trong danh sách host được phép (mock/localhost/demo).
"""
import pytest
from selenium.common.exceptions import NoAlertPresentException

from base.base_test import BaseTest

pytestmark = pytest.mark.security


# Khai báo payload ở mức module để decorator parametrize đọc được.
SQLI_PAYLOADS = {
    # --- Nhóm cơ bản ---
    "SEC01_or_1_eq_1_username":  ("' OR '1'='1", "x"),
    "SEC02_comment_bypass":      ("admin'--", "x"),
    "SEC03_or_1_eq_1_password":  ("student", "' OR '1'='1"),
    "SEC04_drop_table":          ("'; DROP TABLE users;--", "x"),
    # --- Nhóm bổ sung ---
    "SEC08_or_1_eq_1_comment":   ("' OR 1=1--", "x"),
    "SEC09_admin_hash_comment":  ("admin'#", "x"),
    "SEC10_union_select":        ("' UNION SELECT 1,2,3--", "x"),
    "SEC11_quote_empty_eq":      ("' OR ''='", "x"),
    "SEC12_paren_bypass":        ('") OR ("1"="1', "x"),
    "SEC13_double_quote_pass":   ("student", '" OR ""="'),
    "SEC14_time_based_blind":    ("'; WAITFOR DELAY '0:0:5'--", "x"),
    "SEC15_stacked_update":      ("x'; UPDATE users SET pass='1'--", "x"),
}

XSS_PAYLOADS = {
    "SEC05_script_tag":  "<script>alert(1)</script>",
    "SEC06_img_onerror": '"><img src=x onerror=alert(1)>',
}


class TestLoginSecurity(BaseTest):
    REQUIRE_SECURITY_ALLOWED = True  # -> BaseTest tự skip nếu mục tiêu không được phép

    def _no_alert(self):
        """True nếu KHÔNG có hộp alert (payload XSS không chạy)."""
        try:
            self.driver.switch_to.alert  # noqa: B018
            return False
        except NoAlertPresentException:
            return True

    # ===================== SQL INJECTION =====================

    @pytest.mark.parametrize("case", list(SQLI_PAYLOADS), ids=list(SQLI_PAYLOADS))
    def test_sql_injection_khong_bypass(self, case):
        """SEC01-04, SEC08-15: payload SQLi KHÔNG được đăng nhập thành công."""
        username, password = SQLI_PAYLOADS[case]
        self.login_page.login_as(username, password)

        assert not self.login_page.logged_in(), f"[{case}] SQLi KHÔNG được bypass đăng nhập!"
        assert self.login_page.error_message() != ""

    # ===================== XSS =====================

    @pytest.mark.parametrize("case", list(XSS_PAYLOADS), ids=list(XSS_PAYLOADS))
    def test_xss_khong_thuc_thi_ma(self, case):
        """SEC05-06: payload XSS KHÔNG được chạy (không có alert), không đăng nhập."""
        self.login_page.login_as(XSS_PAYLOADS[case], "x")

        assert self._no_alert(), f"[{case}] Payload XSS đã thực thi (xuất hiện alert)!"
        assert not self.login_page.logged_in()
