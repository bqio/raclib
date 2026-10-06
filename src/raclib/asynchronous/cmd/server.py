"""Рабочие серверы кластера.

Соответствует разделу ``rac server``."""

from __future__ import annotations

from ..._shared import RacRecord
from ...cmd.command import Arg, Command
from ...utils import b2yn
from ..session import AsyncSession


class AsyncServer:
    """Рабочие серверы кластера.
    """
    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        server: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> RacRecord:
        """Возвращает параметры рабочего сервера.

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
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
                Arg("server"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(server, "--server={}"),
            )
        ).to_dict()

    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает список рабочих серверов кластера.

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
        return await session.async_exec(
            Command(
                Arg("server"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        ).to_list()

    @staticmethod
    async def insert(
        session: AsyncSession,
        cluster: str,
        agent_host: str,
        agent_port: int,
        port_range: str,
        name: str | None = None,
        using: str = "main",
        infobases_limit: int = 8,
        memory_limit: int | None = None,
        connections_limit: int = 256,
        cluster_port: int | None = None,
        dedicate_managers: str = "all",
        safe_working_processess_memory_limit: int | None = None,
        safe_call_memory_limit: int | None = None,
        critical_total_memory: int | None = None,
        temporary_allowed_total_memory: int | None = None,
        temporary_allowed_total_memory_time_limit: int = 300,
        service_principal_name: str | None = None,
        restart_schedule: str | None = None,
        add_prohibiting_assignment_rule: bool | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> str:
        """Регистрирует рабочий сервер в кластере и возвращает его идентификатор.

        Сервер должен быть доступен по сети: RAC обращается к его агенту.

        Args:
            cluster: Идентификатор (UUID) кластера.
            agent_host: Имя хоста, на котором работает агент сервера.
            agent_port: Порт агента сервера.
            port_range: Диапазон IP-портов рабочих процессов, например ``1560:1591``.
            name: Отображаемое имя рабочего сервера.
            using: Назначение сервера: ``main``, ``normal`` или ``job``.
            infobases_limit: Максимальное число информационных баз на сервере.
            memory_limit: Максимальный объём памяти рабочих процессов в КБ.
            connections_limit: Максимальное число соединений на процесс.
            cluster_port: Порт, на котором сервер слушает кластер.
            dedicate_managers: Выделять менеджеры: ``all``, ``none`` или ``isolated``.
            safe_working_processess_memory_limit: Порог памяти рабочего процесса для безопасного режима.
            safe_call_memory_limit: Порог памяти вызова для безопасного режима.
            critical_total_memory: Критический общий объём памяти.
            temporary_allowed_total_memory: Временно разрешённый общий объём памяти.
            temporary_allowed_total_memory_time_limit: Время действия временного лимита памяти в секундах.
            service_principal_name: Имя субъекта-службы (SPN) для аутентификации.
            restart_schedule: Расписание перезапуска сервера.
            add_prohibiting_assignment_rule: Добавить запрещающее требование размещения.
            cluster_user: Имя администратора кластера.
            cluster_pwd: Пароль администратора кластера.

        Returns:
            str: идентификатор (UUID) зарегистрированного рабочего сервера.

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        server = await session.async_exec(
            Command(
                Arg("server"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("insert"),
                Arg(agent_host, "--agent-host={}"),
                Arg(agent_port, "--agent-port={}"),
                Arg(str(port_range), "--port-range={}"),
                Arg(name, "--name={}"),
                Arg(using, "--using={}"),
                Arg(infobases_limit, "--infobases-limit={}"),
                Arg(memory_limit, "--memory-limit={}"),
                Arg(connections_limit, "--connections-limit={}"),
                Arg(cluster_port, "--cluster-port={}"),
                Arg(dedicate_managers, "--dedicate-managers={}"),
                Arg(
                    safe_working_processess_memory_limit,
                    "--safe-working-processess-memory-limit={}",
                ),
                Arg(safe_call_memory_limit, "--safe-call-memory-limit={}"),
                Arg(critical_total_memory, "--critical-total-memory={}"),
                Arg(
                    temporary_allowed_total_memory,
                    "--temporary-allowed-total-memory={}",
                ),
                Arg(
                    temporary_allowed_total_memory_time_limit,
                    "--temporary-allowed-total-memory-time-limit={}",
                ),
                Arg(service_principal_name, "--service-principal-name={}"),
                Arg(
                    restart_schedule,
                    "--restart-schedule={}",
                ),
                Arg(
                    b2yn(add_prohibiting_assignment_rule),
                    "--add-prohibiting-assignment-rule={}",
                ),
            )
        ).to_dict()
        return str(server["server"])

    @staticmethod
    async def update(
        session: AsyncSession,
        cluster: str,
        server: str,
        port_range: str | None = None,
        using: str | None = None,
        infobases_limit: int | None = None,
        memory_limit: int | None = None,
        connections_limit: int | None = None,
        dedicate_managers: str | None = None,
        safe_working_processess_memory_limit: int | None = None,
        safe_call_memory_limit: int | None = None,
        critical_total_memory: int | None = None,
        temporary_allowed_total_memory: int | None = None,
        temporary_allowed_total_memory_time_limit: int | None = None,
        service_principal_name: str | None = None,
        restart_schedule: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Изменяет параметры рабочего сервера.

        Меняются только явно переданные параметры: ``None`` означает «оставить как есть».

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
            port_range: Диапазон IP-портов рабочих процессов.
            using: Назначение сервера: ``main``, ``normal`` или ``job``.
            infobases_limit: Максимальное число информационных баз.
            memory_limit: Максимальный объём памяти рабочих процессов в КБ.
            connections_limit: Максимальное число соединений на процесс.
            dedicate_managers: Выделять менеджеры: ``all``, ``none`` или ``isolated``.
            safe_working_processess_memory_limit: Порог памяти рабочего процесса для безопасного режима.
            safe_call_memory_limit: Порог памяти вызова для безопасного режима.
            critical_total_memory: Критический общий объём памяти.
            temporary_allowed_total_memory: Временно разрешённый общий объём памяти.
            temporary_allowed_total_memory_time_limit: Время действия временного лимита памяти в секундах.
            service_principal_name: Имя субъекта-службы (SPN) для аутентификации.
            restart_schedule: Расписание перезапуска сервера.
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
                Arg("server"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("update"),
                Arg(server, "--server={}"),
                Arg(using, "--using={}"),
                Arg(dedicate_managers, "--dedicate-managers={}"),
                Arg(port_range, "--port-range={}"),
                Arg(infobases_limit, "--infobases-limit={}"),
                Arg(memory_limit, "--memory-limit={}"),
                Arg(connections_limit, "--connections-limit={}"),
                Arg(
                    safe_working_processess_memory_limit,
                    "--safe-working-processess-memory-limit={}",
                ),
                Arg(safe_call_memory_limit, "--safe-call-memory-limit={}"),
                Arg(critical_total_memory, "--critical-total-memory={}"),
                Arg(
                    temporary_allowed_total_memory,
                    "--temporary-allowed-total-memory={}",
                ),
                Arg(
                    temporary_allowed_total_memory_time_limit,
                    "--temporary-allowed-total-memory-time-limit={}",
                ),
                Arg(service_principal_name, "--service-principal-name={}"),
                Arg(restart_schedule, "--restart-schedule={}"),
            )
        )

    @staticmethod
    async def remove(
        session: AsyncSession,
        cluster: str,
        server: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Удаляет рабочий сервер из кластера.

        Центральный сервер кластера удалить нельзя: попытка приводит к :class:`raclib.errors.ServerIsMainError`.

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
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
                Arg("server"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("remove"),
                Arg(server, "--server={}"),
            )
        )
