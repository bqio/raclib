"""Настройки служб на рабочих серверах.

Соответствует разделу ``rac service-setting``."""

from __future__ import annotations

from .._shared import RacRecord
from ..session import Session
from .command import Arg, Command


class ServiceSetting:
    """Настройки служб на рабочих серверах.
    """
    @staticmethod
    def info(
        session: Session,
        cluster: str,
        server: str,
        setting: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> RacRecord:
        """Возвращает настройку службы на рабочем сервере.

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
            setting: Идентификатор настройки службы.
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
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(setting, "--setting={}"),
            )
        ).to_dict()

    @staticmethod
    def list(
        session: Session,
        cluster: str,
        server: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает список настроек служб рабочего сервера.

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
        return session.exec(
            Command(
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        ).to_list()

    @staticmethod
    def insert(
        session: Session,
        cluster: str,
        server: str,
        service_name: str,
        infobase_name: str | None = None,
        service_data_dir: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> str:
        """Добавляет настройку службы на рабочем сервере.

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
            service_name: Имя службы.
            infobase_name: Имя информационной базы, к которой привязана служба.
            service_data_dir: Каталог данных службы.
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
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("insert"),
                Arg(service_name, "--service-name={}"),
                Arg(infobase_name, "--infobase-name={}"),
                Arg(service_data_dir, "--service-data-dir={}"),
            )
        )

    @staticmethod
    def update(
        session: Session,
        cluster: str,
        server: str,
        setting: str,
        service_data_dir: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Изменяет настройку службы.

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
            setting: Идентификатор настройки службы.
            service_data_dir: Новый каталог данных службы.
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
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("update"),
                Arg(setting, "--setting={}"),
                Arg(service_data_dir, "--service-data-dir={}"),
            )
        )

    @staticmethod
    def get_service_data_dirs_for_transfer(
        session: Session,
        cluster: str,
        server: str,
        service_name: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает каталоги данных служб, которые нужно перенести.

        Используется при переносе службы на другой рабочий сервер.

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
            service_name: Имя службы; если не указано — по всем службам сервера.
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
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("get-service-data-dirs-for-transfer"),
                Arg(service_name, "--service-name={}"),
            )
        ).to_list()

    @staticmethod
    def remove(
        session: Session,
        cluster: str,
        server: str,
        setting: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Удаляет настройку службы.

        Args:
            cluster: Идентификатор (UUID) кластера.
            server: Идентификатор (UUID) рабочего сервера.
            setting: Идентификатор настройки службы.
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
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("remove"),
                Arg(setting, "--setting={}"),
            )
        )

    @staticmethod
    def apply(
        session: Session,
        cluster: str,
        server: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Применяет настройки служб на рабочем сервере.

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
        return session.call(
            Command(
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("apply"),
            )
        )
