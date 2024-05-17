import pytest
from playwright.sync_api import sync_playwright
from page_object import LoginPage


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


def test_valid_login(browser):
    login_page = LoginPage(browser)
    login_page.navigate()
    login_page.login("valid_username", "valid_password")
    assert browser.url == "https://demoqa.com/profile"
    assert "Welcome, valid_username" in browser.text_content('div')


def test_invalid_login_incorrect_password(browser):
    login_page = LoginPage(browser)
    login_page.navigate()
    login_page.login("valid_username", "invalid_password")
    assert login_page.get_error_message() == "Invalid username or password!"


def test_invalid_login_non_existent_username(browser):
    login_page = LoginPage(browser)
    login_page.navigate()
    login_page.login("non_existent_username", "any_password")
    assert login_page.get_error_message() == "Invalid username or password!"


def test_empty_username(browser):
    login_page = LoginPage(browser)
    login_page.navigate()
    login_page.login("", "any_password")
    assert login_page.get_error_message() == "Username is required"


def test_empty_password(browser):
    login_page = LoginPage(browser)
    login_page.navigate()
    login_page.login("valid_username", "")
    assert login_page.get_error_message() == "Password is required"


def test_empty_username_and_password(browser):
    login_page = LoginPage(browser)
    login_page.navigate()
    login_page.login("", "")
    assert login_page.get_error_message() == "Username is required"


def test_sql_injection_attempt(browser):
    login_page = LoginPage(browser)
    login_page.navigate()
    login_page.login("' OR '1'='1", "any_password")
    assert login_page.get_error_message() == "Invalid username or password!"
