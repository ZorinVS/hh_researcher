from typing import Dict, List, Tuple, Union

from src.utils.validator import SalaryValidator


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


def get_salary(item: Tuple[str, Dict[str, str]]) -> Union[int, float]:
    """
    Ключ для сортировки в функции sorted.
    Предназначен для обращения к ключу вакансии "salary".

    Вспомогательные функции:
        avg_salary: Из строки возвращает среднее значение зарплаты.

    :param item: Параметр для перебора списка картежей.
                 Список хранит картежи формата (ID, vacancy), где vacancy - словарь, содержащий информацию о вакансии.
    :return: Зарплата в виде одного числа.
    """
    return avg_salary(item[1]["salary"])


def sort_by_salary(data: Dict[str, Dict[str, str]], descending: bool = True) -> List[Tuple[str, Dict[str, str]]]:
    """
    Функция для сортировки вакансий по зарплате.

    :param data: Данные, хранящие информацию о вакансиях.
    :param descending: Направление сортировки (по умолчанию сортирует от большего к меньшему - True).
    :return: Отсортированные вакансии в виде списка картежей ( List[(ID, vacancy)] ).
    """
    return sorted(data.items(), key=get_salary, reverse=descending)
