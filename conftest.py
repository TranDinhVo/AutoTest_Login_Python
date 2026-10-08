"""Fixtures dùng chung cho toàn bộ test (pytest tự nạp file này)."""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from utils.config_loader import Config
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def config():
    return Config()


@pytest.fixture
def driver(config):
    """Khởi tạo WebDriver trước mỗi test, đóng sau khi test xong.

    Selenium Manager (có sẵn trong Selenium 4) tự tải driver phù hợp,
    không cần tải chromedriver thủ công.
    """
    if config.browser == "edge":
        opts = EdgeOptions()
        if config.headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1280,900")
        drv = webdriver.Edge(options=opts)
    else:
        opts = ChromeOptions()
        if config.headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1280,900")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        drv = webdriver.Chrome(options=opts)

    drv.implicitly_wait(2)
    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver, config):
    """Mở sẵn trang login trước mỗi test."""
    page = LoginPage(driver, config)
    page.open()
    return page
