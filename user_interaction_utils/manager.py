import os

from paths import HH_DATA_PATH
from src.utils.top_n_utility import get_top_vacancies, print_top_vacancies
from src.vacancy.vacancy import Vacancy
from src.vacancy_already_exists_error import VacancyAlreadyExistsError
from user_interaction_utils.searcher import select_search_menu_items


def manager_menu_items():
    print("\n=== Меню менеджера ===")
    print("1. Смотреть добавленные вакансии")
    print("2. Добавить вакансию")
    print("3. Удалить вакансию")
    print("4. Назад в главное меню")
    print("=====================")


def select_manager_menu_items(hh_api, data_saver, vacancy_saver, vacancies_dict):
    manager_menu_items()

    while True:
        choice = input("Выберите пункт меню (1-4): ").strip()

        if choice == "1":
            if view_vacancies(vacancy_saver):
                break  # Выход в главное меню
        elif choice == "2":
            if add_(hh_api, data_saver, vacancy_saver, vacancies_dict):
                break  # Выход в главное меню
        elif choice == "3":
            if delete_menu(vacancy_saver, vacancies_dict):
                break  # Выход в главное меню
        elif choice == "4":
            break  # Выход в главное меню


def view_vacancies(vacancy_saver):
    print("\n--- Список вакансий ---")
    if os.path.exists(vacancy_saver.file_path):
        vacancy_saver.get_vacancies()
        print("---------------------")
        return True

    print("Список вакансий пуст")
    return True


def add_(hh_api, data_saver, vacancy_saver, vacancies_dict):
    if not os.path.exists(HH_DATA_PATH):
        print("\n--- Добавление вакансии ---")
        print("Прежде чем добавлять, необходимо сделать поиск вакансий")
        if select_search_menu_items(hh_api, data_saver):
            return True  # Выход в главное меню

    print("\n--- Добавление вакансии ---")
    json_data = data_saver.load_vacancies()
    quantity = len(json_data)
    print("Всего найдено вакансий:", quantity)
    print("1. Показать все найденные вакансии")
    print("2. Показать топ-N вакансий")
    print("---------------------")

    while True:
        choice = input("Выберите пункт меню добавления вакансии (1-2): ").strip()

        print("\n--- Добавление вакансии ---")
        if choice == "1":
            vacancy_saver.print_vacancies(json_data)
            break
        elif choice == "2":
            top_n = get_top_vacancies(json_data)
            print_top_vacancies(top_n)
            break

    print("---------------------")

    while True:
        choice = input("Q - назад в главное меню / ID вакансии, которую хотите добавить: ").strip()

        if choice in json_data:
            vacancy_data = json_data[choice]
            vacancy = Vacancy(**vacancy_data)  # Создаем экземпляр класса Vacancy
            try:
                vacancy_saver.add_vacancy(vacancy)
            except VacancyAlreadyExistsError as e:
                vacancy.delete()
                print(e)
            else:
                vacancies_dict.update({vacancy.id: vacancy})
        elif choice.lower() == "q":
            return True


def delete_menu(vacancy_saver, vacancies_dict):
    print("\n--- Удаление вакансии ---")
    if os.path.exists(vacancy_saver.file_path):
        vacancies = vacancy_saver.get_vacancies()
        print("---------------------")

        while True:
            selected_id = input("ID вакансии, которую хотите удалить: ").strip()

            if selected_id in vacancies:
                v_for_delete = vacancies_dict[int(selected_id)]
                vacancy_saver.delete_vacancy(v_for_delete)
                del vacancies_dict[int(selected_id)]
                if not vacancies_dict:
                    os.remove(vacancy_saver.file_path)
                return True

    print("Вакансии еще пока не добавлены")
    return True
