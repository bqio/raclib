#!/usr/bin/env python3
"""Сверяет параметры команд raclib с реальной справкой ``rac``.

Инструмент запускается там, где есть ``rac`` (обычно машина администратора), и
находит два класса ошибок, которые не видны ни тестам, ни сборке:

* **опечатки в именах параметров** — RAC молча игнорирует неизвестный параметр,
  поэтому команда уходит без нужной настройки. Так был найден
  ``--safe-working-processess-memory-limit`` вместо ``...processes...``;
* **параметры, которых у команды нет** — например, ``--db-user`` у
  ``rac infobase drop``: RAC принимает учётные данные только у ``create`` и
  ``update``.

Проверяется каждый метод командного дерева: набор ``--флагов``, который собирает
метод, сравнивается с описанием соответствующей команды в ``rac help``.

Использование::

    python tools/audit_rac_help.py                       # найти rac автоматически
    python tools/audit_rac_help.py --rac "C:\\...\\rac.exe"
    python tools/audit_rac_help.py --check               # код 1 при расхождениях

Если ``rac`` не найден, инструмент сообщает об этом и завершается с кодом 2:
это не ошибка библиотеки, а отсутствие утилиты на машине.
"""

from __future__ import annotations

import argparse
import ast
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SYNC_CMD = REPO_ROOT / "src" / "raclib" / "cmd"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

#: Режим ``rac`` для каждого командного модуля (первый аргумент команды).
MODULE_MODES = {
    "agent": "agent",
    "bindatastorage": "binary-data-storage",
    "cluster": "cluster",
    "connection": "connection",
    "counter": "counter",
    "infobase": "infobase",
    "limit": "limit",
    "lock": "lock",
    "manager": "manager",
    "process": "process",
    "profile": "profile",
    "rule": "rule",
    "server": "server",
    "service": "service",
    "servicesetting": "service-setting",
    "session": "session",
}

#: Флаги, которые RAC принимает у любой команды и которых нет в описании режима.
COMMON_FLAGS = {"--cluster", "--cluster-user", "--cluster-pwd"}


def find_rac(explicit: str | None) -> Path | None:
    """Ищет исполняемый файл ``rac``."""
    if explicit:
        path = Path(explicit)
        return path if path.exists() else None
    found = shutil.which("rac") or shutil.which("rac.exe")
    if found:
        return Path(found)
    # Типовые каталоги установки 1С.
    for root in (r"C:\Program Files\1cv8", r"C:\Program Files (x86)\1cv8"):
        base = Path(root)
        if not base.is_dir():
            continue
        for version in sorted(base.iterdir(), reverse=True):
            candidate = version / "bin" / "rac.exe"
            if candidate.exists():
                return candidate
    return None


def run_help(rac: Path, *args: str) -> str:
    """Возвращает вывод ``rac help ...`` в виде текста."""
    completed = subprocess.run(
        [str(rac), "help", *args],
        capture_output=True,
        timeout=30,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    return completed.stdout.decode("cp866", errors="replace")


#: Ключ для параметров, объявленных на уровне режима, а не отдельной команды.
MODE_LEVEL = "__mode__"


def flags_by_command(help_output: str, mode: str) -> dict[str, set[str]]:
    """Разбирает справку режима: имя команды → набор её флагов.

    В справке три части: «Общие параметры», «Параметры» (общие для режима) и
    «Команды». У ``binary-data-storage`` в параметрах режима лежат
    ``--infobase``, у ``service-setting`` — ``--server``, поэтому параметры
    режима запоминаются отдельно и при проверке объединяются с параметрами
    команды.

    Разбор идёт по секциям: имя команды — это первое слово в строке внутри
    секции «Команды», а не любой заголовок (иначе «Команды:» тоже считалось
    именем команды и параметры режима пропадали).
    """
    result: dict[str, set[str]] = {MODE_LEVEL: set()}
    current = MODE_LEVEL
    in_commands = False

    for line in help_output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        indent = len(line) - len(line.lstrip())

        if indent == 0:
            # Заголовок секции: переключаем контекст.
            in_commands = stripped.startswith("Команды")
            current = MODE_LEVEL
            continue

        if in_commands and indent <= 4 and not stripped.startswith(("-", "<")):
            word = stripped.split()[0]
            if re.fullmatch(r"[a-z][a-z0-9-]*", word):
                current = word
                result.setdefault(current, set())
                continue

        if stripped.startswith("--"):
            result[current].add(stripped.split("=")[0].split()[0])
        for argument in re.findall(r"(--[a-z0-9-]+)=", stripped):
            result[current].add(argument)
    return result


def method_flags(module: str, method: str) -> set[str]:
    """Собирает ``--флаги``, которые метод отправляет в RAC."""
    source = (SYNC_CMD / f"{module}.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == method:
            return {
                child.value.split("=")[0]
                for child in ast.walk(node)
                if isinstance(child, ast.Constant)
                and isinstance(child.value, str)
                and child.value.startswith("--")
            }
    return set()


def command_names() -> list[tuple[str, str]]:
    """Возвращает пары (модуль, метод) для всех публичных методов команд."""
    pairs: list[tuple[str, str]] = []
    for module in sorted(MODULE_MODES):
        path = SYNC_CMD / f"{module}.py"
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                pairs.append((module, node.name))
    return pairs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rac", help="путь к исполняемому файлу rac")
    parser.add_argument("--check", action="store_true", help="код 1 при расхождениях")
    args = parser.parse_args(argv)

    rac = find_rac(args.rac)
    if rac is None:
        print(
            "rac не найден: укажите путь через --rac. "
            "Проверка параметров возможна только там, где установлена 1С.",
            file=sys.stderr,
        )
        return 2
    print(f"использую rac: {rac}")

    help_by_mode = {mode: run_help(rac, mode) for mode in sorted(set(MODULE_MODES.values()))}
    commands_by_mode = {
        mode: flags_by_command(text, mode) for mode, text in help_by_mode.items()
    }

    problems: list[str] = []
    checked = 0
    for module, method in command_names():
        mode = MODULE_MODES[module]
        documented = commands_by_mode[mode]
        command_flags = documented.get(method)
        if not command_flags:
            # Команда может называться иначе (например, вложенный режим).
            continue
        checked += 1
        known = command_flags | documented.get(MODE_LEVEL, set())
        used = method_flags(module, method)
        unknown = sorted(used - known - COMMON_FLAGS)
        if unknown:
            problems.append(f"{module}.{method}: RAC не знает параметры {unknown}")

    if problems:
        print("Расхождения со справкой rac:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1 if args.check else 0

    print(f"Проверено методов: {checked}. Все параметры есть в справке rac.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
