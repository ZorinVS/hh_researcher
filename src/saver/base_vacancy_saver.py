from abc import ABC, abstractmethod
from typing import Dict

from src.vacancy.vacancy import Vacancy


class VacancySaver(ABC):
    """
    Абстрактный класс для работы с файлами.

    Методы:
        add_vacancy: Абстрактный метод добавления вакансии в файл.
        delete_vacancy: Абстрактный метод удаления вакансии из файла.
        get_vacancies: Абстрактный метод выгрузки вакансий из файла.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Абстрактный метод добавления вакансии в файл.

        :param vacancy: Объект вакансии.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Абстрактный метод удаления вакансии из файла.

        :param vacancy: Объект вакансии.
        """
        pass

    @abstractmethod
    def get_vacancies(self, with_print: bool = True) -> Dict:
        """
        Абстрактный метод выгрузки вакансий из файла.

        :param with_print:
        :return: Словарь вакансий.
        """
        pass
