"""Ошибки, которые RAC сообщает в stderr.

Классы получают исходный текст ``stderr`` и **номер строки**, в которой лежит
содержательное сообщение. Номер строки необязателен: если RAC ответил короче
ожидаемого (или текст сообщения изменился в новой версии 1С), используется
``stderr`` целиком. Раньше здесь стояли жёсткие ``stderr.split("\\n")[2]``, из-за
чего при коротком ответе пользователь получал ``IndexError`` вместо понятной
ошибки.
"""

import re

from ._shared import RACInvocationError, RACNotFoundError, RACTimeoutError

__all__ = [
    "handler",
    "errors",
    "UnknownError",
    "RACNotFoundError",
    "RACInvocationError",
    "RACTimeoutError",
]


def _line(stderr: str, index: int) -> str:
    """Возвращает строку ``index`` из stderr или весь текст, если её нет."""
    lines = [line for line in stderr.splitlines() if line.strip()]
    if 0 <= index < len(lines):
        return lines[index].strip()
    return stderr.strip()


class UnknownError(Exception):
    """RAC вернул ошибку, которой нет в таблице соответствий."""

    def __init__(self, stderr: str):
        lines = [line.strip() for line in stderr.splitlines() if line.strip()]
        self.stderr = stderr
        super().__init__("\n".join(lines) if lines else stderr.strip())


class ClusterNotFoundError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Кластер с указанным идентификатором не найден")


class ClustersNotFoundError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Не найдено ни одного кластера")


class AgentAdminsNotFoundError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Не найдено ни одного администратора агента кластера")


class InfobaseNotFoundError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Информационная база с указанным идентификатором не найдена")


class InfobaseCredentialsError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Недостаточно прав пользователя на информационную базу")


class ClusterCredentialsError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Администратор кластера не аутентифицирован")


class AgentCredentialsError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__(
            "Администратор агента кластера не аутентифицирован. Передайте корректные данные авторизации администратора агента кластера."
        )


class CentralServerCredentialsError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Администратор центрального сервера не аутентифицирован.")


class AgentAdminCreateError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__(
            "В кластере не остается ни одного администратора с разрешенной аутентификацией паролем"
        )


class AgentAdminNotFoundError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Администратор кластера серверов 1С:Предприятия не найден")


class ConnectionError(ConnectionError):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__(
            "Ошибка соединения с сервером администрирования. Проверьте настройки подключения"
        )

    def __str__(self) -> str:
        args = self.args
        return str(args[0]) if args else super().__str__()


class CreateInfobaseParamsError(Exception):
    def __init__(self, stderr: str, index: int = 2):
        super().__init__(_line(stderr, index))


class DatabaseConnectionError(Exception):
    def __init__(self, stderr: str, index: int = 2):
        super().__init__(_line(stderr, index))


class ServerNotCentralError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__(_line(stderr, index))


class DatabaseError(Exception):
    def __init__(self, stderr: str, index: int = 3):
        super().__init__(_line(stderr, index))


class InfobaseDatabaseNotFoundError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__(
            "База данных не найдена на сервере баз данных. Задайте create_database значение в True"
        )


class InfobaseAlreadyExistsError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__(
            "Информационная база уже зарегистрирована в кластере серверов 1С:Предприятия"
        )


class ServerAlreadyExistsError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Рабочий сервер уже зарегистрирован в кластере")


class ServerIPRangeError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Левая граница диапазона IP портов больше правой")


class ServerIsMainError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Рабочий сервер является центральным. Удаление невозможно")


class IncorrectVersionError(Exception):
    def __init__(self, stderr: str, index: int = 1):
        super().__init__(_line(stderr, index))


class ParamError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__(_line(stderr, index))


class PortConflictError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__(
            "Запуск рабочего процесса не возможен из-за конфликта IP портов"
        )


class UnknownHostError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Компьютер отсутствует в сети или недоступен")


class CounterNotFoundError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Счетчик с указанным идентификатором не найден")


class LimitNotFoundError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Ограничение ресурсов с указанным идентификатором не найдено")


