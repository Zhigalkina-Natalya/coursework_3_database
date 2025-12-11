import psycopg

from config import DB_CONFIG


def create_database_if_not_exists():
    """
    Создаёт базу данных hh_project_db, если она ещё не существует.
    """
    dbname = DB_CONFIG["dbname"]

    # Подключаемся к дефолтной базе postgres
    with psycopg.connect(
        dbname="postgres",
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
    ) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
            exists = cur.fetchone()
            if not exists:
                print(f"База данных '{dbname}' не найдена. Создаю новую...")
                cur.execute(f'CREATE DATABASE "{dbname}";')
                print(f"База данных '{dbname}' успешно создана.")
            else:
                print(f"База данных '{dbname}' уже существует.")


def create_tables():
    """Создаёт таблицы companies и vacancies."""
    create_database_if_not_exists()

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                    CREATE TABLE IF NOT EXISTS companies (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255),
                        area VARCHAR(255),
                        description TEXT
                    );
                """
            )

            cur.execute(
                """
                    CREATE TABLE IF NOT EXISTS vacancies (
                        id SERIAL PRIMARY KEY,
                        title TEXT,
                        salary_from NUMERIC,
                        salary_to NUMERIC,
                        salary_currency VARCHAR(10),
                        url TEXT UNIQUE,
                        company_id INTEGER REFERENCES companies(id)
                    );
                """
            )

            conn.commit()
            print("Таблицы успешно созданы или уже существуют.")
