from typing import List, Tuple


def format_salary(salary_from, salary_to, currency):
    """
    Возвращает зарплату в человекочитаемом формате с пробелами между тысячами.
    """

    def fmt(value):
        """
        Форматирует число с пробелами между тысячами.
        """
        return f"{int(value):,}".replace(",", " ")

    if salary_from and salary_to:
        return f"{fmt(salary_from)}–{fmt(salary_to)} {currency}"
    elif salary_from:
        return f"от {fmt(salary_from)} {currency}"
    elif salary_to:
        return f"до {fmt(salary_to)} {currency}"
    return "не указана"


def print_companies(companies: List[Tuple[str, int]]):
    """
    Выводит список компаний и количество вакансий.
    """
    print("\n Компании и количество вакансий")
    print("-" * 45)
    for name, count in companies:
        print(f"{name:<30} | {count} вакансий")
    print("-" * 45)


def print_vacancies(vacancies: List[Tuple[str, str, float, float, str, str]]):
    """
    Выводит список вакансий в красивом формате.
    """
    print("\n Список вакансий")
    print("-" * 90)
    for company, title, salary_from, salary_to, url, currency in vacancies:
        salary = format_salary(salary_from, salary_to, currency)
        print(f"Компания: {company}\nВакансия: {title}\nЗарплата: {salary}\nСсылка: {url}\n")
    print("-" * 90)


def print_avg_salary(avg_salary: float):
    """
    Выводит среднюю зарплату в человекочитаемом виде с пробелами между тысячами.
    """
    if avg_salary:
        formatted = f"{int(avg_salary):,}".replace(",", " ")
        print(f"\n Средняя зарплата: {formatted} RUB")
    else:
        print("\n Средняя зарплата не указана.")
