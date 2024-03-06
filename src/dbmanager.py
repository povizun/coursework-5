from config import load_config
import psycopg2


class DBManager:

    def __init__(self, database_name):
        self.conn = None
        self.create_database(database_name)

    def create_database(self, database_name):
        """Очистка и создание дата базы с добавлением необходимых таблиц"""
        conn = psycopg2.connect(**load_config(), database="postgres")
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(f"DROP DATABASE {database_name}")
        except psycopg2.Error as error:
            print(error)
        cur.execute(f"CREATE DATABASE {database_name}")

        conn.close()
        self.conn = psycopg2.connect(**load_config(), database=database_name)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("""
                            CREATE TABLE employers (
                                employer_id INTEGER PRIMARY KEY,
                                employer_name VARCHAR NOT NULL
                            )
                        """)
            with self.conn.cursor() as cur:
                cur.execute("""
                            CREATE TABLE vacancies (
                                vacancy_id INTEGER PRIMARY KEY,
                                employer_id INTEGER REFERENCES employers(employer_id),
                                vacancy_name VARCHAR,
                                salary INTEGER,
                                currency VARCHAR,
                                link VARCHAR
                            )
                        """)

    def is_employer_exist(self, employer_id):
        """Проверка на наличие компании в таблице компаний"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT EXISTS(SELECT employer_id FROM employers WHERE employer_id={employer_id})")
                current_ids = cur.fetchall()
                return current_ids[0][0]

    def add_employer(self, employer_id, employer_name):
        """Добавление компании в таблицу компаний"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO employers VALUES (%s, %s)",
                            (employer_id, employer_name))

    def add_vacancy(self, vacancy_id, employer_id, name, salary, currency, link):
        """Добавление вакансии в таблицу вакансий"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                            (vacancy_id, employer_id, name, salary, currency, link))

    def get_companies_and_vacancies_count(self):
        """Функция возвращает список всех компаний и количество вакансий у каждой компании"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("""SELECT employer_name, COUNT(vacancy_id) FROM vacancies JOIN employers USING(employer_id) 
GROUP BY employer_name""")
                result = cur.fetchall()
                return result

    def get_all_vacancies(self):
        """Функция возвращает список всех вакансий с указанием названия компании, названия вакансии,
           зарплаты и ссылки на вакансию"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("""SELECT employer_name, vacancy_name, salary, currency, link FROM vacancies 
JOIN employers USING(employer_id)""")
                result = cur.fetchall()
                return result

    def get_avg_salary(self):
        """Функция возвращает среднюю зарплату по вакансиям"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT ROUND(AVG(salary), 2) FROM vacancies WHERE currency IS NOT NULL")
                result = cur.fetchall()
                return result[0][0]

    def get_vacancies_with_higher_salary(self):
        """Функция возвращает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("""SELECT employer_name, vacancy_name, salary, currency, link FROM vacancies 
JOIN employers USING(employer_id) 
WHERE salary > (SELECT ROUND(AVG(salary), 2) 
FROM vacancies WHERE currency IS NOT NULL)""")
                result = cur.fetchall()
                return result

    def get_vacancies_with_keyword(self, keyword):
        """Функция возвращает список всех вакансий, в названии которых содержатся переданные в метод слова,
           например python"""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"""SELECT employer_name, vacancy_name, salary, currency, link FROM vacancies 
JOIN employers USING(employer_id) 
WHERE vacancy_name LIKE '%{keyword}%'""")
                result = cur.fetchall()
                return result
