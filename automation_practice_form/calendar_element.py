from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

class CalendarElement:
    CALENDAR_INPUT = (By.ID, "dateOfBirthInput")
    YEAR_OF_BIRTH_SELECT = (
        By.CSS_SELECTOR, ".react-datepicker__year-select"
    )
    MONTH_OF_BIRTH_SELECT = (
        By.CSS_SELECTOR, ".react-datepicker__month-select"
    )

    def __init__(self, driver):
        self.driver = driver

    def select_date(self, date):
        self.driver.find_element(*self.CALENDAR_INPUT).click()

        Select(
            self.driver.find_element(*self.YEAR_OF_BIRTH_SELECT)
        ).select_by_value(date[0])

        Select(
            self.driver.find_element(*self.MONTH_OF_BIRTH_SELECT)
        ).select_by_value(date[1])

        self.driver.find_element(
            By.CSS_SELECTOR,
            f".react-datepicker__day--0{date[2]}[tabindex='0']"
        ).click()