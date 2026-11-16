import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumpagefactory.Pagefactory import PageFactory


class TableElement:
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    @property
    def element(self):
        return self.driver.find_element(*self.locator)

    def get_headers(self) -> list[str]:
        headers = self.element.find_elements(By.CSS_SELECTOR, "thead th")
        return [header.text for header in headers]

    def get_row_data(self, row_index: int) -> list[str]:
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row_index].find_elements(By.TAG_NAME, "td")
        return [cell.text for cell in cells]

    def get_cell_value(self, row_index: int, column_index: int) -> str:
        return self.get_row_data(row_index)[column_index]


class TableElementPF(TableElement, PageFactory):
    def __init__(self, driver, locator):
        self.driver = driver
        locator_type, locator_value = locator
        self.locators = {
            "table_root": (locator_type, locator_value)
        }

    @property
    def element(self):
        return self.table_root


@pytest.fixture
def driver():
    browser_driver = webdriver.Chrome()
    browser_driver.maximize_window()

    try:
        browser_driver.get("https://the-internet.herokuapp.com/tables")

        wait = WebDriverWait(browser_driver, 10)
        for table_id in ("table1", "table2"):
            wait.until(
                EC.visibility_of_element_located((By.ID, table_id))
            )

        yield browser_driver
    finally:
        browser_driver.quit()


@pytest.fixture(params=[
    pytest.param(TableElement, id="selenium"),
    pytest.param(TableElementPF, id="page_factory"),
])
def tables(driver, request):
    table_class = request.param
    table1 = table_class(driver, (By.ID, "table1"))
    table2 = table_class(driver, (By.ID, "table2"))
    return table1, table2


def test_headers_in_both_tables(tables):
    expected = [
        "Last Name",
        "First Name",
        "Email",
        "Due",
        "Web Site",
        "Action",
    ]

    for number, table in enumerate(tables, start=1):
        assert table.get_headers() == expected, (
            f"Не совпадают заголовки таблицы {number}"
        )


def test_first_row_in_both_tables(tables):
    expected = [
        "Smith",
        "John",
        "jsmith@gmail.com",
        "$50.00",
        "http://www.jsmith.com",
        "edit delete",
    ]

    for number, table in enumerate(tables, start=1):
        assert table.get_row_data(0) == expected, (
            f"Не совпадает первая строка таблицы {number}"
        )


def test_cells_in_both_tables(tables):
    for number, table in enumerate(tables, start=1):
        assert table.get_cell_value(0, 0) == "Smith", (
            f"Не совпадает фамилия в таблице {number}"
        )
        assert table.get_cell_value(2, 3) == "$100.00", (
            f"Не совпадает сумма Due в таблице {number}"
        )