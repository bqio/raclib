"""Тесты сборки команд и сквозные проверки на фейковой сессии."""

from __future__ import annotations

import unittest

from raclib import errors
from raclib._shared import RawOutput
from raclib.cmd.agent import Agent
from raclib.cmd.cluster import Cluster
from raclib.cmd.command import Arg, Command, Flag
from raclib.cmd.infobase import Infobase
from raclib.cmd.process import Process
from raclib.cmd.rule import Rule
from raclib.cmd.session import UserSession


class RecordingSession:
    """Сессия-заглушка: запоминает argv и отдаёт заранее заданный вывод."""

    def __init__(self, stdout: str = "") -> None:
        self.stdout = stdout
        self.calls: list[list[str]] = []

    def exec(self, command: Command | str) -> RawOutput:
        self.calls.append(getattr(command, "args", [str(command)]))
        return RawOutput(self.stdout)

    def call(self, command: Command | str) -> None:
        self.calls.append(getattr(command, "args", [str(command)]))


class CommandTestCase(unittest.TestCase):
    """``Arg`` и ``Flag`` собирают argv, а не строку для shell."""

    def test_arg_renders_value(self) -> None:
        self.assertEqual(str(Arg("cl-1", "--cluster={}")), "--cluster=cl-1")

    def test_enum_value_is_rendered(self) -> None:
        from enum import Enum

        class Kind(Enum):
            CLUSTER = "cluster"

        self.assertEqual(str(Arg(Kind.CLUSTER)), "cluster")

    def test_none_values_are_dropped(self) -> None:
        command = Command(Arg("cluster"), Arg(None, "--cluster={}"), Arg("list"))
        self.assertEqual(command.args, ["cluster", "list"])

    def test_flag_with_false_state_is_dropped(self) -> None:
        command = Command(Arg("list"), Flag(False, "--licenses"))
        self.assertEqual(command.args, ["list"])

    def test_flag_with_true_state_is_added(self) -> None:
        command = Command(Arg("list"), Flag(True, "--licenses"))
        self.assertEqual(command.args, ["list", "--licenses"])

    def test_values_with_spaces_stay_a_single_argv_item(self) -> None:
        # Важно: argv передаётся в subprocess списком, поэтому пробелы в имени
        # базы не требуют экранирования и не могут развалить команду.
        command = Command(Arg("Тестовая база", "--name={}"))
        self.assertEqual(command.args, ["--name=Тестовая база"])
        self.assertEqual(len(command.args), 1)


