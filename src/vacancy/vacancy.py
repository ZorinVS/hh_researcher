from typing import Union

from src.vacancy.base_vacancy import BaseVacancy
from src.vacancy.vacancy_id_manager import VacancyIDManager


class Vacancy(BaseVacancy):
    """
    Класс для представления информации о вакансии.

    Атрибуты:
        _name (str): Название вакансии.
        _url (str): URL-адрес вакансии.
        _salary (Union[str, int]): Зарплата, может быть представлена строкой или числом.
        _requirements (str): Требования к вакансии.
        _id (int): Идентификатор вакансии.

    Методы:
        delete: Метод для удаления вакансии и освобождения id.
        _avg_salary: Рассчитывает среднюю зарплату, если указаны диапазоны.
        _validate_other: Проверяет, что другой объект для сравнения также является экземпляром Vacancy.
        __lt__: Абстрактный метод для сравнения вакансий по зарплате.
        __repr__: Метод для строкового представления вакансии.

        Наследующиеся от BaseVacancy:
            __init__: Конструктор для инициализации вакансии.

            name: Геттер и сеттер для названия вакансии.
            url: Геттер и сеттер для URL вакансии.
            salary: Геттер и сеттер для зарплаты вакансии.
            requirements: Геттер и сеттер для требований к вакансии.
            id: Геттер и сеттер для работы с динамическим id вакансии.
    """

    def delete(self) -> None:
        """Метод для удаления вакансии и освобождения id."""
        VacancyIDManager.delete_id(self.id)
        self._id: None = None

    def _avg_salary(self) -> Union[int, float]:
        """
        Метод, использующийся при сравнении зарплат.
        Делает расчет средней зарплаты, если указаны диапазоны.

        :return: Средняя зарплата.
        """
        if isinstance(self._salary, tuple):
            return round(sum(self._salary) / 2, 2)
        return self._salary

    @staticmethod
    def _validate_other(other: Union["BaseVacancy", object]) -> bool:
        """
        Метод для проверки является ли другой объект экземпляром класса Vacancy.

        :param other: Проверяемый объект.
        :exception TypeError: Если объект для сравнения не является экземпляром Vacancy.
        :return: True, если объект корректен.
        """
        if not isinstance(other, BaseVacancy):
            raise TypeError("Сравнение возможно только между объектами Vacancy.")
        return True

    def __lt__(self, other: "BaseVacancy") -> bool:
        """
        Дандер для сравнения вакансий по зарплате.

        :param other: Другой объект вакансии для сравнения.
        :return: True, если зарплата текущей вакансии меньше, чем у другой.
        """
        self._validate_other(other)
        return self._avg_salary() < other._avg_salary()

    def __repr__(self) -> str:
        """
        Дандер для строкового представления вакансии.

        :return: Строка для представления инициализации объекта вакансии.
        """
        if self._salary:
            return (
                f"{self.__class__.__name__}"
                f"('{self._name}', "
                f"'{self._url}', "
                f"'{self.salary}', "
                f"'{self._requirements}')"
            )
        return (
            f"{self.__class__.__name__}"
            f"('name={self._name}', "
            f"url='{self._url}', "
            f"requirements='{self._requirements}')"
        )
