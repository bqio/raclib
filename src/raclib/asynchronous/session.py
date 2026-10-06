"""Асинхронная ветка: сессия администрирования на базе ``asyncio``.

Файл сгенерирован из ``src/raclib/session.py`` скриптом
``tools/generate_async.py``. Правки вносите в синхронную ветку.
"""

from __future__ import annotations

import asyncio

from .. import errors
from .._shared import (
    Client,
    CommandResult,
    RACInvocationError,
    RawOutput,
    resolve_encoding,
    validate_rac_path,
)
from ..cmd.command import Command
from ._transport import run_rac_async

__all__ = ["AsyncSession"]


class AsyncSession:
    """Асинхронная сессия администрирования.

    :param max_concurrency: предел одновременных запусков ``rac`` в рамках
        одной сессии. ``None`` — без ограничения. Без него ``asyncio.gather``
        по сотням кластеров порождает столько же процессов ``rac``.
    Остальные параметры совпадают с :class:`raclib.session.Session`.
    """

    def __init__(
        self,
        client: Client,
        host: str = "localhost",
        port: int = 1545,
        timeout: float | None = None,
        encoding: str | None = None,
        max_concurrency: int | None = None,
        debug: bool = False,
    ):
        """Создаёт сессию; параметры совпадают с синхронной веткой."""
        self.client = client
        self.host = host
        self.port = port
        self.timeout = timeout
        self.encoding = resolve_encoding(encoding)
        self.max_concurrency = max_concurrency
        self.debug = debug
        self._semaphore: asyncio.Semaphore | None = (
            asyncio.Semaphore(max_concurrency) if max_concurrency else None
        )

    async def async_exec(self, command: Command | str) -> RawOutput:
        """Выполняет команду RAC и возвращает её вывод."""
        return RawOutput((await self._execute(command)).stdout)

    async def async_call(self, command: Command | str) -> None:
        """Выполняет команду, отбрасывая вывод."""
        await self._execute(command)

    #: Псевдонимы, чтобы набор методов совпадал с
    #: :class:`raclib.session.Session` (там они называются ``exec``/``call``).
    exec = async_exec
    call = async_call

    async def _execute(self, command: Command | str) -> CommandResult:
        validate_rac_path(self.client.rac_path)
        args = [f"{self.host}:{self.port}", *_command_args(command)]
        if self.debug:
            print("[DEBUG]", args)
        try:
            if self._semaphore is None:
                result = await self._invoke(args)
            else:
                async with self._semaphore:
                    result = await self._invoke(args)
        except TimeoutError:
            # Важно: этот блок обязан идти раньше OSError. В Python 3.11+
            # TimeoutError наследуется от OSError (asyncio.TimeoutError —
            # его псевдоним), и иначе перехватился бы общий блок.
            raise errors.RACTimeoutError(self.timeout or 0) from None
        except FileNotFoundError as exc:
            raise RACInvocationError(
                f"Не удалось запустить RAC по пути {self.client.rac_path}: {exc}"
            ) from exc
        except OSError as exc:
            raise RACInvocationError(
                f"Не удалось запустить RAC по пути {self.client.rac_path}: {exc}"
            ) from exc
        if result.returncode != 0:
            if self.debug:
                print("[DEBUG]", result.stderr)
            raise errors.handler(result.stderr) from None
        if self.debug:
            print(result.stdout)
        return result

    async def _invoke(self, args: list[str]) -> CommandResult:
        return await run_rac_async(
            self.client.rac_path,
            args,
            timeout=self.timeout,
            encoding=self.encoding,
        )


def _command_args(command: Command | str) -> list[str]:
    if isinstance(command, Command):
        return command.args
    return [str(command)]