class CommandIntegrationTestCase(unittest.TestCase):
    """Проверяем фактическую последовательность аргументов для каждого вызова."""

    def test_cluster_list(self) -> None:
        session = RecordingSession()
        Cluster.list(session)
        self.assertEqual(session.calls[0], ["cluster", "list"])

    def test_cluster_info_passes_cluster(self) -> None:
        session = RecordingSession()
        Cluster.info(session, "cl-1")
        self.assertEqual(session.calls[0], ["cluster", "info", "--cluster=cl-1"])

    def test_cluster_admin_list(self) -> None:
        session = RecordingSession()
        Cluster.Admin.list(session, "cl-1", "admin", "secret")
        self.assertEqual(
            session.calls[0],
            [
                "cluster",
                "admin",
                "--cluster=cl-1",
                "--cluster-user=admin",
                "--cluster-pwd=secret",
                "list",
            ],
        )

    def test_cluster_insert_returns_identifier(self) -> None:
        session = RecordingSession("cluster : new-cluster-id\n")
        result = Cluster.insert(session, "host", 1541)
        self.assertEqual(result, "new-cluster-id")
        self.assertIn("--host=host", session.calls[0])
        self.assertIn("--port=1541", session.calls[0])

    def test_cluster_remove(self) -> None:
        session = RecordingSession()
        Cluster.remove(session, "cl-1", "admin", "secret")
        self.assertEqual(
            session.calls[0],
            ["cluster", "remove", "--cluster=cl-1", "--cluster-user=admin", "--cluster-pwd=secret"],
        )

    def test_booleans_are_converted_to_rac_words(self) -> None:
        session = RecordingSession("cluster : id\n")
        Cluster.insert(session, "host", 1541, kill_problem_processes=False)
        self.assertIn("--kill-problem-processes=no", session.calls[0])

    def test_infobase_create_builds_full_command(self) -> None:
        session = RecordingSession("infobase : ib-id\n")
        result = Infobase.create(
            session, "cl-1", "Тестовая", "PostgreSQL", "localhost", "TestIB", "ru_RU"
        )
        argv = session.calls[0]
        self.assertEqual(result, "ib-id")
        self.assertIn("--dbms=PostgreSQL", argv)
        self.assertIn("--name=Тестовая", argv)
        self.assertIn("--locale=ru_RU", argv)
        self.assertIn("--db-server=localhost", argv)
        self.assertIn("--db-name=TestIB", argv)
        self.assertNotIn("--create-database", argv)

    def test_infobase_create_flag_when_requested(self) -> None:
        session = RecordingSession("infobase : ib-id\n")
        Infobase.create(
            session, "cl-1", "n", "PostgreSQL", "localhost", "db", "ru_RU",
            create_database=True,
        )
        self.assertIn("--create-database", session.calls[0])

    def test_infobase_drop_accepts_database_credentials(self) -> None:
        # Регрессия: параметры db_user/db_pwd отсутствовали, и попытка их
        # передать приводила к TypeError, а сама команда уходила без них.
        session = RecordingSession()
        Infobase.drop(
            session, "cl-1", "ib-1", db_user="postgres", db_pwd="pg-secret"
        )
        self.assertIn("--db-user=postgres", session.calls[0])
        self.assertIn("--db-pwd=pg-secret", session.calls[0])

    def test_infobase_drop_flags(self) -> None:
        session = RecordingSession()
        Infobase.drop(session, "cl-1", "ib-1", drop_database=True)
        self.assertIn("--drop-database", session.calls[0])
        self.assertNotIn("--clear-database", session.calls[0])

    def test_user_session_list_with_licenses(self) -> None:
        session = RecordingSession()
        UserSession.list(session, "cl-1", licenses=True)
        self.assertEqual(
            session.calls[0],
            ["session", "--cluster=cl-1", "list", "--licenses"],
        )

    def test_process_info(self) -> None:
        session = RecordingSession()
        Process.info(session, "cl-1", "proc-1")
        self.assertEqual(
            session.calls[0], ["process", "--cluster=cl-1", "info", "--process=proc-1"]
        )

    def test_rule_insert_returns_identifier(self) -> None:
        session = RecordingSession("rule : rule-id\n")
        result = Rule.insert(session, "cl-1", "srv-1", 1)
        self.assertEqual(result, "rule-id")
        self.assertIn("--position=1", session.calls[0])

    def test_rule_apply_partial_flag(self) -> None:
        session = RecordingSession()
        Rule.apply(session, "cl-1", partial=True)
        self.assertEqual(session.calls[0], ["rule", "--cluster=cl-1", "apply", "--partial"])

    def test_agent_version(self) -> None:
        session = RecordingSession("version : 8.3.24.1548\n")
        self.assertEqual(Agent.version(session), "version : 8.3.24.1548")


class ErrorsFromFakeSessionTestCase(unittest.TestCase):
    """Ошибки RAC доходят до пользователя в виде понятных исключений."""

    def test_mapped_error_is_raised_by_transport(self) -> None:
        # Проверяем связку errors.handler + raise, как это делает Session._execute.
        with self.assertRaises(errors.ClusterNotFoundError):
            raise errors.handler("Кластер с указанным идентификатором не найден")


if __name__ == "__main__":
    unittest.main()
