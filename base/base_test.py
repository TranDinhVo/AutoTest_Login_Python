"""BaseTest — lớp cha cho mọi test E2E (tương đương BaseTest trong JUnit 5).

Nhiệm vụ: khởi tạo WebDriver + timeout trước mỗi test, mở sẵn trang login,
và đóng trình duyệt sau khi test xong. Các lớp test chỉ việc kế thừa BaseTest
và dùng self.login_page / self.driver / self.config.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from utils.config_loader import Config
from pages.login_page import LoginPage


def create_driver(config):
    """Khởi tạo WebDriver theo cấu hình (browser + headless).

    Selenium Manager (có sẵn trong Selenium 4) tự tải driver phù hợp.
    """
    if config.browser == "edge":
        opts = EdgeOptions()
        if config.headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1280,900")
        return webdriver.Edge(options=opts)

    opts = ChromeOptions()
    if config.headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=opts)


class BaseTest:
    # Lớp con đặt = True nếu là test bảo mật -> tự skip khi mục tiêu không được phép
    REQUIRE_SECURITY_ALLOWED = False

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Chạy trước/sau mỗi test (giống @BeforeEach/@AfterEach của JUnit)."""
        self.config = Config()

        # Chốt an toàn: test bảo mật chỉ chạy trên host được phép
        if self.REQUIRE_SECURITY_ALLOWED and not self.config.security_tests_allowed:
            pytest.skip(
                f"Mục tiêu '{self.config.target_host}' không được phép chạy test bảo mật. "
                f"Chỉ chạy trên: {self.config.security_allowed_hosts}"
            )

        self.driver = create_driver(self.config)
        self.driver.implicitly_wait(2)
        self.login_page = LoginPage(self.driver, self.config)
        self.login_page.open()

        yield  # ----- test chạy ở đây -----

        self.driver.quit()
