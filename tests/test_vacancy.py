from typing import List

import pytest


def test_vacancy_init_with_all_arguments(vacancies: List) -> None:
    """
    Тест инициализации объекта со всеми атрибутами.

    :param vacancies: Список вакансий.
    """
    vacancy1 = vacancies[0]
    vacancy2 = vacancies[1]

    assert vacancy1.name == "Чайный сомелье"
    assert vacancy1.url == "https://hh.ru/vacancy/106029258"
    assert vacancy1.salary == "80000 руб."
    assert vacancy1.city == "Санкт-Петербург"
    assert vacancy1.requirements == "Требования не указаны."

    assert vacancy2.name == "Тестировщик комфорта квартир"
    assert vacancy2.url == "https://hh.ru/vacancy/93353083"
    assert vacancy2.salary == "350000-450000 руб."
    assert vacancy2.city == "Воронеж"
    assert vacancy2.requirements == "Занимать активную жизненную позицию"


def test_vacancy_init_without_requirements(vacancies: List) -> None:
    """
    Тест инициализации объекта без вода данных для атрибута requirements.

    :param vacancies: Список вакансий.
    """
    vacancy = vacancies[2]

    assert vacancy.name == "Go Developer"
    assert vacancy.url == "https://hh.ru/vacancy/106507837"
    assert vacancy.salary == "600000 руб."
    assert vacancy.city == "Москва"
    assert vacancy.requirements == "Требования не указаны."


def test_vacancy_init_without_salary(vacancies: List) -> None:
    """
    Тест инициализации объекта без вода данных для атрибута salary.

    :param vacancies: Список вакансий.
    """
    vacancy = vacancies[3]

    assert vacancy.name == "Контролер склада"
    assert vacancy.url == "https://hh.ru/vacancy/103531332"
    assert vacancy.salary == "0 руб."
    assert vacancy.city == "Москва"
    assert vacancy.requirements == "От Вас: Желание зарабатывать. Внимательность, ответственность."


def test_vacancy_str(vacancies: List) -> None:
    """
    Тест строкового представления объекта.

    :param vacancies: Список вакансий.
    """
    vacancy = vacancies[0]
    print(str(vacancy))
    assert str(vacancy) == (
        "Название вакансии: Чайный сомелье\n"
        "Ссылка на вакансию: https://hh.ru/vacancy/106029258\n"
        "Зарплата: 80000 руб.\n"
        "Локация размещения вакансии: Санкт-Петербург\n"
        "Требования: Требования не указаны."
    )


def test_vacancy_lt(vacancies: List) -> None:
    """
    Тест сравнения объектов по зарплате.

    :param vacancies: Список вакансий.
    """
    v1, v2 = vacancies[:2]

    assert v1 < v2  # (v1 < v2) is True
    assert not v2 < v1  # (v2 < v1) is False

    assert not v1 > v2  # (v1 > v2) is False
    assert v2 > v1  # (v2 > v1) is True


def test_vacancy_lt_error(vacancies: List) -> None:
    """
    Тест сравнение вакансии с объектом, который не является экземпляром класса Vacancy.

    :param vacancies: Список вакансий.
    :exception TypeError: Если экземпляр вакансии сравнивается не с объектом класса Vacancy.
    """
    vacancy = vacancies[0]

    with pytest.raises(TypeError) as exc_info:
        vacancy < 100_000

    assert str(exc_info.value) == "Сравнение возможно только между объектами Vacancy."
