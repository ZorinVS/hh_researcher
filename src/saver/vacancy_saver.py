import json
import os
from typing import Any, Dict

from paths import ROOT_PATH, VACANCIES_JSON_PATH
from src.saver.base_vacancy_saver import VacancySaver
from src.vacancy.vacancy import Vacancy
from src.vacancy_already_exists_error import VacancyAlreadyExistsError


class VacancyJSON(VacancySaver):
    """
    Класс для работы с JSON-файлами.

    Атрибуты:
        file_path (str): Путь к файлу.

    Методы:
        add_vacancy: ...
        delete_vacancy: ...
        get_vacancies: ...
        _read_file: ...
        _write_file: ...
    """

    def __init__(self, file_path: str = VACANCIES_JSON_PATH) -> None:
        """
        Конструктор для инициализации JSONSaver.

        :param file_path: Имя файла: vacancies.json - по умолчанию.
        """
        if file_path != VACANCIES_JSON_PATH:
            if not file_path.endswith(".json"):
                file_path = file_path + ".json"
            file_path = os.path.join(
                ROOT_PATH,
                file_path,
            )

        self._file_path = file_path

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в файл.

        :param vacancy: Объект вакансии.
        :exception VacancyAlreadyExistsError: Если вакансия уже имеется в файле.
        """
        id_ = str(vacancy.id)

        vacancy_json = {
            id_: {
                "name": vacancy.name,
                "url": vacancy.url,
                "salary": vacancy.salary,
                "requirements": vacancy.requirements,
            }
        }

        vacancies = self._read_file()
        if vacancy_json[id_] in vacancies.values():
            raise VacancyAlreadyExistsError()

        vacancies.update(vacancy_json)

        self._write_file(vacancies)
        print(f"Вакансия ID{id_} добавлена в файл: {self._file_path}")

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Метод для удаления вакансии из файла.

        :param vacancy: Объект вакансии.
        """
        id_ = str(vacancy.id)

        vacancies = self._read_file()
        vacancy.delete()  # Освобождение id вакансии
        del vacancies[id_]  # Удаление вакансии из данных, хранящихся в файле

        self._write_file(vacancies)
        print(f"Вакансия ID{id_} удалена из файла: {self._file_path}")

    def get_vacancies(self, with_print: bool = True) -> Any:
        """
        Метод для получения вакансий из файла.

        :param with_print: Опциональный параметр для вывода вакансий в консоль.
        :return: Словарь с вакансиями.
        """
        vacancies = self._read_file()

        if with_print:
            self.print_vacancies(vacancies)

        return vacancies

    @staticmethod
    def print_vacancies(vacancies: Dict[str, Dict]) -> None:
        for id_, vacancy in vacancies.items():
            print(f"ID: {id_}")
            print(f"Название: {vacancy["name"]}")
            print(f"URL: {vacancy["url"]}")
            print(f"Зарплата: {vacancy["salary"]}")
            print(f"Требования: {vacancy["requirements"]}")
            print()

    def _read_file(self) -> Any:
        """
        Метод для чтения файлов.

        :return: Словарь вакансий.
        """
        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def _write_file(self, data: Dict[str, Dict]) -> None:
        """
        Метод для записи информации о вакансии в файл.

        :param data: Данные для записи в файл.
        """
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @property
    def file_path(self) -> str:
        """
        Геттер для получения пути к файлу.

        :return: Путь к файлу.
        """
        return self._file_path
