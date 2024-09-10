from typing import List

from src.utils.sort_utility import sort_by_salary
from src.vacancy.vacancy import Vacancy


def get_top_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Функция, выводящая топ N вакансий.

    :param vacancies: Список вакансий, среди которых требуется получить топ N вакансий.
    :return: Топ N вакансий.
    """
    sorted_vacancies = sort_by_salary(vacancies)
    quantity = len(sorted_vacancies)
    while True:
        top_n_str = input("Какой топ N вакансий хотите получить и сохранить (введите число): ").strip()
        if top_n_str.isdigit():
            top_n = int(top_n_str)
            if top_n > quantity:
                print(f"Нет возможности получения 'Топ-{top_n}'")
                print(f"Всего найдено вакансий: {quantity}")
                continue
            break

    return sorted_vacancies[:top_n]
