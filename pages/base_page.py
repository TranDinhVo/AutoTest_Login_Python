"""BasePage — lớp cha cho mọi Page Object (mô hình Page Object Model).

Gói các thao tác Selenium dùng chung (mở trang, tìm/bấm/nhập phần tử, chờ,
lấy text, chạy JS...) để các Page cụ thể kế thừa, tránh lặp code.

Locator được truyền vào dưới dạng tuple (By, "giá trị"), ví dụ (By.ID, "username").
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------- Điều hướng ----------
    def open_url(self, url):
        self.driver.get(url)
        return self

    def current_url(self):
        return self.driver.current_url

    # ---------- Tương tác phần tử ----------
    def find(self, locator):
        """Chờ tới khi phần tử hiển thị rồi trả về (Explicit Wait)."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def type(self, locator, text):
        """Chờ phần tử hiển thị -> xoá nội dung cũ -> nhập text."""
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        if text:
            el.send_keys(text)
        return self

    def click(self, locator):
        """Chờ phần tử bấm được rồi click."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        return self

    def get_text(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).text.strip()
        except Exception:
            return ""

    def is_checkbox_selected(self, locator):
        return self.find(locator).is_selected()

    def set_checkbox(self, locator, checked):
        """Tick/bỏ tick checkbox về đúng trạng thái mong muốn."""
        try:
            box = self.driver.find_element(*locator)
            if box.is_selected() != checked:
                box.click()
        except Exception:
            pass  # trang không có checkbox -> bỏ qua
        return self

    # ---------- Chờ điều kiện ----------
    def url_contains(self, fragment, timeout=DEFAULT_TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(fragment))
            return True
        except Exception:
            return fragment in self.driver.current_url

    # ---------- JavaScript ----------
    def run_js(self, script):
        return self.driver.execute_script(script)
