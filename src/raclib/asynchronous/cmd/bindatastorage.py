"""Хранилище двоичных данных информационной базы.

Соответствует разделу ``rac binary-data-storage``."""

from __future__ import annotations

from ..._shared import RacRecord
from ...cmd.command import Arg, Command
from ..session import AsyncSession


class AsyncBinaryDataStorage:
    """Хранилище двоичных данных информационной базы.
    """
    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        infobase: str,
        storage: str,
        name: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> RacRecord:
        """Возвращает сведения о двоичных данных информационной базы.

        Соответствует ``rac binary-data-storage info``.

        Args:
            cluster: Идентификатор (UUID) кластера.
            infobase: Идентификатор (UUID) информационной базы.
            storage: Идентификатор хранилища двоичных данных.
            name: Имя объекта внутри хранилища.
            infobase_user: Имя пользователя информационной базы.
            infobase_pwd: Пароль пользователя информационной базы.
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
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("info"),
                Arg(storage, "--storage={}"),
                Arg(name, "--name={}"),
            )
        )).to_dict()

    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        infobase: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает список хранилищ двоичных данных информационной базы.

        Args:
            cluster: Идентификатор (UUID) кластера.
            infobase: Идентификатор (UUID) информационной базы.
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
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("list"),
            )
        )).to_list()

    @staticmethod
    async def create_full_backup(
        session: AsyncSession,
        cluster: str,
        infobase: str,
        server_path: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Создаёт полную резервную копию хранилища двоичных данных.

        Args:
            cluster: Идентификатор (UUID) кластера.
            infobase: Идентификатор (UUID) информационной базы.
            server_path: Каталог на рабочем сервере, куда будет записана копия.
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
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("create-full-backup"),
                Arg(server_path, "--server-path={}"),
            )
        )

    @staticmethod
    async def create_diff_backup(
        session: AsyncSession,
        cluster: str,
        infobase: str,
        server_path: str,
        full_backup_server_path: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Создаёт differential-копию хранилища двоичных данных.

        Копия содержит изменения относительно полной резервной копии.

        Args:
            cluster: Идентификатор (UUID) кластера.
            infobase: Идентификатор (UUID) информационной базы.
            server_path: Каталог на рабочем сервере для differential-копии.
            full_backup_server_path: Каталог, где лежит полная резервная копия.
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
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("create-diff-backup"),
                Arg(server_path, "--server-path={}"),
                Arg(full_backup_server_path, "--full-backup-server-path={}"),
            )
        )

    @staticmethod
    async def load_full_backup(
        session: AsyncSession,
        cluster: str,
        infobase: str,
        server_path: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Восстанавливает хранилище двоичных данных из полной резервной копии.

        Args:
            cluster: Идентификатор (UUID) кластера.
            infobase: Идентификатор (UUID) информационной базы.
            server_path: Каталог на рабочем сервере с полной резервной копией.
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
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("load-full-backup"),
                Arg(server_path, "--server-path={}"),
            )
        )

    @staticmethod
    async def load_diff_backup(
        session: AsyncSession,
        cluster: str,
        infobase: str,
        server_path: str,
        full_backup_server_path: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Восстанавливает хранилище из differential-копии поверх полной.

        Args:
            cluster: Идентификатор (UUID) кластера.
            infobase: Идентификатор (UUID) информационной базы.
            server_path: Каталог на рабочем сервере с differential-копией.
            full_backup_server_path: Каталог, где лежит полная резервная копия.
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
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("load-diff-backup"),
                Arg(server_path, "--server-path={}"),
                Arg(full_backup_server_path, "--full-backup-server-path={}"),
            )
        )

    @staticmethod
    async def clear_unused_space(
        session: AsyncSession,
        cluster: str,
        infobase: str,
        storage: str,
        name: str,
        by_universal_date: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Освобождает в хранилище место, занятое устаревшими версиями данных.

        Args:
            cluster: Идентификатор (UUID) кластера.
            infobase: Идентификатор (UUID) информационной базы.
            storage: Идентификатор хранилища двоичных данных.
            name: Имя объекта внутри хранилища.
            by_universal_date: Универсальная дата, до которой данные считаются устаревшими.
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
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("clear-unused-space"),
                Arg(storage, "--storage={}"),
                Arg(name, "--name={}"),
                Arg(by_universal_date, "--by-universal-date={}"),
            )
        )
