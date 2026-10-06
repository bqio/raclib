#!/usr/bin/env python3
"""Генерация асинхронной ветки raclib из синхронной.

Асинхронное дерево ``src/raclib/asynchronous/`` **не редактируется вручную**.
Единственный источник правды для команд — ``src/raclib/cmd/``. Скрипт читает
синхронные модули, механически переписывает их в ``async``-вариант и пишет
результат в асинхронное дерево.

Зачем: до этого деревья существовали как две ручные копии. Они уже разошлись —
в частности, регекс разбора вывода в асинхронной ветке отличался от
синхронного и на Linux-выводе молча возвращал пустой список. Генерация делает
такое расхождение невозможным.

Использование::

    python tools/generate_async.py            # записать файлы
    python tools/generate_async.py --check    # проверить, что дерево актуально

``--check`` возвращает код 1 и печатает список расхождений; этот режим
используется в CI и в тестах.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "src" / "raclib"
SYNC_CMD = SRC / "cmd"
ASYNC_DIR = SRC / "asynchronous"

#: Русский текст в сообщениях скрипта: гарантируем UTF-8 на любой консоли.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

#: Файлы, которые генерируются из синхронного дерева команд.
GENERATED_COMMAND_MODULES = ("agent", "bindatastorage", "cluster", "connection",
                             "counter", "infobase", "limit", "lock", "manager",
                             "process", "profile", "rule", "server", "service",
                             "servicesetting", "session")

#: Файлы, которые поддерживаются вручную. Генератор их не трогает и не удаляет.
HAND_WRITTEN = {
    "__init__.py",
    "_transport.py",
    "client.py",
    "errors.py",
    "session.py",
}

#: Виды импортов, которые нужно переписать на асинхронные модули.
#: Синхронные командные модули импортируют ``Session`` (класс из
#: ``raclib/session.py``), а в асинхронной ветке этот класс называется
#: ``AsyncSession``, поэтому одной заменой пути не обойтись.
IMPORT_REWRITES = (
    ("from .command import", "from ...cmd.command import"),
    ("from ...cmd.command import", "from ...cmd.command import"),
    ("from ..cmd.command import", "from ...cmd.command import"),
    ("from ..utils import", "from ...utils import"),
    ("from .._shared import", "from ..._shared import"),
    ("from ..session import Session", "from ..session import AsyncSession"),
    ("from ...session import Session", "from ...session import AsyncSession"),
)


def strip_specials(source: str) -> str:
    """Убирает из синхронного модуля то, что асинхронной ветке не нужно."""
    # `raise errors.handler(x) from None` в async-сессии не встречается.
    source = re.sub(r"\s*from None\b", "", source)
    return source


def rewrite_imports(source: str) -> str:
    """Перенаправляет импорты на общие (``_shared``) и асинхронные модули."""
    for old, new in IMPORT_REWRITES:
        source = source.replace(old, new)
    return source


def add_await_to_session_calls(source: str) -> str:
    """``session.exec(...)`` → ``await session.async_exec(...)``.

    Синхронный код во всех командах построен по шаблону
    ``return session.exec(...).to_list()``. В асинхронной ветке вызов нужно
    дождаться, поэтому ``await`` ставится непосредственно перед вызовом, а
    ``.to_dict()``/``.to_list()``/``.to_str()`` продолжают работать поверх
    дождавшегося объекта.
    """
    source = re.sub(r"(?<![\w.])session\.exec\(", "await session.async_exec(", source)
    source = re.sub(r"(?<![\w.])session\.call\(", "await session.async_call(", source)
    return source


def make_functions_async(source: str) -> str:
    """Превращает ``def`` / ``return`` с ``await`` в асинхронные.

    Порядок важен: сначала добавляются ``await``, затем ``def`` становится
    ``async def``, и только потом в ``return`` подставляется ``await`` — но
    только там, где ожидание ещё не проставлено.
    """
    source = re.sub(r"(?<![\w.])def ", "async def ", source)
    source = re.sub(
        r"(?m)^([ \t]*)return (?!await\b)(?=.*\bawait\b)",
        r"\1return await ",
        source,
    )
    return source


def rename_async_identifiers(source: str) -> str:
    """Переименовывает определения **верхнеуровневых** классов и аннотации типов.

    Вложенные классы (``Cluster.Admin``, ``Infobase.Summary``,
    ``Infobase.Denied``) намеренно не переименовываются: они адресуются по
    имени через внешний класс, и вложенный ``AsyncAdmin`` сломал бы
    ``AsyncCluster.Admin``. Поэтому шаблон требует, чтобы ``class`` начинался с
    нулевой колонки и был отделён пустой строкой.
    """
    source = re.sub(
        r"(?m)^class (?!Async)([A-Za-z_][A-Za-z0-9_]*)",
        r"class Async\1",
        source,
        count=1,
    )
    # Аннотации типов сессии и клиента внутри командных модулей.
    source = re.sub(r":\s*Session\b", ": AsyncSession", source)
    source = re.sub(r":\s*Client\b", ": AsyncClient", source)
    return source


def transform_command_module(name: str, source: str) -> str:
    """Преобразует синхронный командный модуль в асинхронный."""
    source = strip_specials(source)
    source = rewrite_imports(source)
    source = add_await_to_session_calls(source)
    source = make_functions_async(source)
    source = rename_async_identifiers(source)
    return sort_import_block(source)


def sort_imported_names(line: str) -> str:
    """Сортирует имена внутри ``from X import a, b``.

    ruff (isort) требует алфавитный порядок имён; синхронный источник написан
    как ``Command, Arg``, поэтому при генерации порядок нужно привести к норме.
    Имена с ``as`` (``Client as AsyncClient``) не трогаем: их порядок задан
    смыслом.
    """
    if " import " not in line or " as " in line or "(" in line:
        return line
    head, _, names = line.partition(" import ")
    if "," not in names:
        return line
    ordered = ", ".join(sorted(part.strip() for part in names.split(",")))
    return f"{head} import {ordered}"


def sort_import_block(source: str) -> str:
    """Сортирует импорты так, как этого требует ruff (правило I001).

    Синхронные модули уже отсортированы, но при переписывании путей ``from ..x``
    превращается в ``from ...x`` и порядок ломается. Сортировка здесь, а не
    запуском ``ruff --fix``, нужна потому, что файл генерируется: иначе
    расхождение возвращалось бы после каждой перегенерации.

    ruff (isort) ставит ``from``-импорты по возрастанию глубины: ``..session``
    идёт раньше, чем ``...cmd.command``.
    """
    lines = source.split("\n")

    # Находим непрерывный блок импортов в начале модуля.
    start = 0
    while start < len(lines) and not lines[start].startswith(("import ", "from ")):
        start += 1
    end = start
    while end < len(lines) and (
        lines[end].startswith(("import ", "from ")) or not lines[end].strip()
    ):
        end += 1

    block = [sort_imported_names(line) for line in lines[start:end] if line.strip()]
    if len(block) < 2:
        return source

    def sort_key(line: str) -> tuple[int, int, str]:
        if line.startswith("import "):
            # Плоские `import x` идут после `from __future__` и сортируются по имени.
            return (1, 0, line)
        after_from = line.split(" ", 1)[1]
        if after_from.startswith("__future__"):
            # `from __future__` обязан стоять в самом начале файла: иначе Python
            # падает с SyntaxError, а не просто меняет порядок импортов.
            return (0, 0, "")
        depth = len(after_from) - len(after_from.lstrip("."))
        if depth:
            # Относительные импорты: ruff ставит более глубокие раньше.
            return (2, -depth, line)
        # Абсолютные импорты идут после относительных.
        return (3, 0, line)

    ordered = sorted(block, key=sort_key)
    if any(line.startswith("from __future__") for line in ordered):
        # ruff отделяет `from __future__` пустой строкой от остальных импортов.
        index = max(i for i, line in enumerate(ordered) if line.startswith("from __future__"))
        ordered.insert(index + 1, "")

    # Сохраняем ровно столько пустых строк после последнего импорта, сколько
    # было: пустая строка между `from __future__` и остальными импортами
    # хвостовой не является, и при подсчёте «всех пустых» блок каждый прогон рос.
    trailing = 0
    for line in reversed(lines[start:end]):
        if line.strip():
            break
        trailing += 1
    return "\n".join(
        [*lines[:start], *ordered, *([""] * max(trailing, 1)), *lines[end:]]
    )


def transform_client_module(source: str) -> str:
    """``client.py``: тонкий реэкспорт общего класса."""
    return (
        '"""Асинхронный двойник :class:`raclib.client.Client`.\n'
        "\n"
        "Класс общий для обеих веток и объявлен в :mod:`raclib._shared`; здесь\n"
        "оставлен реэкспорт под именем ``AsyncClient`` для единообразия API.\n"
        '"""\n'
        "\n"
        "from .._shared import Client as AsyncClient\n"
        "\n"
        '__all__ = ["AsyncClient"]\n'
    )


