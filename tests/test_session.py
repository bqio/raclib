"""Тесты транспорта, сессии и клиента."""

from __future__ import annotations

import asyncio
import stat
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import raclib
from raclib import errors
from raclib._shared import (
    CommandResult,
    RawOutput,
    default_encoding,
    resolve_encoding,
    validate_rac_path,
)
from raclib._transport import run_rac
from raclib.asynchronous import session as async_session_module
from raclib.asynchronous._transport import run_rac_async
from raclib.asynchronous.session import AsyncSession
from raclib.cmd.command import Arg, Command
from raclib.session import Session, _command_args, _creation_flags

from . import CLUSTER_INFO, make_executable, temp_dir


def fake_rac(path: Path) -> Path:
    """Создаёт исполняемый файл-заглушку вместо реального ``rac``."""
    path.write_text("stub", encoding="utf-8")
    make_executable(path)
    return path


class PathValidationTestCase(unittest.TestCase):
    """Путь к RAC проверяется до запуска процесса."""

    def test_missing_path(self) -> None:
        with self.assertRaises(errors.RACNotFoundError):
            validate_rac_path("/definitely/not/here/rac")

    def test_directory_is_rejected(self) -> None:
        with temp_dir() as directory, self.assertRaises(errors.RACNotFoundError):
            validate_rac_path(directory)

    def test_existing_file_is_accepted(self) -> None:
        with temp_dir() as directory:
            validate_rac_path(fake_rac(Path(directory) / "rac"))

    @unittest.skipIf(sys.platform == "win32", "бит исполнения есть только в POSIX")
    def test_non_executable_file_is_rejected(self) -> None:
        with temp_dir() as directory:
            path = Path(directory) / "rac"
            path.write_text("stub", encoding="utf-8")
            path.chmod(stat.S_IRUSR | stat.S_IWUSR)
            with self.assertRaises(errors.RACNotFoundError):
                validate_rac_path(path)


class EncodingTestCase(unittest.TestCase):
    """Кодировка вывода RAC подбирается по платформе и переопределяется."""

    def test_default_encoding_matches_platform(self) -> None:
        expected = "cp866" if sys.platform == "win32" else "utf-8"
        self.assertEqual(default_encoding(), expected)

    def test_explicit_encoding_wins(self) -> None:
        self.assertEqual(resolve_encoding("utf-16"), "utf-16")

    def test_none_means_platform_default(self) -> None:
        self.assertEqual(resolve_encoding(None), default_encoding())

    def test_session_picks_platform_encoding(self) -> None:
        session = Session(raclib.Client("rac"))
        self.assertEqual(session.encoding, default_encoding())

    def test_session_encoding_can_be_overridden(self) -> None:
        # На Linux RAC отдаёт UTF-8, на Windows — cp866; прежний жёсткий cp866
        # превращал русские ключи в мусор на Linux.
        session = Session(raclib.Client("rac"), encoding="utf-8")
        self.assertEqual(session.encoding, "utf-8")


