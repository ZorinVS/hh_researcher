from unittest.mock import Mock, patch

import pytest
import requests

from src.hh_api.hh_api import API_URL, DEFAULT_AREA_ID, HEADERS, HH


@patch("src.hh_api.hh_api.requests.get")
def test_connect_to_api_successful(mock_get: Mock) -> None:
    """
    Тест успешного подключения к API.

    :param mock_get: Mock для requests.get.
    """
    # Настройка mock-объекта
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    hh = HH()
    response = hh._connect_to_api()

    assert response == mock_response
    mock_get.assert_called_once_with(url=API_URL, headers=HEADERS)


@patch("src.hh_api.hh_api.requests.get")
def test_connect_to_api_unsuccessful(mock_get: Mock) -> None:
    """
    Тест неуспешного подключения к API.

    :param mock_get: Mock для requests.get.
    """
    # Настройка mock-объекта для вызова исключения при запросе
    mock_get.side_effect = requests.RequestException("Ошибка при подключении к API")

    hh = HH()
    response = hh._connect_to_api()

    assert response is None
    mock_get.assert_called_once_with(url=API_URL, headers=HEADERS)


@patch("src.hh_api.hh_api.requests.get")
def test_get_vacancies_request_exception(mock_get: Mock, capsys: pytest.CaptureFixture[str]) -> None:
    """
    Тест метода get_vacancies на корректную обработку исключения requests.RequestException.

    :param mock_get: Mock для requests.get.
    :param capsys: Фикстура для перехвата вывода.
    """
    # Настройка mock-объекта для генерации исключения RequestException
    mock_get.side_effect = requests.RequestException("error")

    hh = HH()
    result = hh.get_vacancies(keyword="Python")

    message = capsys.readouterr()
    error_ = message.out.strip()

    assert error_ == "Ошибка при подключении к API: error"
    assert result == []

    mock_get.assert_called_once()


@patch("src.hh_api.hh_api.HH._connect_to_api")
@patch("src.hh_api.hh_api.requests.get")
def test_get_vacancies_page_limit(mock_get: Mock, mock_connect: Mock) -> None:
    """
    Тестирует, что метод get_vacancies прекращает запросы после достижения предела в 20 страниц.

    :param mock_get: Mock для requests.get.
    :param mock_connect: Mock для _connect_to_api.
    """
    # Настройка mock-объекта для успешного подключения
    mock_connect.return_value = Mock()

    # Настройка mock-объекта для возврата списка вакансий на каждой странице
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {"items": [{"id": "1", "name": "Test Vacancy"}]}
    mock_get.return_value = mock_response

    hh = HH()
    hh.get_vacancies(keyword="Python")

    assert mock_get.call_count == 20


@patch("src.hh_api.hh_api.requests.get")
def test_get_area_id_successful(mock_get: Mock) -> None:
    """
    Тест успешного получения ID города.

    :param mock_get: Mock для requests.get.
    """
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {
        "areas": [
            {"id": "1", "name": "Москва", "areas": []},
            {"id": "2", "name": "Санкт-Петербург", "areas": []},
        ]
    }
    mock_get.return_value = mock_response

    hh = HH()
    area_id = hh._get_area_id("Москва")

    assert area_id == 1


@patch("src.hh_api.hh_api.requests.get")
def test_get_area_id_not_found(mock_get: Mock, capsys: pytest.CaptureFixture[str]) -> None:
    """
    Тест неудачного поиска города и возврата DEFAULT_AREA_ID.

    :param mock_get: Mock для requests.get.
    :param capsys: Фикстура для перехвата вывода.
    """
    mock_response = Mock()
    mock_response.raise_for_status = Mock()
    mock_response.json.return_value = {"areas": []}
    mock_get.return_value = mock_response

    hh = HH()
    area_id = hh._get_area_id("X")

    message = capsys.readouterr()
    not_found = message.out.strip()

    assert not_found == "Не удалось найти город 'X'. Поиск вакансий будет осуществлен по всей России."
    assert area_id == DEFAULT_AREA_ID


@patch("src.hh_api.hh_api.requests.get")
def test_get_area_id_request_exception(mock_get: Mock, capsys: pytest.CaptureFixture[str]) -> None:
    """
    Тест обработки исключения при поиске ID города и возврата DEFAULT_AREA_ID.

    :param mock_get: Mock для requests.get.
    :param capsys: Фикстура для перехвата вывода.
    """
    mock_get.side_effect = requests.RequestException("Ошибка подключения")

    hh = HH()
    area_id = hh._get_area_id("Москва")

    message = capsys.readouterr()
    error_, m = message.out.strip().split("\n")

    assert error_ == "Ошибка при запросе областей: Ошибка подключения"
    assert m == "Не удалось найти город 'Москва'. Поиск вакансий будет осуществлен по всей России."
    assert area_id == DEFAULT_AREA_ID
