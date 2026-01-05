from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from components.base_component import BaseComponent
import time

class SearchForm(BaseComponent):
    FROM_INPUT = (By.NAME, "autocomplete-avia-arrival")
    TO_INPUT = (By.NAME, "autocomplete-avia-departure")
    
    DATE_BUTTON = (By.CSS_SELECTOR, ".search-form-calendar-activator.departure button.selector")
    CALENDAR_GRID = (By.CSS_SELECTOR, ".search-form-calendar-grid")
    CALENDAR_CELL = (By.CSS_SELECTOR, ".search-form-calendar-cell.today")
    ANY_AVAILABLE_CELL = (By.CSS_SELECTOR, ".search-form-calendar-cell:not(.disabled)")
    
    # Hotel booking checkbox
    HOTEL_CHECKBOX = (By.CSS_SELECTOR, ".search-form-booking-checkbox input[type='checkbox']")
    HOTEL_CHECKBOX_LABEL = (By.CSS_SELECTOR, "label.search-form-booking-checkbox")
    
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def search(self, from_city, to_city):
        """Search for flights without hotel booking"""
        print(f"🔍 Searching flights: {from_city} → {to_city}")
        time.sleep(2)
        
        # Fill FROM
        print("  ↪ Filling FROM field...")
        from_field = self.find(self.FROM_INPUT)
        from_field.clear()
        from_field.send_keys(from_city)
        time.sleep(1.5)
        from_field.send_keys(Keys.ENTER)
        time.sleep(0.5)
        
        # Fill TO
        print("  ↪ Filling TO field...")
        to_field = self.find(self.TO_INPUT)
        to_field.clear()
        to_field.send_keys(to_city)
        time.sleep(1.5)
        to_field.send_keys(Keys.ENTER)
        time.sleep(0.5)
        
        # Select date
        print("  ↪ Selecting departure date...")
        self.select_departure_date()
        
        # Uncheck hotel booking
        print("  ↪ Disabling hotel booking...")
        self.disable_hotel_booking()
        
        # Submit search
        print("  ↪ Clicking search button...")
        time.sleep(1)
        self.click(self.SEARCH_BUTTON)
        print("✅ Flight search submitted!")
        time.sleep(2)
    
    def disable_hotel_booking(self):
        """Uncheck the hotel booking checkbox"""
        try:
            label = self.driver.find_element(*self.HOTEL_CHECKBOX_LABEL)
            checkbox = self.driver.find_element(*self.HOTEL_CHECKBOX)
            
            # Check if checked (attribute 'checked' exists)
            is_checked = checkbox.get_attribute('checked') is not None
            
            if is_checked:
                # Scroll to checkbox
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label)
                time.sleep(0.3)
                
                # Click label to uncheck
                label.click()
                time.sleep(0.5)
                print("    ✓ Hotel booking disabled")
            else:
                print("    ✓ Hotel booking already disabled")
                
        except Exception as e:
            print(f"    ⚠️ Could not disable hotel booking: {e}")
    
    def select_departure_date(self):
        """Select departure date"""
        self.click(self.DATE_BUTTON)
        time.sleep(1.5)
        self.wait.until(EC.visibility_of_element_located(self.CALENDAR_GRID))
        
        try:
            self.click(self.CALENDAR_CELL)
            print("    ✓ Selected today")
        except:
            self.click(self.ANY_AVAILABLE_CELL)
            print("    ✓ Selected first available date")