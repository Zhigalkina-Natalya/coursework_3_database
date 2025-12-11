from create_db import create_tables
from data_loader import load_data
from db_manager import DBManager
from utils import print_avg_salary, print_companies, print_vacancies


def menu():
    """
    Интерактивное меню управления.
    """
    print("\nМЕНЮ УПРАВЛЕНИЯ")
    print("1. Список компаний и количество вакансий")
    print("2. Все вакансии")
    print("3. Средняя зарплата по вакансиям")
    print("4. Вакансии с зарплатой выше средней")
    print("5. Поиск вакансий по ключевому слову")
    print("0. Выход")
    return input("\nВыберите пункт меню: ")


def main():
    print("Запуск проекта HH Database\n")

    # 1 Создание БД и таблиц
    create_tables()

    # 2 Подключение к БД
    db = DBManager()

    # 3 Предложение загрузить данные
    choice = input("Хотите загрузить данные о компаниях с hh.ru? (y/n): ").strip().lower()
    if choice == "y":
        load_data(db)

    # 4 Основной цикл меню
    while True:
        choice = menu()

        if choice == "1":
            companies = db.get_companies_and_vacancies_count()
            print_companies(companies)

        elif choice == "2":
            vacancies = db.get_all_vacancies()
            print_vacancies(vacancies)

        elif choice == "3":
            avg = db.get_avg_salary()
            print_avg_salary(avg)

        elif choice == "4":
            vacancies = db.get_vacancies_with_higher_salary()
            print_vacancies(vacancies)

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска (нажмите Enter для поиска по 'Python'): ").strip()
            if not keyword:  # если пользователь ничего не ввёл
                keyword = "Python"
                print("\nПоиск вакансий по умолчанию: 'Python'\n")
            else:
                print(f"\nПоиск вакансий по слову: '{keyword}'\n")
            vacancies = db.get_vacancies_with_keyword(keyword)
            print_vacancies(vacancies)

        elif choice == "0":
            print("\nЗавершение работы. До встречи!")
            db.close()
            break

        else:
            print("Неверный пункт меню. Повторите ввод.")


if __name__ == "__main__":
    main()
