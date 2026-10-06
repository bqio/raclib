"""Общие для синхронной и асинхронной веток примитивы.

Модуль внутренний (подчёркивание в имени), но переиспользуется
сгенерированным асинхронным деревом, чтобы у обеих веток был ровно один
источник правды для разбора вывода RAC и для разбора сообщений об ошибках.
"""

from __future__ import annotations

import re
import shutil
import stat
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")

#: Одна запись вывода RAC: ключи с подчёркиваниями вместо дефисов, числовые
#: значения приведены к ``int``. Используется в аннотациях методов команд и
#: попадает в справочник API.
type RacRecord = dict[str, str | int]

__all__ = [
    "Client",
    "CommandResult",
    "RACInvocationError",
    "RACNotFoundError",
    "RACTimeoutError",
    "RacRecord",
    "RawOutput",
    "b2ana",
    "b2da",
    "b2of",
    "b2yn",
    "any2b",
    "decode_stream",
    "default_encoding",
    "dict_entry_count",
    "get_array_chunks",
    "resolve_encoding",
    "to_record",
    "to_records",
    "validate_rac_path",
]

#: Локаль RAC: "ключ : значение". Разделитель — первое двоеточие в строке,
#: поэтому значения, содержащие двоеточие (например строки соединения с БД),
#: разбираются корректно.
LIST_DICT_REGEX = r"^\s*(.+?)\s*:\s?(.*)$"

#: Разделитель строк, который RAC использует для многострочных значений.
LINE_CONTINUATION_PREFIX = "-"

#: Символы, в которые разворачиваются экранированные последовательности.
#: Применяются только к значениям, начинающимся с ``"``.
_ESCAPES = ((r"\"", '"'), (r"\n", "\n"), (r"\r", "\r"), (r"\t", "\t"), (r"\\", "\\"))


def default_encoding() -> str:
    """Кодировка вывода RAC по умолчанию для текущей платформы.

    ``cp866`` — то, что отдаёт ``rac.exe`` на Windows. На остальных платформах
    вывод идёт в UTF-8, и жёсткое декодирование cp866 превращало бы русские
    ключи в мусор, полностью ломая разбор.
    """
    return "cp866" if sys.platform == "win32" else "utf-8"


def resolve_encoding(encoding: str | None) -> str:
    """Подставляет кодировку платформы, если явная не задана."""
    return encoding or default_encoding()


def b2yn(b: bool | None) -> str | None:
    match b:
        case True:
            return "yes"
        case False:
            return "no"
        case None:
            return None


def b2of(b: bool | None) -> str | None:
    match b:
        case True:
            return "on"
        case False:
            return "off"
        case None:
            return None


def b2da(b: bool | None) -> str | None:
    match b:
        case True:
            return "allow"
        case False:
            return "deny"
        case None:
            return None


def b2ana(b: bool | None) -> str | None:
    match b:
        case True:
            return "analyze"
        case False:
            return "not-analyze"
        case None:
            return None


def any2b(an: str | int) -> bool | str | int:
    match an:
        case "yes":
            return True
        case "no":
            return False
        case "on":
            return True
        case "off":
            return False
        case "allow":
            return True
        case "deny":
            return False
        case "analyze":
            return True
        case "not-analyze":
            return False
        case _:
            return an


def get_array_chunks(arr: list[tuple[str, str]], n: int) -> list[list[tuple[str, str]]]:
    """Режет список на куски по ``n`` элементов.

    Устаревшая утилита: ``RawOutput`` больше не разбивает записи по количеству
    свойств. Оставлена для обратной совместимости.
    """
    if n <= 0:
        raise ValueError(f"Размер куска должен быть положительным, получено: {n}")
    return [arr[i : i + n] for i in range(0, len(arr), n)]


def dict_entry_count(lines: list[str]) -> int:
    """Число строк до первой пустой.

    Устаревшая утилита, оставлена для обратной совместимости. Новый разбор
    записей от неё не зависит.
    """
    return next((i for i, line in enumerate(lines) if line == ""), len(lines))


def _unescape(value: str) -> str:
    if not value.startswith('"'):
        return value
    for escaped, real in _ESCAPES:
        value = value.replace(escaped, real)
    return value


def _parse_value(raw: str) -> str | int:
    """Снимает кавычки, разворачивает escape-последовательности, приводит тип."""
    value = _unescape(raw.strip())
    if value.startswith('"') or value.endswith('"'):
        value = value.strip('"')
    if value.isdecimal():
        return int(value)
    return value


def _iter_lines(output: str) -> Iterator[str]:
    """Строки вывода без разделителей строк.

    ``str.splitlines()`` корректно обрабатывает и LF, и CRLF, и CR, и не
    оставляет ``\\r`` в конце строки. Именно из-за ``output.split("\\n")``
    прежний разбор ломался на Windows, склеивая все записи в одну.
    """
    return (line for line in output.splitlines() if line.strip(" \t\r") != "")


