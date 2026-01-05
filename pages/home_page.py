from pages.base_page import BasePage
from components.search_form import SearchForm

class HomePage(BasePage):
    URL = "https://tickets.kz/avia"

    def search_tickets(self, from_city, to_city):
        search_form = SearchForm(self.driver)
        search_form.search(from_city, to_city)
