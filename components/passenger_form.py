from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from components.base_component import BaseComponent
import time

class PassengerForm(BaseComponent):
    GENDER_MALE = (By.XPATH, "//button[contains(text(), 'Мужской')]")
    GENDER_FEMALE = (By.XPATH, "//button[contains(text(), 'Женский')]")
    PASSENGER_INPUTS = (By.CSS_SELECTOR, ".t-passenger-input input, input.t-passenger-input")
    DATE_OF_BIRTH = (By.CSS_SELECTOR, ".t-passenger-birthday input, .t-date-input input, input[placeholder*='рождения']")
    CITIZENSHIP = (By.CSS_SELECTOR, ".t-passenger-citizenship select, .t-passenger-citizenship input")
    DOCUMENT_TYPE_BUTTON = (By.CSS_SELECTOR, "button[name='docType']")
    DOCUMENT_NUMBER = (By.CSS_SELECTOR, "input[name='docnum']")
    DOCUMENT_EXPIRY = (By.CSS_SELECTOR, "input[name='docExpireDate']")
    IIN = (By.CSS_SELECTOR, ".t-passenger-ipn input, input[placeholder*='ИНН']")
    EMAIL = (By.CSS_SELECTOR, "input[type='email'], input[placeholder*='почта']")
    PHONE = (By.CSS_SELECTOR, "input[type='tel'], input[placeholder*='телефон']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "button.t-btn.preset-1.w-100, button.t-btn.preset-1.f--grow")
    MODAL_OVERLAY = (By.CSS_SELECTOR, ".t-menu__overlay")
    MODAL_DECLINE_BUTTON = (By.XPATH, "//div[@class='t-menu__content']//button[@class='t-btn preset-3']")

    def fill(self, gender, first_name, last_name, date_of_birth, email, phone, 
             citizenship=None, document_type="ID", document_number=None, 
             document_expiry=None, iin=None):
        time.sleep(2)
        
        try:
            if gender.lower() in ["male", "мужской", "m"]:
                self.click(self.GENDER_MALE)
            else:
                self.click(self.GENDER_FEMALE)
            time.sleep(0.5)
        except:
            pass
        
        inputs = self.driver.find_elements(*self.PASSENGER_INPUTS)
        if len(inputs) >= 2:
            inputs[0].clear()
            inputs[0].send_keys(last_name)
            time.sleep(0.3)
            inputs[1].clear()
            inputs[1].send_keys(first_name)
            time.sleep(0.3)
        
        try:
            dob_field = self.find(self.DATE_OF_BIRTH)
            dob_field.clear()
            dob_field.send_keys(date_of_birth)
            time.sleep(0.3)
        except:
            pass
        
        self.driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(0.5)
        
        if citizenship:
            try:
                citizenship_elem = self.find(self.CITIZENSHIP)
                if citizenship_elem.tag_name == 'select':
                    Select(citizenship_elem).select_by_visible_text(citizenship)
                else:
                    citizenship_elem.clear()
                    citizenship_elem.send_keys(citizenship)
                time.sleep(0.3)
            except:
                pass
        
        try:
            doc_type_btn = self.find(self.DOCUMENT_TYPE_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", doc_type_btn)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", doc_type_btn)
            time.sleep(1.5)
            
            items = self.driver.find_elements(By.CSS_SELECTOR, "button.item[type='button']")
            if not items:
                items = self.driver.find_elements(By.XPATH, "//button[@class='item']")
            
            if items:
                doc_type_lower = document_type.lower()
                if doc_type_lower in ["id", "удостоверение", "identity"]:
                    self.driver.execute_script("arguments[0].click();", items[0])
                elif doc_type_lower in ["passport", "паспорт", "заграничный"] and len(items) > 1:
                    self.driver.execute_script("arguments[0].click();", items[1])
                elif doc_type_lower in ["birthcert", "birth", "свидетельство"] and len(items) > 2:
                    self.driver.execute_script("arguments[0].click();", items[2])
                else:
                    self.driver.execute_script("arguments[0].click();", items[0])
                time.sleep(0.5)
        except:
            pass
        
        if document_number:
            try:
                self.type(self.DOCUMENT_NUMBER, document_number)
                time.sleep(0.3)
            except:
                pass
        
        if document_expiry:
            try:
                self.type(self.DOCUMENT_EXPIRY, document_expiry)
                time.sleep(0.3)
            except:
                pass
        
        if iin:
            try:
                self.type(self.IIN, iin)
                time.sleep(0.3)
            except:
                pass
        
        self.driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)
        
        email_field = self.find(self.EMAIL)
        email_field.clear()
        email_field.send_keys(email)
        time.sleep(0.3)
        
        phone_field = self.find(self.PHONE)
        phone_field.clear()
        phone_field.send_keys(phone)
        time.sleep(0.3)

    def submit(self, select_flexible_ticket=False):
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        self.driver.execute_script("window.scrollBy(0, -300);")
        time.sleep(1)
        
        continue_btn = None
        
        try:
            buttons = self.driver.find_elements(*self.CONTINUE_BUTTON)
            for btn in buttons:
                if "Продолжить" in btn.text or "продолжить" in btn.text.lower():
                    continue_btn = btn
                    break
        except:
            pass
        
        if not continue_btn:
            try:
                buttons = self.driver.find_elements(By.XPATH, "//button[contains(., 'Продолжить')]")
                visible = [b for b in buttons if b.is_displayed()]
                if visible:
                    continue_btn = visible[0]
            except:
                pass
        
        if not continue_btn:
            try:
                all_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.t-btn")
                for btn in all_buttons:
                    if btn.is_displayed() and "Продолжить" in btn.text:
                        continue_btn = btn
                        break
            except:
                pass
        
        if not continue_btn:
            raise Exception("Continue button not found")
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", continue_btn)
        time.sleep(3)
        
        self._handle_modal(select_flexible_ticket)

    def _handle_modal(self, select_flexible):
        try:
            self.wait.until(EC.presence_of_element_located(self.MODAL_OVERLAY))
            time.sleep(1)
            decline_btn = self.wait.until(EC.element_to_be_clickable(self.MODAL_DECLINE_BUTTON))
            decline_btn.click()
            self.wait.until(EC.invisibility_of_element_located(self.MODAL_OVERLAY))
            time.sleep(2)
        except TimeoutException:
            pass