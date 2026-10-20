import time
from selenium import webdriver
from selenium.webdriver.common.by import By


# Первый шаг - выделение каждого теста в отдельную функцию и ее последующий вызов

def test01():
    print("Рефакторинг - итерация 1!")

    # 1. Запуск браузера Chrome
    driver = webdriver.Chrome()

    try:
        # 2. Открытие страницы
        driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
        driver.maximize_window()
        time.sleep(5)  # Пауза, чтобы визуально заметить открытие

        # 3. Поиск элементов и заполнение полей
        # Находим поле Full Name по его ID и вводим текст
        full_name_field = driver.find_element(By.ID, "userName")
        # web_elements = driver.find_elements(By.XPATH, "someXPath")

        full_name_field.send_keys("Иван Иванов")

        # Находим поле Email по его ID и вводим текст
        email_field = driver.find_element(By.ID, "userEmail")
        email_field.send_keys("ivan@example.com")

        current_address_field = driver.find_element(By.ID, "currentAddress")
        current_address_field.send_keys("Москва, улица Лесная, дом 10")

        permanent_address_field = driver.find_element(By.ID, "permanentAddress")
        permanent_address_field.send_keys("Казань, улица Мира, дом 5")

        # Находим кнопку Submit по ее ID и кликаем
        # Находим кнопку, прокручиваем к ней и нажимаем
        submit_button = driver.find_element(By.ID, "submit")
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            submit_button
        )
        submit_button.click()

        # 4. Проверка результата
        time.sleep(5)  # Пауза, чтобы увидеть результат отправки

        # Находим блок с отправленными данными
        result_box = driver.find_element(By.ID, "output")

        # Проверяем, что в блоке результата появился введенный текст
        assert "Иван Иванов" in result_box.text
        assert "Москва, улица Лесная, дом 10" in result_box.text
        assert "Казань, улица Мира, дом 5" in result_box.text
        print("Тест успешно пройден!")

    finally:
        # 5. Закрытие браузера в любом случае
        driver.quit()


def test02():
    print("Рефакторинг - итерация 1!")

    # 1. Запуск браузера Chrome
    driver = webdriver.Chrome()

    try:
        # 2. Открытие страницы
        driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
        driver.maximize_window()
        time.sleep(5)  # Пауза, чтобы визуально заметить открытие

        # 3. Поиск элементов и заполнение полей
        # Находим поле Full Name по его ID и вводим текст
        full_name_field = driver.find_element(By.ID, "userName")
        # web_elements = driver.find_elements(By.XPATH, "someXPath")

        full_name_field.send_keys("Иван Иванов")

        # Находим поле Email по его ID и вводим текст
        email_field = driver.find_element(By.ID, "userEmail")
        email_field.send_keys("ivanexample.com")

        # Находим кнопку Submit по ее ID и кликаем
        submit_button = driver.find_element(By.ID, "submit")
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            submit_button
        )
        submit_button.click()

        # 4. Проверка результата
        time.sleep(5)  # Пауза, чтобы увидеть результат отправки

        # Находим блок с отправленными данными
        result_box = driver.find_element(By.ID, "output")

        # Проверяем, что некорректный email отклонён и результат не показан
        assert email_field.get_property("validity")["typeMismatch"]
        assert not result_box.is_displayed()
        print("Тест успешно пройден!")

    finally:
        # 5. Закрытие браузера в любом случае
        driver.quit()


test01()
test02()