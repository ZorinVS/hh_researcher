from typing import Tuple, Union

from src.utils.validator import AreaNameValidator, NameValidator, RequirementsValidator, SalaryValidator, URLValidator


class Vacancy:
    """
    Класс для представления информации о вакансии.

    Атрибуты:
        _name (str): Название вакансии.
        _url (str): URL-адрес вакансии.
        _salary (Union[str, int]): Зарплата, может быть представлена строкой или числом.
        _city (str): Город размещения вакансии.
        _requirements (str): Требования к вакансии.

    Методы:
        __init__: Конструктор для инициализации вакансии.

        _avg_salary: Рассчитывает среднюю зарплату, если указаны диапазоны.
        _validate_other: Проверяет, что другой объект для сравнения также является экземпляром Vacancy.
        __lt__: Метод для сравнения вакансий по зарплате.
        __str__: Метод для строкового представления вакансии.

        name: Геттер и сеттер для названия вакансии.
        url: Геттер и сеттер для URL вакансии.
        salary: Геттер и сеттер для зарплаты вакансии.
        city: Геттер и сеттер для названия города размещения вакансии.
        requirements: Геттер и сеттер для требований к вакансии.
    """

    __slots__ = ("_name", "_url", "_salary", "_city", "_requirements")

    def __init__(
        self, name: str = "", url: str = "", salary: Union[str, int] = 0, city: str = "", requirements: str = ""
    ) -> None:
        """
        Конструктор для инициализации объекта вакансии с валидацией данных.

        :param name: Название вакансии. По умолчанию пустая строка.
        :param url: URL вакансии. По умолчанию пустая строка.
        :param salary: Зарплата вакансии. По умолчанию 0.
        :param city: Город размещения вакансии. По умолчанию пустая строка.
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
            self._city = ""
            self._requirements = ""
        else:
            self._requirements = RequirementsValidator.validate(requirements)
            self._salary = SalaryValidator.validate(salary)
            self._city = AreaNameValidator.validate(city)

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
    def _validate_other(other: Union["Vacancy", object]) -> bool:
        """
        Метод для проверки является ли другой объект экземпляром класса Vacancy.

        :param other: Проверяемый объект.
        :exception TypeError: Если объект для сравнения не является экземпляром Vacancy.
        :return: True, если объект корректен.
        """
        if not isinstance(other, Vacancy):
            raise TypeError("Сравнение возможно только между объектами Vacancy.")
        return True

    def __lt__(self, other: "Vacancy") -> bool:
        """
        Дандер для сравнения вакансий по зарплате.

        :param other: Другой объект вакансии для сравнения.
        :return: True, если зарплата текущей вакансии меньше, чем у другой.
        """
        self._validate_other(other)
        return self._avg_salary() < other._avg_salary()

    def __str__(self) -> str:
        """
        Дандер для строкового представления вакансии.

        :return: Вывод информации о вакансии в виде читаемой строки.
        """
        return (
            f"Название вакансии: {self._name}\n"
            f"Ссылка на вакансию: {self._url}\n"
            f"Зарплата: {self.salary}\n"
            f"Локация размещения вакансии: {self.city}\n"
            f"Требования: {self._requirements}"
        )

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
    def city(self) -> str:
        """
        Геттер для получения названия города размещения вакансии.

        :return: Название города размещения вакансии (если имеется, если нет - Россия).
        """
        return self._city

    @city.setter
    def city(self, value: str) -> None:
        """
        Сеттер названия города.

        :param value: Название города.
        """
        self._city = AreaNameValidator.validate(value)

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