class RuleNotFoundError(Exception):
    def __init__(self, stderr: str, index: int = 0):
        super().__init__("Требование размещения с указанным идентификатором не найдено")


#: Таблица соответствия «шаблон сообщения RAC → класс ошибки и номер строки».
#: Побеждает первое совпадение. Сообщения локализованы, поэтому таблица не
#: является исчерпывающей: незнакомый текст приводит к ``UnknownError``,
#: который сохраняет исходные строки RAC.
errors = [
    (
        r"Различаются версии клиента и сервера",
        IncorrectVersionError,
        1,
    ),
    (
        r"Требование размещения с указанным идентификатором не найдено",
        RuleNotFoundError,
        0,
    ),
    (
        r"Ограничение ресурсов с указанным идентификатором не найдено",
        LimitNotFoundError,
        0,
    ),
    (
        r"Счетчик с указанным идентификатором не найден",
        CounterNotFoundError,
        0,
    ),
    (
        r"Рабочий сервер является центральным. Удаление невозможно",
        ServerIsMainError,
        0,
    ),
    (
        r"Левая граница диапазона IP портов больше правой",
        ServerIPRangeError,
        0,
    ),
    (
        r"Рабочий сервер уже зарегистрирован в кластере",
        ServerAlreadyExistsError,
        0,
    ),
    (
        r"Компьютер отсутствует в сети или недоступен",
        UnknownHostError,
        0,
    ),
    (
        r"Запуск рабочего процесса не возможен из-за конфликта IP портов",
        PortConflictError,
        0,
    ),
    (
        r"Сервер .* не является центральным для кластера .*",
        ServerNotCentralError,
        0,
    ),
    (
        r"Ошибка разбора параметра: .*",
        ParamError,
        0,
    ),
    (
        r"Администратор кластера серверов 1С:Предприятия не найден",
        AgentAdminNotFoundError,
        0,
    ),
    (
        r"В кластере не остается ни одного администратора с разрешенной аутентификацией паролем",
        AgentAdminCreateError,
        0,
    ),
    (
        r"Информационная база .* уже зарегистрирована в кластере серверов 1С:Предприятия",
        InfobaseAlreadyExistsError,
        0,
    ),
    (
        r"База данных .* не найдена в сервере баз данных",
        InfobaseDatabaseNotFoundError,
        0,
    ),
    (
        r".*Ошибка при выполнении операции с информационной базой.*",
        DatabaseError,
        3,
    ),
    (
        r".*Сервер баз данных не обнаружен.*",
        DatabaseConnectionError,
        2,
    ),
    (
        r".*Неверные или отсутствующие параметры соединения, необходимые для создания информационной базы.*",
        CreateInfobaseParamsError,
        2,
    ),
    (
        r".*Администратор кластера не аутентифицирован.*",
        ClusterCredentialsError,
        0,
    ),
    (
        r".*Администратор центрального сервера не аутентифицирован.*",
        CentralServerCredentialsError,
        0,
    ),
    (
        r"Недостаточно прав пользователя на информационную базу.*",
        InfobaseCredentialsError,
        0,
    ),
    (
        r"Ошибка соединения с сервером",
        ConnectionError,
        0,
    ),
    (
        r"Кластер с указанным идентификатором не найден",
        ClusterNotFoundError,
        0,
    ),
    (
        r"Информационная база с указанным идентификатором не найдена",
        InfobaseNotFoundError,
        0,
    ),
]


def handler(stderr: str) -> Exception:
    """Возвращает исключение, соответствующее тексту ``stderr``.

    Не выбрасывает исключение сама: вызывающая сторона решает, как его поднять,
    чтобы сохранить исходную цепочку ошибок.
    """
    for pattern, error_class, index in errors:
        if re.search(pattern, stderr):
            try:
                return error_class(stderr, index)
            except Exception as exc:  # pragma: no cover - защитная сетка
                return UnknownError(f"{stderr}\n[{type(exc).__name__}: {exc}]")
    return UnknownError(stderr)
