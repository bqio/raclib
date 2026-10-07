"""Службы, зарегистрированные в кластере.

Соответствует разделу ``rac service``."""

from __future__ import annotations

from ..._shared import RacRecord
from ...cmd.command import Arg, Command
from ..session import AsyncSession


class AsyncService:
    """Службы, зарегистрированные в кластере.
    """
    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает список служб, зарегистрированных в кластере.

        Args:
            cluster: Идентификатор (UUID) кластера.
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
                Arg("service"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        )).to_list()
