import pytest
from selene import browser, by, be, have
# https://github.com/yashaka/selene

# TODO: переписать используя "голый" Selenium
class Calendar:
    def __init__(self, base_element):
        self.input_field = base_element

    def select_date(self, day: str, month: str, year: str):
        # TODO: Как исправить - убрать всплывающее окно что мешает, используя Selene?
        
        # Переписать например такое Selenium решение на Selene - посмотреть насколько проще итоговый код
        #wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Level up your automation')]")))
        ## Находим и кликаем по кнопке закрытия (крестику) модального окна
        #close_banner_btn = wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="fixedban"]/div/div/button""")))
        #close_banner_btn.click()
        ## Ожидаем, пока баннер полностью исчезнет, чтобы он не перекрывал элементы формы
        #wait.until(EC.invisibility_of_element(close_banner_btn))

        self.input_field.click()
        browser.element(".react-datepicker__month-select").click().element(by.text(month)).click()
        browser.element(".react-datepicker__year-select").click().element(by.text(year)).click()
        day_padded = day.zfill(3)
        browser.element(f".react-datepicker__day--{day_padded}:not(.react-datepicker__day--outside-month)").click()

class AutomationPracticeFormPage:
    def __init__(self):
        browser.open("https://qa-guru.github.io/one-page-form/automation-practice-form.html")
        browser.element("#fixedban button").click()
        browser.element("#fixedban").should(be.not_.visible)
        self.birthday_calendar = Calendar(browser.element("#dateOfBirthInput"))

@pytest.mark.parametrize("day, month, year, expected", [
    ("15", "July", "2000", "15 Jul 2000"),
    ("5", "January", "1990", "05 Jan 1990"),
    ("29", "February", "2000", "29 Feb 2000"),
])
def test_select_birthday_date(day, month, year, expected):
    try:
        page = AutomationPracticeFormPage()
        page.birthday_calendar.select_date(
            day=day, month=month, year=year
        )
        page.birthday_calendar.input_field.should(
            have.value(expected)
        )
    finally:
        browser.quit()

print("test_select_birthday_date: PASS")