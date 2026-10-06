#!/usr/bin/env python3
"""Проверяет собранное колесо: содержимое и импортируемость.

Скрипт запускается в CI после сборки. Он решает две задачи:

* убедиться, что в колесо попали все нужные файлы (в том числе ``py.typed``);
* импортировать пакет **именно из колеса**, а не из ``src/``.

Сделано на Python, а не на shell: на Windows-раннере вызовы ``python -m zipfile``
с путями в стиле POSIX и подстановка ``dist/*.whl`` в bash вели себя иначе, чем
на Ubuntu, и шаг падал по причинам, не связанным с кодом.

Использование::

    python tools/check_wheel.py                 # взять единственное колесо из dist/
    python tools/check_wheel.py dist/raclib-1.2.0-py3-none-any.whl
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

#: Файлы, которые обязаны быть в колесе. Список важен: без ``py.typed``
#: аннотации не видны mypy у потребителей, а без ``_shared`` пакет не импортируется.
REQUIRED_FILES = (
    "raclib/__init__.py",
    "raclib/_shared.py",
    "raclib/_transport.py",
    "raclib/py.typed",
    "raclib/errors.py",
    "raclib/session.py",
    "raclib/client.py",
    "raclib/cmd/command.py",
    "raclib/cmd/infobase.py",
    "raclib/asynchronous/__init__.py",
    "raclib/asynchronous/_transport.py",
    "raclib/asynchronous/errors.py",
    "raclib/asynchronous/session.py",
    "raclib/asynchronous/client.py",
)

#: Код проверки импорта: выполняется в отдельном процессе, куда путь к
#: распакованному колесу передаётся аргументом и вставляется в ``sys.path``
#: вручную. Полагаться на ``PYTHONPATH`` нельзя: на Windows-раннере он вёл себя
#: иначе, чем на Ubuntu, и шаг падал по причинам, не связанным с кодом.
IMPORT_CHECK = (
    "import pathlib, sys; "
    "sys.path.insert(0, sys.argv[1]); "
    "import raclib, raclib.asynchronous as asynchronous; "
    "root = pathlib.Path(raclib.__file__).resolve().parent; "
    "installed = pathlib.Path(sys.argv[1]).resolve() / 'raclib'; "
    "assert root == installed, f'импорт пришёл не из колеса: {root}'; "
    "assert (root / 'py.typed').exists(), 'py.typed нет рядом с пакетом'; "
    "assert raclib.Client is asynchronous.AsyncClient, 'ветки разошлись'; "
    "print('колесо импортируется:', raclib.Session.__name__, '| файл:', root)"
)


def find_wheel(explicit: str | None) -> Path:
    """Возвращает путь к колесу: указанное явно или единственное в dist/."""
    if explicit:
        wheel = Path(explicit)
        if not wheel.exists():
            raise SystemExit(f"Колесо не найдено: {wheel}")
        return wheel

    dist = REPO_ROOT / "dist"
    wheels = sorted(dist.glob("raclib-*.whl"))
    if not wheels:
        raise SystemExit("В каталоге dist/ нет собранных колёс")
    if len(wheels) > 1:
        raise SystemExit(
            "В dist/ несколько колёс, укажите нужное явно: "
            + ", ".join(wheel.name for wheel in wheels)
        )
    return wheels[0]


def check_contents(wheel: Path) -> list[str]:
    """Проверяет, что в колесе есть все обязательные файлы."""
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())

    return [name for name in REQUIRED_FILES if name not in names]


def check_import(wheel: Path) -> int:
    """Распаковывает колесо и импортирует пакет из него."""
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory) / "wheel"
        with zipfile.ZipFile(wheel) as archive:
            archive.extractall(target)

        environment = dict(os.environ)
        # PYTHONPATH очищаем: путь передаётся аргументом, чтобы импорт не мог
        # подхватить raclib из рабочего каталога или из установленного пакета.
        environment.pop("PYTHONPATH", None)
        try:
            completed = subprocess.run(
                [sys.executable, "-c", IMPORT_CHECK, str(target)],
                cwd=target,
                env=environment,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        except OSError as exc:  # pragma: no cover - защитная сетка
            print(f"Не удалось запустить проверку импорта: {exc}", file=sys.stderr)
            return 1

        if completed.stdout.strip():
            print(completed.stdout.strip())
        if completed.returncode != 0:
            print("Проверка импорта из колеса не прошла.", file=sys.stderr)
            if completed.stderr.strip():
                print(completed.stderr.strip(), file=sys.stderr)
            print(f"  python: {sys.executable}", file=sys.stderr)
            print(f"  распаковано в: {target}", file=sys.stderr)
            print(f"  содержимое: {sorted(p.name for p in target.iterdir())}", file=sys.stderr)
        return completed.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", nargs="?", help="путь к колесу; по умолчанию — из dist/")
    args = parser.parse_args(argv)

    wheel = find_wheel(args.wheel)
    print(f"проверяю колесо: {wheel.name}")

    missing = check_contents(wheel)
    if missing:
        print("В колесе нет обязательных файлов:", file=sys.stderr)
        for name in missing:
            print(f"  - {name}", file=sys.stderr)
        return 1
    print(f"обязательные файлы на месте: {len(REQUIRED_FILES)}")

    return check_import(wheel)


if __name__ == "__main__":
    raise SystemExit(main())
