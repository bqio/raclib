"""Ограничения ресурсов, привязанные к счётчикам производительности.

Соответствует разделу ``rac limit``."""

from __future__ import annotations

from .._shared import RacRecord
from ..session import Session
from .command import Arg, Command


class Limit:
    """Ограничения ресурсов, привязанные к счётчикам производительности.
    """
    @staticmethod
    def list(
        session: Session,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает список ограничений ресурсов кластера.

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
        return session.exec(
            Command(
                Arg("limit"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        ).to_list()

    @staticmethod
    def info(
        session: Session,
        cluster: str,
        limit: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> RacRecord:
        """Возвращает описание ограничения ресурсов.

        Args:
            cluster: Идентификатор (UUID) кластера.
            limit: Имя ограничения.
            cluster_user: Имя администратора кластера.
            cluster_pwd: Пароль администратора кластера.

        Returns:
            dict[str, str | int]: одна запись RAC. Ключи соответствуют полям вывода, дефисы заменены на подчёркивания, числовые значения приведены к ``int``.

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        return session.exec(
            Command(
                Arg("limit"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(limit, "--limit={}"),
            )
        ).to_dict()

    @staticmethod
    def update(
        session: Session,
        cluster: str,
        name: str,
        action: str,
        counter: str | None = None,
        duration: int | None = None,
        cpu_time: int | None = None,
        memory: int | None = None,
        read: int | None = None,
        write: int | None = None,
        duration_dbms: int | None = None,
        dbms_bytes: int | None = None,
        service: int | None = None,
        call: int | None = None,
        number_of_active_sessions: int | None = None,
        number_of_sessions: int | None = None,
        error_message: str | None = None,
        descr: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Создаёт или изменяет ограничение ресурсов.

        Работает как upsert по имени. Пороговые параметры (``duration``, ``memory`` и прочие) задаются в единицах соответствующего счётчика.

        Args:
            cluster: Идентификатор (UUID) кластера.
            name: Имя ограничения.
            action: Что делать при превышении: ``restart`` или ``ignore``.
            counter: Имя счётчика, к которому привязано ограничение.
            duration: Порог общего времени выполнения вызовов.
            cpu_time: Порог времени процессора.
            memory: Порог занятой памяти.
            read: Порог объёма чтения.
            write: Порог объёма записи.
            duration_dbms: Порог времени выполнения запросов к СУБД.
            dbms_bytes: Порог объёма данных, переданных в СУБД.
            service: Порог служебных метрик.
            call: Порог метрик вызовов сервера.
            number_of_active_sessions: Порог числа активных сеансов.
            number_of_sessions: Порог общего числа сеансов.
            error_message: Сообщение, которое увидит пользователь при срабатывании ограничения.
            descr: Произвольное описание ограничения.
            cluster_user: Имя администратора кластера.
            cluster_pwd: Пароль администратора кластера.

        Returns:
            None

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        return session.call(
            Command(
                Arg("limit"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("update"),
                Arg(name, "--name={}"),
                Arg(action, "--action={}"),
                Arg(counter, "--counter={}"),
                Arg(duration, "--duration={}"),
                Arg(cpu_time, "--cpu-time={}"),
                Arg(memory, "--memory={}"),
                Arg(read, "--read={}"),
                Arg(write, "--write={}"),
                Arg(duration_dbms, "--duration-dbms={}"),
                Arg(dbms_bytes, "--dbms-bytes={}"),
                Arg(service, "--service={}"),
                Arg(call, "--call={}"),
                Arg(number_of_active_sessions, "--number-of-active-sessions={}"),
                Arg(number_of_sessions, "--number-of-sessions={}"),
                Arg(error_message, "--error-message={}"),
                Arg(descr, "--descr={}"),
            )
        )

    @staticmethod
    def remove(
        session: Session,
        cluster: str,
        name: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Удаляет ограничение ресурсов.

        Args:
            cluster: Идентификатор (UUID) кластера.
            name: Имя ограничения.
            cluster_user: Имя администратора кластера.
            cluster_pwd: Пароль администратора кластера.

        Returns:
            None

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        return session.call(
            Command(
                Arg("limit"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("remove"),
                Arg(name, "--name={}"),
            )
        )