class SessionExecTestCase(unittest.TestCase):
    """Сессия передаёт в транспорт правильные параметры."""

    def setUp(self) -> None:
        self.tempdir = temp_dir()
        self.addCleanup(self.tempdir.cleanup)
        self.rac = fake_rac(Path(self.tempdir.name) / "rac")

    def test_argv_contains_host_and_command(self) -> None:
        captured: dict[str, object] = {}

        def fake_run(rac_path, args, **kwargs):
            captured["path"] = rac_path
            captured["args"] = list(args)
            captured["kwargs"] = kwargs
            return CommandResult(0, CLUSTER_INFO, "")

        with patch("raclib.session.run_rac", fake_run):
            session = Session(raclib.Client(self.rac), host="srv", port=1545)
            result = session.exec(Command(Arg("cluster"), Arg("list")))

        self.assertEqual(captured["path"], self.rac)
        self.assertEqual(captured["args"], ["srv:1545", "cluster", "list"])
        self.assertEqual(result.to_dict()["name"], "Production")

    def test_timeout_is_forwarded(self) -> None:
        captured: dict[str, object] = {}

        def fake_run(rac_path, args, **kwargs):
            captured.update(kwargs)
            return CommandResult(0, "", "")

        with patch("raclib.session.run_rac", fake_run):
            Session(raclib.Client(self.rac), timeout=7.5).exec("cluster list")

        self.assertEqual(captured["timeout"], 7.5)

    def test_encoding_is_forwarded(self) -> None:
        captured: dict[str, object] = {}

        def fake_run(rac_path, args, **kwargs):
            captured.update(kwargs)
            return CommandResult(0, "", "")

        with patch("raclib.session.run_rac", fake_run):
            Session(raclib.Client(self.rac), encoding="utf-16").exec("cluster list")

        self.assertEqual(captured["encoding"], "utf-16")

    def test_non_zero_returncode_raises_mapped_error(self) -> None:
        def fake_run(rac_path, args, **kwargs):
            return CommandResult(1, "", "Кластер с указанным идентификатором не найден")

        with (
            patch("raclib.session.run_rac", fake_run),
            self.assertRaises(errors.ClusterNotFoundError),
        ):
            Session(raclib.Client(self.rac)).exec("cluster info")

    def test_unknown_stderr_raises_unknown_error_with_text(self) -> None:
        def fake_run(rac_path, args, **kwargs):
            return CommandResult(1, "", "Новая ошибка неизвестного вида")

        with (
            patch("raclib.session.run_rac", fake_run),
            self.assertRaises(errors.UnknownError) as context,
        ):
            Session(raclib.Client(self.rac)).exec("cluster info")

        self.assertIn("Новая ошибка", str(context.exception))

    def test_call_returns_none(self) -> None:
        with patch(
            "raclib.session.run_rac",
            lambda *a, **k: CommandResult(0, "что-то", ""),
        ):
            self.assertIsNone(Session(raclib.Client(self.rac)).call("cluster list"))

    def test_missing_binary_raises_before_running(self) -> None:
        with (
            patch("raclib.session.run_rac") as fake_run,
            self.assertRaises(errors.RACNotFoundError),
        ):
            Session(raclib.Client("/nope/rac")).exec("cluster list")
        fake_run.assert_not_called()

    def test_args_helper_accepts_string_and_command(self) -> None:
        self.assertEqual(_command_args("cluster list"), ["cluster list"])
        self.assertEqual(
            _command_args(Command(Arg("cluster"), Arg("list"))), ["cluster", "list"]
        )

    def test_creation_flags_are_hidden_by_default(self) -> None:
        flags_default = _creation_flags(new_window=False)
        if sys.platform == "win32":
            self.assertNotEqual(flags_default, 0)
        else:
            self.assertEqual(flags_default, 0)
        self.assertEqual(_creation_flags(new_window=True), 0)


