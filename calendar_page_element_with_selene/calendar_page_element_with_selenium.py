import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class Calendar:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def open(self):
        field = self.wait.until(
            EC.element_to_be_clickable((By.ID, "dateOfBirthInput"))
        )
        field.click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".react-datepicker__month-container")
            )
        )

    def select_month(self, month):
        field = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".react-datepicker__month-select")
            )
        )
        Select(field).select_by_visible_text(month)

    def select_year(self, year):
        field = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".react-datepicker__year-select")
            )
        )
        Select(field).select_by_visible_text(year)

    def select_day(self, day):
        day_padded = day.zfill(3)
        field = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    f".react-datepicker__day--{day_padded}"
                    ":not(.react-datepicker__day--outside-month)"
                )
            )
        )
        field.click()

    def select_date(self, day, month, year):
        self.open()
        self.select_month(month)
        self.select_year(year)
        self.select_day(day)


@pytest.fixture
def driver():
    browser_driver = webdriver.Chrome()
    browser_driver.maximize_window()
    try:
        yield browser_driver
    finally:
        browser_driver.quit()

@pytest.mark.parametrize("day, month, year, expected", [
    ("15", "July", "2000", "15 Jul 2000"),
    ("5", "January", "1990", "05 Jan 1990"),
    ("29", "February", "2000", "29 Feb 2000"),
])
def test_select_birthday_date(driver, day, month, year, expected):
    driver.get(
        "https://qa-guru.github.io/one-page-form/automation-practice-form.html"
    )
    wait = WebDriverWait(driver, 5)

    close_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#fixedban button"))
    )
    close_button.click()
    wait.until(
        EC.invisibility_of_element_located((By.ID, "fixedban"))
    )

    calendar = Calendar(driver)
    calendar.select_date(day=day, month=month, year=year)

    wait.until(
        lambda browser_driver: browser_driver.find_element(
            By.ID, "dateOfBirthInput"
        ).get_property("value") == expected
    )