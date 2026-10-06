"""Синхронная ветка: клиент, сессия и разбор вывода RAC.

Разбор и обработка ошибок вынесены в :mod:`raclib._shared`, чтобы асинхронная
ветка использовала ровно ту же логику.
"""

from __future__ import annotations

import subprocess
import sys

from . import errors
from ._shared import (
    Client,
    CommandResult,
    RACInvocationError,
    RACNotFoundError,
    RACTimeoutError,
    RawOutput,
    resolve_encoding,
    validate_rac_path,
)
from ._transport import run_rac
from .cmd.command import Command

__all__ = ["Client", "RawOutput", "Session", "RACNotFoundError", "RACTimeoutError"]


class Session:
    """Сессия администрирования: одна пара ``host:port`` сервера 1С.

    :param host: хост сервера администрирования.
    :param port: порт сервера администрирования (по умолчанию 1545).
    :param timeout: предел ожидания ответа RAC в секундах. ``None`` — без
        ограничения. Настоятельно рекомендуется задавать: без таймаута
        недоступный кластер подвесит вызывающий поток навсегда.
    :param encoding: кодировка вывода RAC. По умолчанию подбирается по
        платформе (``cp866`` на Windows, ``utf-8`` в остальных случаях).
    :param new_window: не показывать окно консоли при запуске RAC на Windows.
    :param debug: печатать argv и вывод RAC.
    """

    def __init__(
        self,
        client: Client,
        host: str = "localhost",
        port: int = 1545,
        timeout: float | None = None,
        encoding: str | None = None,
        new_window: bool = False,
        debug: bool = False,
    ):
        self.client = client
        self.host = host
        self.port = port
        self.timeout = timeout
        self.encoding = resolve_encoding(encoding)
        self.new_window = new_window
        self.debug = debug

    def exec(self, command: Command | str) -> RawOutput:
        """Выполняет команду RAC и возвращает её вывод.

        :raises RACNotFoundError: файл ``rac`` не найден или не исполняем.
        :raises RACTimeoutError: RAC не ответил за ``self.timeout`` секунд.
        :raises raclib.errors.UnknownError: RAC вернул незнакомую ошибку.
        """
        return RawOutput(self._execute(command).stdout)

    def call(self, command: Command | str) -> None:
        """Выполняет команду, отбрасывая вывод."""
        self._execute(command)

    def _execute(self, command: Command | str) -> CommandResult:
        validate_rac_path(self.client.rac_path)
        args = [f"{self.host}:{self.port}", *_command_args(command)]
        if self.debug:
            print("[DEBUG]", args)
        try:
            result = run_rac(
                self.client.rac_path,
                args,
                timeout=self.timeout,
                encoding=self.encoding,
                creationflags=_creation_flags(self.new_window),
            )
        except subprocess.TimeoutExpired:
            raise RACTimeoutError(self.timeout or 0) from None
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


def _command_args(command: Command | str) -> list[str]:
    if isinstance(command, Command):
        return command.args
    return [str(command)]


def _creation_flags(new_window: bool) -> int:
    """Флаги создания процесса, скрывающие окно консоли на Windows."""
    if sys.platform != "win32":
        return 0
    return 0 if new_window else subprocess.CREATE_NO_WINDOW
