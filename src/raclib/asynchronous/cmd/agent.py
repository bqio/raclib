"""Агент кластера и его администраторы.

Соответствует разделу ``rac agent``."""

from __future__ import annotations

from ..._shared import RacRecord
from ...cmd.command import Arg, Command
from ..session import AsyncSession


class AsyncAgent:
    """Агент кластера и его администраторы.
    """
    class Admin:
        """Администраторы агента кластера.
        """
        @staticmethod
        async def list(
            session: AsyncSession,
            agent_user: str | None = None,
            agent_pwd: str | None = None,
        ) -> list[RacRecord]:
            """Возвращает список администраторов агента кластера.

            Args:
                agent_user: Имя администратора агента кластера.
                agent_pwd: Пароль администратора агента кластера.

            Returns:
                list[dict[str, str | int]]: записи RAC. Пустой список, если RAC ничего не вернул.

            :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
            :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
            :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
            """
            return await session.async_exec(
                Command(
                    Arg("agent"),
                    Arg(agent_user, "--agent-user={}"),
                    Arg(agent_pwd, "--agent-pwd={}"),
                    Arg("admin"),
                    Arg("list"),
                )
            ).to_list()

        @staticmethod
        async def register(
            session: AsyncSession,
            name: str,
            pwd: str | None = None,
            auth: str = "pwd",
            descr: str | None = None,
            os_user: str | None = None,
            agent_user: str | None = None,
            agent_pwd: str | None = None,
        ) -> None:
            """Регистрирует администратора агента кластера.

            После регистрации администратор сможет подключаться к агенту и управлять его рабочими процессами.

            Args:
                name: Имя администратора.
                pwd: Пароль администратора.
                auth: Способ аутентификации: ``pwd`` (пароль) или ``os`` (пользователь ОС).
                descr: Произвольное описание.
                os_user: Имя пользователя операционной системы при ``auth="os"``.
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
                    Arg("agent"),
                    Arg(agent_user, "--agent-user={}"),
                    Arg(agent_pwd, "--agent-pwd={}"),
                    Arg("admin"),
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
            name: str,
            agent_user: str | None = None,
            agent_pwd: str | None = None,
        ) -> None:
            """Удаляет администратора агента кластера.

            Args:
                name: Имя администратора.
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
                    Arg("agent"),
                    Arg(agent_user, "--agent-user={}"),
                    Arg(agent_pwd, "--agent-pwd={}"),
                    Arg("admin"),
                    Arg("remove"),
                    Arg(name, "--name={}"),
                ),
            )

    @staticmethod
    async def version(session: AsyncSession) -> str:
        """Возвращает версию агента кластера вместе с версией RAC.

        Returns:
            str: вывод RAC без завершающих пробельных символов.

        :raises raclib.errors.RACNotFoundError: файл ``rac`` не найден или не может быть запущен.
        :raises raclib.errors.RACTimeoutError: RAC не ответил за ``timeout`` секунд, заданный в сессии.
        :raises raclib.errors.UnknownError: RAC вернул ошибку, которой нет в таблице соответствий ``raclib.errors``.
        """
        return await session.async_exec(Command(Arg("agent"), Arg("version"))).to_str()
