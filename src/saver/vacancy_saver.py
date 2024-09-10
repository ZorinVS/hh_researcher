import json
import os
from typing import Any, Dict, List

from paths import ROOT_PATH, VACANCIES_JSON_PATH
from src.saver.base_vacancy_saver import VacancySaver
from src.vacancy.vacancy import Vacancy
from src.vacancy.vacancy_already_exists_error import VacancyAlreadyExistsError


class VacancyJSON(VacancySaver):
    """
    Класс для работы с JSON-файлами.

    Атрибуты:
        file_path (str): Путь к файлу.

    Методы:
        __init__: Конструктор для инициализации JSONSaver.
        add_vacancy: Метод для добавления вакансии в файл.
        delete_vacancy: Метод для удаления вакансии из файла.
        get_vacancies: Метод для получения вакансий из файла.
        _read_file: Метод для чтения файлов.
        _write_file: Метод для записи информации о вакансии в файл.
        print_vacancies: Статический метод для читабельного вывода информации о вакансии.
        file_path: Геттер пути файла.
    """

    def __init__(self, file_name: str = VACANCIES_JSON_PATH) -> None:
        """
        Конструктор для инициализации JSONSaver.

        :param file_name: Имя файла: vacancies.json - по умолчанию.
        """
        if file_name != VACANCIES_JSON_PATH:
            if not file_name.endswith(".json"):
                file_name = file_name + ".json"
            file_name = os.path.join(
                ROOT_PATH,
                file_name,
            )

        self._file_path = file_name

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в файл.

        :param vacancy: Объект вакансии.
        :exception VacancyAlreadyExistsError: Если вакансия уже имеется в файле.
        """

        vacancy_json = {
            "name": vacancy.name,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "city": vacancy.city,
            "requirements": vacancy.requirements,
        }

        vacancy_name = vacancy.name if len(vacancy.name) < 50 else vacancy.name[:50] + "..."
        vacancy_added = f"Вакансия '{vacancy_name}' добавлена в файл: {self._file_path}"

        if not os.path.exists(self._file_path):
            self._write_file([vacancy_json])
            print(vacancy_added)
            return

        vacancies_data = self._read_file()

        try:
            if vacancy.url in (vacancy_data["url"] for vacancy_data in vacancies_data):
                raise VacancyAlreadyExistsError()
        except VacancyAlreadyExistsError as e:
            print(e)
        else:
            vacancies_data.append(vacancy_json)
            self._write_file(vacancies_data)
            print(vacancy_added)

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Метод для удаления вакансии из файла.

        :param vacancy: Объект вакансии.
        """
        vacancy_name = vacancy.name if len(vacancy.name) < 50 else vacancy.name[:50] + "..."
        vacancies_data = self._read_file()

        for index, vacancy_data in enumerate(vacancies_data):
            if vacancy_data["url"] == vacancy.url:
                del vacancies_data[index]
                self._write_file(vacancies_data)
                print(f"Вакансия '{vacancy_name}' удалена из файла: {self._file_path}")
                return

        print(f"Вакансии '{vacancy_name}' нет в файле: {self._file_path}")

    def get_vacancies(self, with_print: bool = True) -> Any:
        """
        Метод для получения вакансий из файла.

        :param with_print: Опциональный параметр для вывода вакансий в консоль.
        :return: Словарь с вакансиями.
        """
        vacancies = self._read_file()
        if vacancies:
            print(f"Количество вакансий в файле: {len(vacancies)}\n")
        else:
            print("В файле нет вакансий")

        if with_print and vacancies:
            self.print_vacancies(vacancies)

        return vacancies

    def _read_file(self) -> Any:
        """
        Метод для чтения файлов.

        :return: Словарь вакансий.
        """
        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _write_file(self, vacancies_data: List[Dict]) -> None:
        """
        Метод для записи информации о вакансии в файл.

        :param vacancies_data: Данные для записи в файл.
        """
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(vacancies_data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def print_vacancies(vacancies_data: List[Dict]) -> None:
        """
        Статический метод для читабельного вывода информации о вакансии.

        :param vacancies_data: Информация о вакансиях.
        """
        for vacancy_data in vacancies_data:
            print(f"Название вакансии: {vacancy_data['name']}")
            print(f"Ссылка на вакансию: {vacancy_data['url']}")
            print(f"Зарплата: {vacancy_data['salary']}")
            print(f"Локация размещения вакансии: {vacancy_data['city']}")
            print(f"Требования: {vacancy_data['requirements']}")

            print()

    @property
    def file_path(self) -> str:
        """
        Геттер для получения пути к файлу.

        :return: Путь к файлу.
        """
        return self._file_path
