from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.booking_page import BookingPage
import time

def test_booking_flow(driver):

    home_page = HomePage(driver)
    home_page.open(HomePage.URL)

    home_page.search_tickets("Almaty", "Astana")

    # 🔒 Guard against hotel redirect
    if "booking.com" in driver.current_url.lower():
        driver.save_screenshot("redirected_to_booking.png")
        raise AssertionError(
            "Flight search redirected to Booking.com"
        )

    results_page = SearchResultsPage(driver)
    results_page.select_first_ticket()

    booking_page = BookingPage(driver)
    booking_page.fill_passenger_details(
        gender="male",
        first_name="Ivan",
        last_name="Petrov",
        date_of_birth="01.01.1990",
        email="test@example.com",
        phone="7012345678"
    )
