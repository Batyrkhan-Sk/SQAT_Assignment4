from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from components.base_component import BaseComponent
import time

class PassengerForm(BaseComponent):
    GENDER_MALE = (By.XPATH, "//button[contains(text(), 'Мужской')]")
    GENDER_FEMALE = (By.XPATH, "//button[contains(text(), 'Женский')]")
    
    PASSENGER_NAME_CONTAINER = (By.CSS_SELECTOR, ".t-passenger-name")
    FIRST_NAME = (By.CSS_SELECTOR, ".t-passenger-name input, input.t-passenger-input")
    LAST_NAME = (By.CSS_SELECTOR, ".t-passenger-input")
    
    DATE_OF_BIRTH = (By.CSS_SELECTOR, ".t-passenger-birthday input, .t-date-input input")
    
    CITIZENSHIP = (By.CSS_SELECTOR, ".t-passenger-citizenship select, .t-passenger-citizenship input")
    
    DOCUMENT_TYPE = (By.CSS_SELECTOR, ".t-passenger-doc-type select, .t-passenger-doc-type input")
    
    DOCUMENT_NUMBER = (By.CSS_SELECTOR, ".t-passenger-docnum input")
    
    DOCUMENT_EXPIRY = (By.CSS_SELECTOR, ".t-passenger-doc-expire-date input")
    
    IIN = (By.CSS_SELECTOR, ".t-passenger-ipn input")
    
    EMAIL = (By.CSS_SELECTOR, "input[type='email'], input[placeholder*='почта']")
    PHONE = (By.CSS_SELECTOR, "input[type='tel'], input[placeholder*='телефон']")
    
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Продолжить')]")

    def fill(self, gender, first_name, last_name, date_of_birth, email, phone):
        
        time.sleep(2)
        
        try:
            if gender.lower() in ["male", "мужской", "m"]:
                self.click(self.GENDER_MALE)
            else:
                self.click(self.GENDER_FEMALE)
            time.sleep(0.5)
        except Exception as e:
            print(f"Gender selection failed: {e}")
        
        try:
            inputs = self.driver.find_elements(By.CSS_SELECTOR, ".t-passenger-input input, input.t-passenger-input")
            
            if len(inputs) >= 2:
                print(f"  Found {len(inputs)} passenger input fields")
                
                inputs[0].clear()
                inputs[0].send_keys(last_name)
                print(f"Last name: {last_name}")
                
                inputs[1].clear()
                inputs[1].send_keys(first_name)
                print(f" First name: {first_name}")
            else:
                raise Exception(f"Expected at least 2 passenger inputs, found {len(inputs)}")
        except Exception as e:
            print(f"Error filling name fields: {e}")
            raise
        
        try:
            dob_field = self.find(self.DATE_OF_BIRTH)
            dob_field.clear()
            dob_field.send_keys(date_of_birth)
            print(f"Date of birth: {date_of_birth}")
        except Exception as e:
            print(f"Date of birth failed (might be optional): {e}")
        
        self.driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)
        
        try:
            email_field = self.find(self.EMAIL)
            email_field.clear()
            email_field.send_keys(email)
            print(f"Email: {email}")
        except Exception as e:
            print(f"Email field failed: {e}")
        
        try:
            phone_field = self.find(self.PHONE)
            phone_field.clear()
            phone_field.send_keys(phone)
            print(f" Phone: {phone}")
        except Exception as e:
            print(f" Phone field failed: {e}")
        
        print("Passenger form filled")

    def submit(self):
        self.driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)
        
        try:
            continue_btn = self.wait.until(
                EC.element_to_be_clickable(self.CONTINUE_BUTTON)
            )
            continue_btn.click()
            print("Clicked continue button")
        except Exception as e:
            print(f"Failed to click continue button: {e}")
            btn = self.driver.find_element(*self.CONTINUE_BUTTON)
            self.driver.execute_script("arguments[0].click();", btn)
            print("Clicked continue button (JavaScript)")