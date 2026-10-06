"""Тесты разбора ошибок RAC.

Регрессия: ``IncorrectVersionError``, ``CreateInfobaseParamsError``,
``DatabaseError`` и ``DatabaseConnectionError`` читали ``stderr.split("\\n")[1..3]``
без проверки длины, поэтому на коротком ответе RAC пользователь получал
``IndexError`` вместо описания проблемы.
"""

from __future__ import annotations

import unittest

from raclib import errors

from . import CLUSTER_AUTH_STDERR, SHORT_STDERR

#: Классы, которые раньше падали на коротком stderr.
INDEX_SENSITIVE_ERRORS = (
    errors.IncorrectVersionError,
    errors.CreateInfobaseParamsError,
    errors.DatabaseError,
    errors.DatabaseConnectionError,
)

#: Все классы ошибок, которые конструируются из текста stderr.
ALL_STDERR_ERRORS = tuple(
    value
    for value in vars(errors).values()
    if isinstance(value, type)
    and issubclass(value, Exception)
    and value.__module__ == errors.__name__
    and value
    not in (errors.UnknownError, errors.RACNotFoundError, errors.RACTimeoutError)
)


class ErrorConstructionTestCase(unittest.TestCase):
    """Ни один класс ошибки не должен падать при конструировании."""

    def test_all_errors_survive_short_stderr(self) -> None:
        for error_class in ALL_STDERR_ERRORS:
            with self.subTest(error=error_class.__name__):
                instance = error_class(SHORT_STDERR)
                self.assertTrue(str(instance), "сообщение не должно быть пустым")

    def test_all_errors_survive_empty_stderr(self) -> None:
        for error_class in ALL_STDERR_ERRORS:
            with self.subTest(error=error_class.__name__):
                self.assertIsInstance(str(error_class("")), str)

    def test_all_errors_survive_crlf_stderr(self) -> None:
        payload = "Первая строка\r\nВторая строка\r\nТретья строка\r\n"
        for error_class in ALL_STDERR_ERRORS:
            with self.subTest(error=error_class.__name__):
                self.assertIsInstance(str(error_class(payload)), str)

    def test_index_sensitive_errors_use_available_line(self) -> None:
        # Раньше здесь был IndexError; теперь берётся последняя доступная строка.
        payload = "Строка один\nСтрока два"
        self.assertIn("Строка", str(errors.IncorrectVersionError(payload)))


class HandlerDispatchTestCase(unittest.TestCase):
    """Таблица соответствий должна срабатывать на реальных сообщениях RAC."""

    def test_known_messages_map_to_classes(self) -> None:
        cases = {
            "Ошибка соединения с сервером администрирования": errors.ConnectionError,
            "Кластер с указанным идентификатором не найден": errors.ClusterNotFoundError,
            "Информационная база с указанным идентификатором не найдена": errors.InfobaseNotFoundError,
            "Левая граница диапазона IP портов больше правой": errors.ServerIPRangeError,
            "Компьютер отсутствует в сети или недоступен": errors.UnknownHostError,
            "Рабочий сервер является центральным. Удаление невозможно": errors.ServerIsMainError,
            "Счетчик с указанным идентификатором не найден": errors.CounterNotFoundError,
            "Ограничение ресурсов с указанным идентификатором не найдено": errors.LimitNotFoundError,
            "Требование размещения с указанным идентификатором не найдено": errors.RuleNotFoundError,
            "Различаются версии клиента и сервера": errors.IncorrectVersionError,
            "Ошибка разбора параметра: --port": errors.ParamError,
            "Администратор кластера серверов 1С:Предприятия не найден": errors.AgentAdminNotFoundError,
            "Запуск рабочего процесса не возможен из-за конфликта IP портов": errors.PortConflictError,
        }
        for message, expected in cases.items():
            with self.subTest(message=message):
                self.assertIsInstance(errors.handler(message), expected)

    def test_credentials_message_from_real_stderr(self) -> None:
        self.assertIsInstance(
            errors.handler(CLUSTER_AUTH_STDERR), errors.ClusterCredentialsError
        )

    def test_patterns_with_wildcards_still_match(self) -> None:
        # Раньше в двух шаблонах стояла одинокая звёздочка (".*Ошибка...*"),
        # из-за чего совпадение не срабатывало и ошибка попадала в UnknownError.
        payload = (
            "Ошибка при выполнении операции с информационной базой TestIB\n"
            "строка 2\nстрока 3\nНе удалось подключиться к серверу баз данных"
        )
        self.assertIsInstance(errors.handler(payload), errors.DatabaseError)

    def test_unknown_message_gives_unknown_error(self) -> None:
        instance = errors.handler("Совершенно новое сообщение RAC")
        self.assertIsInstance(instance, errors.UnknownError)
        self.assertIn("Совершенно новое сообщение", str(instance))

    def test_handler_returns_exception_instead_of_raising(self) -> None:
        # handler() обязана возвращать исключение: вызывающий код сам решает,
        # как его поднять, сохраняя исходную цепочку.
        result = errors.handler("Кластер с указанным идентификатором не найден")
        self.assertIsInstance(result, Exception)
        with self.assertRaises(errors.ClusterNotFoundError):
            raise result

    def test_connection_error_message_is_readable(self) -> None:
        # У ConnectionError есть собственный __str__, иначе OSError.__str__
        # вернул бы просто args[0] без пояснения.
        instance = errors.ConnectionError("Ошибка соединения с сервером")
        self.assertIn("Проверьте настройки подключения", str(instance))


class TransportErrorTestCase(unittest.TestCase):
    """Ошибки транспорта."""

    def test_rac_not_found_message(self) -> None:
        self.assertIn("RAC CLI not found", str(errors.RACNotFoundError()))

    def test_rac_timeout_reports_seconds(self) -> None:
        self.assertIn("30", str(errors.RACTimeoutError(30)))

    def test_rac_not_found_is_file_not_found(self) -> None:
        self.assertIsInstance(errors.RACNotFoundError(), FileNotFoundError)

    def test_rac_timeout_is_timeout_error(self) -> None:
        self.assertIsInstance(errors.RACTimeoutError(1), TimeoutError)


if __name__ == "__main__":
    unittest.main()
