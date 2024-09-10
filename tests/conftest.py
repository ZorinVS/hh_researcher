import os
from typing import Dict, List

import pytest

from paths import VACANCIES_JSON_PATH
from src.vacancy.vacancy import Vacancy


@pytest.fixture
def vacancies() -> List[Vacancy]:
    """
    Фикстура, содержащая экземпляры класса Vacancy.

    :return: Экземпляры класса Vacancy.
    """
    v1 = Vacancy(
        "Чайный сомелье", "https://hh.ru/vacancy/106029258", "от 80 000 ₽", "Санкт-Петербург", "Требования не указаны."
    )

    v2 = Vacancy(
        "Тестировщик комфорта квартир",
        "https://hh.ru/vacancy/93353083",
        "350 000 - 450 000 ₽",
        "Воронеж",
        "Занимать активную жизненную позицию",
    )

    v3 = Vacancy("Go Developer", "https://hh.ru/vacancy/106507837", "600 000 руб.", "Москва")

    v4 = Vacancy(
        "Контролер склада",
        "https://hh.ru/vacancy/103531332",
        city="Москва",
        requirements="От Вас: Желание зарабатывать. Внимательность, ответственность.",
    )

    return [v1, v2, v3, v4]


@pytest.fixture(autouse=True)
def cleanup_file() -> None:
    """Фикстура, удаляющая файл vacancies.json перед каждым тестом, если он существует"""
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
            "name": "Чайный сомелье",
            "area": {"id": "2", "name": "Санкт-Петербург"},
            "salary": {"from": 80000, "to": None},
            "alternate_url": "https://hh.ru/vacancy/106029258",
            "snippet": {"requirement": None},
        },
        {
            "name": "Тестировщик комфорта квартир",
            "area": {"id": "26", "name": "Воронеж"},
            "salary": {"from": 350000, "to": 450000},
            "alternate_url": "https://hh.ru/vacancy/93353083",
            "snippet": {"requirement": "Занимать активную жизненную позицию"},
        },
        {
            "name": "Go Developer",
            "area": {"id": "1", "name": "Москва"},
            "salary": {"from": None, "to": 600000},
            "alternate_url": "https://hh.ru/vacancy/106507837",
            "snippet": {"requirement": None},
        },
        {
            "name": "Контролер склада",
            "area": {"id": "1", "name": "Москва"},
            "salary": None,
            "alternate_url": "https://hh.ru/vacancy/103531332",
            "snippet": {"requirement": "От Вас: Желание зарабатывать. Внимательность, ответственность."},
        },
    ]


@pytest.fixture
def vacancies_from_file() -> List:
    """
    Фикстура, содержащая данные загруженные из файла.

    :return: Данные о вакансиях.
    """
    return [
        {
            "name": "Чайный сомелье",
            "url": "https://hh.ru/vacancy/106029258",
            "salary": "80000 руб.",
            "city": "Санкт-Петербург",
            "requirements": "Требования не указаны.",
        },
        {
            "name": "Тестировщик комфорта квартир",
            "url": "https://hh.ru/vacancy/93353083",
            "salary": "350000-450000 руб.",
            "city": "Воронеж",
            "requirements": "Занимать активную жизненную позицию",
        },
        {
            "name": "Go Developer",
            "url": "https://hh.ru/vacancy/106507837",
            "salary": "600000 руб.",
            "city": "Москва",
            "requirements": "Требования не указаны.",
        },
        {
            "name": "Контролер склада",
            "url": "https://hh.ru/vacancy/103531332",
            "salary": "0 руб.",
            "city": "Москва",
            "requirements": "От Вас: Желание зарабатывать. Внимательность, ответственность.",
        },
    ]


@pytest.fixture
def strings_for_print() -> List:
    """
    Фикстура, содержащая строки, которые печатаются в консоль.

    :return: Информация о вакансиях в виде читабельных строк.
    """
    return [
        "Название вакансии: Чайный сомелье\n"
        "Ссылка на вакансию: https://hh.ru/vacancy/106029258\n"
        "Зарплата: 80000 руб.\n"
        "Локация размещения вакансии: Санкт-Петербург\n"
        "Требования: Требования не указаны",
        "Название вакансии: Тестировщик комфорта квартир\n"
        "Ссылка на вакансию: https://hh.ru/vacancy/93353083\n"
        "Зарплата: 350000-450000 руб.\n"
        "Локация размещения вакансии: Воронеж\n"
        "Требования: Занимать активную жизненную позицию",
        "Название вакансии: Go Developer\n"
        "Ссылка на вакансию: https://hh.ru/vacancy/106507837\n"
        "Зарплата: 600000 руб.\n"
        "Локация размещения вакансии: Москва\n"
        "Требования: Требования не указаны.",
        "Название вакансии: Контролер склада\n"
        "Ссылка на вакансию: https://hh.ru/vacancy/103531332\n"
        "Зарплата: 0 руб.\n"
        "Локация размещения вакансии: Москва\n"
        "Требования: От Вас: Желание зарабатывать. Внимательность, ответственность.",
    ]
