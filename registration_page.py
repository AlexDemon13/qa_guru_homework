from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

class RegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def open(self):
        self.driver.get(
            "https://qa-guru.github.io/one-page-form/automation-practice-form.html"
        )

    def close_banner(self):
        close_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#fixedban button"))
        )
        close_button.click()
        self.wait.until(EC.invisibility_of_element(close_button))

    def fill_first_name(self, name):
        first_name = self.wait.until(
            EC.element_to_be_clickable((By.ID, "firstName"))
        )
        first_name.send_keys(name)

    def fill_last_name(self, last_name):
        field = self.wait.until(
            EC.element_to_be_clickable((By.ID, "lastName"))
        )
        field.send_keys(last_name)

    def fill_email(self, email):
        field = self.wait.until(
            EC.element_to_be_clickable((By.ID, "userEmail"))
        )
        field.send_keys(email)

    def select_male(self):
        label = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "label[for='gender-radio-1']")
            )
        )
        label.click()

    def fill_mobile(self, mobile):
        field = self.wait.until(
            EC.element_to_be_clickable((By.ID, "userNumber"))
        )
        field.send_keys(mobile)

    def open_calendar(self):
        field = self.wait.until(
            EC.element_to_be_clickable((By.ID, "dateOfBirthInput"))
        )
        field.click()

        self.wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "react-datepicker__month-container")
            )
        )

    def select_birth_month(self, month_value):
        field = self.wait.until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "react-datepicker__month-select")
            )
        )
        Select(field).select_by_value(month_value)

    def select_birth_year(self, year):
        field = self.wait.until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "react-datepicker__year-select")
            )
        )
        Select(field).select_by_value(year)

    def select_birth_day(self, day):
        field = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    f".react-datepicker__day--{day}:not(.react-datepicker__day--outside-month)"
                )
            )
        )
        field.click()

    def select_subject(self, subject):
        field = self.wait.until(
            EC.element_to_be_clickable((By.ID, "subjectsInput"))
        )
        field.send_keys(subject)
        field.send_keys(Keys.ENTER)

    def select_sports(self):
        label = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']")
            )
        )
        label.click()

    def select_music(self):
        label = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "label[for='hobbies-checkbox-3']")
            )
        )
        label.click()

    def upload_picture(self, file_path):
        field = self.driver.find_element(By.ID, "uploadPicture")
        field.send_keys(file_path)

    def fill_current_address(self, address):
        field = self.wait.until(
            EC.element_to_be_clickable((By.ID, "currentAddress"))
        )
        field.send_keys(address)

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

    def select_state(self, state):
        dropdown = self.wait.until(
            EC.element_to_be_clickable((By.ID, "state"))
        )
        dropdown.click()

        option = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[@id='stateCity-wrapper']/div[normalize-space(.)='{state}']"
                )
            )
        )
        option.click()

    def select_city(self, city):
        dropdown = self.wait.until(
            EC.element_to_be_clickable((By.ID, "city"))
        )
        dropdown.click()

        option = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//div[@id='stateCity-wrapper']/div[normalize-space(.)='{city}']"
                )
            )
        )
        option.click()

    def submit(self):
        button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "submit"))
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )
        button.click()

    def get_error_message(self):
        element = self.wait.until(
            EC.visibility_of_element_located((By.ID, "formError"))
        )
        return element.text

    def get_result_title(self):
        element = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "example-modal-sizes-title-lg")
            )
        )
        return element.text

    def get_result_text(self):
        table = self.wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "table-responsive")
            )
        )
        return table.text

    def get_birth_date(self):
        field = self.driver.find_element(By.ID, "dateOfBirthInput")
        return field.get_property("value")

    def is_male_selected(self):
        field = self.driver.find_element(By.ID, "gender-radio-1")
        return field.is_selected()

    def is_sports_selected(self):
        field = self.driver.find_element(By.ID, "hobbies-checkbox-1")
        return field.is_selected()

    def is_music_selected(self):
        field = self.driver.find_element(By.ID, "hobbies-checkbox-3")
        return field.is_selected()

    def get_title(self):
        element = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/main/section/h1")
            )
        )
        return element.text

    def get_subtitle(self):
        element = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/main/section/div/p")
            )
        )
        return element.text

