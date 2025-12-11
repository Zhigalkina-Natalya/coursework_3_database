from typing import List, Tuple

import psycopg

from config import DB_CONFIG


class DBManager:
    """
    Класс для взаимодействия с базой данных PostgreSQL.
    """

    def __init__(self)-> None:
        """
       Инициализирует подключение к базе данных и создаёт курсор.
       conn - объект соединения с базой данных.
       cur - объект курсора для выполнения SQL-запросов.
       """
        self.conn = psycopg.connect(**DB_CONFIG)
        self.cur = self.conn.cursor()

    def close(self)-> None:
        """
        Закрывает курсор и соединение с базой данных.
        """
        self.cur.close()
        self.conn.close()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Возвращает список компаний и количество вакансий у каждой компании.
        """
        self.cur.execute(
            """
            SELECT c.name, COUNT(v.id)
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.name;
        """
        )
        return self.cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, float, float, str, str]]:
        """
        Возвращает список всех вакансий с информацией (указанием компании, должности, зарплаты, валюты и ссылки).
        """
        self.cur.execute(
            """
            SELECT c.name, v.title, v.salary_from, v.salary_to, v.url, v.salary_currency
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id;
        """
        )
        return self.cur.fetchall()

    def get_avg_salary(self) -> float:
        """
        Возвращает среднюю зарплату по вакансиям.
        """
        self.cur.execute(
            """
            SELECT AVG((salary_from + salary_to)/2) FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
        """
        )
        result = self.cur.fetchone()
        avg_salary = result[0]
        return avg_salary

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, float, float, str, str]]:
        """
        Возвращает вакансии, у которых средняя зарплата выше средней по всем вакансиям.
        """
        avg_salary = self.get_avg_salary()
        self.cur.execute(
            """
                SELECT c.name, v.title, v.salary_from, v.salary_to, v.url, v.salary_currency
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE v.salary_from IS NOT NULL
                  AND v.salary_to IS NOT NULL
                  AND ((v.salary_from + v.salary_to) / 2) > %s;
            """,
            (avg_salary,),
        )

        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, float, float, str, str]]:
        """
        Возвращает вакансии, в названии которых есть ключевое слово.
        """
        self.cur.execute(
            """
            SELECT c.name, v.title, v.salary_from, v.salary_to, v.url, v.salary_currency
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.title ILIKE %s;
        """,
            (f"%{keyword}%",),
        )
        return self.cur.fetchall()
