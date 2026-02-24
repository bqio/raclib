import re


class UnknownError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class RACNotFoundError(FileNotFoundError):
    def __init__(self):
        super().__init__("RAC CLI not found. Check client params")


class ClusterNotFoundError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Кластер с указанным идентификатором не найден")


class ClustersNotFoundError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Не найдено ни одного кластера")


class AgentAdminsNotFoundError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Не найдено ни одного администратора агента кластера")


class InfobaseNotFoundError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Информационная база с указанным идентификатором не найдена")


class InfobaseCredentialsError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Недостаточно прав пользователя на информационную базу")


class ClusterCredentialsError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Администратор кластера не аутентифицирован")


class AgentCredentialsError(Exception):
    def __init__(self, stderr: str):
        super().__init__(
            "Администратор агента кластера не аутентифицирован. Передайте корректные данные авторизации администратора агента кластера."
        )


class CentralServerCredentialsError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Администратор центрального сервера не аутентифицирован.")


class AgentAdminCreateError(Exception):
    def __init__(self, stderr: str):
        super().__init__(
            "В кластере не остается ни одного администратора с разрешенной аутентификацией паролем"
        )


class AgentAdminNotFoundError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Администратор кластера серверов 1С:Предприятия не найден")


class ConnectionError(ConnectionError):
    def __init__(self, stderr: str):
        super().__init__(
            "Ошибка соединения с сервером администрирования. Проверьте настройки подключения"
        )


class CreateInfobaseParamsError(Exception):
    def __init__(self, message: str):
        super().__init__(message.split("\n")[2])


class DatabaseConnectionError(Exception):
    def __init__(self, stderr: str):
        print(stderr)
        super().__init__(stderr.split("\n")[2])


class ServerNotCentralError(Exception):
    def __init__(self, stderr: str):
        super().__init__(stderr.split("\n")[0])


class DatabaseError(Exception):
    def __init__(self, stderr: str):
        super().__init__(stderr.split("\n")[3].strip())


class InfobaseDatabaseNotFoundError(Exception):
    def __init__(self, stderr: str):
        super().__init__(
            "База данных не найдена на сервере баз данных. Задайте create_database значение в True"
        )


class InfobaseAlreadyExistsError(Exception):
    def __init__(self, stderr: str):
        super().__init__(
            "Информационная база уже зарегистрирована в кластере серверов 1С:Предприятия"
        )


class ServerAlreadyExistsError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Рабочий сервер уже зарегистрирован в кластере")


class ServerIPRangeError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Левая граница диапазона IP портов больше правой")


class ServerIsMainError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Рабочий сервер является центральным. Удаление невозможно")


class IncorrectVersionError(Exception):
    def __init__(self, stderr: str):
        super().__init__(stderr.split("\n")[1].strip())


class ParamError(Exception):
    def __init__(self, stderr: str):
        super().__init__(stderr.split("\n")[0])


class PortConflictError(Exception):
    def __init__(self, stderr: str):
        super().__init__(
            "Запуск рабочего процесса не возможен из-за конфликта IP портов"
        )


class UnknownHostError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Компьютер отсутствует в сети или недоступен")


class CounterNotFoundError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Счетчик с указанным идентификатором не найден")


class LimitNotFoundError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Ограничение ресурсов с указанным идентификатором не найдено")


class RuleNotFoundError(Exception):
    def __init__(self, stderr: str):
        super().__init__("Требование размещения с указанным идентификатором не найдено")


errors = [
    (
        r"Различаются версии клиента и сервера",
        IncorrectVersionError,
    ),
    (
        r"Требование размещения с указанным идентификатором не найдено",
        RuleNotFoundError,
    ),
    (
        r"Ограничение ресурсов с указанным идентификатором не найдено",
        LimitNotFoundError,
    ),
    (
        r"Счетчик с указанным идентификатором не найден",
        CounterNotFoundError,
    ),
    (
        r"Рабочий сервер является центральным. Удаление невозможно",
        ServerIsMainError,
    ),
    (
        r"Левая граница диапазона IP портов больше правой",
        ServerIPRangeError,
    ),
    (
        r"Рабочий сервер уже зарегистрирован в кластере",
        ServerAlreadyExistsError,
    ),
    (
        r"Компьютер отсутствует в сети или недоступен",
        UnknownHostError,
    ),
    (
        r"Запуск рабочего процесса не возможен из-за конфликта IP портов",
        PortConflictError,
    ),
    (
        r"Сервер .* не является центральным для кластера .*",
        ServerNotCentralError,
    ),
    (
        r"Ошибка разбора параметра: .*",
        ParamError,
    ),
    (
        r"Администратор кластера серверов 1С:Предприятия не найден",
        AgentAdminNotFoundError,
    ),
    (
        r"В кластере не остается ни одного администратора с разрешенной аутентификацией паролем",
        AgentAdminCreateError,
    ),
    (
        r"Информационная база .* уже зарегистрирована в кластере серверов 1С:Предприятия",
        InfobaseAlreadyExistsError,
    ),
    (
        r"База данных .* не найдена в сервере баз данных",
        InfobaseDatabaseNotFoundError,
    ),
    (
        r".*Ошибка при выполнении операции с информационной базой*",
        DatabaseError,
    ),
    (
        r".*Сервер баз данных не обнаружен*",
        DatabaseConnectionError,
    ),
    (
        r".*Неверные или отсутствующие параметры соединения, необходимые для создания информационной базы.*",
        CreateInfobaseParamsError,
    ),
    (
        r".*Администратор кластера не аутентифицирован.*",
        ClusterCredentialsError,
    ),
    (
        r".*Администратор центрального сервера не аутентифицирован.*",
        CentralServerCredentialsError,
    ),
    (
        r"Недостаточно прав пользователя на информационную базу.*",
        InfobaseCredentialsError,
    ),
    (
        r"Ошибка соединения с сервером",
        ConnectionError,
    ),
    (
        r"Кластер с указанным идентификатором не найден",
        ClusterNotFoundError,
    ),
    (
        r"Информационная база с указанным идентификатором не найдена",
        InfobaseNotFoundError,
    ),
]


def handler(stderr: str) -> Exception:
    for error in errors:
        if re.findall(error[0], stderr):
            return error[1](stderr)
    return UnknownError(stderr)
