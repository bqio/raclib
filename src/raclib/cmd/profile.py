from .command import Command, Arg
from ..session import Session
from ..utils import b2yn


class Profile:
    @staticmethod
    def list(
        session: Session,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("profile"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        ).to_list()

    @staticmethod
    def update(
        session: Session,
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
    ):
        return session.call(
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
    def remove(
        session: Session,
        cluster: str,
        name: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
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
        class Directory:
            @staticmethod
            def list(
                session: Session,
                cluster: str,
                name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.exec(
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
                ).to_list()

            @staticmethod
            def update(
                session: Session,
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
            ):
                return session.call(
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
            def remove(
                session: Session,
                cluster: str,
                name: str,
                alias: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.call(
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
            @staticmethod
            def list(
                session: Session,
                cluster: str,
                name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.exec(
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
                ).to_list()

            @staticmethod
            def update(
                session: Session,
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
            ):
                return session.call(
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
            def remove(
                session: Session,
                cluster: str,
                name: str,
                com_name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.call(
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
            @staticmethod
            def list(
                session: Session,
                cluster: str,
                name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.exec(
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
                ).to_list()

            @staticmethod
            def update(
                session: Session,
                cluster: str,
                name: str,
                addin_name: str,
                descr: str | None = None,
                hash: str | None = None,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.call(
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
            def remove(
                session: Session,
                cluster: str,
                name: str,
                addin_name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.call(
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
            @staticmethod
            def list(
                session: Session,
                cluster: str,
                name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.exec(
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
                ).to_list()

            @staticmethod
            def update(
                session: Session,
                cluster: str,
                name: str,
                module_name: str,
                descr: str | None = None,
                hash: str | None = None,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.call(
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
            def remove(
                session: Session,
                cluster: str,
                name: str,
                module_name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.call(
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
            @staticmethod
            def list(
                session: Session,
                cluster: str,
                name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.exec(
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
                ).to_list()

            @staticmethod
            def update(
                session: Session,
                cluster: str,
                name: str,
                app_name: str,
                descr: str | None = None,
                wild: str | None = None,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.call(
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
            def remove(
                session: Session,
                cluster: str,
                name: str,
                app_name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.call(
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
            @staticmethod
            def list(
                session: Session,
                cluster: str,
                name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.exec(
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
                ).to_list()

            @staticmethod
            def update(
                session: Session,
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
            ):
                return session.call(
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
            def remove(
                session: Session,
                cluster: str,
                name: str,
                inet_name: str,
                access: str = "list",
                cluster_user: str | None = None,
                cluster_pwd: str | None = None,
            ):
                return session.call(
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
