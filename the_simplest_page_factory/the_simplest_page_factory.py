import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from seleniumpagefactory.Pagefactory import PageFactory


class LoginPage(PageFactory):
    URL = "https://qa-guru.github.io/one-page-form/login.html"

    def __init__(self, driver):
        self.driver = driver
        self.locators = {
            "username_input": ("ID", "login-input"),
            "password_input": ("ID", "password-input"),
            "submit_button": ("ID", "submit-button"),
            "welcome_message": ("ID", "welcome-message"),
            "error_message": ("ID", "error-message"),
        }

    def open(self):
        self.driver.get(self.URL)

    def login(self, username, password):
        self.username_input.clear_text()
        self.username_input.set_text(username)
        self.password_input.clear_text()
        self.password_input.set_text(password)
        self.submit_button.click_button()

    def get_message(self, message_name):
        element = getattr(self, message_name)
        WebDriverWait(self.driver, 5).until(
            lambda _: element.text.strip() != ""
        )
        return element.text


@pytest.fixture
def driver():
    browser_driver = webdriver.Chrome()
    browser_driver.maximize_window()
    try:
        yield browser_driver
    finally:
        browser_driver.quit()


@pytest.mark.parametrize(
    "username, password, message_name, expected",
    [
        (
            "user1",
            "password1",
            "welcome_message",
            "Welcome, user1!",
        ),
        (
            "user1",
            "wrong_pass",
            "error_message",
            "Wrong login or password",
        ),
        (
            "",
            "password1",
            "error_message",
            "Login is required (minimum 3 characters)",
        ),
    ],
    ids=["successful_login", "wrong_password", "empty_login"],
)
def test_login(driver, username, password, message_name, expected):
    page = LoginPage(driver)
    page.open()
    page.login(username, password)

    assert page.get_message(message_name) == expected