from typing import Tuple

import pytest

from src.vacancy.vacancy import Vacancy


def test_vacancy_init_with_all_arguments(vacancies: Tuple) -> None:
    """
    Тест инициализации объекта со всеми атрибутами.

    :param vacancies: Картеж вакансий.
    """
    vacancy1 = vacancies[0]
    vacancy2 = vacancies[1]

    assert vacancy1.id == 1  # Тест генерации ID
    assert vacancy1.name == "Чайный сомелье"
    assert vacancy1.url == "https://hh.ru/vacancy/106029258"
    assert vacancy1.salary == "80000 руб."
    assert vacancy1.requirements == "Требования не указаны"

    assert vacancy2.id == 2
    assert vacancy2.name == "Тестировщик комфорта квартир"
    assert vacancy2.url == "https://hh.ru/vacancy/93353083"
    assert vacancy2.salary == "350000-450000 руб."
    assert vacancy2.requirements == "Занимать активную жизненную позицию"

    # Освобождение id для нового теста
    for vacancy in vacancies:
        vacancy.delete()


def test_vacancy_init_without_requirements(vacancies: Tuple) -> None:
    """
    Тест инициализации объекта без вода данных для атрибута requirements.

    :param vacancies: Картеж вакансий.
    """
    vacancy = vacancies[2]

    assert vacancy.id == 3
    assert vacancy.name == "Go Developer"
    assert vacancy.url == "https://hh.ru/vacancy/106507837"
    assert vacancy.salary == "600000 руб."
    assert vacancy.requirements == "Требования не указаны."

    # Освобождение id для нового теста
    for vacancy in vacancies:
        vacancy.delete()


def test_vacancy_init_without_salary(vacancies: Tuple) -> None:
    """
    Тест инициализации объекта без вода данных для атрибута salary.

    :param vacancies: Картеж вакансий.
    """
    vacancy = vacancies[3]

    assert vacancy.id == 4  # Тест генерации ID
    assert vacancy.name == "Контролер склада"
    assert vacancy.url == "https://hh.ru/vacancy/103531332"
    assert vacancy.salary == "0 руб."
    assert vacancy.requirements == "От Вас: Желание зарабатывать. Внимательность, ответственность."


def test_vacancy_delete(vacancies: Tuple) -> None:
    """
    Тест удаления вакансии (освобождения ID).

    :param vacancies: Картеж вакансий.
    :exception ValueError: Если ID вакансии не установлен.
    """
    vacancy1 = vacancies[0]
    assert vacancy1.id == 5

    vacancy1.delete()  # Освобождаем ID5 для новой вакансии

    vacancy2 = Vacancy("test1", "https://hh.ru/vacancy/12345")
    assert vacancy2.id == 5

    with pytest.raises(ValueError) as exc_info:
        vacancy1.id

    assert str(exc_info.value) == "ID вакансии не установлен."


def test_vacancy_repr(vacancies: Tuple) -> None:
    """
    Тест строкового представления объекта.

    :param vacancies: Картеж вакансий.
    """
    vacancy = vacancies[0]

    assert repr(vacancy) == (
        "Vacancy('Чайный сомелье', 'https://hh.ru/vacancy/106029258', '80000 руб.', 'Требования не указаны')"
    )


def test_vacancy_lt(vacancies: Tuple) -> None:
    """
    Тест сравнения объектов по зарплате.

    :param vacancies: Картеж вакансий.
    """
    v1, v2 = vacancies[:2]

    assert v1 < v2  # (v1 < v2) is True
    assert not v2 < v1  # (v2 < v1) is False

    assert not v1 > v2  # (v1 > v2) is False
    assert v2 > v1  # (v2 > v1) is True


def test_vacancy_lt_error(vacancies: Tuple) -> None:
    """
    Тест сравнение вакансии с объектом, который не является экземпляром класса Vacancy.

    :param vacancies: Картеж вакансий.
    :exception TypeError: Если экземпляр вакансии сравнивается не с объектом класса Vacancy.
    """
    vacancy = vacancies[0]

    with pytest.raises(TypeError) as exc_info:
        vacancy < 100_000

    assert str(exc_info.value) == "Сравнение возможно только между объектами Vacancy."
