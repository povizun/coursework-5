import requests
from src.dbmanager import DBManager


class HeadHunterAPI:
    """Класс API HeadHunter"""
    def __init__(self, companies):
        headers = {"User-Agent": "AM"}
        self.unprocessed_vacancies = []
        for company in companies:
            response = requests.get("https://api.hh.ru/vacancies", headers=headers,
                                    params=f"per_page=100&employer_id={company}")

            self.unprocessed_vacancies.append(response.json())

    def upload_vacancies(self, dbmanager: DBManager):
        """Обработка вакансий и загрузка в базу данных"""
        for company in self.unprocessed_vacancies:
            for vacancy in company["items"]:
                name = vacancy['name']
                vacancy_id = vacancy['id']
                link = f"https://hh.ru/vacancy/{vacancy_id}"
                salary, currency = self.convert_salary(vacancy['salary'])
                employer_id = vacancy['employer']['id']
                if not dbmanager.is_employer_exist(employer_id):
                    dbmanager.add_employer(employer_id, vacancy['employer']['name'])
                dbmanager.add_vacancy(vacancy_id, employer_id, name, salary, currency, link)

    @staticmethod
    def convert_salary(salary):
        """Обработка зарплаты, приведение к общему виду"""
        if salary is None:
            value = 0
            currency = None
        elif salary["to"] is None:
            value = salary["from"]
            currency = salary["currency"]
        elif salary["from"] is None:
            value = salary["to"]
            currency = salary["currency"]
        else:
            value = round((salary["to"] + salary["from"]) / 2)
            currency = salary["currency"]
        return value, currency
