"""Тесты документации и докстрингов.

Документация не должна разъезжаться с кодом. Здесь проверяется три вещи:

* у каждого публичного метода команд есть докстринг;
* докстринги в репозитории совпадают с тем, что генерирует ``add_docstrings.py``;
* страницы, директивы ``:::`` и ссылки в ``docs/`` указывают на существующие
  объекты — то же, что проверяет ``mkdocs build --strict``, но без его
  зависимостей.
"""

from __future__ import annotations

import ast
import importlib.util
import inspect
import unittest
from pathlib import Path

import raclib

from . import REPO_ROOT, temp_dir

DOCS = REPO_ROOT / "docs"
SYNC_CMD = REPO_ROOT / "src" / "raclib" / "cmd"


def load_tool(name: str):
    """Загружает скрипт из ``tools/`` как модуль."""
    path = REPO_ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"raclib_tool_{name}", path)
    if spec is None or spec.loader is None:  # pragma: no cover - защита
        raise ImportError(f"Не удалось загрузить инструмент: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DocstringCoverageTestCase(unittest.TestCase):
    """У всех методов команд должен быть докстринг."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.tool = load_tool("add_docstrings")

    def test_every_command_method_is_documented(self) -> None:
        missing: list[str] = []
        for path in sorted(SYNC_CMD.glob("*.py")):
            if path.stem == "command":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            missing.extend(
                f"{path.stem}:{node.name}"
                for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef) and ast.get_docstring(node) is None
            )

        self.assertEqual(missing, [], f"Нет докстрингов у методов: {missing}")

    def test_docstrings_match_the_generator(self) -> None:
        # Рассинхронизация означает, что кто-то правил докстринг руками
        # либо менял сигнатуру, не обновив описание параметров.
        problems: list[str] = []
        for path in sorted(SYNC_CMD.glob("*.py")):
            if path.stem == "command" or path.stem not in self.tool.DOCSTRINGS:
                continue
            generated, undocumented, missing_params = self.tool.process_module(path)
            if undocumented:
                problems.append(f"{path.stem}: нет описания {undocumented}")
            if missing_params:
                problems.append(f"{path.stem}: нет описания параметров {missing_params}")
            self.assertEqual(
                generated,
                path.read_text(encoding="utf-8"),
                f"{path.name} разошёлся с tools/add_docstrings.py. "
                "Запустите: python tools/add_docstrings.py",
            )
        self.assertEqual(problems, [], "\n".join(problems))

    def test_public_entities_have_class_docstrings(self) -> None:
        missing = [
            name
            for name in raclib.__all__
            if name not in {"errors", "command"}
            and not name.startswith("Async")
            and inspect.isclass(getattr(raclib, name, None))
            and not (getattr(raclib, name).__doc__ or "").strip()
        ]
        self.assertEqual(missing, [], f"Нет докстрингов у классов: {missing}")

    def test_generator_is_idempotent(self) -> None:
        # Регрессия: генератор дописывал по пустой строке за прогон, из-за чего
        # `--check` никогда не сходился, а файлы незаметно росли.
        #
        # Работаем с временной копией модуля: тест не должен менять исходники.
        with temp_dir() as tmp:
            for path in sorted(SYNC_CMD.glob("*.py")):
                if path.stem == "command" or path.stem not in self.tool.DOCSTRINGS:
                    continue
                with self.subTest(module=path.name):
                    # Копию создаём без расширения: генератор определяет модуль
                    # по path.stem и по нему ищет таблицу докстрингов.
                    copy = Path(tmp.name) / path.stem
                    copy.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
                    once, _, _ = self.tool.process_module(copy)
                    copy.write_text(once, encoding="utf-8")
                    twice, _, _ = self.tool.process_module(copy)
                    self.assertEqual(
                        once,
                        twice,
                        f"{path.name}: повторный прогон генератора меняет файл",
                    )

    def test_every_command_method_has_return_annotation(self) -> None:
        # Без аннотации mkdocstrings (griffe) ругается на секцию Returns,
        # а `mkdocs build --strict` падает на предупреждениях.
        missing: list[str] = []
        for path in sorted(SYNC_CMD.glob("*.py")):
            if path.stem == "command":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            missing.extend(
                f"{path.stem}:{node.name}"
                for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef) and node.returns is None
            )
        self.assertEqual(missing, [], f"Нет аннотации возврата: {missing}")

    def test_future_annotations_are_first(self) -> None:
        # В классах есть методы с именами `list` и `dict`, затеняющие встроенные
        # типы: без отложенных аннотаций `-> list[RacRecord]` падает с TypeError.
        # Проверяем только модули, где такая аннотация реально есть.
        checked = 0
        for path in sorted(SYNC_CMD.glob("*.py")):
            text = path.read_text(encoding="utf-8")
            if "RacRecord" not in text:
                continue
            checked += 1
            with self.subTest(module=path.name):
                self.assertIn("from __future__ import annotations", text)
                first_import = next(
                    line
                    for line in text.split("\n")
                    if line.startswith(("import ", "from "))
                )
                self.assertEqual(first_import, "from __future__ import annotations")
        self.assertGreater(checked, 0, "ни один модуль не использует RacRecord")


class DocumentationIntegrityTestCase(unittest.TestCase):
    """Документация ссылается только на существующие страницы и объекты."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.tool = load_tool("check_docs")

    def test_nav_pages_exist(self) -> None:
        self.assertEqual(self.tool.check_nav(), [])

    def test_directives_resolve_to_real_objects(self) -> None:
        problems, total = self.tool.check_directives()
        self.assertGreater(total, 0, "в справочнике нет ни одной директивы :::")
        self.assertEqual(problems, [])

    def test_relative_links_exist(self) -> None:
        problems, _ = self.tool.check_links()
        self.assertEqual(problems, [])

    def test_removed_pdoc_artifacts_are_gone(self) -> None:
        # Раньше в репозитории лежало 4.4 МБ сгенерированного pdoc HTML.
        for stale in ("index.html", "raclib.html", "search.js"):
            with self.subTest(file=stale):
                self.assertFalse(
                    (DOCS / stale).exists(),
                    f"{stale} — артефакт старой сборки, его не должно быть в git",
                )

    def test_site_output_is_ignored(self) -> None:
        ignored = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("site/", ignored, "сборка MkDocs не должна попадать в git")


if __name__ == "__main__":
    unittest.main()
