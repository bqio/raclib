"""Блокировки, удерживаемые сеансами.

Соответствует разделу ``rac lock``."""

from __future__ import annotations

from .._shared import RacRecord
from ..session import Session
from .command import Arg, Command


class Lock:
    """Блокировки, удерживаемые сеансами.
    """
    @staticmethod
    def list(
        session: Session,
        cluster: str,
        infobase: str | None = None,
        connection: str | None = None,
        infobase_session: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает список блокировок, удерживаемых сеансами.

        Список можно сузить по информационной базе, соединению или сеансу.

        Args:
            cluster: Идентификатор (UUID) кластера.
            infobase: Идентификатор (UUID) информационной базы.
            connection: Идентификатор соединения.
            infobase_session: Номер сеанса информационной базы.
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
                Arg("lock"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
                Arg(infobase, "--infobase={}"),
                Arg(connection, "--connection={}"),
                Arg(infobase_session, "--session={}"),
            )
        ).to_list()
