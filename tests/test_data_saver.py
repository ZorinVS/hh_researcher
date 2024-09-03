import os
from typing import Dict, List

from src.saver.data_saver import HH_DATA_PATH, HeadHunterJSON


def test_prepare_data_for_writing(json_data_items: List[Dict], prepared_data: Dict) -> None:
    """
    Тест подготовки данных к записи в файл.

    :param json_data_items: Данные, полученные от API (ключ 'items').
    :param prepared_data: Данные, подготовленные к записи в файл.
    """
    saver = HeadHunterJSON()
    result = saver._HeadHunterJSON__prepare_data_for_writing(json_data_items)

    assert result == prepared_data


def test_save_and_load_vacancies(json_data_items: List[Dict], prepared_data: Dict) -> None:
    """
    Тест записи данных в файл и выгрузки.

    :param json_data_items: Данные, полученные от API (ключ 'items').
    :param prepared_data: Данные, подготовленные к записи в файл.
    """
    saver = HeadHunterJSON()
    saver.save(json_data_items)

    expected = {str(id_): vacancy for id_, vacancy in prepared_data.items()}  # Преобразование id в string
    result = saver.load_vacancies()
    os.remove(HH_DATA_PATH)

    assert result == expected


def test_load_vacancies_file_not_found_error() -> None:
    """
    Тест попытки загрузить данные из файла, которого нет.
    """
    saver = HeadHunterJSON()

    assert saver.load_vacancies() == {}
