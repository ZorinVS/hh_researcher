from typing import Tuple


class VacancyAlreadyExistsError(Exception):
    """Класс исключения, которое вызывается, если вакансия уже существует в файле."""

    def __init__(self, *args: Tuple) -> None:
        """Конструктор для инициализации исключения с опциональным сообщением."""
        self.message = args[0] if args and isinstance(args[0], str) else "Вакансия уже существует в файле."

    def __str__(self) -> str:
        """Dunder-метод для строкового отображения исключения"""
        return self.message
