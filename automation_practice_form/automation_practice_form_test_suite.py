import os
import automation_practice_form_po

class AutomationPracticeFormTestSuite:
    def __init__(self):
        self.automation_practice_form = automation_practice_form_po.AutomationPracticeFormPO("https://qa-guru.github.io/one-page-form/automation-practice-form.html")

    def setup(self):
        self.automation_practice_form.setup()
        self.tmp_file_name = self._create_tmp_file()

    def _create_tmp_file(self):
        file_path = os.path.abspath('test_file.jpg')
        with open(file_path, 'w') as file:
            file.write("Test")
        return file_path
    
    def test_form_positive01(self):
        self.automation_practice_form.fill_in_form(self.tmp_file_name, "Dmitry","Bugaev", "bugaev@example.com", "Male","1234567890",("1988", "4", "22"),("Maths", "English"), ("Sports", "Music"), "г. Санкт-Петербург, ул. Невский проспект, д 101", "NCR",  "Noida")
        self.assert_form(self.tmp_file_name, "Dmitry","Bugaev", "bugaev@example.com", "Male","1234567890",("1988", "4", "22"),("Maths", "English"), ("Sports", "Music"), "г. Санкт-Петербург, ул. Невский проспект, д 101", "NCR",  "Noida")

    def test_form_positive02(self):
        self.automation_practice_form.fill_in_form(self.tmp_file_name, "Ivan","Petrov", "ivan.petrov@example.com", "Male","9991234567",("1988", "4", "22"),("Maths", "English"), ("Sports", "Music"), "г. Санкт-Петербург, ул. Невский проспект, д 101", "NCR",  "Noida")
        self.assert_form(self.tmp_file_name, "Ivan","Petrov", "ivan.petrov@example.com", "Male","9991234567",("1988", "4", "22"),("Maths", "English"), ("Sports", "Music"), "г. Санкт-Петербург, ул. Невский проспект, д 101", "NCR",  "Noida")

    def test_form_positive03(self):
        self.automation_practice_form.fill_in_form(self.tmp_file_name, "Anna","Petrova", "anna.petrova@example.com", "Female","9997654321",("1995", "11", "25"),("English",), ("Music",), "г. Санкт-Петербург, ул. Невский проспект, д 101", "NCR",  "Noida")
        self.assert_form(self.tmp_file_name, "Anna","Petrova", "anna.petrova@example.com", "Female","9997654321",("1995", "11", "25"),("English",), ("Music",), "г. Санкт-Петербург, ул. Невский проспект, д 101", "NCR",  "Noida")


    def assert_form(self, file_name=None, first_name=None, last_name=None, email=None, gender=None, user_number=None,
                    birth_day=None, subjects=None, hobbies=None, current_address=None, state=None, city=None):
        result_text = self.automation_practice_form.get_result_text()

        months = (
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        )
        year, month, day = birth_day
        expected_birth_date = (
            f"{int(day):02d} {months[int(month)]} {year}"
        )

        expected_data = {
            "Student Name": f"{first_name} {last_name}",
            "Student Email": email,
            "Gender": gender,
            "Mobile": user_number,
            "Date of Birth": expected_birth_date,
            "Subjects": ", ".join(subjects),
            "Hobbies": ", ".join(hobbies),
            "Picture": os.path.basename(file_name),
            "Address": current_address,
            "State and City": f"{state} {city}"
        }

        for key, value in expected_data.items():
            assert key in result_text and value in result_text, f"Значения {value} из строки {key} не совпадают!"

    def tear_down(self):
        if os.path.exists(self.tmp_file_name):
            os.remove(self.tmp_file_name)
        self.automation_practice_form.tear_down()

for test_name in ("test_form_positive01", "test_form_positive02","test_form_positive03"):
    test_suite = AutomationPracticeFormTestSuite()
    try:
        test_suite.setup()
        getattr(test_suite, test_name)()
        print(f"{test_name}: PASS")
    finally:
        test_suite.tear_down()