def transform_session_module(source: str) -> str:
    """``session.py``: асинхронная сессия на базе ``asyncio``.

    Тело подставляется целиком: запуск процесса и ``await`` не сводятся к
    механическим заменам, а вся остальная логика (валидация пути, кодировка,
    таймаут, разбор ошибок) общая с синхронной веткой через ``_shared``.
    """
    return (
        '"""Асинхронная ветка: сессия администрирования на базе ``asyncio``.\n'
        "\n"
        "Файл сгенерирован из ``src/raclib/session.py`` скриптом\n"
        "``tools/generate_async.py``. Правки вносите в синхронную ветку.\n"
        '"""\n'
        "\n"
        "from __future__ import annotations\n"
        "\n"
        "import asyncio\n"
        "\n"
        "from .. import errors\n"
        "from .._shared import (\n"
        "    Client,\n"
        "    CommandResult,\n"
        "    RACInvocationError,\n"
        "    RawOutput,\n"
        "    resolve_encoding,\n"
        "    validate_rac_path,\n"
        ")\n"
        "from ..cmd.command import Command\n"
        "from ._transport import run_rac_async\n"
        "\n"
        '__all__ = ["AsyncSession"]\n'
        "\n"
        "\n"
        "class AsyncSession:\n"
        '    """Асинхронная сессия администрирования.\n'
        "\n"
        "    :param max_concurrency: предел одновременных запусков ``rac`` в рамках\n"
        "        одной сессии. ``None`` — без ограничения. Без него ``asyncio.gather``\n"
        "        по сотням кластеров порождает столько же процессов ``rac``.\n"
        "    Остальные параметры совпадают с :class:`raclib.session.Session`.\n"
        '    """\n'
        "\n"
        "    def __init__(\n"
        "        self,\n"
        "        client: Client,\n"
        '        host: str = "localhost",\n'
        "        port: int = 1545,\n"
        "        timeout: float | None = None,\n"
        "        encoding: str | None = None,\n"
        "        max_concurrency: int | None = None,\n"
        "        debug: bool = False,\n"
        "    ):\n"
        '        """Создаёт сессию; параметры совпадают с синхронной веткой."""\n'
        "        self.client = client\n"
        "        self.host = host\n"
        "        self.port = port\n"
        "        self.timeout = timeout\n"
        "        self.encoding = resolve_encoding(encoding)\n"
        "        self.max_concurrency = max_concurrency\n"
        "        self.debug = debug\n"
        "        self._semaphore: asyncio.Semaphore | None = (\n"
        "            asyncio.Semaphore(max_concurrency) if max_concurrency else None\n"
        "        )\n"
        "\n"
        "    async def async_exec(self, command: Command | str) -> RawOutput:\n"
        '        """Выполняет команду RAC и возвращает её вывод."""\n'
        "        return RawOutput((await self._execute(command)).stdout)\n"
        "\n"
        "    async def async_call(self, command: Command | str) -> None:\n"
        '        """Выполняет команду, отбрасывая вывод."""\n'
        "        await self._execute(command)\n"
        "\n"
        "    #: Псевдонимы, чтобы набор методов совпадал с\n"
        "    #: :class:`raclib.session.Session` (там они называются ``exec``/``call``).\n"
        "    exec = async_exec\n"
        "    call = async_call\n"
        "\n"
        "    async def _execute(self, command: Command | str) -> CommandResult:\n"
        "        validate_rac_path(self.client.rac_path)\n"
        '        args = [f"{self.host}:{self.port}", *_command_args(command)]\n'
        "        if self.debug:\n"
        '            print("[DEBUG]", args)\n'
        "        try:\n"
        "            if self._semaphore is None:\n"
        "                result = await self._invoke(args)\n"
        "            else:\n"
        "                async with self._semaphore:\n"
        "                    result = await self._invoke(args)\n"
        "        except TimeoutError:\n"
        "            # Важно: этот блок обязан идти раньше OSError. В Python 3.11+\n"
        "            # TimeoutError наследуется от OSError (asyncio.TimeoutError —\n"
        "            # его псевдоним), и иначе перехватился бы общий блок.\n"
        "            raise errors.RACTimeoutError(self.timeout or 0) from None\n"
        "        except FileNotFoundError as exc:\n"
        "            raise RACInvocationError(\n"
        '                f"Не удалось запустить RAC по пути {self.client.rac_path}: {exc}"\n'
        "            ) from exc\n"
        "        except OSError as exc:\n"
        "            raise RACInvocationError(\n"
        '                f"Не удалось запустить RAC по пути {self.client.rac_path}: {exc}"\n'
        "            ) from exc\n"
        "        if result.returncode != 0:\n"
        "            if self.debug:\n"
        '                print("[DEBUG]", result.stderr)\n'
        "            raise errors.handler(result.stderr) from None\n"
        "        if self.debug:\n"
        "            print(result.stdout)\n"
        "        return result\n"
        "\n"
        "    async def _invoke(self, args: list[str]) -> CommandResult:\n"
        "        return await run_rac_async(\n"
        "            self.client.rac_path,\n"
        "            args,\n"
        "            timeout=self.timeout,\n"
        "            encoding=self.encoding,\n"
        "        )\n"
        "\n"
        "\n"
        "def _command_args(command: Command | str) -> list[str]:\n"
        "    if isinstance(command, Command):\n"
        "        return command.args\n"
        "    return [str(command)]\n"
    )


