import os
from typing import Dict

from paths import ROOT_PATH
from src.hh_api.hh_api import HH
from src.saver.data_saver import HeadHunterJSON
from src.vacancy.vacancy import Vacancy
from user_interaction_utils.initialization import set_file_name
from user_interaction_utils.manager import select_manager_menu_items
from user_interaction_utils.searcher import select_search_menu_items


def main_menu() -> None:
    print("\n=== Главное меню ===")
    print("1. Поиск вакансий")
    print("2. Менеджер вакансий")
    print("3. Выйти")
    print("=====================")


# Функция для взаимодействия с пользователем
def user_interaction() -> None:
    hh_api = HH()
    data_saver = HeadHunterJSON()
    vacancy_saver = set_file_name()
    vacancies_dict: Dict[int, Vacancy] = {}

    while True:
        main_menu()
        choice = input("Выберите пункт меню (1-3): ").strip()

        if choice == "1":
            select_search_menu_items(hh_api, data_saver)

        elif choice == "2":
            select_manager_menu_items(hh_api, data_saver, vacancy_saver, vacancies_dict)

        elif choice == "3":
            print("Выход из программы")

            for vacancy in vacancies_dict.values():
                vacancy.delete()  # Освобождение id для дальнейшей демонстрации примера работы класса Vacancy

            break


if __name__ == "__main__":
    # Удаление старых файлов
    for root, _, files in os.walk(ROOT_PATH):
        for file in files:
            os.remove(os.path.join(root, file))

    # Запуск программы
    user_interaction()

    # ======================= Демонстрация примера работы класса Vacancy =======================
    print("\n\n=== ПРИМЕР РАБОТЫ КЛАССА VACANCY ===")

    v1 = Vacancy("Чайный сомелье", "https://hh.ru/vacancy/106029258", "от 80 000 ₽", "Требования не указаны")

    v2 = Vacancy(
        "Тестировщик комфорта квартир",
        "https://hh.ru/vacancy/93353083",
        "350 000 - 450 000 ₽",
        (
            "Занимать активную жизненную позицию, "
            "уметь активно танцевать и громко петь. "
            "Обладать навыками коммуникации, чтобы налаживать добрососедские отношения. "
            "Обладать системным мышлением..."
        ),
    )

    print(f"\nID{v1.id}", end=" ")
    print(f"| Название: {v1.name}")
    print(" " * 3, f"| URL: {v1.url}")
    print(" " * 3, f"| Зарплата: {v1.salary}")
    print(" " * 3, f"| Требования: {v1.requirements}")

    print(f"\nID{v2.id}", end=" ")
    print(f"| Название: {v2.name}")
    print(" " * 3, f"| URL: {v2.url}")
    print(" " * 3, f"| Зарплата: {v2.salary}")
    print(" " * 3, f"| Требования: {v2.requirements}")

    print(f"\nv1: {v1.salary}")
    print(f"v2: {v2.salary}")
    print(f"\nv1 > v2: {v1 > v2}")
    print(f"v1 < v2: {v1 < v2}")
