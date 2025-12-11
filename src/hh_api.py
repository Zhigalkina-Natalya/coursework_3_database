from typing import Dict, List

import requests

BASE_URL = "https://api.hh.ru"


def get_company_info(company_id: int) -> Dict:
    """Получает информацию о компании по её ID."""
    response = requests.get(f"{BASE_URL}/employers/{company_id}")
    return response.json()


def get_company_vacancies(employer_id: int, pages: int = 1) -> List[Dict]:
    """Получает вакансии конкретной компании по её ID."""
    vacancies = []
    for page in range(pages):
        response = requests.get(
            f"{BASE_URL}/vacancies", params={"employer_id": employer_id, "page": page, "per_page": 100}
        )
        data = response.json()
        vacancies.extend(data.get("items", []))
    return vacancies
