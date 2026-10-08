"""DashboardPage — Page Object cho trang chủ sau khi đăng nhập thành công.

Tương ứng DashboardPage trong slide buổi 8 (menu, header, thông tin user).
Ở bản mock là trang 'Đăng nhập thành công'.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    # ----- Locators (private) -----
    _welcome = (By.ID, "welcome")
    _logout = (By.ID, "logout")

    def __init__(self, driver, config):
        super().__init__(driver)
        self.cfg = config

    def is_loaded(self):
        """True nếu đã vào trang chủ (URL chứa chuỗi success)."""
        return self.url_contains(self.cfg.success_url_contains)

    def welcome_text(self):
        return self.get_text(self._welcome)

    def logout(self):
        """Đăng xuất, trả về LoginPage (fluent navigation)."""
        self.click(self._logout)
        from pages.login_page import LoginPage  # import trễ, tránh vòng lặp
        return LoginPage(self.driver, self.cfg)
