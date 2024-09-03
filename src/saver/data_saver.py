import json
from typing import Any, Dict, List, Union

from paths import HH_DATA_PATH
from src.saver.base_head_hunter_data_saver import HeadHunterDataSaver


class HeadHunterJSON(HeadHunterDataSaver):
    """
    Сохраняет данные с HH в формате JSON для дальнейшей работы с вакансиями.

    Методы:
        save: Метод для сохранения данных в JSON-файл.
        __prepare_data_for_writing: Вспомогательный метод, подготавливающий данные к записи в файл.
        load_vacancies: Статический метод для выгрузки данных из файла.
        __get_salary: Вспомогательный метод для подготовки информации о зарплате к загрузки в файл.
    """

    def save(self, vacancies_: List[Dict]) -> None:
        """
        Метод для сохранения данных полученных от API.

        :param vacancies_: Список вакансий.
        """
        data = self.__prepare_data_for_writing(vacancies_)
        with open(HH_DATA_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"Результат поиска сохранен в файл: {HH_DATA_PATH}")

    def __prepare_data_for_writing(self, vacancies_: List[Dict]) -> Dict[int, Dict[str, Union[str, Any]]]:
        """
        Метод, подготавливающий данные к записи в файл.
        Структура хранения вакансий: {ID: vacancy}, где vacancy словарь, хранящий данные о вакансии.

        :param vacancies_: Список вакансий.
        :return: Данные подготовленные к записи в файл.
        """
        prepared_data = {}

        for vacancy in vacancies_:
            id_ = int(vacancy["id"])

            name = vacancy["name"]
            url = vacancy["alternate_url"]
            salary = self.__get_salary(vacancy["salary"])
            requirements = vacancy["snippet"].get("requirement", "Информация по требованиям не указана.")

            prepared_data.update({id_: {"name": name, "url": url, "salary": salary, "requirements": requirements}})

        return prepared_data

    @staticmethod
    def load_vacancies() -> Any:
        """
        Статический метод для получения вакансий из файла.

        :return: Вакансии выгруженные из файла.
        """
        try:
            with open(HH_DATA_PATH, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    @staticmethod
    def __get_salary(salary_dict: Dict) -> str:
        """
        Метод для подготовки информации о зарплате к загрузки в файл.

        :param salary_dict: Зарплата в виде словаря.
        :return: Зарплата в виде строки.
        """
        if salary_dict:
            from_ = salary_dict["from"]
            to_ = salary_dict["to"]

            if from_ and to_:
                return f"{from_}-{to_} руб."
            elif from_:
                return f"{from_} руб."
            else:
                return f"{to_} руб."

        return "Нет информации о зарплате."
