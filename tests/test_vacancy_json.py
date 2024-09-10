import os
from typing import List

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


def test_add_and_get_vacancy(vacancies: List, capsys: pytest.CaptureFixture[str], vacancies_from_file: List) -> None:
    """
    Тест добавления вакансий в файл и их выгрузку.

    :param vacancies: Список вакансий.
    :param capsys: Фикстура для перехвата вывода.
    :param vacancies_from_file: Фикстура, представляющая данные полученные из файла.
    """
    v_saver = VacancyJSON()
    file_path = v_saver.file_path

    for vacancy in vacancies:
        v_saver.add_vacancy(vacancy)

    message = capsys.readouterr()
    added_vacancy1 = message.out.strip().split("\n")[0]

    assert added_vacancy1 == f"Вакансия 'Чайный сомелье' добавлена в файл: {file_path}"

    expected = vacancies_from_file
    result = v_saver.get_vacancies(with_print=False)

    assert result == expected


def test_delete_vacancy(vacancies: List, capsys: pytest.CaptureFixture[str]) -> None:
    """
    Тест удаления вакансий из файла.

    :param vacancies: Список вакансий.
    :param capsys: Фикстура для перехвата вывода.
    """
    v_saver = VacancyJSON()
    file_path = v_saver.file_path

    for vacancy in vacancies:
        v_saver.add_vacancy(vacancy)

    for vacancy in vacancies:
        v_saver.delete_vacancy(vacancy)

    message = capsys.readouterr()
    deleted_vacancy = message.out.strip().split("\n")[4]

    assert deleted_vacancy == f"Вакансия 'Чайный сомелье' удалена из файла: {file_path}"

    result = v_saver.get_vacancies(with_print=False)

    assert result == []


def test_print_vacancies(
    vacancies_from_file: List, strings_for_print: List, capsys: pytest.CaptureFixture[str]
) -> None:
    """
    Тест вывода информации в консоль.

    :param vacancies_from_file: Фикстура, представляющая данные выгруженные из файла.
    :param strings_for_print: Фикстура, представляющая строки, ожидаемые в выводе.
    :param capsys: Фикстура для перехвата вывода.
    """
    v_saver = VacancyJSON()
    v_saver.print_vacancies(vacancies_from_file)

    message = capsys.readouterr()
    printed_vacancies = message.out.strip().split("\n\n")

    for index in range(4):
        assert strings_for_print[index] in printed_vacancies[index]
