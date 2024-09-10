from typing import Dict, List

from src.hh_api.hh_api import HH
from src.saver.vacancy_saver import VacancyJSON
from src.vacancy.vacancy import Vacancy


def get_salary(salary_dict: Dict) -> str:
    """
    Функция для подготовки информации о зарплате к инициализации объекта Vacancy.

    :param salary_dict: Зарплата в виде словаря.
    :return: Зарплата в виде строки.
    """
    if salary_dict:
        from_ = salary_dict["from"]
        to_ = salary_dict["to"]

        if isinstance(from_, int) and isinstance(to_, int):
            return f"{from_}-{to_} руб."
        elif isinstance(from_, int):
            return f"{from_} руб."
        elif isinstance(to_, int):
            return f"{to_} руб."

    return "0 руб."


def create_list_of_vacancies(data_from_api: List[Dict]) -> List[Vacancy]:
    """
    Функция для создания списка объектов вакансий из данных, полученных от API.

    :param data_from_api: Данные полученные от API.
    :return: Список объектов вакансий.
    """
    vacancies_list = []

    for vacancy_data in data_from_api:
        name = vacancy_data["name"]
        url = vacancy_data["alternate_url"]
        salary = get_salary(vacancy_data["salary"])
        city = vacancy_data.get("area", {}).get("name")
        requirements = vacancy_data["snippet"]["requirement"]

        vacancies_list.append(Vacancy(name, url, salary, city, requirements))

    return vacancies_list


def initialization_menu() -> VacancyJSON:
    """
    Функция для настройки сейвера.
    Используется для выбора имений файла, в который будут сохраняться вакансии.

    :return: Настроенный JsonSaver.
    """
    print("=== Меню инициализации ===")
    print("Выберите, как вы хотите назвать файл для хранения вакансий:")
    print("1. Использовать стандартное имя файла (vacancies.json)")
    print("2. Задать своё имя файла")
    print("===========================")
    while True:
        choice = input("Выберите пункт меню (1-2): ")

        if choice == "1":
            print("Используется стандартное имя файла: vacancies.json")
            return VacancyJSON()
        elif choice == "2":
            filename = input("Введите имя файла: ").strip()
            if not filename.endswith(".json"):
                filename += ".json"
            print(f"Используется имя файла: {filename}")
            return VacancyJSON(filename)


def search_menu(hh_api: HH) -> List:
    """
    Функция для выбора локации поиска вакансий.

    :param hh_api: Объект класса HH для работы с API.
    :return: Данные полученные от API.
    """
    print("\n=== Меню поиска ===")
    print("1. Поиск по всей России")
    print("2. Сделать поиск в определенном городе")
    print("=====================")
    while True:
        choice = input("Выберите пункт меню (1-2): ").strip()

        if choice == "1":
            result = search_vacancies(hh_api, search_in_city=False)
            return result
        elif choice == "2":
            result = search_vacancies(hh_api, search_in_city=True)
            return result


def search_vacancies(hh_api: HH, search_in_city: bool) -> List:
    """
    Вспомогательная функция для поиска вакансий.

    :param hh_api: Объект класса HH для работы с API.
    :param search_in_city: Булевое значение, использующееся для выбора локации поиска.
    :return: Данные полученные от API.
    """
    print("\n--- Поиск вакансий ---")
    if search_in_city:
        city_name = input("Название города: ").strip()
    query = input("Поисковой запрос: ")
    if search_in_city:
        vacancies = hh_api.get_vacancies(query, city_name)
    else:
        vacancies = hh_api.get_vacancies(query)

    print("\n--- Результат поиска ---")
    if vacancies:
        quantity = len(vacancies)
        print(f"Количество вакансий найденных по запросу '{query}': {quantity}")
        return vacancies
    else:
        print(f"По запросу '{query}' ничего не найдено")
        return []
