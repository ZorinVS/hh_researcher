from typing import Dict
from unittest.mock import Mock, patch

from src.utils.top_n_utility import get_top_vacancies


@patch("builtins.input", side_effect=["3"])
def test_get_top_vacancies(mock_input: Mock, vacancies_from_file: Dict) -> None:
    """
    Тест функции, выводящей топ-N вакансий.

    :param mock_input: Mock для пользовательского ввода количества вакансий.
    :param vacancies_from_file: Фикстура, представляющая данные загруженные из файла.
    """
    result = get_top_vacancies(vacancies_from_file)
    expected = [
        (
            "3",
            {
                "name": "Go Developer",
                "url": "https://hh.ru/vacancy/106507837",
                "salary": "600000 руб.",
                "requirements": "Требования не указаны.",
            },
        ),
        (
            "2",
            {
                "name": "Тестировщик комфорта квартир",
                "url": "https://hh.ru/vacancy/93353083",
                "salary": "350000-450000 руб.",
                "requirements": "Занимать активную жизненную позицию",
            },
        ),
        (
            "1",
            {
                "name": "Чайный сомелье",
                "url": "https://hh.ru/vacancy/106029258",
                "salary": "80000 руб.",
                "requirements": "Требования не указаны",
            },
        ),
    ]

    assert result == expected
    mock_input.assert_called_once_with("Какой топ N вакансий хотите получить (введите число): ")
