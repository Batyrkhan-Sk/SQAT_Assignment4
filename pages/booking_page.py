from pages.base_page import BasePage
from components.passenger_form import PassengerForm
import time

class BookingPage(BasePage):

    def fill_passenger_details(self, gender, first_name, last_name, date_of_birth, email, phone):
        time.sleep(3) 
        
        passenger_form = PassengerForm(self.driver)
        passenger_form.fill(gender, first_name, last_name, date_of_birth, email, phone)
        passenger_form.submit()