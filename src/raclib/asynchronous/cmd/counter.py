"""Счётчики производительности кластера.

Соответствует разделу ``rac counter``."""

from __future__ import annotations

from ..._shared import RacRecord
from ...cmd.command import Arg, Command
from ...utils import b2ana
from ..session import AsyncSession


class AsyncCounter:
    """Счётчики производительности кластера.
    """
    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает список счётчиков производительности кластера.

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
                Arg("counter"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        )).to_list()

    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        counter: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> RacRecord:
        """Возвращает описание счётчика производительности.

        Args:
            cluster: Идентификатор (UUID) кластера.
            counter: Имя счётчика.
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
                Arg("counter"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(counter, "--counter={}"),
            )
        )).to_dict()

    @staticmethod
    async def update(
        session: AsyncSession,
        cluster: str,
        name: str,
        collection_time: str,
        group: str,
        filter_type: str,
        filter: str | None = None,
        duration: bool | None = None,
        cpu_time: bool | None = None,
        memory: bool | None = None,
        read: bool | None = None,
        write: bool | None = None,
        duration_dbms: bool | None = None,
        dbms_bytes: bool | None = None,
        service: bool | None = None,
        call: bool | None = None,
        number_of_active_sessions: bool | None = None,
        number_of_sessions: bool | None = None,
        descr: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Создаёт или изменяет счётчик производительности.

        Метод работает как upsert: если счётчика с таким именем нет, он создаётся. Логические параметры включают и выключают сбор соответствующей метрики: ``True`` — ``analyze``, ``False`` — ``not-analyze``, ``None`` — не менять.

        Args:
            cluster: Идентификатор (UUID) кластера.
            name: Имя счётчика.
            collection_time: Момент сбора значений в формате RAC.
            group: Группа счётчика: ``process``, ``session``, ``connection``, ``call`` или ``dbms``.
            filter_type: Способ фильтрации объектов: ``processor``, ``session``, ``connection`` и другие.
            filter: Значение фильтра для ``filter_type``.
            duration: Собирать общее время выполнения вызовов.
            cpu_time: Собирать время процессора.
            memory: Собирать объём занятой памяти.
            read: Собирать объём чтения.
            write: Собирать объём записи.
            duration_dbms: Собирать время выполнения запросов к СУБД.
            dbms_bytes: Собирать объём данных, переданных в СУБД.
            service: Собирать служебные метрики.
            call: Собирать метрики вызовов сервера.
            number_of_active_sessions: Собирать число активных сеансов.
            number_of_sessions: Собирать общее число сеансов.
            descr: Произвольное описание счётчика.
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
                Arg("counter"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("update"),
                Arg(name, "--name={}"),
                Arg(collection_time, "--collection-time={}"),
                Arg(group, "--group={}"),
                Arg(filter_type, "--filter-type={}"),
                Arg(filter, "--filter={}"),
                Arg(b2ana(duration), "--duration={}"),
                Arg(b2ana(cpu_time), "--cpu-time={}"),
                Arg(b2ana(memory), "--memory={}"),
                Arg(b2ana(read), "--read={}"),
                Arg(b2ana(write), "--write={}"),
                Arg(b2ana(duration_dbms), "--duration-dbms={}"),
                Arg(b2ana(dbms_bytes), "--dbms-bytes={}"),
                Arg(b2ana(service), "--service={}"),
                Arg(b2ana(call), "--call={}"),
                Arg(b2ana(number_of_active_sessions), "--number-of-active-sessions={}"),
                Arg(b2ana(number_of_sessions), "--number-of-sessions={}"),
                Arg(descr, "--descr={}"),
            )
        )

    @staticmethod
    async def values(
        session: AsyncSession,
        cluster: str,
        counter: str,
        object: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает текущие значения счётчика.

        Args:
            cluster: Идентификатор (UUID) кластера.
            counter: Имя счётчика.
            object: Идентификатор объекта, для которого нужно значение.
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
                Arg("counter"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("values"),
                Arg(counter, "--counter={}"),
                Arg(object, "--object={}"),
            )
        )).to_list()

    @staticmethod
    async def remove(
        session: AsyncSession,
        cluster: str,
        name: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Удаляет счётчик производительности.

        Args:
            cluster: Идентификатор (UUID) кластера.
            name: Имя счётчика.
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
                Arg("counter"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("remove"),
                Arg(name, "--name={}"),
            ),
        )

    @staticmethod
    async def clear(
        session: AsyncSession,
        cluster: str,
        counter: str,
        object: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Сбрасывает накопленные значения счётчика.

        Args:
            cluster: Идентификатор (UUID) кластера.
            counter: Имя счётчика.
            object: Идентификатор объекта, значения которого нужно сбросить.
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
                Arg("counter"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("clear"),
                Arg(counter, "--counter={}"),
                Arg(object, "--object={}"),
            ),
        )

    @staticmethod
    async def accumulated_values(
        session: AsyncSession,
        cluster: str,
        counter: str,
        object: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает накопленные значения счётчика за всё время наблюдения.

        Args:
            cluster: Идентификатор (UUID) кластера.
            counter: Имя счётчика.
            object: Идентификатор объекта, для которого нужно значение.
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
                Arg("counter"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("accumulated-values"),
                Arg(counter, "--counter={}"),
                Arg(object, "--object={}"),
            )
        )).to_list()