def generate() -> dict[Path, str]:
    """Возвращает карту «путь → содержимое» для всего асинхронного дерева."""
    files: dict[Path, str] = {}

    for name in GENERATED_COMMAND_MODULES:
        path = SYNC_CMD / f"{name}.py"
        if not path.exists():  # pragma: no cover - защита от опечатки в списке
            raise FileNotFoundError(f"Нет синхронного модуля для генерации: {path}")
        files[ASYNC_DIR / "cmd" / f"{name}.py"] = transform_command_module(
            name, path.read_text(encoding="utf-8")
        )

    files[ASYNC_DIR / "cmd" / "__init__.py"] = ""
    files[ASYNC_DIR / "client.py"] = transform_client_module("")
    files[ASYNC_DIR / "session.py"] = transform_session_module("")
    return files


def write(files: dict[Path, str]) -> None:
    """Записывает файлы на диск и удаляет устаревшие сгенерированные модули."""
    expected = set(files)
    cmd_dir = ASYNC_DIR / "cmd"
    if cmd_dir.exists():
        for existing in cmd_dir.glob("*.py"):
            if existing not in expected and existing.name not in HAND_WRITTEN:
                print(f"удаляю устаревший модуль: {existing.relative_to(REPO_ROOT)}")
                existing.unlink()

    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            path.write_text(content, encoding="utf-8")
            print(f"обновлён: {path.relative_to(REPO_ROOT)}")


