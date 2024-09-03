import os
from typing import Dict, List, Tuple

import pytest

from paths import VACANCIES_JSON_PATH
from src.vacancy.vacancy import Vacancy


@pytest.fixture
def vacancies() -> Tuple[Vacancy, Vacancy, Vacancy, Vacancy]:
    """
    Фикстура содержащая экземпляры класса Vacancy.

    :return: Экземпляры класса Vacancy.
    """
    v1 = Vacancy("Чайный сомелье", "https://hh.ru/vacancy/106029258", "от 80 000 ₽", "Требования не указаны")

    v2 = Vacancy(
        "Тестировщик комфорта квартир",
        "https://hh.ru/vacancy/93353083",
        "350 000 - 450 000 ₽",
        "Занимать активную жизненную позицию",
    )

    v3 = Vacancy("Go Developer", "https://hh.ru/vacancy/106507837", "600 000 руб.")

    v4 = Vacancy(
        "Контролер склада",
        "https://hh.ru/vacancy/103531332",
        requirements="От Вас: Желание зарабатывать. Внимательность, ответственность.",
    )

    return v1, v2, v3, v4


@pytest.fixture(autouse=True)
def cleanup_file() -> None:
    """
    Фикстура, удаляющая файл vacancies.json перед каждым тестом, если он существует
    """
    if os.path.exists(VACANCIES_JSON_PATH):
        os.remove(VACANCIES_JSON_PATH)


@pytest.fixture
def json_data_items() -> List[Dict]:
    """
    Фикстура, содержащая информацию о вакансиях в форме ответа от API (ключ 'items').

    :return: Данные о вакансиях.
    """
    return [
        {
            "id": "105661463",
            "name": "Python разработчик",
            "area": {"id": "1", "name": "Москва"},
            "salary": {"from": 60000, "to": 110000},
            "alternate_url": "https://hh.ru/vacancy/105661463",
            "snippet": {"requirement": "Опыт работы с асинхронным питоном."},
        },
        {
            "id": "101951553",
            "name": "Trainee/Intern/Junior Python backend developer",
            "area": {"id": "2", "name": "Санкт-Петербург"},
            "salary": {"from": 10000, "to": 30000},
            "alternate_url": "https://hh.ru/vacancy/101951553",
            "snippet": {"requirement": "Для этого мы ищем начинающего амбициозного интерна-джуна питониста."},
        },
        {
            "id": "105193821",
            "name": "Python developer",
            "area": {"id": "2", "name": "Санкт-Петербург"},
            "salary": {"from": 80000, "to": "None"},
            "alternate_url": "https://hh.ru/vacancy/105193821",
            "snippet": {"requirement": "Отличное знание Python."},
        },
    ]


@pytest.fixture
def prepared_data() -> Dict:
    """
    Фикстура, содержащая данные о вакансиях, подготовленные к записи в файл.

    :return: Данные о вакансиях.
    """
    return {
        105661463: {
            "name": "Python разработчик",
            "url": "https://hh.ru/vacancy/105661463",
            "salary": "60000-110000 руб.",
            "requirements": "Опыт работы с асинхронным питоном.",
        },
        101951553: {
            "name": "Trainee/Intern/Junior Python backend developer",
            "url": "https://hh.ru/vacancy/101951553",
            "salary": "10000-30000 руб.",
            "requirements": "Для этого мы ищем начинающего амбициозного интерна-джуна питониста.",
        },
        105193821: {
            "name": "Python developer",
            "url": "https://hh.ru/vacancy/105193821",
            "salary": "80000-None руб.",
            "requirements": "Отличное знание Python.",
        },
    }


@pytest.fixture
def vacancies_from_file() -> Dict:
    """
    Фикстура, содержащая данные загруженные из файла.

    :return: Данные о вакансиях.
    """
    return {
        "1": {
            "name": "Чайный сомелье",
            "url": "https://hh.ru/vacancy/106029258",
            "salary": "80000 руб.",
            "requirements": "Требования не указаны",
        },
        "2": {
            "name": "Тестировщик комфорта квартир",
            "url": "https://hh.ru/vacancy/93353083",
            "salary": "350000-450000 руб.",
            "requirements": "Занимать активную жизненную позицию",
        },
        "3": {
            "name": "Go Developer",
            "url": "https://hh.ru/vacancy/106507837",
            "salary": "600000 руб.",
            "requirements": "Требования не указаны.",
        },
        "4": {
            "name": "Контролер склада",
            "url": "https://hh.ru/vacancy/103531332",
            "salary": "0 руб.",
            "requirements": "От Вас: Желание зарабатывать. Внимательность, ответственность.",
        },
    }
