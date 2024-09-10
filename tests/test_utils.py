from typing import Dict, List

from src.utils.utils import create_list_of_vacancies, get_salary
from src.vacancy.vacancy import Vacancy


def test_get_salary(json_data_items: List[Dict], vacancies_from_file: List[Dict]) -> None:
    """
    Тест утилиты, отвечающей за подготовку информации о зарплате к инициализации объекта Vacancy.

    :param json_data_items: Фикстура, представляющая данные полученные от API.
    :param vacancies_from_file: Фикстура, представляющая данные, выгруженные из файла.
    """
    for index in range(4):
        salary_from_json = json_data_items[index]["salary"]
        expected_salary = vacancies_from_file[index]["salary"]

        assert get_salary(salary_from_json) == expected_salary


def test_create_list_of_vacancies(json_data_items: List[Dict], vacancies: List[Vacancy]) -> None:
    """
    Тест утилиты, отвечающей за создание списка объектов вакансий из данных, полученных от API.

    :param json_data_items: Фикстура, представляющая данные полученные от API.
    :param vacancies: Фикстура, представляющая список объектов.
    """
    vacancies_list = create_list_of_vacancies(json_data_items)

    for index in range(4):
        created_vacancy = vacancies_list[index]
        expected_vacancy = vacancies[index]

        assert created_vacancy.name == expected_vacancy.name
        assert created_vacancy.url == expected_vacancy.url
        assert created_vacancy.salary == expected_vacancy.salary
        assert created_vacancy.city == expected_vacancy.city
        assert created_vacancy.requirements == expected_vacancy.requirements
