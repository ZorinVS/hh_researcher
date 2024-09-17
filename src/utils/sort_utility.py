from typing import List, Union

from src.utils.validator import SalaryValidator
from src.vacancy.vacancy import Vacancy


def avg_salary(salary_str: str) -> Union[int, float]:
    """
    Функция для получения среднего значения из строки.

    Вспомогательные функции:
        SalaryValidator.validate: Статический метод для получения чисел из строки.

    :param salary_str: Зарплата в виде строки.
    :return: Зарплата в виде числа.
    """
    salary = SalaryValidator.validate(salary_str)
    if isinstance(salary, tuple):
        salary_avg = sum(salary) / 2
        return round(salary_avg, 2)
    return salary


def get_salary(vacancy: Vacancy) -> Union[int, float]:
    """
    Функция для получения зарплаты из объекта вакансии в виде числа.

    :param vacancy: Объект вакансии.
    :return: Зарплата в виде числа.
    """
    return avg_salary(vacancy.salary)


def sort_by_salary(vacancies_list: List[Vacancy], descending: bool = True) -> List[Vacancy]:
    """
    Функция для сортировки списка вакансий.

    :param vacancies_list: Список объектов вакансий.
    :param descending: Параметр отвечающий за направление сортировки вакансий. По умолчанию от большего к меньшему.
    :return: Отсортированный список вакансий.
    """
    return sorted(vacancies_list, key=get_salary, reverse=descending)
