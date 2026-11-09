import time

import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Локаторы элементов формы на странице
LOGIN_INPUT     = (By.ID, "login-input")
PASSWORD_INPUT  = (By.ID, "password-input")
SUBMIT_BUTTON   = (By.ID, "submit-button")
STATUS_MESSAGE  = (By.ID, "error-message")
WELCOME_MESSAGE = (By.ID, "welcome-message")


@pytest.fixture
def driver():
    """Фикстура для инициализации и закрытия браузера."""
    #options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Фоновый режим для CI/CD
    #options.add_argument("--window-size=1920,1080")    
    #driver = webdriver.Chrome(options=options)

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


# Реализация DDT подхода через параметризацию pytest
@pytest.mark.parametrize(
    "email, password, scenario_type, expected_text",
    [
        # --- ПОЗИТИВНЫЕ СЦЕНАРИИ ---
        ("user1", "password1", "positive", "Welcome, user1!"),

        # --- НЕГАТИВНЫЕ СЦЕНАРИИ ---
        ("user1", "wrong_pass", "negative", "Wrong login or password"),
        ("unknown@qa.guru", "qaguru", "negative", "Wrong login or password"),
        ("", "qaguru", "negative", "Login is required (minimum 3 characters)"),
        ("qaguru@qa.guru", "", "negative", "Password is required (minimum 6 characters)"),
        ("", "", "negative", "Login and password are required (minimum 3 and 6 characters)"),
        ("qaguruqa.guru", "qaguru", "negative", "Wrong login or password"),
        ("qaguru@", "qaguru", "negative", "Wrong login or password"),
        ("@qa.guru", "qaguru", "negative", "Wrong login or password"),
        ("qaguru' OR '1'='1", "' OR '1'='1", "negative", "Wrong login or password"),
        ("USER1", "password1", "negative", "Wrong login or password"), ]
)
def test_login_form(driver, email, password, scenario_type, expected_text):
    """Тест кейс, принимающий наборы данных (DDT)."""
    
    # 1. Открытие тестируемой страницы
    driver.get("https://qa-guru.github.io/one-page-form/login.html")
    
    # 2. Поиск элементов формы
    email_field = driver.find_element(*LOGIN_INPUT)    
    password_field = driver.find_element(*PASSWORD_INPUT)    
    submit_button = driver.find_element(*SUBMIT_BUTTON)
    
    # 3. Очистка полей и ввод тестовых данных
    email_field.clear()
    email_field.send_keys(email)
    
    password_field.clear()
    password_field.send_keys(password)
    
    # 4. Клик по кнопке отправки формы
    submit_button.click()

    # 5. Выбираем, какое сообщение ждать
    if scenario_type == "positive":
        message_locator = WELCOME_MESSAGE
    else:
        message_locator = STATUS_MESSAGE

    # 6. Ждём видимости сообщения и читаем текст
    message = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(message_locator)
    )
    actual_result = message.text

    # 7. Проверяем точное совпадение текста
    assert expected_text == actual_result, (
        f"Ожидали: '{expected_text}', получили: '{actual_result}'"
    )