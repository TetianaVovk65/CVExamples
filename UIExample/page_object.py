from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/login"

        # Selectors
        self.username_input = "#userName"
        self.password_input = "#password"
        self.login_button = "#login"
        self.logout_button = "#submit"
        self.error_message = "#name"

    def load(self):
        self.page.goto(self.url)

    def enter_username(self, username: str):
        self.page.fill(self.username_input, username)

    def enter_password(self, password: str):
        self.page.fill(self.password_input, password)

    def click_login(self):
        self.page.click(self.login_button)

    def get_error_message(self) -> str:
        return self.page.inner_text(self.error_message)

    def is_logout_displayed(self) -> bool:
        return self.page.is_visible(self.logout_button)
