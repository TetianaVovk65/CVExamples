from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator('input[id="userName"]')
        self.password_input = page.locator('input[id="password"]')
        self.login_button = page.locator('button[id="login"]')
        self.error_message = page.locator('#name')

    def navigate(self):
        self.page.goto("https://demoqa.com/login")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self):
        return self.error_message.text_content()
