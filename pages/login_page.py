"""LoginPage — Page Object cho form đăng nhập (theo mẫu POM buổi 8).

Nguyên tắc POM:
- Locator để PRIVATE, giấu sau các method nghiệp vụ.
- Page KHÔNG chứa assertion (chỉ cung cấp dịch vụ giao diện + trạng thái trang).
- Fluent navigation: hành động chuyển trang trả về trang kế tiếp (DashboardPage).
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    # URL trang đăng nhập thật của hệ thống (khớp slide buổi 8).
    # Khi chạy test, URL thực tế lấy từ config (mặc định là mock an toàn).
    URL = "https://vanphongdientu.utc.edu.vn/Login"

    # ----- Locators (private) — dùng đúng name/css như trang UTC -----
    _username = (By.NAME, "username")
    _password = (By.NAME, "userpwd")
    _remember = (By.NAME, "remember")
    _login_btn = (By.CSS_SELECTOR, "input.submit_login")
    _error = (By.ID, "error")

    def __init__(self, driver, config):
        super().__init__(driver)
        self.cfg = config

    # ----- Điều hướng -----
    def open(self):
        """Mở trang login; dọn trạng thái 'giữ đăng nhập' để test độc lập."""
        self.open_url(self.cfg.login_url)
        self._clear_remember_state()
        return self

    def reopen(self):
        """Mô phỏng tắt/mở lại trình duyệt: nạp lại trang login."""
        self.open_url(self.cfg.login_url)
        return self

    def _clear_remember_state(self):
        if self.cfg.is_mock:
            try:
                self.run_js("window.localStorage.clear();")
                self.open_url(self.cfg.login_url)
            except Exception:
                pass

    # ----- Thao tác từng phần (dùng cho ca nhập thiếu) -----
    def fill_username(self, value):
        return self.type(self._username, value)

    def fill_password(self, value):
        return self.type(self._password, value)

    def set_remember(self, checked):
        return self.set_checkbox(self._remember, checked)

    def click_login(self):
        return self.click(self._login_btn)

    # ----- Method nghiệp vụ chính (fluent: trả về trang kế tiếp) -----
    def login_as(self, username, password, remember=False):
        """Nhập thông tin + bấm đăng nhập, trả về DashboardPage.

        (Với ca sai thông tin, trang vẫn ở login — kiểm tra bằng
        is_on_login_page()/error_message() trên chính LoginPage.)
        """
        if username is not None:
            self.fill_username(username)
        if password is not None:
            self.fill_password(password)
        self.set_remember(remember)
        self.click_login()
        from pages.dashboard_page import DashboardPage  # import trễ, tránh vòng lặp
        return DashboardPage(self.driver, self.cfg)

    # ----- Trạng thái trang (không phải assertion) -----
    def error_message(self):
        return self.get_text(self._error)

    def logged_in(self):
        """True nếu đã rời trang login sang trang chủ (URL chứa chuỗi success)."""
        return self.url_contains(self.cfg.success_url_contains)

    def is_on_login_page(self):
        return self.cfg.success_url_contains not in self.current_url()
