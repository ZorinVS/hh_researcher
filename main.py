import os

from paths import ROOT_PATH
from src.hh_api.hh_api import HH
from src.utils.top_n_utility import get_top_vacancies
from src.utils.utils import create_list_of_vacancies, initialization_menu, search_menu
from src.vacancy.vacancy import Vacancy


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем"""

    vacancies_saver = initialization_menu()
    vacancies_data = search_menu(hh_api=HH())
    if not vacancies_data:
        return
    vacancies_list = create_list_of_vacancies(vacancies_data)

    print("\n=== Меню просмотра ===")
    print("1. Показать и сохранить все найденные вакансии")
    print("2. Показать и сохранить топ N вакансий")
    print("=====================")

    while True:
        choice = input("Выберите пункт меню (1-2): ").strip()

        if choice == "1":
            break
        elif choice == "2":
            vacancies_list = get_top_vacancies(vacancies_list)
            break

    print("\n--- Сохранение вакансий ---")
    for vacancy in vacancies_list:
        vacancies_saver.add_vacancy(vacancy)
    print("\n--- Вывод вакансий ---")
    vacancies_saver.get_vacancies()


if __name__ == "__main__":
    # Удаление старых файлов
    for root, _, files in os.walk(ROOT_PATH):
        for file in files:
            os.remove(os.path.join(root, file))

    # Запуск программы
    user_interaction()

    # ======================= Демонстрация примера работы класса Vacancy =======================
    print("\n\n=== ПРИМЕР РАБОТЫ КЛАССА VACANCY ===")

    v1 = Vacancy(
        "Чайный сомелье", "https://hh.ru/vacancy/106029258", "от 80 000 ₽", "Санкт-Петербург", "Требования не указаны"
    )

    v2 = Vacancy(
        "Тестировщик комфорта квартир",
        "https://hh.ru/vacancy/93353083",
        "350 000 - 450 000 ₽",
        "Воронеж",
        "Занимать активную жизненную позицию",
    )

    print(v1, end="\n\n")
    print(v2, end="\n\n")

    print(f"v1: {v1.salary}\n" f"v2: {v2.salary}\n")

    print(f"v1 > v2: {v1 > v2}\n" f"v1 < v2: {v1 < v2}")
