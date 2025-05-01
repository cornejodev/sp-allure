import os
from selenium.common import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class BasePage:
    def __init__(self, driver: WebDriver):
        self._driver = driver

    def find(self, locator: tuple) -> WebElement:
        return self._driver.find_element(*locator)

    def type(self, locator: tuple, text: str, time: int = 10):
        self.wait_until_element_is_visible(locator, time)
        self.find(locator).send_keys(text)

    def clear(self, locator: tuple, time: int = 10):
        self.wait_until_element_is_visible(locator, time)
        self.find(locator).clear()

    def click(self, locator: tuple, time: int = 10):
        self.wait_until_element_is_visible(locator, time)
        self.find(locator).click()

    def wait_until_element_is_visible(self, locator: tuple, time: int = 10):
        wait = WebDriverWait(self._driver, time)
        wait.until(ec.visibility_of_element_located(locator))

    def wait_until_element_is_clickable(self, locator: tuple, time: int = 10):
        wait = WebDriverWait(self._driver, time)
        wait.until(ec.element_to_be_clickable(locator))

    def save_screenshot(self, method_name: str):
        screenshots_dir = os.path.join(os.getcwd(), "reports", "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        filename = f"{method_name}.png"
        screenshot_path = os.path.join(screenshots_dir, filename)
        self._driver.save_screenshot(screenshot_path)

    @property
    def current_url(self) -> str:
        return self._driver.current_url

    def is_displayed(self, locator: tuple) -> bool:
        try:
            return self.find(locator).is_displayed()
        except NoSuchElementException:
            return False

    def open_url(self, url: str):
        self._driver.get(url)

    def get_text(self, locator: tuple, time: int = 10) -> str:
        self.wait_until_element_is_visible(locator, time)
        return self.find(locator).text
