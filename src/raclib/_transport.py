"""Транспорт: запуск ``rac`` и нормализация результата.

Синхронная и асинхронная реализации возвращают один и тот же
:class:`raclib._shared.CommandResult`, поэтому вся логика обработки кода
возврата и сообщений об ошибках у них общая.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from ._shared import CommandResult, decode_stream

__all__ = ["run_rac"]


def run_rac(
    rac_path: Path | str,
    args: list[str],
    *,
    timeout: float | None = None,
    encoding: str = "utf-8",
    creationflags: int = 0,
) -> CommandResult:
    """Запускает ``rac`` и возвращает результат.

    :param timeout: предел ожидания в секундах. ``None`` — ждать бесконечно
        (прежнее поведение), но тогда зависший RAC повесит вызывающий поток.
    :param encoding: кодировка вывода RAC. По умолчанию UTF-8; для Windows
        подставляется ``cp866`` на уровне :class:`raclib.session.Session`.
    :param creationflags: флаги создания процесса (на Windows позволяет
        скрыть окно консоли).
    :raises RACTimeoutError: RAC не ответил за ``timeout`` секунд.
    """
    process = subprocess.run(
        [str(rac_path), *args],
        capture_output=True,
        text=True,
        encoding=encoding,
        errors="replace",
        timeout=timeout,
        creationflags=creationflags if sys.platform == "win32" else 0,
    )
    return CommandResult(
        returncode=process.returncode,
        stdout=decode_stream(process.stdout, encoding),
        stderr=decode_stream(process.stderr, encoding),
    )
