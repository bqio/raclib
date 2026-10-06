#!/usr/bin/env python3
"""Проверяет целостность документации без сборки сайта.

`mkdocs build --strict` умеет всё это сам, но требует установленных
зависимостей. Этот скрипт проверяет то же самое средствами стандартной
библиотеки, поэтому его можно запускать и в CI, и в тестах:

* каждая страница из ``nav`` в ``mkdocs.yml`` существует;
* каждая директива ``:::`` в справочнике ссылается на реальный объект Python
  (опечатка в пути приводила бы к пустой странице, а не к ошибке);
* все относительные ссылки между страницами ведут на существующие файлы.

Использование::

    python tools/check_docs.py
"""

from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
SRC = REPO_ROOT / "src"
MKDOCS_YML = REPO_ROOT / "mkdocs.yml"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

#: Директива mkdocstrings: ``::: путь.к.объекту``.
DIRECTIVE_RE = re.compile(r"^:::\s+([\w.]+)\s*$", re.MULTILINE)

#: Ссылка между страницами: ``[текст](путь.md)`` или ``](путь.md#anchor)``.
LINK_RE = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)\s]*)?\)")

#: Ссылка на страницу в nav: ``- Название: путь.md``.
NAV_RE = re.compile(r":\s*([\w./-]+\.md)\s*$", re.MULTILINE)


def check_nav() -> list[str]:
    """Проверяет, что все страницы из nav существуют."""
    problems: list[str] = []
    text = MKDOCS_YML.read_text(encoding="utf-8")
    for relative in NAV_RE.findall(text):
        if not (DOCS / relative).exists():
            problems.append(f"mkdocs.yml: страница из nav не найдена: {relative}")
    return problems


def resolve_object(dotted: str) -> object:
    """Импортирует объект по точечному пути, начиная с верхнего модуля."""
    parts = dotted.split(".")
    module = importlib.import_module(parts[0])
    current: object = module
    for part in parts[1:]:
        current = getattr(current, part)
    return current


def check_directives() -> tuple[list[str], int]:
    """Проверяет, что каждая директива ``:::`` указывает на существующий объект."""
    problems: list[str] = []
    total = 0
    for page in sorted(DOCS.rglob("*.md")):
        for dotted in DIRECTIVE_RE.findall(page.read_text(encoding="utf-8")):
            total += 1
            try:
                resolve_object(dotted)
            except Exception as exc:  # noqa: BLE001 - нужен любой сбой импорта
                problems.append(
                    f"{page.relative_to(REPO_ROOT)}: не удалось разрешить "
                    f"'{dotted}': {type(exc).__name__}: {exc}"
                )
    return problems, total


def check_links() -> tuple[list[str], int]:
    """Проверяет относительные ссылки между страницами."""
    problems: list[str] = []
    total = 0
    for page in sorted(DOCS.rglob("*.md")):
        for target in LINK_RE.findall(page.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://")):
                continue
            total += 1
            resolved = (page.parent / target).resolve()
            if not resolved.exists():
                problems.append(
                    f"{page.relative_to(REPO_ROOT)}: битая ссылка на {target}"
                )
    return problems, total


def main() -> int:
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))

    problems = check_nav()
    directive_problems, directives = check_directives()
    link_problems, links = check_links()
    problems.extend(directive_problems)
    problems.extend(link_problems)

    if problems:
        print("Проблемы в документации:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    print(
        f"Документация целостна: страниц в nav "
        f"{len(NAV_RE.findall(MKDOCS_YML.read_text(encoding='utf-8')))}, "
        f"директив ::: {directives}, относительных ссылок {links}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
