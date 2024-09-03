from typing import Dict, List, Tuple

from src.utils.sort_utility import sort_by_salary


def get_top_vacancies(vacancies: Dict[str, Dict]) -> List[Tuple[str, Dict]]:
    """
    Функция, выводящая топ N вакансий.

    :param vacancies: Вакансии, среди которых требуется получить топ N вакансий.
    :return: Топ N вакансий.
    """
    sorted_vacancies = sort_by_salary(vacancies)
    quantity = len(sorted_vacancies)
    while True:
        top_n_str = input("Какой топ N вакансий хотите получить (введите число): ").strip()
        print()
        if top_n_str.isdigit():
            top_n = int(top_n_str)
            if top_n > quantity:
                print(f"Нет возможности вывода 'Топ {top_n} вакансий'")
                print(f"Всего найдено вакансий: {quantity}\n")
                continue
            break

    return sorted_vacancies[:top_n]


def print_top_vacancies(top_n: List[Tuple[str, Dict]]) -> None:
    """
    Функция, выводящая топ N вакансий в консоль в читаемой форме.

    :param top_n: Список топ N вакансий.
    """
    for vacancy_tuple in top_n:
        id_, vacancy = vacancy_tuple

        print(f"ID: {id_}")
        print(f"Название: {vacancy["name"]}")
        print(f"URL: {vacancy["url"]}")
        print(f"Зарплата: {vacancy["salary"]}")
        print(f"Требования: {vacancy["requirements"]}")
        print()
