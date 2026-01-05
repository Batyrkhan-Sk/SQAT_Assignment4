from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BaseComponent:
    def __init__(self, driver, root=None, timeout=15):
        self.driver = driver
        self.root = root
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator):
        try:
            if self.root:
                return self.root.find_element(*locator)
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            print(f"Element not found: {locator}")
            raise

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)