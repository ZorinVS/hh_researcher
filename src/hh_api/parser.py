from abc import ABC, abstractmethod
from typing import Dict, List, Optional

import requests


class Parser(ABC):
    """
    Абстрактный класс парсера.

    Методы:
        __init__: Конструктор инициализирующий объект для работы с API HeadHunter.
        _connect_to_api: Метод позволяющий проверить подключение к API.
        get_vacancies: Метод для получения информации о вакансиях от API в виде списка словарей.
        _get_area_id: Статический метод для получения id города.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Конструктор парсера."""
        pass

    @abstractmethod
    def _connect_to_api(self) -> Optional[requests.Response]:
        """
        Подключение к API.

        :return: Ответ от API.
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, city_name: str) -> List[Dict]:
        """
        Получение вакансий по ключевому слову и городу(опционально).

        :param keyword: Ключевое слово для поиска вакансий.
        :param city_name: Название города
        :return: Полученная информация о вакансиях в виде списка словарей.
        """
        pass

    @staticmethod
    @abstractmethod
    def _get_area_id(city_name: str) -> int:
        """
        Статический метод для получения id города.

        :param city_name: Название города, id которого необходимо получить.
        :return: ID города.
        """
        pass
