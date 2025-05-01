# conftest.py
import os
import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


# @pytest.fixture(scope="session", autouse=True)
# def clear_allure_dirs():
#     # Remove old results & report folders
#     for d in ("allure-results", "allure-report"):
#         if os.path.isdir(d):
#             shutil.rmtree(d)
#     # Recreate the raw-results dir
#     os.makedirs("allure-results", exist_ok=True)


@pytest.fixture(scope="function")
def driver():
    """
    Picks up BROWSER (chrome|firefox) and HEADLESS (true|false) from env.
    Defaults: chrome + headless.
    """
    browser = os.getenv("BROWSER", "chrome").lower()
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    print(f"Launching {browser} (headless={headless})")

    if browser == "chrome":
        opts = ChromeOptions()
        if headless:
            opts.add_argument("--headless=new")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_argument("--disable-gpu")
            opts.add_argument("--window-size=1920,1080")
            opts.add_argument("--user-data-dir=/tmp/chrome-profile")
        drv = webdriver.Chrome(options=opts)

    elif browser == "firefox":
        opts = FirefoxOptions()
        if headless:
            opts.add_argument("--headless")
        drv = webdriver.Firefox(options=opts)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    drv.maximize_window()
    yield drv
    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    On test failure, take a screenshot into allure-results/
    and attach it to the Allure report if available.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if not drv:
            return

        path_dir = "allure-results"
        os.makedirs(path_dir, exist_ok=True)
        path = os.path.join(path_dir, f"{item.name}.png")
        drv.save_screenshot(path)

        # attach to allure if plugin is installed
        try:
            import allure
            from allure_commons.types import AttachmentType

            allure.attach.file(
                path, name="screenshot", attachment_type=AttachmentType.PNG
            )
        except ImportError:
            pass
