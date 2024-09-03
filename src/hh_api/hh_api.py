import re
from typing import Dict, List, Optional, Union

import requests

from src.hh_api.parser import Parser
from src.utils.validator import SearchValidator

# Константы
API_URL: str = "https://api.hh.ru/vacancies"
HEADERS: Dict[str, str] = {"User-Agent": "HH-User-Agent"}
DEFAULT_AREA_ID: int = 113  # По умолчанию — Россия
DEFAULT_AREA_URL: str = "https://api.hh.ru/areas/113"


class HH(Parser):
    """
    Класс для работы с API.

    Методы:
        __init__: Конструктор инициализирующий объект для работы с API HeadHunter.
        _connect_to_api: Метод позволяющий проверить подключение к API.
        get_vacancies: Метод для получения информации о вакансиях от API в виде списка словарей.
        _get_area_id: Статический метод для получения id города.
    """

    def __init__(self) -> None:
        """Конструктор для инициализации объекта, работающего с API."""
        self.__url: str = API_URL
        self.__headers: Dict[str, str] = HEADERS
        self.__params: Dict[str, Optional[Union[str, int]]] = {
            "text": "",
            "area": DEFAULT_AREA_ID,
            "page": 0,
            "per_page": 100,
            "only_with_salary": "true",
        }
        self.__vacancies: List[Dict] = []

    def _connect_to_api(self) -> Optional[requests.Response]:
        """
        Подключение к API и проверка успешности подключения.
        """
        try:
            response = requests.get(url=self.__url, headers=self.__headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка при подключении к API: {e}")
            return None
        else:
            return response

    def get_vacancies(self, keyword: str, city_name: str = "", with_salary: bool = True) -> List[Dict]:
        """
        Получение вакансий по ключевому слову и городу(опционально).

        :param keyword: Ключевое слово, по которому будет сделан запрос.
        :param city_name: Название города (Опционально).
        :param with_salary: Булевое значение, по умолчанию True - поиск только тех вакансий,
                                                                    которые содержат информацию о зарплате.
        :return: Список найденных вакансий.
        """
        if not self._connect_to_api():
            return []  # Возврат пустого списка в случае ошибки подключения

        self.__params["text"] = keyword
        self.__params["area"] = self._get_area_id(city_name) if city_name else DEFAULT_AREA_ID
        self.__params["only_with_salary"] = "false" if not with_salary else "true"
        self.__params["page"] = 0  # Обнуление

        # Запуск цикла для перебора страниц
        while self.__params["page"] is not None and self.__params["page"] != 20:
            try:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                response.raise_for_status()
                part_of_vacancies = response.json().get("items", [])
            except requests.RequestException as e:
                print(f"Ошибка при запросе вакансий: {e}")
                break
            else:
                if not part_of_vacancies:
                    break
                self.__vacancies.extend(part_of_vacancies)
                self.__params["page"] = int(self.__params["page"]) + 1

        return self.__vacancies

    @staticmethod
    def _get_area_id(city_name: str) -> int:
        """
        Получение ID города.

        :param city_name: Название города, для которого будет осуществлен поиск ID.
        :return: ID города.
        """
        # Валидация города перед поиском ID
        name = SearchValidator.validate(city_name)
        # not_found = f"Не удалось найти город '{city_name}'. " f"Поиск вакансий будет осуществлен по всей России."
        not_found = f"Не удалось найти город '{city_name}'. Поиск вакансий будет осуществлен по всей России."
        if not name:
            print(not_found)
            return DEFAULT_AREA_ID

        pattern = r"\b(?:" + "|".join(re.escape(n) for n in name) + r")\b"
        regex = re.compile(pattern, re.IGNORECASE)  # Объект шаблона для поиска

        try:
            response = requests.get(DEFAULT_AREA_URL)
            response.raise_for_status()
            regions = response.json().get("areas", [])
        except requests.RequestException as e:
            print(f"Ошибка при запросе областей: {e}")
        else:
            for region in regions:
                region_name = set(regex.findall(region["name"]))
                # Проверка полного совпадения словесных частей названия города
                if all(n.lower() in (rn.lower() for rn in region_name) for n in name):
                    return int(region["id"])

                for city_ in region["areas"]:
                    city_full_name = set(regex.findall(city_["name"]))
                    # Проверка полного совпадения словесных частей названия города
                    if all(n.lower() in (cfn.lower() for cfn in city_full_name) for n in name):
                        return int(city_["id"])

        print(not_found)
        return DEFAULT_AREA_ID
