"""Асинхронный транспорт, лежащий в основе библиотеки ``asyncio``.

Возвращает тот же :class:`raclib._shared.CommandResult`, что и синхронный
транспорт, поэтому обработка кода возврата и текста ошибок общая.

Модуль поддерживается вручную и **не генерируется** из синхронной ветки:
здесь нет ничего, кроме специфичного для ``asyncio`` запуска процесса.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from .._shared import CommandResult, decode_stream

__all__ = ["run_rac_async"]


async def run_rac_async(
    rac_path: Path | str,
    args: list[str],
    *,
    timeout: float | None = None,
    encoding: str = "utf-8",
) -> CommandResult:
    """Запускает ``rac`` и возвращает результат.

    :param timeout: предел ожидания в секундах. При превышении процесс
        принудительно завершается, чтобы не оставлять висящих ``rac``.
    :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд.
    """
    process = await asyncio.create_subprocess_exec(
        str(rac_path),
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
    except TimeoutError:
        process.kill()
        await process.wait()
        raise
    return CommandResult(
        returncode=process.returncode or 0,
        stdout=decode_stream(stdout, encoding),
        stderr=decode_stream(stderr, encoding),
    )
