"""Профили безопасности и правила доступа к внешним ресурсам.

Соответствует разделу ``rac profile``."""

from __future__ import annotations

from ..._shared import RacRecord
from ...cmd.command import Arg, Command
from ...utils import b2yn
from ..session import AsyncSession


class AsyncProfile:
    """Профили безопасности и правила доступа к внешним ресурсам.
    """
    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> list[RacRecord]:
        """Возвращает список профилей безопасности кластера.

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
                Arg("profile"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        )).to_list()

    @staticmethod
    async def update(
        session: AsyncSession,
        cluster: str,
        name: str,
        descr: str | None = None,
        config: bool | None = None,
        priv: bool | None = None,
        full_privileged_mode: bool | None = None,
        privileged_mode_roles: str | None = None,
        crypto: bool | None = None,
        right_extension: bool | None = None,
        right_extension_definition_roles: str | None = None,
        all_modules_extension: bool | None = None,
        modules_available_for_extension: str | None = None,
        modules_not_available_for_extension: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ) -> None:
        """Создаёт или изменяет профиль безопасности.

        Профиль безопасности ограничивает доступ к внешним ресурсам (файлам, COM-объектам, внешним компонентам) для кода, выполняемого в безопасном режиме.

        Args:
            cluster: Идентификатор (UUID) кластера.
            name: Имя профиля безопасности.
            descr: Произвольное описание.
            config: Разрешение на доступ к файлам конфигурации: ``allow`` или ``deny``.
            priv: Разрешение на привилегированный режим: ``allow`` или ``deny``.
            full_privileged_mode: Разрешить полный привилегированный режим.
            privileged_mode_roles: Роли, которым разрешён привилегированный режим.
            crypto: Разрешение на работу с криптографией: ``allow`` или ``deny``.
            right_extension: Разрешение на расширение прав: ``allow`` или ``deny``.
            right_extension_definition_roles: Роли, которым разрешено расширение прав.
            all_modules_extension: Разрешить расширение всех модулей.
            modules_available_for_extension: Модули, расширение которых разрешено.
            modules_not_available_for_extension: Модули, расширение которых запрещено.
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
                Arg("profile"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("update"),
                Arg(name, "--name={}"),
                Arg(descr, "--descr={}"),
                Arg(b2yn(config), "--config={}"),
                Arg(b2yn(priv), "--priv={}"),
                Arg(b2yn(full_privileged_mode), "--full-privileged-mode={}"),
                Arg(privileged_mode_roles, "--privileged-mode-roles={}"),
                Arg(b2yn(crypto), "--crypto={}"),
                Arg(b2yn(right_extension), "--right-extension={}"),
                Arg(
                    right_extension_definition_roles,
                    "--right-extension-definition-roles={}",
                ),
                Arg(b2yn(all_modules_extension), "--all-modules-extension={}"),
                Arg(
                    modules_available_for_extension,
                    "--modules-available-for-extension={}",
                ),
                Arg(
                    modules_not_available_for_extension,
                    "--modules-not-available-for-extension={}",
                ),
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
        """Удаляет профиль безопасности.

        Args:
            cluster: Идентификатор (UUID) кластера.
            name: Имя профиля безопасности.
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
                Arg("profile"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("remove"),
                Arg(name, "--name={}"),
            )
        )

    class ACL:
        """Правила доступа профиля безопасности к внешним ресурсам.
        """
        class Directory:
            """Правила доступа к каталогам файловой системы.
            """
            @staticmethod
            async def list(
                session: AsyncSession,
                cluster: str,
                name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> list[RacRecord]:
                """Возвращает список каталогов, доступ к которым описан в профиле.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("directory"),
                        Arg("list"),
                        Arg(access, "--access={}"),
                    )
                )).to_list()

            @staticmethod
            async def update(
                session: AsyncSession,
                cluster: str,
                name: str,
                alias: str,
                descr: str | None = None,
                physicalPath: str | None = None,
                allowedRead: bool | None = None,
                allowedWrite: bool | None = None,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> None:
                """Добавляет или изменяет правило доступа к каталогу.

                Правило состоит из псевдонима и физического пути со своими правами на чтение и запись.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    alias: Псевдоним каталога, который используется в коде.
                    descr: Произвольное описание правила.
                    physicalPath: Физический путь к каталогу.
                    allowedRead: Разрешить чтение из каталога.
                    allowedWrite: Разрешить запись в каталог.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("directory"),
                        Arg("update"),
                        Arg(alias, "--alias={}"),
                        Arg(descr, "--descr={}"),
                        Arg(physicalPath, "--physicalPath={}"),
                        Arg(b2yn(allowedRead), "--allowedRead={}"),
                        Arg(b2yn(allowedWrite), "--allowedWrite={}"),
                        Arg(access, "--access={}"),
                    )
                )

            @staticmethod
            async def remove(
                session: AsyncSession,
                cluster: str,
                name: str,
                alias: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> None:
                """Удаляет правило доступа к каталогу.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    alias: Псевдоним каталога.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("directory"),
                        Arg("remove"),
                        Arg(alias, "--alias={}"),
                        Arg(access, "--access={}"),
                    )
                )

        class COM:
            """Правила доступа к COM-объектам.
            """
            @staticmethod
            async def list(
                session: AsyncSession,
                cluster: str,
                name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> list[RacRecord]:
                """Возвращает список COM-объектов, доступ к которым описан в профиле.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("com"),
                        Arg("list"),
                        Arg(access, "--access={}"),
                    )
                )).to_list()

            @staticmethod
            async def update(
                session: AsyncSession,
                cluster: str,
                name: str,
                com_name: str,
                descr: str | None = None,
                file_name: str | None = None,
                id: str | None = None,
                host: str | None = None,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> None:
                """Добавляет или изменяет правило доступа к COM-объекту.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    com_name: Имя COM-объекта.
                    descr: Произвольное описание правила.
                    file_name: Имя файла компоненты.
                    id: Идентификатор COM-объекта.
                    host: Хост, на котором разрешён COM-объект.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("com"),
                        Arg("update"),
                        Arg(com_name, "--name={}"),
                        Arg(descr, "--descr={}"),
                        Arg(file_name, "--fileName={}"),
                        Arg(id, "--id={}"),
                        Arg(host, "--host={}"),
                        Arg(access, "--access={}"),
                    )
                )

            @staticmethod
            async def remove(
                session: AsyncSession,
                cluster: str,
                name: str,
                com_name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> None:
                """Удаляет правило доступа к COM-объекту.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    com_name: Имя COM-объекта.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("com"),
                        Arg("remove"),
                        Arg(com_name, "--name={}"),
                        Arg(access, "--access={}"),
                    )
                )

        class Addin:
            """Правила доступа к внешним компонентам.
            """
            @staticmethod
            async def list(
                session: AsyncSession,
                cluster: str,
                name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> list[RacRecord]:
                """Возвращает список внешних компонент, доступных в профиле.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("addin"),
                        Arg("list"),
                        Arg(access, "--access={}"),
                    )
                )).to_list()

            @staticmethod
            async def update(
                session: AsyncSession,
                cluster: str,
                name: str,
                addin_name: str,
                descr: str | None = None,
                hash: str | None = None,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> None:
                """Добавляет или изменяет правило доступа к внешней компоненте.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    addin_name: Имя внешней компоненты.
                    descr: Произвольное описание правила.
                    hash: Хеш файла внешней компоненты для проверки подлинности.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("addin"),
                        Arg("update"),
                        Arg(addin_name, "--name={}"),
                        Arg(descr, "--descr={}"),
                        Arg(hash, "--hash={}"),
                        Arg(access, "--access={}"),
                    )
                )

            @staticmethod
            async def remove(
                session: AsyncSession,
                cluster: str,
                name: str,
                addin_name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> None:
                """Удаляет правило доступа к внешней компоненте.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    addin_name: Имя внешней компоненты.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("addin"),
                        Arg("remove"),
                        Arg(addin_name, "--name={}"),
                        Arg(access, "--access={}"),
                    )
                )

        class Module:
            """Правила доступа к модулям.
            """
            @staticmethod
            async def list(
                session: AsyncSession,
                cluster: str,
                name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> list[RacRecord]:
                """Возвращает список модулей, доступ к которым описан в профиле.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("module"),
                        Arg("list"),
                        Arg(access, "--access={}"),
                    )
                )).to_list()

            @staticmethod
            async def update(
                session: AsyncSession,
                cluster: str,
                name: str,
                module_name: str,
                descr: str | None = None,
                hash: str | None = None,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> None:
                """Добавляет или изменяет правило доступа к модулю.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    module_name: Имя модуля.
                    descr: Произвольное описание правила.
                    hash: Хеш модуля для проверки подлинности.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("module"),
                        Arg("update"),
                        Arg(module_name, "--name={}"),
                        Arg(descr, "--descr={}"),
                        Arg(hash, "--hash={}"),
                        Arg(access, "--access={}"),
                    )
                )

            @staticmethod
            async def remove(
                session: AsyncSession,
                cluster: str,
                name: str,
                module_name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> None:
                """Удаляет правило доступа к модулю.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    module_name: Имя модуля.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("module"),
                        Arg("remove"),
                        Arg(module_name, "--name={}"),
                        Arg(access, "--access={}"),
                    )
                )

        class App:
            """Правила доступа к приложениям.
            """
            @staticmethod
            async def list(
                session: AsyncSession,
                cluster: str,
                name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> list[RacRecord]:
                """Возвращает список приложений, доступ к которым описан в профиле.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("app"),
                        Arg("list"),
                        Arg(access, "--access={}"),
                    )
                )).to_list()

            @staticmethod
            async def update(
                session: AsyncSession,
                cluster: str,
                name: str,
                app_name: str,
                descr: str | None = None,
                wild: str | None = None,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> None:
                """Добавляет или изменяет правило доступа к приложению.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    app_name: Имя приложения.
                    descr: Произвольное описание правила.
                    wild: Разрешить приложения по маске.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("app"),
                        Arg("update"),
                        Arg(app_name, "--name={}"),
                        Arg(descr, "--descr={}"),
                        Arg(wild, "--wild={}"),
                        Arg(access, "--access={}"),
                    )
                )

            @staticmethod
            async def remove(
                session: AsyncSession,
                cluster: str,
                name: str,
                app_name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> None:
                """Удаляет правило доступа к приложению.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    app_name: Имя приложения.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("app"),
                        Arg("remove"),
                        Arg(app_name, "--name={}"),
                        Arg(access, "--access={}"),
                    )
                )

        class Inet:
            """Правила доступа к интернет-ресурсам.
            """
            @staticmethod
            async def list(
                session: AsyncSession,
                cluster: str,
                name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> list[RacRecord]:
                """Возвращает список интернет-ресурсов, доступных в профиле.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("inet"),
                        Arg("list"),
                        Arg(access, "--access={}"),
                    )
                )).to_list()

            @staticmethod
            async def update(
                session: AsyncSession,
                cluster: str,
                name: str,
                inet_name: str,
                descr: str | None = None,
                protocol: str | None = None,
                url: str | None = None,
                port: int | None = None,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> None:
                """Добавляет или изменяет правило доступа к интернет-ресурсу.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    inet_name: Имя интернет-ресурса.
                    descr: Произвольное описание правила.
                    protocol: Протокол доступа: ``http``, ``https``, ``ftp`` и другие.
                    url: URL или маска URL ресурса.
                    port: Порт ресурса.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("inet"),
                        Arg("update"),
                        Arg(inet_name, "--name={}"),
                        Arg(descr, "--descr={}"),
                        Arg(protocol, "--protocol={}"),
                        Arg(url, "--url={}"),
                        Arg(port, "--port={}"),
                        Arg(access, "--access={}"),
                    )
                )

            @staticmethod
            async def remove(
                session: AsyncSession,
                cluster: str,
                name: str,
                inet_name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ) -> None:
                """Удаляет правило доступа к интернет-ресурсу.

                Args:
                    cluster: Идентификатор (UUID) кластера.
                    name: Имя профиля безопасности.
                    inet_name: Имя интернет-ресурса.
                    access: Вид доступа: ``read`` или ``write``.
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
                        Arg("profile"),
                        Arg(cluster, "--cluster={}"),
                        Arg(cluster_user, "--cluster-user={}"),
                        Arg(cluster_pwd, "--cluster-pwd={}"),
                        Arg("acl"),
                        Arg(name, "--name={}"),
                        Arg("inet"),
                        Arg("remove"),
                        Arg(inet_name, "--name={}"),
                        Arg(access, "--access={}"),
                    )
                )
