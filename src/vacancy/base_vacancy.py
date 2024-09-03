from abc import ABC, abstractmethod
from typing import Tuple, Union

from src.utils.validator import NameValidator, RequirementsValidator, SalaryValidator, URLValidator
from src.vacancy.vacancy_id_manager import VacancyIDManager


class BaseVacancy(ABC):
    """
    Абстрактный класс для представления вакансии.

    Атрибуты:
        _name (str): Название вакансии.
        _url (str): URL-адрес вакансии.
        _salary (Union[str, int]): Зарплата, может быть представлена строкой или числом.
        _requirements (str): Требования к вакансии.
        _id (int): Идентификатор вакансии.

    Методы:
        __init__: Конструктор для инициализации вакансии.
        delete: Абстрактный метод для удаления вакансии и освобождения id.
        _avg_salary: Абстрактный метод для расчета средней зарплаты, если указаны диапазоны.
        __lt__: Абстрактный метод для сравнения вакансий по зарплате.
        __repr__: Абстрактный метод для строкового представления вакансии.

        name: Геттер и сеттер для названия вакансии.
        url: Геттер и сеттер для URL вакансии.
        salary: Геттер и сеттер для зарплаты вакансии.
        requirements: Геттер и сеттер для требований к вакансии.
        id: Геттер и сеттер для работы с динамическим id вакансии.
    """

    __slots__ = ("_name", "_url", "_salary", "_requirements", "_id")

    def __init__(self, name: str = "", url: str = "", salary: Union[str, int] = 0, requirements: str = "") -> None:
        """
        Конструктор для инициализации объекта вакансии с валидацией данных.

        :param name: Название вакансии. По умолчанию пустая строка.
        :param url: URL вакансии. По умолчанию пустая строка.
        :param salary: Зарплата вакансии. По умолчанию 0.
        :param requirements: Требования к вакансии. По умолчанию пустая строка.
        :exception ValueError: Если данные не прошли валидацию.
        """
        try:
            self._name = NameValidator.validate(name)
            self._url = URLValidator.validate(url)
        except ValueError as e:
            print(f"Ошибка при инициализации объекта: {e}")
            self._name = ""
            self._url = ""
            self._salary: Union[int, Tuple[int, int]] = 0
            self._requirements = ""
        else:
            self._requirements = RequirementsValidator.validate(requirements)
            self._salary = SalaryValidator.validate(salary)
            self._id: Union[None, int] = VacancyIDManager.generate_id()

    @abstractmethod
    def delete(self) -> None:
        """Метод для удаления вакансии и освобождения id."""
        pass

    @abstractmethod
    def _avg_salary(self) -> Union[int, float]:
        """
        Метод, использующийся при сравнении зарплат.
        Делает расчет средней зарплаты, если указаны диапазоны.

        :return: Средняя зарплата.
        """
        pass

    @abstractmethod
    def __lt__(self, other: "BaseVacancy") -> bool:
        """
        Дандер для сравнения вакансий по зарплате.

        :param other: Другой объект вакансии для сравнения.
        :return: True, если зарплата текущей вакансии меньше, чем у другой.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """
        Дандер для строкового представления вакансии.

        :return: Строка для представления инициализации объекта вакансии.
        """
        pass

    # Геттеры и сеттеры
    @property
    def name(self) -> str:
        """
        Геттер для получения названия вакансии.

        :return: Название вакансии.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Сеттер названия вакансии с валидацией.

        :param value: Название вакансии.
        """
        self._name = NameValidator.validate(value)

    @property
    def url(self) -> str:
        """
        Геттер для получения URL вакансии.

        :return: URL вакансии.
        """
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        """
        Сеттер URL вакансии с валидацией.

        :param value: URL вакансии.
        """
        self._url = URLValidator.validate(value)

    @property
    def salary(self) -> str:
        """
        Геттер для получения зарплаты в виде строки.

        :return: Зарплата вакансии.
        """
        salary = self._salary
        if isinstance(salary, int):
            return f"{salary} руб."
        return f"{salary[0]}-{salary[1]} руб."

    @salary.setter
    def salary(self, value: Union[str, int]) -> None:
        """
        Сеттер зарплаты с валидацией.

        :param value: Зарплата вакансии.
        """
        self._salary = SalaryValidator.validate(value)

    @property
    def requirements(self) -> str:
        """
        Геттер для получения требований вакансии.

        :return: Требования вакансии.
        """
        return self._requirements

    @requirements.setter
    def requirements(self, value: str) -> None:
        """
        Сеттер требований вакансии с валидацией.

        :param value: Требования вакансии.
        """
        self._requirements = RequirementsValidator.validate(value)

    @property
    def id(self) -> int:
        """
        Геттер для получения id вакансии.

        :exception ValueError: Если id не установлен.
        :return: Идентификатор вакансии.
        """
        if self._id is None:
            raise ValueError("ID вакансии не установлен.")
        return self._id

    @id.setter
    def id(self, value: Union[None, int]) -> None:
        """
        Сеттер для работы с id (используется методами):
        - VacancyIDManager.generate_id()
        - VacancyJSON.add_vacancy()
        - self.delete()

        :param value: Значение id или его отсутствие.
        """
        self._id = value
