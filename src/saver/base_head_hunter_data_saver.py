from abc import ABC, abstractmethod
from typing import Dict, List


class HeadHunterDataSaver(ABC):
    """
    Абстрактный класс для сохранения данных полученных от API.

    Методы:
        save: Абстрактный метод для сохранения данных в файл.
        load_vacancies: Абстрактно-статический метод для выгрузки данных из файла.
    """

    @abstractmethod
    def save(self, vacancies_: List[Dict]) -> None:
        """
        Абстрактный метод для сохранения данных полученных от API.

        :param vacancies_: Список вакансий.
        """

    @staticmethod
    @abstractmethod
    def load_vacancies() -> Dict[str, Dict]:
        """
        Статический метод для получения вакансий из файла.

        :return: Словарь вакансий, загруженный из файла.
        """
        pass