def check(files: dict[Path, str]) -> list[str]:
    """Возвращает список расхождений между деревом и результатом генерации."""
    problems: list[str] = []
    for path, content in files.items():
        relative = path.relative_to(REPO_ROOT)
        if not path.exists():
            problems.append(f"отсутствует: {relative}")
            continue
        if path.read_text(encoding="utf-8") != content:
            problems.append(f"расходится с генератором: {relative}")

    expected = set(files)
    cmd_dir = ASYNC_DIR / "cmd"
    if cmd_dir.exists():
        for existing in sorted(cmd_dir.glob("*.py")):
            if existing not in expected and existing.name not in HAND_WRITTEN:
                problems.append(
                    f"лишний модуль (нет синхронного источника): "
                    f"{existing.relative_to(REPO_ROOT)}"
                )
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="только проверить актуальность асинхронного дерева",
    )
    args = parser.parse_args(argv)

    files = generate()
    if args.check:
        problems = check(files)
        if problems:
            print("Асинхронное дерево устарело:", file=sys.stderr)
            for problem in problems:
                print(f"  - {problem}", file=sys.stderr)
            print(
                "\nЗапустите: python tools/generate_async.py",
                file=sys.stderr,
            )
            return 1
        print(f"Асинхронное дерево актуально ({len(files)} файлов).")
        return 0

    write(files)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
