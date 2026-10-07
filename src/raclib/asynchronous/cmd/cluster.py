"""Кластеры 1С: создание, настройка, администраторы.

Соответствует разделу ``rac cluster``."""

from __future__ import annotations

from ..._shared import RacRecord
from ...cmd.command import Arg, Command
from ...utils import b2yn
from ..session import AsyncSession


class AsyncCluster:
    """Кластеры 1С: создание, настройка, администраторы.
    """
    class Admin:
        """Администраторы кластера.
        """
        @staticmethod
        async def list(
            session: AsyncSession,
            cluster: str,
            cluster_user: str | None = None,
            cluster_pwd: str | None = None,
        ) -> list[RacRecord]:
            """Возвращает список администраторов кластера.

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
                    Arg("cluster"),
                    Arg("admin"),
                    Arg(cluster, "--cluster={}"),
                    Arg(cluster_user, "--cluster-user={}"),
                    Arg(cluster_pwd, "--cluster-pwd={}"),
                    Arg("list"),
                )
            )).to_list()

        @staticmethod
        async def register(
            session: AsyncSession,
            cluster: str,
            name: str,
            pwd: str | None = None,
            auth: str = "pwd",
            descr: str | None = None,
            os_user: str | None = None,
            cluster_user: str | None = None,
            cluster_pwd: str | None = None,
        ) -> None:
            """Регистрирует администратора кластера.

            Args:
                cluster: Идентификатор (UUID) кластера.
                name: Имя администратора.
                pwd: Пароль администратора.
                auth: Способ аутентификации: ``pwd`` (пароль) или ``os`` (пользователь ОС).
                descr: Произвольное описание.
                os_user: Имя пользователя операционной системы при ``auth="os"``.
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
                    Arg("cluster"),
                    Arg("admin"),
                    Arg(cluster, "--cluster={}"),
                    Arg(cluster_user, "--cluster-user={}"),
                    Arg(cluster_pwd, "--cluster-pwd={}"),
                    Arg("register"),
                    Arg(name, "--name={}"),
                    Arg(pwd, "--pwd={}"),
                    Arg(descr, "--descr={}"),
                    Arg(auth, "--auth={}"),
                    Arg(os_user, "--os-user={}"),
                )
            )

        @staticmethod
        async def remove(
            session: AsyncSession,
            cluster: str,
            name: str,
            cluster_user: str | None = None,
            cluster_pwd: str | None = None,
        ) -> None:
            """Удаляет администратора кластера.

            RAC не позволит удалить последнего администратора с разрешённой аутентификацией по паролю — такой случай приводит к :class:`raclib.errors.AgentAdminCreateError`.

            Args:
                cluster: Идентификатор (UUID) кластера.
                name: Имя администратора.
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
                    Arg("cluster"),
                    Arg("admin"),
                    Arg(cluster, "--cluster={}"),
                    Arg(cluster_user, "--cluster-user={}"),
                    Arg(cluster_pwd, "--cluster-pwd={}"),
                    Arg("remove"),
                    Arg(name, "--name={}"),
                ),
            )

    @staticmethod
    async def info(session: AsyncSession, cluster: str) -> RacRecord:
        """Возвращает параметры кластера.

        Args:
            cluster: Идентификатор (UUID) кластера.

        Returns:
            dict[str, str | int]: одна запись RAC. Ключи соответствуют полям вывода, дефисы заменены на подчёркивания, числовые значения приведены к ``int``.

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        return (await session.async_exec(
            Command(
                Arg("cluster"),
                Arg("info"),
                Arg(cluster, "--cluster={}"),
            )
        )).to_dict()

    @staticmethod
    async def list(session: AsyncSession) -> list[RacRecord]:
        """Возвращает список кластеров, зарегистрированных у агента.

        Returns:
            list[dict[str, str | int]]: записи RAC. Пустой список, если RAC ничего не вернул.

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        return (await session.async_exec(
            Command(
                Arg("cluster"),
                Arg("list"),
            )
        )).to_list()

    @staticmethod
    async def insert(
        session: AsyncSession,
        host: str,
        port: int,
        name: str | None = None,
        expiration_timeout: int = 60,
        lifetime_limit: int = 0,
        max_memory_size: int | None = None,
        max_memory_time_limit: int | None = None,
        security_level: str = "disabled",
        session_fault_tolerance_level: int = 0,
        load_balancing_mode: str = "performance",
        errors_count_threshold: int | None = None,
        kill_problem_processes: bool = True,
        kill_by_memory_with_dump: bool = False,
        allow_access_right_audit_events_recording: bool = False,
        ping_period: int = 0,
        ping_timeout: int = 0,
        agent_user: str | None = None,
        agent_pwd: str | None = None,
    ) -> str:
        """Создаёт кластер и возвращает его идентификатор.

        Для создания кластера нужны права администратора агента кластера, поэтому обычно передают ``agent_user`` и ``agent_pwd``.

        Args:
            host: Имя хоста, на котором работает агент кластера.
            port: Порт агента кластера (по умолчанию 1540).
            name: Отображаемое имя кластера.
            expiration_timeout: Таймаут завершения сеансов, потерявших связь, в секундах.
            lifetime_limit: Максимальное время жизни сеанса в секундах; 0 — без ограничения.
            max_memory_size: Максимальный объём памяти рабочего процесса в КБ.
            max_memory_time_limit: Интервал проверки превышения памяти рабочим процессом в секундах.
            security_level: Уровень безопасности кластера: ``disabled``, ``basic`` или ``integrity``.
            session_fault_tolerance_level: Уровень отказоустойчивости сеансов: 0, 1 или 2.
            load_balancing_mode: Режим распределения нагрузки: ``performance`` или ``memory``.
            errors_count_threshold: Число ошибок, после которого рабочий процесс считается проблемным.
            kill_problem_processes: Завершать проблемные рабочие процессы автоматически.
            kill_by_memory_with_dump: Завершать процессы при превышении памяти, снимая дамп.
            allow_access_right_audit_events_recording: Разрешить запись событий аудита доступа к данным.
            ping_period: Период проверки связи с рабочими процессами в секундах; 0 — автоматически.
            ping_timeout: Таймаут проверки связи с рабочими процессами в секундах; 0 — автоматически.
            agent_user: Имя администратора агента кластера.
            agent_pwd: Пароль администратора агента кластера.

        Returns:
            str: идентификатор (UUID) созданного кластера.

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        cluster = (await session.async_exec(
            Command(
                Arg("cluster"),
                Arg("insert"),
                Arg(host, "--host={}"),
                Arg(port, "--port={}"),
                Arg(name, "--name={}"),
                Arg(expiration_timeout, "--expiration-timeout={}"),
                Arg(lifetime_limit, "--lifetime-limit={}"),
                Arg(max_memory_size, "--max-memory-size={}"),
                Arg(max_memory_time_limit, "--max-memory-time-limit={}"),
                Arg(security_level, "--security-level={}"),
                Arg(
                    session_fault_tolerance_level, "--session-fault-tolerance-level={}"
                ),
                Arg(load_balancing_mode, "--load-balancing-mode={}"),
                Arg(errors_count_threshold, "--errors-count-threshold={}"),
                Arg(b2yn(kill_problem_processes), "--kill-problem-processes={}"),
                Arg(b2yn(kill_by_memory_with_dump), "--kill-by-memory-with-dump={}"),
                Arg(
                    b2yn(allow_access_right_audit_events_recording),
                    "--allow-access-right-audit-events-recording={}",
                ),
                Arg(ping_period, "--ping-period={}"),
                Arg(ping_timeout, "--ping-timeout={}"),
                Arg(agent_user, "--agent-user={}"),
                Arg(agent_pwd, "--agent-pwd={}"),
            )
        )).to_dict()
        return str(cluster["cluster"])

    @staticmethod
    async def update(
        session: AsyncSession,
        cluster: str,
        name: str | None = None,
        expiration_timeout: int | None = None,
        lifetime_limit: int | None = None,
        max_memory_size: int | None = None,
        max_memory_time_limit: int | None = None,
        security_level: str | None = None,
        session_fault_tolerance_level: int | None = None,
        load_balancing_mode: str | None = None,
        errors_count_threshold: int | None = None,
        kill_problem_processes: bool | None = None,
        kill_by_memory_with_dump: bool | None = None,
        allow_access_right_audit_events_recording: bool | None = None,
        ping_period: int | None = None,
        ping_timeout: int | None = None,
        agent_user: str | None = None,
        agent_pwd: str | None = None,
    ) -> None:
        """Изменяет параметры кластера.

        Меняются только явно переданные параметры: значение ``None`` означает «оставить как есть». Сбросить параметр в значение по умолчанию через этот метод нельзя.

        Args:
            cluster: Идентификатор (UUID) кластера.
            name: Новое отображаемое имя кластера.
            expiration_timeout: Таймаут завершения сеансов, потерявших связь, в секундах.
            lifetime_limit: Максимальное время жизни сеанса в секундах.
            max_memory_size: Максимальный объём памяти рабочего процесса в КБ.
            max_memory_time_limit: Интервал проверки превышения памяти в секундах.
            security_level: Уровень безопасности: ``disabled``, ``basic`` или ``integrity``.
            session_fault_tolerance_level: Уровень отказоустойчивости сеансов: 0, 1 или 2.
            load_balancing_mode: Режим распределения нагрузки: ``performance`` или ``memory``.
            errors_count_threshold: Порог числа ошибок рабочего процесса.
            kill_problem_processes: Завершать проблемные рабочие процессы автоматически.
            kill_by_memory_with_dump: Завершать процессы при превышении памяти, снимая дамп.
            allow_access_right_audit_events_recording: Разрешить запись событий аудита доступа к данным.
            ping_period: Период проверки связи с рабочими процессами в секундах.
            ping_timeout: Таймаут проверки связи с рабочими процессами в секундах.
            agent_user: Имя администратора агента кластера.
            agent_pwd: Пароль администратора агента кластера.

        Returns:
            None

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        return await session.async_call(
            Command(
                Arg("cluster"),
                Arg("update"),
                Arg(cluster, "--cluster={}"),
                Arg(name, "--name={}"),
                Arg(expiration_timeout, "--expiration-timeout={}"),
                Arg(lifetime_limit, "--lifetime-limit={}"),
                Arg(max_memory_size, "--max-memory-size={}"),
                Arg(max_memory_time_limit, "--max-memory-time-limit={}"),
                Arg(security_level, "--security-level={}"),
                Arg(
                    session_fault_tolerance_level, "--session-fault-tolerance-level={}"
                ),
                Arg(load_balancing_mode, "--load-balancing-mode={}"),
                Arg(errors_count_threshold, "--errors-count-threshold={}"),
                Arg(b2yn(kill_problem_processes), "--kill-problem-processes={}"),
                Arg(b2yn(kill_by_memory_with_dump), "--kill-by-memory-with-dump={}"),
                Arg(
                    b2yn(allow_access_right_audit_events_recording),
                    "--allow-access-right-audit-events-recording={}",
                ),
                Arg(ping_period, "--ping-period={}"),
                Arg(ping_timeout, "--ping-timeout={}"),
                Arg(agent_user, "--agent-user={}"),
                Arg(agent_pwd, "--agent-pwd={}"),
            )
        )

    @staticmethod
    async def remove(
        session: AsyncSession,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Удаляет кластер со всеми рабочими серверами и информационными базами.

        Операция необратима: вместе с кластером удаляются его настройки, но не сами базы данных на сервере СУБД.

        Args:
            cluster: Идентификатор (UUID) кластера.
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
                Arg("cluster"),
                Arg("remove"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
            )
        )
