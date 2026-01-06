from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.booking_page import BookingPage

def test_booking_flow(driver):
    home_page = HomePage(driver)
    home_page.open(HomePage.URL)
    home_page.search_tickets("Almaty", "Astana")
    
    if "booking.com" in driver.current_url.lower():
        driver.save_screenshot("redirected_to_booking.png")
        raise AssertionError("Flight search redirected to Booking.com")
    
    results_page = SearchResultsPage(driver)
    results_page.select_first_ticket()
    
    booking_page = BookingPage(driver)
    booking_page.fill_passenger_details(
        gender="male",
        first_name="Magzhan",
        last_name="Akzhanov",
        date_of_birth="05.01.1978",
        email="batyr@example.com",
        phone="7014225678",
        document_type="ID",
        document_number="232324242",
        document_expiry="09.01.2026",
        iin="124453324452",
        select_flexible_ticket=False
    )
    
    driver.save_screenshot("booking_completed.png")