class AsyncSessionExecTestCase(unittest.IsolatedAsyncioTestCase):
    """Асинхронная сессия ведёт себя так же, как синхронная."""

    def setUp(self) -> None:
        self.tempdir = temp_dir()
        self.addCleanup(self.tempdir.cleanup)
        self.rac = fake_rac(Path(self.tempdir.name) / "rac")

    async def test_exec_returns_parsed_output(self) -> None:
        async def fake_run(rac_path, args, **kwargs):
            return CommandResult(0, CLUSTER_INFO, "")

        with patch.object(async_session_module, "run_rac_async", fake_run):
            session = AsyncSession(raclib.AsyncClient(self.rac))
            output = await session.async_exec("cluster info")

        self.assertEqual(output.to_dict()["name"], "Production")

    async def test_exec_alias_matches_sync_api(self) -> None:
        async def fake_run(rac_path, args, **kwargs):
            return CommandResult(0, CLUSTER_INFO, "")

        with patch.object(async_session_module, "run_rac_async", fake_run):
            session = AsyncSession(raclib.AsyncClient(self.rac))
            self.assertIsInstance(await session.exec("cluster info"), RawOutput)

    async def test_timeout_and_encoding_are_forwarded(self) -> None:
        captured: dict[str, object] = {}

        async def fake_run(rac_path, args, **kwargs):
            captured.update(kwargs)
            return CommandResult(0, "", "")

        with patch.object(async_session_module, "run_rac_async", fake_run):
            session = AsyncSession(
                raclib.AsyncClient(self.rac), timeout=3.0, encoding="utf-8"
            )
            await session.async_exec("cluster list")

        self.assertEqual(captured["timeout"], 3.0)
        self.assertEqual(captured["encoding"], "utf-8")

    async def test_errors_are_mapped(self) -> None:
        async def fake_run(rac_path, args, **kwargs):
            return CommandResult(1, "", "Кластер с указанным идентификатором не найден")

        with (
            patch.object(async_session_module, "run_rac_async", fake_run),
            self.assertRaises(errors.ClusterNotFoundError),
        ):
            await AsyncSession(raclib.AsyncClient(self.rac)).async_exec("cluster info")

    async def test_timeout_error_is_mapped(self) -> None:
        async def fake_run(rac_path, args, **kwargs):
            raise TimeoutError

        # Проверяем именно маппинг ошибки, поэтому валидацию пути отключаем:
        # она покрыта отдельным тестом-классом PathValidationTestCase.
        with patch.object(async_session_module, "run_rac_async", fake_run), patch.object(
            async_session_module, "validate_rac_path", lambda *_: None
        ), self.assertRaises(errors.RACTimeoutError):
            await AsyncSession(
                raclib.AsyncClient(self.rac), timeout=1
            ).async_exec("cluster list")

    async def test_semaphore_limits_concurrency(self) -> None:
        active = 0
        peak = 0

        async def fake_run(rac_path, args, **kwargs):
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0.01)
            active -= 1
            return CommandResult(0, CLUSTER_INFO, "")

        with patch.object(async_session_module, "run_rac_async", fake_run):
            session = AsyncSession(raclib.AsyncClient(self.rac), max_concurrency=2)
            await asyncio.gather(*(session.async_exec("cluster info") for _ in range(8)))

        self.assertLessEqual(peak, 2, "семафор не ограничил число запусков rac")

    async def test_without_semaphore_all_run_concurrently(self) -> None:
        active = 0
        peak = 0

        async def fake_run(rac_path, args, **kwargs):
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0.01)
            active -= 1
            return CommandResult(0, CLUSTER_INFO, "")

        with patch.object(async_session_module, "run_rac_async", fake_run):
            session = AsyncSession(raclib.AsyncClient(self.rac))
            await asyncio.gather(*(session.async_exec("cluster info") for _ in range(4)))

        self.assertGreater(peak, 1)


#: Код, который «притворяется» RAC: печатает CLUSTER_INFO в UTF-8 и завершается.
PRINT_OUTPUT_CODE = (
    "import sys\n"
    f"sys.stdout.buffer.write({CLUSTER_INFO!r}.encode('utf-8'))\n"
)


