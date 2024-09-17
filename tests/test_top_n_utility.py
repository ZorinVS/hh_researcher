from typing import List
from unittest.mock import Mock, patch

from src.utils.top_n_utility import get_top_vacancies


@patch("builtins.input", side_effect=["2"])
def test_get_top_vacancies(mock_input: Mock, vacancies: List) -> None:
    """
    Тест функции, выводящей топ-N вакансий.

    :param mock_input: Mock для пользовательского ввода количества вакансий.
    :param vacancies: Фикстура, представляющая список вакансий.
    """
    result = [vacancy.name for vacancy in get_top_vacancies(vacancies)]
    expected = ["Go Developer", "Тестировщик комфорта квартир"]

    assert result == expected
    mock_input.assert_called_once_with("Какой топ N вакансий хотите получить и сохранить (введите число): ")
