# conftest.py
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser with UI (not headless)",
    )


@pytest.fixture
def browser(request):
    opts = Options()
    headed = request.config.getoption("--headed")

    if not headed:
        # headless mode
        opts.add_argument("--headless=new")  # or "--headless"
    # common options
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--user-data-dir=/tmp/chrome-user-data")
    opts.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=opts)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        browser = item.funcargs.get("browser")
        if browser:
            screenshot_dir = "allure-results"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            browser.save_screenshot(screenshot_path)
            try:
                import allure

                allure.attach.file(
                    screenshot_path,
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except ImportError:
                pass
