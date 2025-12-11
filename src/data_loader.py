import datetime

from db_manager import DBManager
from hh_api import get_company_info, get_company_vacancies


def load_data(db: DBManager):
    """
    Загружает данные о компаниях и их вакансиях с hh.ru.
    """
    company_ids = [1740, 3529, 78638, 80, 15478, 2180, 1057, 2748, 3776, 1122462]

    print("\nЗагрузка данных с hh.ru...")

    errors_found = False  # флаг наличия ошибок

    # Создаём/очищаем лог перед загрузкой
    with open("errors.log", "w", encoding="utf-8") as f:
        f.write("Ошибки загрузки данных с hh.ru\n")
        f.write(f"Дата: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n\n")

    # Загружаем данные по каждой компании
    for cid in company_ids:
        try:
            company = get_company_info(cid)

            if "id" not in company:
                print(f"Не удалось получить данные для компании ID {cid}. Пропускаю.")
                errors_found = True
                with open("errors.log", "a", encoding="utf-8") as f:
                    f.write(f"Не удалось получить данные для компании ID {cid}\n")
                continue

            db.cur.execute(
                "INSERT INTO companies (id, name, area, description)"
                "VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;",
                (int(company["id"]), company["name"], company.get("area", {}).get("name"), company.get("description")),
            )

            # Загружаем вакансии компании
            vacancies = get_company_vacancies(cid)
            for v in vacancies:
                salary = v.get("salary") or {}
                db.cur.execute(
                    """
                    INSERT INTO vacancies (title, salary_from, salary_to, salary_currency, url, company_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                    """,
                    (
                        v.get("name"),
                        salary.get("from"),
                        salary.get("to"),
                        salary.get("currency"),
                        v.get("alternate_url"),
                        int(company["id"]),
                    ),
                )

            print(f"{company['name']} — данные успешно загружены.")

        except Exception as e:
            errors_found = True
            msg = f"Ошибка при обработке компании ID {cid}: {e}"
            print(msg)
            with open("errors.log", "a", encoding="utf-8") as f:
                f.write(f"{msg}\n")

    db.conn.commit()

    # Итоговая запись в лог
    with open("errors.log", "a", encoding="utf-8") as f:
        if not errors_found:
            f.write("Ошибок не обнаружено\n")

    # Сообщение пользователю
    if errors_found:
        print("\nЗагрузка завершена с ошибками. Подробности — в errors.log\n")
    else:
        print("\nЗагрузка данных успешно завершена. Ошибок не обнаружено.\n")
