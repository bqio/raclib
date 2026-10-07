"""Соединения клиентов с информационными базами.

Соответствует разделу ``rac connection``."""

from __future__ import annotations

from ..._shared import RacRecord
from ...cmd.command import Arg, Command
from ..session import AsyncSession


class AsyncConnection:
    """Соединения клиентов с информационными базами.
    """
    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        connection: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> RacRecord:
        """Возвращает сведения о соединении с информационной базой.

        Args:
            cluster: Идентификатор (UUID) кластера.
            connection: Идентификатор соединения.
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
                Arg("connection"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(connection, "--connection={}"),
            )
        )).to_dict()

    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        process: str | None = None,
        infobase: str | None = None,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает список соединений с информационными базами кластера.

        Список можно сузить по рабочему процессу или по информационной базе.

        Args:
            cluster: Идентификатор (UUID) кластера.
            process: Идентификатор рабочего процесса: только его соединения.
            infobase: Идентификатор (UUID) информационной базы: только её соединения.
            infobase_user: Имя пользователя информационной базы.
            infobase_pwd: Пароль пользователя информационной базы.
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
                Arg("connection"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
                Arg(process, "--process={}"),
                Arg(infobase, "--infobase={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
            )
        )).to_list()

    @staticmethod
    async def disconnect(
        session: AsyncSession,
        cluster: str,
        process: str,
        connection: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Принудительно разрывает соединение с информационной базой.

        Args:
            cluster: Идентификатор (UUID) кластера.
            process: Идентификатор рабочего процесса.
            connection: Идентификатор соединения.
            infobase_user: Имя пользователя информационной базы.
            infobase_pwd: Пароль пользователя информационной базы.
            cluster_user: Имя администратора кластера.
            cluster_pwd: Пароль администратора кластера.

        Returns:
            None

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        return await session.async_call(
            Command(
                Arg("connection"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("disconnect"),
                Arg(process, "--process={}"),
                Arg(connection, "--connection={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
            )
        )
