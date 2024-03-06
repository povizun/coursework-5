from src.hhapi import HeadHunterAPI
from src.dbmanager import DBManager


def user_interaction():
    """Функция взаимодействия с пользователем"""
    db_manager = None
    try:
        db_manager = DBManager("coursework_5")
        list_of_companies = [1008541, 9245166, 1002298, 10400968, 2753595, 4787018, 1104183, 2723603, 1418923, 1789341]
        hh_api = HeadHunterAPI(list_of_companies)
        hh_api.upload_vacancies(db_manager)

        while True:
            user_answer = input("""
Введите цифру для выбора информации, которую хотите получить:
1) Список всех компаний и количество вакансий у каждой компании
2) Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
3) Среднюю зарплату по вакансиям
4) Список всех вакансий, у которых зарплата выше средней по всем вакансиям
5) Список всех вакансий, в названии которых содержится ключевое слово, например python
""")

            user_answer_processing(user_answer, db_manager)

            user_answer_repeat = input("\nВы хотите еще вывести какую-то информацию? (Да/Нет)\n").lower()

            if user_answer_repeat == "да":
                pass
            elif user_answer_repeat == "нет":
                break
            else:
                print("Вы ввели неправильный ответ, можно вводить только Да или Нет. Засчитываю ваш ответ как отказ.")
                break

    finally:
        db_manager.conn.close()


def user_answer_processing(user_answer, db_manager):
    """Функция обработки запроса пользователя"""
    if user_answer == "1":
        answer = db_manager.get_companies_and_vacancies_count()
        for company in answer:
            print(f"\nУ компании {company[0]} {company[1]} вакансий")
    elif user_answer == "2":
        answer = db_manager.get_all_vacancies()
        for vacancy in answer:
            print(f"""
    Название компании: {vacancy[0]}
    Название вакансии: {vacancy[1]}
    Зарплата: {vacancy[2]} {vacancy[3]}
    Ссылка на вакансию: {vacancy[4]}
    """)
    elif user_answer == "3":
        answer = db_manager.get_avg_salary()
        print(f"\nСредняя зарплата по вакансиям: {answer}\n")
    elif user_answer == "4":
        answer = db_manager.get_vacancies_with_higher_salary()
        for vacancy in answer:
            print(f"""
    Название компании: {vacancy[0]}
    Название вакансии: {vacancy[1]}
    Зарплата: {vacancy[2]} {vacancy[3]}
    Ссылка на вакансию: {vacancy[4]}
    """)
    elif user_answer == "5":
        user_keyword = input("Введите ключевое слово, регистр важен ")
        answer = db_manager.get_vacancies_with_keyword(user_keyword)
        for vacancy in answer:
            print(f"""
    Название компании: {vacancy[0]}
    Название вакансии: {vacancy[1]}
    Зарплата: {vacancy[2]} {vacancy[3]}
    Ссылка на вакансию: {vacancy[4]}
    """)
    else:
        print("Вы ввели неправильный ответ, можно вводить только цифры от 1 до 5")
