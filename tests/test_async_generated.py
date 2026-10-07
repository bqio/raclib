"""Проверки сгенерированной асинхронной ветки на исполнимость.

Здесь ловится ошибка, которую не видел тест паритета сигнатур: ``await``
применялся только к ``session.async_exec``, а пост-обработка
(``.to_list()``, ``.to_dict()``, ``.to_str()``) вызывалась у корутины. Код
импортировался, сигнатуры совпадали, но **ни один** метод не работал:
пользователь получал ``AttributeError: 'coroutine' object has no attribute
'to_list'``.

Поэтому проверки ниже действительно вызывают методы команд на подменённом
транспорте и сравнивают результат.
"""

from __future__ import annotations

import re
import unittest
from unittest.mock import patch

from raclib._shared import CommandResult
from raclib.asynchronous import AsyncClient, AsyncCluster, AsyncInfobase, AsyncService
from raclib.asynchronous import session as async_session_module
from raclib.asynchronous.session import AsyncSession

from . import CLUSTER_INFO, CLUSTER_LIST, REPO_ROOT

ASYNC_CMD = REPO_ROOT / "src" / "raclib" / "asynchronous" / "cmd"


def _session_with(stdout: str, returncode: int = 0):
    """Сессия с подменённым транспортом, без обращения к реальному `rac`.

    Проверка пути тоже отключается: тест проверяет генерацию команд, а не
    наличие исполняемого файла на машине.
    """

    async def fake_run(rac_path, args, **kwargs):
        return CommandResult(returncode, stdout, "")

    return (
        patch.object(async_session_module, "run_rac_async", fake_run),
        patch.object(async_session_module, "validate_rac_path", lambda *_: None),
    )


def make_session() -> AsyncSession:
    """Настоящая асинхронная сессия; транспорт в тестах подменяется."""
    return AsyncSession(AsyncClient("rac"), timeout=30)


class GeneratedTreeCallsTestCase(unittest.IsolatedAsyncioTestCase):
    """Методы команд действительно возвращают разобранные данные."""

    async def test_list_returns_records(self) -> None:
        transport, validation = _session_with(CLUSTER_LIST)
        with transport, validation:
            records = await AsyncCluster.list(make_session())

        # Главное: это список словарей, а не корутина и не исключение.
        self.assertIsInstance(records, list)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["name"], "Production")

    async def test_info_returns_dict(self) -> None:
        transport, validation = _session_with(CLUSTER_INFO)
        with transport, validation:
            record = await AsyncCluster.info(make_session(), "cl-1")

        self.assertIsInstance(record, dict)
        self.assertEqual(record["port"], 1541)

    async def test_create_style_method_returns_identifier(self) -> None:
        # Форма `result = session.exec(...)`: метод возвращает строку с UUID.
        transport, validation = _session_with("infobase : ib-42\n")
        with transport, validation:
            identifier = await AsyncInfobase.create(
                make_session(), "cl-1", "Test", "PostgreSQL", "db", "TestIB", "ru_RU"
            )

        self.assertEqual(identifier, "ib-42")

    async def test_call_style_method_returns_none(self) -> None:
        # Форма без пост-обработки: `session.call(...)` ничего не возвращает.
        transport, validation = _session_with("")
        with transport, validation:
            self.assertIsNone(await AsyncCluster.remove(make_session(), "cl-1"))

    async def test_empty_output_gives_empty_list(self) -> None:
        # Пустой ответ RAC — это пустой список, а не ошибка.
        transport, validation = _session_with("")
        with transport, validation:
            self.assertEqual(await AsyncService.list(make_session(), "cl-1"), [])


class GeneratedTreeAwaitTestCase(unittest.TestCase):
    """Статические проверки: ``await`` стоит там, где нужно."""

    def test_every_session_call_is_awaited(self) -> None:
        unawaited: list[str] = []
        total = 0
        for path in sorted(ASYNC_CMD.glob("*.py")):
            text = path.read_text(encoding="utf-8")
            for match in re.finditer(r"session\.(async_exec|async_call)\(", text):
                total += 1
                before = text[max(0, match.start() - 30) : match.start()]
                if "await" not in before:
                    unawaited.append(f"{path.name}:{text[:match.start()].count(chr(10)) + 1}")
        self.assertGreater(total, 0, "в асинхронном дереве нет обращений к сессии")
        self.assertEqual(unawaited, [], f"Обращения без await: {unawaited}")

    def test_await_wraps_whole_call_not_coroutine(self) -> None:
        # Ошибка выглядела так: `await session.async_exec(...).to_list()` —
        # `.to_list()` вызывался у корутины. Правильно: `(await ...).to_list()`.
        wrong = re.compile(r"await session\.async_\w+\([^)]*\)\s*\.\s*to_")
        problems: list[str] = []
        for path in sorted(ASYNC_CMD.glob("*.py")):
            text = path.read_text(encoding="utf-8")
            for match in wrong.finditer(text):
                problems.append(f"{path.name}: {match.group(0)[:60]}")
        self.assertEqual(problems, [], f"await применён к корутине: {problems}")

    def test_async_tree_is_syntactically_valid(self) -> None:
        for path in sorted(ASYNC_CMD.glob("*.py")):
            with self.subTest(module=path.name):
                compile(path.read_text(encoding="utf-8"), str(path), "exec")


class GeneratorPreservesFormattingTestCase(unittest.TestCase):
    """Генератор не должен схлопывать многострочные вызовы в одну строку."""

    def test_command_calls_stay_multiline(self) -> None:
        # `ast.unparse` собирал весь вызов Command(...) в одну строку — код
        # становился нечитаемым. Проверяем, что многострочность сохранилась.
        text = (ASYNC_CMD / "cluster.py").read_text(encoding="utf-8")
        start = text.find("async def list(session: AsyncSession)")
        self.assertGreater(start, 0)
        # Отступаем past докстринг: он тоже содержит текст, но не вызовы.
        body = text[text.find("(await session.async_exec(", start) :][:400]
        self.assertIn("Command(\n", body, "вызов Command схлопнут в одну строку")
        self.assertIn('Arg("cluster"),', body)
        self.assertIn('.to_list()', body)

    def test_generator_is_idempotent(self) -> None:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "raclib_gen_idem", REPO_ROOT / "tools" / "generate_async.py"
        )
        assert spec and spec.loader
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)

        first = generator.generate()
        second = generator.generate()
        self.assertEqual(first, second)

    def test_transformer_handles_three_call_shapes(self) -> None:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "raclib_gen_shapes", REPO_ROOT / "tools" / "generate_async.py"
        )
        assert spec and spec.loader
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)

        source = (
            "def a(session, x):\n"
            "    return session.exec(Command(Arg('x'))).to_list()\n"
            "\n"
            "def b(session, x):\n"
            "    result = session.exec(Command(Arg('x'))).to_dict()\n"
            "    return str(result['x'])\n"
            "\n"
            "def c(session, x):\n"
            "    session.call(Command(Arg('x')))\n"
        )
        converted = generator.add_await_to_session_calls(source)
        self.assertIn("(await session.async_exec(", converted)
        # Ошибочной формы быть не должно: `.to_list()` вызывался бы у корутины.
        self.assertNotIn("await session.async_exec(Command(Arg('x'))).to_list()", converted)
        # Проверяем, что получается синтаксически валидный модуль: заголовки
        # функций делает следующий шаг генератора.
        generated = generator.make_functions_async(converted)
        compile(generated, "<generated>", "exec")


if __name__ == "__main__":
    unittest.main()
