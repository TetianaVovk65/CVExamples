from playwright.sync_api import sync_playwright
from page_object import LoginPage


def test_successful_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for headless mode
        context = browser.new_context()
        page = context.new_page()
        login_page = LoginPage(page)

        login_page.load()
        login_page.enter_username("valid_username")
        login_page.enter_password("valid_password")
        login_page.click_login()

        assert login_page.is_logout_displayed(), "Logout button should be displayed after successful login"

        browser.close()


def test_invalid_username():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        login_page = LoginPage(page)

        login_page.load()
        login_page.enter_username("invalid_username")
        login_page.enter_password("valid_password")
        login_page.click_login()

        assert "Invalid username or password" in login_page.get_error_message(), "Error message should indicate invalid username"

        browser.close()


def test_invalid_password():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        login_page = LoginPage(page)

        login_page.load()
        login_page.enter_username("valid_username")
        login_page.enter_password("invalid_password")
        login_page.click_login()

        assert "Invalid username or password" in login_page.get_error_message(), "Error message should indicate invalid password"

        browser.close()


def test_empty_username():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        login_page = LoginPage(page)

        login_page.load()
        login_page.enter_username("")
        login_page.enter_password("valid_password")
        login_page.click_login()

        assert "Username is required" in login_page.get_error_message(), "Error message should indicate username is required"

        browser.close()


def test_empty_password():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        login_page = LoginPage(page)

        login_page.load()
        login_page.enter_username("valid_username")
        login_page.enter_password("")
        login_page.click_login()

        assert "Password is required" in login_page.get_error_message(), "Error message should indicate password is required"

        browser.close()


if __name__ == "__main__":
    test_successful_login()
    test_invalid_username()
    test_invalid_password()
    test_empty_username()
    test_empty_password()
