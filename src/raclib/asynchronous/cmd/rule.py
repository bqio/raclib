"""Требования размещения информационных баз по рабочим серверам.

Соответствует разделу ``rac rule``."""

from __future__ import annotations

from ..._shared import RacRecord
from ...cmd.command import Arg, Command, Flag
from ..session import AsyncSession


class AsyncRule:
    """Требования размещения информационных баз по рабочим серверам.
    """
    @staticmethod
    async def apply(
        session: AsyncSession,
        cluster: str,
        partial: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Применяет требования размещения к кластеру.

        Args:
            cluster: Идентификатор (UUID) кластера.
            partial: Применить частично, не дожидаясь полного перераспределения.
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
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("apply"),
                Flag(partial, "--partial"),
            )
        )

    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        server: str,
        rule: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> RacRecord:
        """Возвращает требование размещения информационных баз.

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
            rule: Идентификатор требования размещения.
            cluster_user: Имя администратора кластера.
            cluster_pwd: Пароль администратора кластера.

        Returns:
            dict[str, str | int]: одна запись RAC. Ключи соответствуют полям вывода, дефисы заменены на подчёркивания, числовые значения приведены к ``int``.

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        return await session.async_exec(
            Command(
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(server, "--server={}"),
                Arg(rule, "--rule={}"),
            )
        ).to_dict()

    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        server: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает список требований размещения рабочих серверов.

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
            cluster_user: Имя администратора кластера.
            cluster_pwd: Пароль администратора кластера.

        Returns:
            list[dict[str, str | int]]: записи RAC. Пустой список, если RAC ничего не вернул.

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        return await session.async_exec(
            Command(
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
                Arg(server, "--server={}"),
            )
        ).to_list()

    @staticmethod
    async def insert(
        session: AsyncSession,
        cluster: str,
        server: str,
        position: int,
        object_type: str | None = None,
        infobase_name: str | None = None,
        rule_type: str | None = None,
        application_ext: str | None = None,
        priority: int | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> str:
        """Добавляет требование размещения и возвращает его идентификатор.

        Требования задают, какие информационные базы могут выполняться на конкретном рабочем сервере.

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
            position: Позиция требования в списке.
            object_type: Тип объекта требования: ``Infobase`` или ``Server``.
            infobase_name: Имя информационной базы, к которой применяется требование.
            rule_type: Вид требования: ``Assign`` или ``Deny``.
            application_ext: Расширение приложения, к которому применяется требование.
            priority: Приоритет требования.
            cluster_user: Имя администратора кластера.
            cluster_pwd: Пароль администратора кластера.

        Returns:
            str: идентификатор созданного требования размещения.

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        rule = await session.async_exec(
            Command(
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("insert"),
                Arg(server, "--server={}"),
                Arg(position, "--position={}"),
                Arg(object_type, "--object-type={}"),
                Arg(infobase_name, "--infobase-name={}"),
                Arg(rule_type, "--rule-type={}"),
                Arg(application_ext, "--application-ext={}"),
                Arg(priority, "--priority={}"),
            )
        ).to_dict()
        return str(rule["rule"])

    @staticmethod
    async def update(
        session: AsyncSession,
        cluster: str,
        server: str,
        rule: str,
        position: int,
        object_type: str | None = None,
        infobase_name: str | None = None,
        rule_type: str | None = None,
        application_ext: str | None = None,
        priority: int | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Изменяет требование размещения.

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
            rule: Идентификатор требования размещения.
            position: Новая позиция требования в списке.
            object_type: Тип объекта требования: ``Infobase`` или ``Server``.
            infobase_name: Имя информационной базы.
            rule_type: Вид требования: ``Assign`` или ``Deny``.
            application_ext: Расширение приложения.
            priority: Приоритет требования.
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
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("update"),
                Arg(server, "--server={}"),
                Arg(rule, "--rule={}"),
                Arg(position, "--position={}"),
                Arg(object_type, "--object-type={}"),
                Arg(infobase_name, "--infobase-name={}"),
                Arg(rule_type, "--rule-type={}"),
                Arg(application_ext, "--application-ext={}"),
                Arg(priority, "--priority={}"),
            ),
        )

    @staticmethod
    async def remove(
        session: AsyncSession,
        cluster: str,
        server: str,
        rule: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Удаляет требование размещения.

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
            rule: Идентификатор требования размещения.
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
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("remove"),
                Arg(server, "--server={}"),
                Arg(rule, "--rule={}"),
            )
        )
