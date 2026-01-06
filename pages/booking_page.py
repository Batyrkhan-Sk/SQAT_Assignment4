from pages.base_page import BasePage
from components.passenger_form import PassengerForm
import time

class BookingPage(BasePage):
    def fill_passenger_details(self, gender, first_name, last_name, date_of_birth, 
                               email, phone, citizenship=None, document_type="ID", 
                               document_number=None, document_expiry=None, iin=None, 
                               select_flexible_ticket=False):
        time.sleep(3)
        passenger_form = PassengerForm(self.driver)
        passenger_form.fill(
            gender=gender,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            email=email,
            phone=phone,
            citizenship=citizenship,
            document_type=document_type,
            document_number=document_number,
            document_expiry=document_expiry,
            iin=iin
        )
        passenger_form.submit(select_flexible_ticket=select_flexible_ticket)