class RealSubprocessTestCase(unittest.TestCase):
    """Сквозная проверка транспорта: настоящий процесс, настоящие байты.

    Вместо заглушки RAC используется сам интерпретатор Python: так тест
    проверяет реальный ``subprocess``, реальное декодирование вывода и реальный
    код возврата, не завися ни от платформы, ни от бита исполнения.
    """

    def test_decodes_utf8_output_of_real_process(self) -> None:
        result = run_rac(
            sys.executable,
            ["-c", PRINT_OUTPUT_CODE, "srv:1545", "cluster", "info"],
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, CLUSTER_INFO)
        self.assertEqual(RawOutput(result.stdout).to_dict()["name"], "Production")

    def test_decodes_cp866_output_of_real_process(self) -> None:
        # На Windows RAC печатает в cp866: проверяем именно этот путь декодирования.
        payload = "cluster : abc\nname : Тестовая\n"
        code = (
            "import sys\n"
            f"sys.stdout.buffer.write({payload!r}.encode('cp866'))\n"
        )
        result = run_rac(sys.executable, ["-c", code], encoding="cp866")
        self.assertEqual(RawOutput(result.stdout).to_dict()["name"], "Тестовая")

    def test_non_zero_returncode_is_reported(self) -> None:
        # Пишем байты напрямую: текстовый stderr использовал бы кодировку
        # консоли, а проверяем мы декодирование заданной кодировки.
        code = (
            "import sys\n"
            "sys.stderr.buffer.write('Ошибка разбора параметра'.encode('utf-8'))\n"
            "sys.exit(1)\n"
        )
        result = run_rac(sys.executable, ["-c", code], encoding="utf-8")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Ошибка", result.stderr)

    def test_timeout_is_raised_and_process_is_killed(self) -> None:
        with self.assertRaises(subprocess.TimeoutExpired):
            run_rac(sys.executable, ["-c", "import time; time.sleep(10)"], timeout=0.3)

    def test_session_maps_real_timeout_to_rac_timeout_error(self) -> None:
        # subprocess.TimeoutExpired обязан превращаться в понятную ошибку raclib.
        session = Session(raclib.Client(sys.executable), timeout=0.3)
        with patch(
            "raclib.session.run_rac",
            side_effect=subprocess.TimeoutExpired(cmd="rac", timeout=0.3),
        ), self.assertRaises(errors.RACTimeoutError) as context:
            session.exec("cluster list")
        self.assertIn("0.3", str(context.exception))


class RealSubprocessAsyncTestCase(unittest.IsolatedAsyncioTestCase):
    """Сквозная проверка асинхронного транспорта на настоящем процессе.

    На Windows ``asyncio`` создаёт каналы через именованные pipe-объекты, а
    ограниченные среды (в том числе песочница DSH) запрещают их открытие. Это
    ограничение окружения, а не библиотеки, поэтому такие тесты там
    пропускаются; на Linux и macOS они выполняются.
    """

    @unittest.skipIf(
        sys.platform == "win32",
        "asyncio на Windows требует именованных каналов, которые запрещены в ограниченной среде",
    )
    async def test_decodes_utf8_output_of_real_process(self) -> None:
        result = await run_rac_async(
            sys.executable,
            ["-c", PRINT_OUTPUT_CODE, "srv:1545", "cluster", "info"],
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(RawOutput(result.stdout).to_dict()["port"], 1541)

    @unittest.skipIf(
        sys.platform == "win32",
        "asyncio на Windows требует именованных каналов, которые запрещены в ограниченной среде",
    )
    async def test_non_zero_returncode_is_reported(self) -> None:
        code = (
            "import sys\n"
            "sys.stderr.buffer.write('Кластер с указанным идентификатором не найден'.encode('utf-8'))\n"
            "sys.exit(1)\n"
        )
        result = await run_rac_async(sys.executable, ["-c", code], encoding="utf-8")
        self.assertEqual(result.returncode, 1)
        self.assertIsInstance(errors.handler(result.stderr), errors.ClusterNotFoundError)

    @unittest.skipIf(
        sys.platform == "win32",
        "asyncio на Windows требует именованных каналов, которые запрещены в ограниченной среде",
    )
    async def test_timeout_kills_the_process(self) -> None:
        code = "import time; time.sleep(30)"
        with self.assertRaises(asyncio.TimeoutError):
            await run_rac_async(sys.executable, ["-c", code], timeout=0.3)


if __name__ == "__main__":
    unittest.main()
