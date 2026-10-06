"""Сборка argv команды ``rac``.

Каждая команда собирается из объектов :class:`Arg` и :class:`Flag`. Значение
``None`` означает «параметр не задан», и такой объект в argv не попадает —
именно поэтому методы команд принимают ``None`` как «оставить как есть».

Готовый список аргументов передаётся в :class:`raclib.Session` и запускается
**без shell**: argv уходит списком, поэтому пробелы и кавычки в именах
информационных баз не требуют экранирования.
"""

from enum import Enum
from typing import Protocol


class SupportsStr(Protocol):
    """Значение, которое умеет превращаться в строку."""

    def __str__(self) -> str: ...


class Flag:
    """Флаг без значения: ``--licenses``.

    Попадает в argv только при ``state=True``.
    """

    def __init__(
        self,
        state: bool,
        value: str,
    ):
        self.value = value if state else None

    def __str__(self) -> str:
        return self.value if self.value is not None else ""

    def is_valid(self) -> bool:
        """Нужно ли включать флаг в argv."""
        return self.value is not None


class Arg:
    """Параметр со значением: ``--cluster=6a4c0b3f-...``.

    :param value: значение параметра; ``None`` — параметр не передаётся.
    :param fmt: шаблон вида ``--cluster={}``. Пробелы и кавычки в значении
        экранировать не нужно: argv уходит в процесс списком, а не строкой.
    """

    def __init__(self, value: SupportsStr, fmt: str = "{}"):
        self.value = value.value if isinstance(value, Enum) else value
        self.fmt = fmt

    def __str__(self) -> str:
        return self.fmt.format(self.value)

    def is_valid(self) -> bool:
        """Нужно ли включать параметр в argv."""
        return self.value is not None


class Command:
    """Готовая команда: список аргументов для запуска ``rac``."""

    def __init__(self, *args: Arg | Flag):
        self.args = [str(arg) for arg in args if arg.is_valid()]

    def __str__(self) -> str:
        """Команда одной строкой — удобно для логов и отладки."""
        return " ".join(self.args)
