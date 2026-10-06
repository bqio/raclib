"""Тесты генератора асинхронной ветки.

Главная проверка: асинхронное дерево в репозитории обязано совпадать с тем,
что генерируется из синхронных исходников. Если кто-то поправит асинхронный
файл руками, тест это покажет — именно так раньше и разошлись регексы разбора
вывода, из-за чего на Linux асинхронный ``to_list()`` возвращал пустой список.
"""

from __future__ import annotations

import importlib.util
import inspect
import unittest

import raclib
import raclib.asynchronous as async_package

from . import REPO_ROOT

GENERATOR_PATH = REPO_ROOT / "tools" / "generate_async.py"


def load_generator():
    """Загружает ``tools/generate_async.py`` как модуль."""
    spec = importlib.util.spec_from_file_location("raclib_generate_async", GENERATOR_PATH)
    if spec is None or spec.loader is None:  # pragma: no cover - защита
        raise ImportError(f"Не удалось загрузить генератор: {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AsyncTreeIsGeneratedTestCase(unittest.TestCase):
    """Асинхронное дерево не должно расходиться с генератором."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator()

    def test_repository_tree_matches_generator_output(self) -> None:
        problems = self.generator.check(self.generator.generate())
        self.assertEqual(
            problems,
            [],
            "Асинхронное дерево разошлось с синхронными исходниками. "
            "Запустите: python tools/generate_async.py\n" + "\n".join(problems),
        )

    def test_generator_is_idempotent(self) -> None:
        # Повторный прогон не должен ничего менять: генерация детерминирована.
        first = self.generator.generate()
        second = self.generator.generate()
        self.assertEqual(first, second)

    def test_regeneration_produces_identical_content(self) -> None:
        # Прогон через временную копию дерева даёт тот же результат.
        files = self.generator.generate()
        for path, content in files.items():
            with self.subTest(path=str(path.relative_to(REPO_ROOT))):
                self.assertEqual(path.read_text(encoding="utf-8"), content)

    def test_no_generated_module_lost_its_sync_source(self) -> None:
        cmd_dir = REPO_ROOT / "src" / "raclib" / "asynchronous" / "cmd"
        sync_dir = REPO_ROOT / "src" / "raclib" / "cmd"
        for async_module in sorted(cmd_dir.glob("*.py")):
            if async_module.name == "__init__.py":
                continue
            with self.subTest(module=async_module.name):
                self.assertTrue(
                    (sync_dir / async_module.name).exists(),
                    f"{async_module.name} сгенерирован, но синхронного источника нет",
                )

    def test_transport_modules_are_marked_hand_written(self) -> None:
        # Транспорт отличается по существу (asyncio vs subprocess) и не генерируется.
        self.assertIn("_transport.py", self.generator.HAND_WRITTEN)
        self.assertIn("session.py", self.generator.HAND_WRITTEN)
        self.assertIn("client.py", self.generator.HAND_WRITTEN)


class SyncAsyncParityTestCase(unittest.TestCase):
    """Публичный API обеих веток должен совпадать по составу."""

    #: Имена, которые сознательно отличаются или ведут себя иначе.
    KNOWN_DIFFERENCES = {"AsyncSession": {"exec", "call", "async_exec", "async_call"}}

    #: Общие для обеих веток сущности: дублировать их под именем Async* не нужно.
    SHARED_NAMES = {"RawOutput", "RACNotFoundError", "RACTimeoutError", "Client"}

    def test_every_sync_entity_has_async_twin(self) -> None:
        for name in raclib.__all__:
            if name in {"errors", "command"} or name.startswith("Async"):
                continue
            if name in self.SHARED_NAMES:
                continue
            sync_object = getattr(raclib, name, None)
            if sync_object is None or not inspect.isclass(sync_object):
                continue
            with self.subTest(entity=name):
                self.assertTrue(
                    hasattr(async_package, f"Async{name}"),
                    f"у {name} нет асинхронного двойника Async{name}",
                )

    def test_method_sets_match(self) -> None:
        for name in raclib.__all__:
            if name in {"errors", "command"} or name.startswith("Async"):
                continue
            if name in self.SHARED_NAMES:
                continue
            sync_object = getattr(raclib, name, None)
            async_object = getattr(async_package, f"Async{name}", None)
            if not (
                sync_object
                and async_object
                and inspect.isclass(sync_object)
                and inspect.isclass(async_object)
            ):
                continue
            sync_methods = {
                key
                for key, value in vars(sync_object).items()
                if not key.startswith("_") and callable(value)
            }
            async_methods = {
                key
                for key, value in vars(async_object).items()
                if not key.startswith("_") and callable(value)
            }
            allowed = self.KNOWN_DIFFERENCES.get(f"Async{name}", set())
            with self.subTest(entity=name):
                self.assertEqual(
                    sync_methods - async_methods - allowed,
                    set(),
                    f"{name}: методы отсутствуют в асинхронной ветке",
                )
                self.assertEqual(
                    async_methods - sync_methods - allowed,
                    set(),
                    f"{name}: лишние методы в асинхронной ветке",
                )

    def test_command_signatures_match(self) -> None:
        for name in raclib.__all__:
            if name in {"errors", "command"} or name.startswith("Async"):
                continue
            if name in self.SHARED_NAMES:
                continue
            sync_object = getattr(raclib, name, None)
            async_object = getattr(async_package, f"Async{name}", None)
            if not (
                sync_object
                and async_object
                and inspect.isclass(sync_object)
                and inspect.isclass(async_object)
            ):
                continue
            for method in dir(sync_object):
                if method.startswith("_") or not callable(getattr(sync_object, method)):
                    continue
                if not hasattr(async_object, method):
                    continue
                with self.subTest(entity=name, method=method):
                    self.assertEqual(
                        list(inspect.signature(getattr(sync_object, method)).parameters),
                        list(inspect.signature(getattr(async_object, method)).parameters),
                        f"{name}.{method}: сигнатуры разошлись",
                    )

    def test_nested_classes_keep_their_names(self) -> None:
        # Вложенные классы адресуются через внешний, поэтому переименовывать
        # их нельзя: AsyncCluster.Admin, AsyncInfobase.Summary.
        self.assertTrue(hasattr(async_package.AsyncCluster, "Admin"))
        self.assertTrue(hasattr(async_package.AsyncInfobase, "Summary"))
        self.assertTrue(hasattr(async_package.AsyncProfile, "ACL"))

    def test_shared_primitives_are_the_same_objects(self) -> None:
        # RawOutput и Client не дублируются: у обеих веток один класс.
        from raclib._shared import Client, RawOutput

        self.assertIs(raclib.RawOutput, RawOutput)
        self.assertIs(async_package.RawOutput, RawOutput)
        self.assertIs(raclib.Client, Client)
        self.assertIs(async_package.AsyncClient, Client)


if __name__ == "__main__":
    unittest.main()