def to_records(output: str) -> list[dict[str, str | int]]:
    """Разбирает вывод RAC в список записей.

    Границы записей определяются по повтору ключа, а не по пустым строкам и не
    по количеству свойств. Такой разбор не зависит от:

    * переводов строк (LF/CRLF/CR);
    * наличия пустой строки после последней записи;
    * различий в наборе свойств между записями разных версий 1С.

    Многострочные значения RAC продолжает строками, начинающимися с ``-``.
    Такие строки дописываются в значение предыдущего ключа.

    :param output: текст, полученный от RAC.
    :returns: список записей; ключи переведены на ``_`` вместо ``-``.
    """
    records: list[dict[str, str | int]] = []
    current: dict[str, str | int] = {}
    last_key: str | None = None

    for line in _iter_lines(output):
        if line.lstrip().startswith(LINE_CONTINUATION_PREFIX):
            if last_key is not None and isinstance(current.get(last_key), str):
                continuation = line.strip().strip(LINE_CONTINUATION_PREFIX).strip()
                current[last_key] = (
                    f"{str(current[last_key]).rstrip('"')} {continuation.strip('"')}"
                ).strip()
            continue

        match = re.match(LIST_DICT_REGEX, line)
        if match is None:
            continue

        key = match.group(1).replace("-", "_")
        if key in current:
            records.append(current)
            current = {}
        current[key] = _parse_value(match.group(2))
        last_key = key

    if current:
        records.append(current)
    return records


def to_record(output: str) -> dict[str, str | int]:
    """Разбирает вывод RAC в одну запись (последнюю, как и раньше)."""
    records = to_records(output)
    return records[-1] if records else {}


class RawOutput:
    """Результат выполнения команды RAC с методами разбора."""

    def __init__(self, output: str) -> None:
        self.output = output

    def to_str(self) -> str:
        return self.output.strip()

    def to_dict(self) -> dict[str, str | int]:
        return to_record(self.output)

    def to_dataclass(self, dc: type[T]) -> T:
        return dc(**self.to_dict())

    def to_list_of_dataclass(self, dc: type[T]) -> list[T]:
        return [dc(**entry) for entry in self.to_list()]

    def to_list(self) -> list[dict[str, str | int]]:
        return to_records(self.output)


class Client:
    """Путь к исполняемому файлу ``rac``."""

    def __init__(self, rac_path: Path | str):
        self.rac_path = Path(rac_path).expanduser()


class RACNotFoundError(FileNotFoundError):
    """Исполняемый файл ``rac`` не найден.

    Историческое имя, используется в публичном API.
    """

    def __init__(self, message: str | None = None):
        super().__init__(message or "RAC CLI not found. Check client params")


class RACInvocationError(RACNotFoundError):
    """``rac`` найден, но запустить его нельзя: каталог, нет прав и т.п."""


class RACTimeoutError(TimeoutError):
    """RAC не ответил за отведённое время."""

    def __init__(self, timeout: float):
        super().__init__(
            f"RAC не ответил за {timeout} с. "
            "Проверьте доступность сервера администрирования "
            "или увеличьте значение timeout"
        )


def validate_rac_path(rac_path: Path | str) -> None:
    """Проверяет, что путь указывает на исполняемый файл ``rac``.

    Вызывается лениво, при первом запуске команды, чтобы ``Client`` можно было
    создавать до того, как каталог с 1С появится в системе.

    :raises RACNotFoundError: путь не найден или непригоден для запуска.
    """
    path = Path(rac_path).expanduser()
    resolved = shutil.which(str(path)) if not path.parent.name else None
    candidate = Path(resolved) if resolved else path

    if not resolved and not candidate.exists():
        raise RACInvocationError(f"Исполняемый файл RAC не найден по пути: {candidate}")
    if candidate.is_dir():
        raise RACInvocationError(
            f"По пути {candidate} находится каталог, а не исполняемый файл RAC"
        )
    if candidate.is_file() and not _is_executable(candidate):
        raise RACInvocationError(
            f"Файл {candidate} не является исполняемым. Проверьте права доступа"
        )


def _is_executable(path: Path) -> bool:
    if sys.platform == "win32":
        # На Windows бит исполнения не используется, достаточно существования
        # файла: отсутствие PE-заголовка отловит сама ОС при запуске.
        return True
    return bool(path.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))


@dataclass(frozen=True)
class CommandResult:
    """Нормализованный результат запуска процесса.

    Нужен, чтобы у синхронного и асинхронного транспорта был одинаковый
    интерфейс и общая логика обработки ошибок.
    """

    returncode: int
    stdout: str
    stderr: str


def decode_stream(raw: bytes | str, encoding: str) -> str:
    """Приводит stdout/stderr к тексту в нужной кодировке."""
    if isinstance(raw, bytes):
        return raw.decode(encoding=encoding, errors="replace")
    return raw
