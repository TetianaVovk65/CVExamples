import pytest
from playwright.sync_api import sync_playwright
from login_page import LoginPage  # Correct import statement


# Fixture to launch the browser
@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


# Test cases
def test_valid_login(browser):
    login_page = LoginPage(browser)
    login_page.navigate()
    login_page.login("valid_username", "valid_password")
    assert browser.url == "https://demoqa.com/profile"
    assert "Welcome, valid_username" in browser.text_content('div')

# Write other test cases similarly
