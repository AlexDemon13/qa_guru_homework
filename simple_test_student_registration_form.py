import time
import os
import unittest
from selenium import webdriver
from registration_page import RegistrationPage

# python -m unittest simple_test_student_registration_form.py

class TestAutomationForm(unittest.TestCase):

    def setUp(self):
        # Инициализация WebDriver (в данном примере Chrome)
        #options = webdriver.ChromeOptions()
        #options.add_argument("--window-size=1920,1080")
        # Раскомментируйте строку ниже, если хотите запустить в фоновом режиме:
        # options.add_argument("--headless")        
        #self.driver = webdriver.Chrome(options=options)

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.page = RegistrationPage(self.driver)


    def test_fill_entire_form(self):
        self.page.open()

        # 0. Ожидаем загрузки страницы (проверяем видимость главного заголовка формы)

        self.assertEqual(self.page.get_title(), "Practice Form")
        self.assertEqual(
            self.page.get_subtitle(),
            "Student Registration Form"
        )

        # 1. Убираем окно "Level up your automation" которое как минимум будет закрывать часть web element-ов и мешать с ними работать!

        # Ожидаем, пока баннер полностью исчезнет, чтобы он не перекрывал элементы формы
        self.page.close_banner()
        # 2. Текстовые поля: Имя и Фамилия
        self.page.fill_first_name("Иван")

        self.page.fill_last_name("Петров")

        # 3. Текстовое поле: Email
        self.page.fill_email("ivan.petrov@example.com")

        # 4. Радиокнопки (Gender): кликаем по связанному тегу <label>, так как сам <input> скрыт
        self.page.select_male()

        self.assertTrue(self.page.is_male_selected())

        # 5. Текстовое поле: Номер телефона (Mobile)
        self.page.fill_mobile("9991234567")

        # 6. Виджет календаря (Date of Birth)
        self.page.open_calendar()

        # Выбираем месяц (декабрь) через выпадающий список внутри календаря
        self.page.select_birth_month("11")

        # Выбираем год (1995)
        self.page.select_birth_year("1995")

        # Выбираем конкретный день месяца (например, 25-е число)
        # Используем специальный класс react-datepicker__day--025, исключая дни соседних месяцев (outside-month)
        self.page.select_birth_day("025")
        self.assertEqual(
            self.page.get_birth_date(),
            "25 Dec 1995"
        )
        # 7. Поле автодополнения (Subjects)
        self.page.select_subject("Computer Science")

        # 8. Чекбоксы (Hobbies): кликаем по связанному <label>
        self.page.select_sports()

        self.page.select_music()

        self.assertTrue(self.page.is_sports_selected())
        self.assertTrue(self.page.is_music_selected())

        # 9. Загрузка файла (Picture)
        # Создаем временный файл для теста, чтобы код оставался переносимым
        temp_file_path = os.path.abspath("test_image.jpg")
        with open(temp_file_path, "w") as f:
            f.write("fake image data")

        self.page.upload_picture(temp_file_path)

        # 10. Текстовая область: Текущий адрес (Current Address)
        self.page.fill_current_address("123456, г. Москва, ул. Ленина, д. 1")

        # Избавляемся от футеров или рекламы, которые могут перекрывать кастомные дропдауны, делаем скрол (главное, демонстрация execute_script)
        self.page.scroll_to_bottom()
        #driver.execute_script("document.getElementsByTagName('footer')[0].style.display='none';")
        #driver.execute_script("document.getElementById('fixedban').style.display='none';")

        # 11. Выпадающий список (Dropdown): Выбор Штата (State)
        self.page.select_state("NCR")
        

        # 12. Выпадающий список (Dropdown): Выбор Города (City)
        self.page.select_city("Delhi")

        # 13. Отправка формы (Submit)
        self.page.submit()

        # 14. Проверка результатов (Expected Conditions для модального окна)
        # Проверяем, что появилось финальное окно с подтверждением
        modal_title = self.page.get_result_title()
        self.assertEqual(modal_title, "Thanks for submitting the form")

        # Проверяем наличие валидных данных в таблице результатов
        result_text = self.page.get_result_text()

        self.assertIn("Иван Петров", result_text)
        self.assertIn("ivan.petrov@example.com", result_text)
        self.assertIn("Male", result_text)
        self.assertIn("9991234567", result_text)
        self.assertIn("25 Dec 1995", result_text) # форма вывода даты может меняться от настроек
        self.assertIn("Computer Science", result_text)
        self.assertIn("Sports, Music", result_text)
        self.assertIn("test_image.jpg", result_text)
        self.assertIn("123456, г. Москва, ул. Ленина, д. 1", result_text)
        self.assertIn("NCR Delhi", result_text)

    def test_empty_form(self):

        self.page.open()
        self.page.close_banner()

        self.page.submit()

        error_message = self.page.get_error_message()
        self.assertEqual(
            error_message,
            "Please fill required fields and enter a valid 10-digit mobile number."
        )

    def test_short_mobile(self):
            self.page.open()
            self.page.close_banner()
            self.page.fill_first_name("Иван")
            self.page.fill_last_name("Петров")
            self.page.select_male()
            self.page.fill_mobile("12345")
            self.page.submit()

            error_message = self.page.get_error_message()
            self.assertEqual(
                error_message,
                "Please fill required fields and enter a valid 10-digit mobile number."
            )

    def tearDown(self):
        # Удаляем созданный временный файл, если он существует
        if os.path.exists("test_image.jpg"):
            os.remove("test_image.jpg")
        # Закрываем браузер
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()