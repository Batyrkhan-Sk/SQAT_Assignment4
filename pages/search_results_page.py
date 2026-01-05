from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
import time

class SearchResultsPage(BasePage):
    FLIGHT_BOOK_BUTTON = (By.XPATH, "//button[@type='button']//span[contains(text(), 'Бронировать')]")
    
    def select_first_ticket(self):
        """Click first flight booking button"""
        time.sleep(5)
        
        original_window = self.driver.current_window_handle
        
        # Find buttons
        buttons = self.driver.find_elements(
            By.XPATH,
            "//button[@type='button']//span[contains(text(), 'Бронировать')]"
        )
        
        print(f"Found {len(buttons)} booking buttons")
        
        if buttons:
            button = buttons[0].find_element(By.XPATH, "..")  # Get parent button
            
            # Scroll and click
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(1)
            
            windows_before = len(self.driver.window_handles)
            
            # Click with JavaScript (most reliable)
            self.driver.execute_script("arguments[0].click();", button)
            print("✅ Clicked booking button")
            
            time.sleep(3)
            
            # Check for new window
            if len(self.driver.window_handles) > windows_before:
                new_window = self.driver.window_handles[-1]
                self.driver.switch_to.window(new_window)
                print(f"✅ Switched to: {self.driver.current_url}")
            
            time.sleep(2)
        else:
            self.driver.save_screenshot("no_buttons.png")
            raise Exception("No booking buttons found!")