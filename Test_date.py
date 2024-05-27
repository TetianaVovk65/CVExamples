import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    page = browser.new_page()
    page.goto("https://demoqa.com/date-picker")
    page.wait_for_load_state("load")
    yield page
    page.close()


def test_select_date(page):
    # Selecting a date from the date picker
    page.click("#datePickerMonthYearInput")
    page.click(".react-datepicker__month-select")
    page.select_option(".react-datepicker__month-select", value="6")  # Selecting July
    page.click(".react-datepicker__year-select")
    page.select_option(".react-datepicker__year-select", value="2023")  # Selecting 2023
    page.click(".react-datepicker__day--002", timeout=5000)  # Selecting 2d day of July 2023

    # Verifying the selected date
    selected_date = page.query_selector("#datePickerMonthYearInput")
    value = selected_date.get_attribute("value")
    assert value == "07/02/2023"


def test_invalid_date(page):
    local_date = datetime.now().strftime("%m/%d/%Y")
    # Entering an invalid date
    page.fill("#datePickerMonthYearInput", "15/25/2022")  # Entering an invalid date
    page.press("#datePickerContainer", "Enter")

    # Verifying error message
    selected_date = page.get_attribute("#datePickerMonthYearInput", "value")
    assert selected_date == local_date


def test_disabled_date(page):
    # Trying to select a disabled date
    page.click("#datePickerMonthYearInput")
    page.click(".react-datepicker__month-select")
    page.select_option(".react-datepicker__month-select", value="3")  # Selecting April
    page.click(".react-datepicker__year-select")
    page.select_option(".react-datepicker__year-select", value="2023")  # Selecting 2023
    page.click(".react-datepicker__day--008")  # Trying to select 8th day of April 2023 (which is disabled)

    # Verifying the selected date remains unchanged
    selected_date = page.text_content(".react-datepicker__input-container input")
    assert selected_date == ""


def test_change_date_format(page):
    # Changing the date format
    page.click("#datePickerMonthYearInput")
    page.click(".react-datepicker__input-container input")
    page.fill(".react-datepicker__input-container input", "2023-05-15")  # Entering date in yyyy-mm-dd format
    page.press("#datePickerContainer", "Enter")

    # Verifying the changed date format
    selected_date = page.get_attribute("#datePickerMonthYearInput", "value")
    assert selected_date == "05/15/2023"


def test_select_specific_date_and_time_field2(page):
    # Open the Date and Time Picker
    page.click("#dateAndTimePickerInput")

    # Select Year
    page.click(".react-datepicker__year-read-view--down-arrow")
    page.click("//div[@class='react-datepicker__year-option'][text()='2023']")

    # Select Month
    page.click(".react-datepicker__month-read-view--down-arrow")
    page.click("//div[@class='react-datepicker__month-option'][text()='July']")

    # Select Day
    page.click(".react-datepicker__day--001:not(.react-datepicker__day--outside-month)")

    # Select Time
    time_locator = page.locator(".react-datepicker__time-list-item").locator('text=10:30')
    time_locator.click()

    # Retrieve the date and time from the input field
    selected_date_time = page.get_attribute("#dateAndTimePickerInput", "value")

    # Verify the selected date and time
    assert selected_date_time == "July 1, 2023 10:30 AM"


def test_invalid_date_and_time_input_field2(page):
    # Entering an invalid date and time into the date and time picker input field
    page.click("#dateAndTimePickerInput")
    page.fill("#dateAndTimePickerInput", "15/25/2023 99:99 AM")
    page.press("#dateAndTimePickerInput", "Enter")

    locale_date = datetime.now().strftime("%m/%d/%Y")

    # Verify the invalid date and time
    selected_date = page.get_attribute("#datePickerMonthYearInput", "value")
    assert selected_date == locale_date


def test_compare_with_local_date_and_time_field2(page):
    # Get the current local date and time
    local_date_time = datetime.now().strftime("%B %-d, %Y %-I:%M %p")

    # Open the Date and Time Picker
    page.click("#dateAndTimePickerInput")
    page.fill("#dateAndTimePickerInput", local_date_time)
    page.press("#dateAndTimePickerInput", "Enter")

    # Retrieve the date and time from the input field
    selected_date_time = page.get_attribute("#dateAndTimePickerInput", "value")

    # Verify the date and time in the date picker matches the local date and time
    assert selected_date_time == local_date_time

