"""Рабочие процессы на рабочих серверах.

Соответствует разделу ``rac process``."""

from __future__ import annotations

from ..._shared import RacRecord
from ...cmd.command import Arg, Command, Flag
from ..session import AsyncSession


class AsyncProcess:
    """Рабочие процессы на рабочих серверах.
    """
    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        process: str,
        licenses: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> RacRecord:
        """Возвращает сведения о рабочем процессе.

        Args:
            cluster: Идентификатор (UUID) кластера.
            process: Идентификатор рабочего процесса.
            licenses: Показать информацию о занятых лицензиях.
            cluster_user: Имя администратора кластера.
            cluster_pwd: Пароль администратора кластера.

        Returns:
            dict[str, str | int]: одна запись RAC. Ключи соответствуют полям вывода, дефисы заменены на подчёркивания, числовые значения приведены к ``int``.

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        return (await session.async_exec(
            Command(
                Arg("process"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(process, "--process={}"),
                Flag(licenses, "--licenses"),
            )
        )).to_dict()

    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        server: str,
        licenses: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает список рабочих процессов указанного рабочего сервера.

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
            licenses: Показать информацию о занятых лицензиях.
            cluster_user: Имя администратора кластера.
            cluster_pwd: Пароль администратора кластера.

        Returns:
            list[dict[str, str | int]]: записи RAC. Пустой список, если RAC ничего не вернул.

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        return (await session.async_exec(
            Command(
                Arg("process"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
                Arg(server, "--server={}"),
                Flag(licenses, "--licenses"),
            )
        )).to_list()
