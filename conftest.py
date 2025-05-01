import pytest
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def browser():
    opts = Options()
    # run headless
    opts.add_argument("--headless=new")  # or "--headless"
    # recommended for containers
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # point to a temp profile so it’s never “already in use”
    opts.add_argument("--user-data-dir=/tmp/chrome-user-data")
    # optional: disable GPU, extensions, etc.
    opts.add_argument("--disable-gpu")
    # now start the driver
    driver = webdriver.Chrome(options=opts)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # We only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        browser = item.funcargs.get("browser", None)
        if browser:
            screenshot_dir = "allure-results"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            browser.save_screenshot(screenshot_path)
            # Attach to allure report if available
            try:
                import allure

                allure.attach.file(
                    screenshot_path,
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except ImportError:
                pass
