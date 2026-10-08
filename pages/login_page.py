"""Page Object cho trang Đăng nhập.

Gom toàn bộ thao tác với trang login vào 1 lớp. Test chỉ gọi hàm nghiệp vụ
(login, get_error_text...) mà không cần biết chi tiết locator -> dễ bảo trì:
nếu trang đổi id, chỉ sửa 1 chỗ ở đây/config.ini.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver, config):
        self.driver = driver
        self.cfg = config
        self.wait = WebDriverWait(driver, 10)

    # ---------- Điều hướng ----------
    def open(self):
        """Mở trang login và xoá trạng thái 'giữ đăng nhập' còn sót (nếu có)."""
        self.driver.get(self.cfg.login_url)
        self._clear_remember_state()
        return self

    def _clear_remember_state(self):
        """Dọn localStorage của trang mock để các test độc lập nhau."""
        if self.cfg.is_mock:
            try:
                self.driver.execute_script("window.localStorage.clear();")
                self.driver.get(self.cfg.login_url)
            except Exception:
                pass

    def reopen(self):
        """Mô phỏng 'tắt trình duyệt rồi mở lại': nạp lại trang login."""
        self.driver.get(self.cfg.login_url)
        return self

    # ---------- Thao tác với các ô nhập ----------
    def _username(self):
        return self.wait.until(EC.presence_of_element_located((By.ID, self.cfg.username_id)))

    def _password(self):
        return self.driver.find_element(By.ID, self.cfg.password_id)

    def enter_username(self, value):
        el = self._username()
        el.clear()
        el.send_keys(value)
        return self

    def enter_password(self, value):
        el = self._password()
        el.clear()
        el.send_keys(value)
        return self

    def set_remember(self, checked):
        try:
            box = self.driver.find_element(By.ID, self.cfg.remember_id)
            if box.is_selected() != checked:
                box.click()
        except Exception:
            pass  # Trang không có ô 'giữ đăng nhập' -> bỏ qua
        return self

    def click_submit(self):
        self.driver.find_element(By.ID, self.cfg.submit_id).click()
        return self

    # ---------- Hành động nghiệp vụ gộp ----------
    def login(self, username, password, remember=False):
        if username is not None:
            self.enter_username(username)
        if password is not None:
            self.enter_password(password)
        self.set_remember(remember)
        self.click_submit()
        return self

    # ---------- Lấy kết quả / kiểm chứng ----------
    def get_error_text(self):
        try:
            return self.driver.find_element(By.ID, self.cfg.error_id).text.strip()
        except Exception:
            return ""

    def is_logged_in(self):
        """True nếu đã chuyển sang trang chủ (URL chứa chuỗi success)."""
        try:
            self.wait.until(EC.url_contains(self.cfg.success_url_contains))
            return True
        except Exception:
            return self.cfg.success_url_contains in self.driver.current_url

    def current_url(self):
        return self.driver.current_url
