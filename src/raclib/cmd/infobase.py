"""Информационные базы кластера.

Соответствует разделам ``rac infobase`` и ``rac infobase summary``."""

from __future__ import annotations

from .._shared import RacRecord
from ..session import Session
from ..utils import b2da, b2of, b2yn
from .command import Arg, Command, Flag


class Infobase:
    """Информационные базы кластера.
    """
    @staticmethod
    def info(
        session: Session,
        cluster: str,
        infobase: str | None = None,
        name: str | None = None,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> RacRecord:
        """Возвращает параметры информационной базы.

        Базу можно указать идентификатором или именем.

        Args:
            cluster: Идентификатор (UUID) кластера.
            infobase: Идентификатор (UUID) информационной базы.
            name: Имя информационной базы в кластере.
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
        return session.exec(
            Command(
                Arg("infobase"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(infobase, "--infobase={}"),
                Arg(name, "--name={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
            )
        ).to_dict()

    class Summary:
        """Сводки по информационным базам кластера.
        """
        @staticmethod
        def info(
            session: Session,
            cluster: str,
            infobase: str | None = None,
            name: str | None = None,
            cluster_user: str | None = None,
            cluster_pwd: str | None = None,
        ) -> RacRecord:
            """Возвращает сводку по информационной базе кластера.

            Сводка содержит суммарные показатели по базе: число сеансов, соединений и занятые ресурсы.

            Args:
                cluster: Идентификатор (UUID) кластера.
                infobase: Идентификатор (UUID) информационной базы.
                name: Имя информационной базы в кластере.
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
                    Arg("infobase"),
                    Arg(cluster, "--cluster={}"),
                    Arg(cluster_user, "--cluster-user={}"),
                    Arg(cluster_pwd, "--cluster-pwd={}"),
                    Arg("summary"),
                    Arg("info"),
                    Arg(infobase, "--infobase={}"),
                    Arg(name, "--name={}"),
                )
            ).to_dict()

        @staticmethod
        def list(
            session: Session,
            cluster: str,
            cluster_user: str | None = None,
            cluster_pwd: str | None = None,
        ) -> list[RacRecord]:
            """Возвращает сводки по всем информационным базам кластера.

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
                    Arg("infobase"),
                    Arg(cluster, "--cluster={}"),
                    Arg(cluster_user, "--cluster-user={}"),
                    Arg(cluster_pwd, "--cluster-pwd={}"),
                    Arg("summary"),
                    Arg("list"),
                )
            ).to_list()

        @staticmethod
        def update(
            session: Session,
            cluster: str,
            infobase: str | None = None,
            name: str | None = None,
            descr: str | None = None,
            cluster_user: str | None = None,
            cluster_pwd: str | None = None,
        ) -> None:
            """Изменяет представление информационной базы в списке сводок.

            Args:
                cluster: Идентификатор (UUID) кластера.
                infobase: Идентификатор (UUID) информационной базы.
                name: Новое имя базы в сводке.
                descr: Новое описание базы в сводке.
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
                    Arg("infobase"),
                    Arg(cluster, "--cluster={}"),
                    Arg(cluster_user, "--cluster-user={}"),
                    Arg(cluster_pwd, "--cluster-pwd={}"),
                    Arg("summary"),
                    Arg("update"),
                    Arg(infobase, "--infobase={}"),
                    Arg(name, "--name={}"),
                    Arg(descr, "--descr={}"),
                )
            )

    @staticmethod
    def create(
        session: Session,
        cluster: str,
        name: str,
        dbms: str,
        db_server: str,
        db_name: str,
        locale: str,
        db_user: str | None = None,
        db_pwd: str | None = None,
        descr: str | None = None,
        date_offset: str = "0",
        security_level: str = "disabled",
        scheduled_jobs_deny: bool = False,
        license_distribution: bool = True,
        create_database: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> str:
        """Создаёт информационную базу в кластере и возвращает её идентификатор.

        По умолчанию база только регистрируется в кластере: база данных на сервере СУБД должна уже существовать. Чтобы RAC создал её сам, передайте ``create_database=True``.

        Args:
            cluster: Идентификатор (UUID) кластера.
            name: Имя информационной базы в кластере.
            dbms: Тип СУБД: ``PostgreSQL``, ``MSSQLServer``, ``IBMDB2``, ``Oracle`` или ``File``.
            db_server: Сервер баз данных вида ``host`` или ``host:port``.
            db_name: Имя базы данных на сервере СУБД.
            locale: Код локали, например ``ru_RU``.
            db_user: Имя пользователя сервера баз данных.
            db_pwd: Пароль пользователя сервера баз данных.
            descr: Произвольное описание.
            date_offset: Смещение даты в часах относительно времени сервера.
            security_level: Уровень безопасности базы: ``disabled``, ``basic`` или ``integrity``.
            scheduled_jobs_deny: Запретить выполнение регламентных заданий.
            license_distribution: Разрешить распределение лицензий.
            create_database: Создать базу данных на сервере СУБД, а не только зарегистрировать её.
            cluster_user: Имя администратора кластера.
            cluster_pwd: Пароль администратора кластера.

        Returns:
            str: идентификатор (UUID) созданной информационной базы.

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        infobase = session.exec(
            Command(
                Arg("infobase"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("create"),
                Flag(create_database, "--create-database"),
                Arg(name, "--name={}"),
                Arg(dbms, "--dbms={}"),
                Arg(db_server, "--db-server={}"),
                Arg(db_name, "--db-name={}"),
                Arg(locale, "--locale={}"),
                Arg(db_user, "--db-user={}"),
                Arg(db_pwd, "--db-pwd={}"),
                Arg(descr, "--descr={}"),
                Arg(date_offset, "--date-offset={}"),
                Arg(security_level, "--security-level={}"),
                Arg(b2of(scheduled_jobs_deny), "--scheduled-jobs-deny={}"),
                Arg(b2da(license_distribution), "--license-distribution={}"),
            )
        ).to_dict()
        return str(infobase["infobase"])

    @staticmethod
    def update(
        session: Session,
        cluster: str,
        infobase: str | None = None,
        name: str | None = None,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        dbms: str | None = None,
        db_server: str | None = None,
        db_name: str | None = None,
        db_user: str | None = None,
        db_pwd: str | None = None,
        descr: str | None = None,
        denied_from: str | None = None,
        denied_message: str | None = None,
        denied_parameter: str | None = None,
        denied_to: str | None = None,
        permission_code: str | None = None,
        sessions_deny: bool | None = None,
        scheduled_jobs_deny: bool | None = None,
        license_distribution: bool | None = None,
        external_session_manager_connection_string: str | None = None,
        external_session_manager_required: bool | None = None,
        reserve_working_processes: bool | None = None,
        security_profile_name: str | None = None,
        safe_mode_security_profile_name: str | None = None,
        disable_local_speech_to_text: bool | None = None,
        configuration_unload_delay_by_working_process_without_active_users: (
            int | None
        ) = None,
        minimum_scheduled_jobs_start_period_without_active_users: int | None = None,
        maximum_scheduled_jobs_start_shift_without_active_users: int | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Изменяет параметры информационной базы.

        Меняются только явно переданные параметры: ``None`` означает «оставить как есть».

        Args:
            cluster: Идентификатор (UUID) кластера.
            infobase: Идентификатор (UUID) информационной базы.
            name: Новое имя базы в кластере.
            infobase_user: Имя пользователя информационной базы.
            infobase_pwd: Пароль пользователя информационной базы.
            dbms: Тип СУБД.
            db_server: Сервер баз данных вида ``host`` или ``host:port``.
            db_name: Имя базы данных на сервере СУБД.
            db_user: Имя пользователя сервера баз данных.
            db_pwd: Пароль пользователя сервера баз данных.
            descr: Произвольное описание.
            denied_from: Начало блокировки подключений.
            denied_message: Сообщение, которое увидят пользователи при блокировке.
            denied_parameter: Параметр блокировки подключений.
            denied_to: Окончание блокировки подключений.
            permission_code: Код доступа к информационной базе.
            sessions_deny: Запретить создание новых сеансов.
            scheduled_jobs_deny: Запретить выполнение регламентных заданий.
            license_distribution: Разрешить распределение лицензий.
            external_session_manager_connection_string: Строка соединения с внешним менеджером сеансов.
            external_session_manager_required: Требовать внешний менеджер сеансов.
            reserve_working_processes: Зарезервировать рабочие процессы.
            security_profile_name: Имя профиля безопасности.
            safe_mode_security_profile_name: Имя профиля безопасности для безопасного режима.
            disable_local_speech_to_text: Отключить локальное распознавание речи.
            configuration_unload_delay_by_working_process_without_active_users: Задержка выгрузки конфигурации рабочим процессом без активных пользователей.
            minimum_scheduled_jobs_start_period_without_active_users: Минимальный период запуска регламентных заданий без активных пользователей.
            maximum_scheduled_jobs_start_shift_without_active_users: Максимальное смещение запуска регламентных заданий без активных пользователей.
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
                Arg("infobase"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("update"),
                Arg(infobase, "--infobase={}"),
                Arg(name, "--name={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg(dbms, "--dbms={}"),
                Arg(db_server, "--db-server={}"),
                Arg(db_name, "--db-name={}"),
                Arg(db_user, "--db-user={}"),
                Arg(db_pwd, "--db-pwd={}"),
                Arg(descr, "--descr={}"),
                Arg(denied_from, "--denied-from={}"),
                Arg(denied_message, "--denied-message={}"),
                Arg(denied_parameter, "--denied-parameter={}"),
                Arg(denied_to, "--denied-to={}"),
                Arg(permission_code, "--permission-code={}"),
                Arg(b2of(sessions_deny), "--sessions-deny={}"),
                Arg(b2of(scheduled_jobs_deny), "--scheduled-jobs-deny={}"),
                Arg(b2da(license_distribution), "--license-distribution={}"),
                Arg(
                    external_session_manager_connection_string,
                    "--external-session-manager-connection-string={}",
                ),
                Arg(
                    b2yn(external_session_manager_required),
                    "--external-session-manager-required={}",
                ),
                Arg(b2yn(reserve_working_processes), "--reserve-working-processes={}"),
                Arg(security_profile_name, "--security-profile-name={}"),
                Arg(
                    safe_mode_security_profile_name,
                    "--safe-mode-security-profile-name={}",
                ),
                Arg(
                    b2yn(disable_local_speech_to_text),
                    "--disable-local-speech-to-text={}",
                ),
                Arg(
                    configuration_unload_delay_by_working_process_without_active_users,
                    "--configuration-unload-delay-by-working-process-without-active-users={}",
                ),
                Arg(
                    minimum_scheduled_jobs_start_period_without_active_users,
                    "--minimum-scheduled-jobs-start-period-without-active-users={}",
                ),
                Arg(
                    maximum_scheduled_jobs_start_shift_without_active_users,
                    "--maximum-scheduled-jobs-start-shift-without-active-users={}",
                ),
            )
        )

    @staticmethod
    def drop(
        session: Session,
        cluster: str,
        infobase: str | None = None,
        name: str | None = None,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        db_user: str | None = None,
        db_pwd: str | None = None,
        drop_database: bool = False,
        clear_database: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Удаляет информационную базу из кластера.

        По умолчанию удаляется только запись о базе в кластере. Чтобы удалить или очистить саму базу данных на сервере СУБД, передайте ``drop_database=True`` или ``clear_database=True``; для этого нужны ``db_user`` и ``db_pwd``.

        Args:
            cluster: Идентификатор (UUID) кластера.
            infobase: Идентификатор (UUID) информационной базы.
            name: Имя информационной базы в кластере.
            infobase_user: Имя пользователя информационной базы.
            infobase_pwd: Пароль пользователя информационной базы.
            db_user: Имя пользователя сервера баз данных; нужен при удалении базы данных.
            db_pwd: Пароль пользователя сервера баз данных.
            drop_database: Удалить базу данных на сервере СУБД.
            clear_database: Очистить базу данных на сервере СУБД, оставив её саму.
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
                Arg("infobase"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("drop"),
                Arg(infobase, "--infobase={}"),
                Arg(name, "--name={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg(db_user, "--db-user={}"),
                Arg(db_pwd, "--db-pwd={}"),
                Flag(drop_database, "--drop-database"),
                Flag(clear_database, "--clear-database"),
            )
        )
