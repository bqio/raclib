"""Тестовые наборы и фикстуры raclib.

Тесты запускаются без внешних зависимостей::

    python -m unittest discover -s tests -t .
"""

from __future__ import annotations

import shutil
import sys
import uuid
from pathlib import Path

#: Каталог с исходниками, чтобы тесты работали без установки пакета.
SRC = Path(__file__).resolve().parent.parent / "src"
REPO_ROOT = Path(__file__).resolve().parent.parent

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


class TempDir:
    """Временный каталог для тестов, пригодный для ограниченных сред.

    ``tempfile`` здесь не используется сознательно:

    * системный ``%TEMP%`` может быть закрыт политикой (в песочнице DSH он не
      доступен для записи);
    * ``tempfile.mkdtemp`` создаёт каталог, у которого в такой среде
      унаследованные права не позволяют создавать файлы, — тесты падали бы на
      подготовке, а не на проверке;
    * очистка ``TemporaryDirectory`` вызывает ``chmod``, который тоже может
      быть запрещён, и тогда падал бы уже сам прогон тестов.

    Поэтому каталог создаётся как обычный подкаталог рабочей области с
    уникальным именем и удаляется без изменения прав.
    """

    def __init__(self) -> None:
        self.path = REPO_ROOT / f".tmp-raclib-{uuid.uuid4().hex[:12]}"
        self.path.mkdir()

    def __enter__(self) -> TempDir:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.cleanup()

    def cleanup(self) -> None:
        """Удаляет каталог, не падая на запретах ограниченной среды.

        ``ignore_errors=True`` здесь недостаточно: он глушит ошибки удаления
        файлов, но ``onerror`` внутри ``shutil`` всё равно может пробросить
        исключение (например, при запрете ``chmod``), и тогда упал бы сам
        прогон тестов. Поэтому ошибки гасятся явным обработчиком.
        """
        shutil.rmtree(self.path, onerror=lambda *_: None)

    @property
    def name(self) -> str:
        """Имя каталога: совместимо с ``tempfile.TemporaryDirectory``."""
        return str(self.path)

    def __fspath__(self) -> str:
        """Позволяет передавать ``TempDir`` прямо в ``Path`` и ``open``."""
        return str(self.path)


def temp_dir() -> TempDir:
    """Возвращает временный каталог с интерфейсом ``TemporaryDirectory``."""
    return TempDir()


def make_executable(path: Path) -> Path:
    """Помечает файл исполняемым, где это имеет смысл.

    На Windows бит исполнения не используется: ``validate_rac_path`` считает
    исполняемым любой существующий файл. ``chmod`` там не нужен и, более того,
    может сломать последующее удаление временного каталога в ограниченной среде.
    """
    if sys.platform != "win32":
        path.chmod(path.stat().st_mode | 0o111)
    return path

#: Реалистичный вывод ``rac cluster list``: две записи, разделённые пустой
#: строкой, значения в кавычках, есть многострочное описание.
CLUSTER_LIST = (
    'cluster              : 6a4c0b3f-1111-2222-3333-444455556666\n'
    'name                 : "Production"\n'
    'host                 : rac1.local\n'
    'port                 : 1541\n'
    'expiration-timeout   : 60\n'
    'lifetime-limit       : 0\n'
    'security-level       : 1\n'
    'descr                : "Основной кластер"\n'
    '\n'
    'cluster              : 7b5d1c4e-aaaa-bbbb-cccc-ddddeeeeffff\n'
    'name                 : "Test"\n'
    'host                 : rac2.local\n'
    'port                 : 1541\n'
    'expiration-timeout   : 60\n'
    'lifetime-limit       : 0\n'
    'security-level       : 1\n'
    'descr                : "Резервный"\n'
    '\n'
)

#: Одна запись без завершающей пустой строки — так RAC отвечает на ``info``.
CLUSTER_INFO = (
    'cluster              : 6a4c0b3f-1111-2222-3333-444455556666\n'
    'name                 : "Production"\n'
    'host                 : rac1.local\n'
    'port                 : 1541\n'
    'expiration-timeout   : 60\n'
)

#: Вывод с многострочным значением и двоеточием внутри значения.
MULTILINE_VALUE = (
    'infobase  : db-1\n'
    'descr     : "Основная база\n'
    '- продолжение описания"\n'
    'dbms      : PostgreSQL\n'
)

#: Типичный stderr RAC при неверном пароле администратора кластера.
CLUSTER_AUTH_STDERR = (
    'Ошибка соединения с сервером администрирования\n'
    'Администратор кластера не аутентифицирован\n'
)

#: Короткий stderr: раньше часть классов ошибок падала на нём с IndexError.
SHORT_STDERR = "Ошибка разбора параметра: --port"
