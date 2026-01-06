from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import time

class SearchResultsPage(BasePage):
    FLIGHT_BOOK_BUTTON = (By.XPATH, "//button[@type='button']//span[@class='t-text'][contains(text(), 'Бронировать')]")
    LOADING_INDICATOR = (By.XPATH, "//*[contains(@class, 'loading') or contains(@class, 'spinner')]")
    
    ALTERNATIVE_SELECTORS = [
        (By.XPATH, "//span[@class='t-text'][text()='Бронировать']/parent::button"),
        (By.XPATH, "//button[contains(@class, 't-btn')]//span[contains(text(), 'Бронировать')]"),
        (By.XPATH, "//button[@type='button'][.//span[text()='Бронировать']]"),
        (By.CSS_SELECTOR, "button.t-btn span.t-text"),
    ]
    
    def wait_for_results(self, timeout=30):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.LOADING_INDICATOR)
            )
        except TimeoutException:
            pass
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.FLIGHT_BOOK_BUTTON)
            )
            time.sleep(2)
            return True
        except TimeoutException:
            for selector in self.ALTERNATIVE_SELECTORS:
                try:
                    elements = self.driver.find_elements(*selector)
                    if selector[0] == By.CSS_SELECTOR:
                        elements = [el for el in elements if 'Бронировать' in el.text]
                    if elements:
                        time.sleep(2)
                        return True
                except:
                    continue
            return False
    
    def select_first_ticket(self):
        if not self.wait_for_results(timeout=30):
            raise Exception("Flight results did not load")
        
        original_window = self.driver.current_window_handle
        buttons = None
        
        for selector in [self.FLIGHT_BOOK_BUTTON] + self.ALTERNATIVE_SELECTORS:
            try:
                found = self.driver.find_elements(*selector)
                if selector[0] == By.CSS_SELECTOR:
                    found = [btn for btn in found if 'Бронировать' in btn.text]
                if found:
                    buttons = found
                    break
            except:
                continue
        
        if not buttons:
            raise Exception("No booking buttons found")
        
        button = buttons[0]
        if button.tag_name.lower() == 'span':
            button = button.find_element(By.XPATH, "..")
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(1)
        
        windows_before = len(self.driver.window_handles)
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(3)
        
        if len(self.driver.window_handles) > windows_before:
            self.driver.switch_to.window(self.driver.window_handles[-1])
        
        time.sleep(2)