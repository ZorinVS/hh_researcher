import os
from typing import Dict, Tuple

import pytest

from src.saver.vacancy_saver import ROOT_PATH, VacancyJSON


def test_init_with_filepath() -> None:
    """
    Тест инициализации сейвера с пользовательским именем.
    """
    filename = "test.json"
    v_saver = VacancyJSON(filename)

    expected = os.path.join(ROOT_PATH, filename)
    result = v_saver.file_path

    assert result == expected


def test_add_and_get_vacancy(vacancies: Tuple, capsys: pytest.CaptureFixture[str]) -> None:
    """
    Тест добавления вакансий в файл и их выгрузку.

    :param vacancies: Картеж вакансий.
    :param capsys: Фикстура для перехвата вывода.
    """
    v_saver = VacancyJSON()

    for vacancy in vacancies:
        v_saver.add_vacancy(vacancy)

    message = capsys.readouterr()
    added_vacancy_id1 = message.out.strip().split("\n")[0]

    assert added_vacancy_id1 == (
        "Вакансия ID21 добавлена в файл: " "/Users/vladislav/SkyPro/hh_researcher/data/vacancies.json"
    )

    expected = {
        "21": {
            "name": "Чайный сомелье",
            "url": "https://hh.ru/vacancy/106029258",
            "salary": "80000 руб.",
            "requirements": "Требования не указаны",
        },
        "22": {
            "name": "Тестировщик комфорта квартир",
            "url": "https://hh.ru/vacancy/93353083",
            "salary": "350000-450000 руб.",
            "requirements": "Занимать активную жизненную позицию",
        },
        "23": {
            "name": "Go Developer",
            "url": "https://hh.ru/vacancy/106507837",
            "salary": "600000 руб.",
            "requirements": "Требования не указаны.",
        },
        "24": {
            "name": "Контролер склада",
            "url": "https://hh.ru/vacancy/103531332",
            "salary": "0 руб.",
            "requirements": "От Вас: Желание зарабатывать. Внимательность, ответственность.",
        },
    }
    result = v_saver.get_vacancies(with_print=False)

    assert result == expected


def test_delete_vacancy(vacancies: Tuple, capsys: pytest.CaptureFixture[str]) -> None:
    """
    Тест удаления вакансий из файла.

    :param vacancies: Картеж вакансий.
    :param capsys: Фикстура для перехвата вывода.
    """
    v_saver = VacancyJSON()

    for vacancy in vacancies:
        v_saver.add_vacancy(vacancy)

    for vacancy in vacancies:
        v_saver.delete_vacancy(vacancy)

    message = capsys.readouterr()
    deleted_vacancy_id5 = message.out.strip().split("\n")[4]

    assert deleted_vacancy_id5 == (
        "Вакансия ID25 удалена из файла: " "/Users/vladislav/SkyPro/hh_researcher/data/vacancies.json"
    )

    result = v_saver.get_vacancies(with_print=False)

    assert result == {}


def test_print_vacancies(vacancies_from_file: Dict, capsys: pytest.CaptureFixture[str]) -> None:
    """
    Тест вывода информации в консоль.

    :param vacancies_from_file: Фикстура, представляющая данные выгруженные из файла.
    :param capsys: Фикстура для перехвата вывода.
    """
    v_saver = VacancyJSON()
    v_saver.print_vacancies(vacancies_from_file)

    message = capsys.readouterr()
    printed_vacancies = message.out.strip()

    v1 = (
        "ID: 1\n"
        "Название: Чайный сомелье\n"
        "URL: https://hh.ru/vacancy/106029258\n"
        "Зарплата: 80000 руб.\n"
        "Требования: Требования не указаны"
    )

    assert v1 in printed_vacancies
