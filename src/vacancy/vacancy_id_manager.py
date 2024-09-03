from abc import ABC, abstractmethod
from typing import Set


class BaseIDManager(ABC):
    """
    Абстрактный класс для управления уникальными идентификаторами.

    Методы:
        generate_id: Генерит новое id.
        delete_id: Удаляет существующее id.
    """

    @classmethod
    @abstractmethod
    def generate_id(cls) -> int:
        """
        Абстрактный метод для генерации нового id.

        :return: Уникальное id.
        """
        pass

    @classmethod
    @abstractmethod
    def delete_id(cls, id_to_delete: int) -> None:
        """
        Абстрактный метод для освобождения id.

        :param id_to_delete: Id, которое необходимо освободить.
        """
        pass


class VacancyIDManager(BaseIDManager):
    """
    Класс для управления уникальными идентификаторами вакансий.

    Атрибуты класса:
        _id_counter (int): Значение конечного id.
        _deleted_ids (set): Множество, хранящее удаленные id.

    Методы:
        generate_id: Генерит новое id.
        delete_id: Удаляет существующее id.
    """

    _id_counter: int = 0  # Начальное значение для id
    _deleted_ids: Set[int] = set()  # Множество для хранения удаленных id

    @classmethod
    def generate_id(cls) -> int:
        """
        Генерация нового уникального id.
        Если есть удаленные id, они переиспользуются.

        :return: Уникальное id.
        """
        # Если есть свободное id
        if cls._deleted_ids:
            # Используем свободное id и убираем его из множества свободных
            return cls._deleted_ids.pop()
        # Если нет свободных, генерим новое
        cls._id_counter += 1
        return cls._id_counter

    @classmethod
    def delete_id(cls, id_to_delete: int) -> None:
        """
        Удаление id, чтобы его можно было заново использовать.

        :param id_to_delete: Id, которое необходимо освободить.
        """
        cls._deleted_ids.add(id_to_delete)
