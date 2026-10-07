"""Сеансы пользователей.

Соответствует разделу ``rac session``."""

from __future__ import annotations

from ..._shared import RacRecord
from ...cmd.command import Arg, Command, Flag
from ..session import AsyncSession


class AsyncUserSession:
    """Сеансы пользователей.
    """
    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        user_session: str,
        licenses: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> RacRecord:
        """Возвращает сведения о сеансе пользователя.

        Args:
            cluster: Идентификатор (UUID) кластера.
            user_session: Номер сеанса.
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
                Arg("session"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(user_session, "--session={}"),
                Flag(licenses, "--licenses"),
            )
        )).to_dict()

    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        infobase: str | None = None,
        licenses: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает список сеансов пользователей кластера.

        Список можно сузить до одной информационной базы.

        Args:
            cluster: Идентификатор (UUID) кластера.
            infobase: Идентификатор (UUID) информационной базы.
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
                Arg("session"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
                Arg(infobase, "--infobase={}"),
                Flag(licenses, "--licenses"),
            )
        )).to_list()

    @staticmethod
    async def terminate(
        session: AsyncSession,
        cluster: str,
        user_session: str,
        error_message: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Завершает сеанс пользователя.

        Пользователь получит сообщение, переданное в ``error_message``.

        Args:
            cluster: Идентификатор (UUID) кластера.
            user_session: Номер сеанса.
            error_message: Сообщение, которое увидит пользователь.
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
                Arg("session"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("terminate"),
                Arg(user_session, "--session={}"),
                Arg(error_message, "--error-message={}"),
            )
        )

    @staticmethod
    async def interrupt_current_server_call(
        session: AsyncSession,
        cluster: str,
        user_session: str,
        error_message: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Прерывает текущий серверный вызов в сеансе пользователя.

        В отличие от :meth:`terminate` сам сеанс не завершается.

        Args:
            cluster: Идентификатор (UUID) кластера.
            user_session: Номер сеанса.
            error_message: Сообщение, которое увидит пользователь.
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
                Arg("session"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("interrupt-current-server-call"),
                Arg(user_session, "--session={}"),
                Arg(error_message, "--error-message={}"),
            )
        )
