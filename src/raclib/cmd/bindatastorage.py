from .command import Command, Arg
from ..session import Session


class BinaryDataStorage:
    @staticmethod
    def info(
        session: Session,
        cluster: str,
        infobase: str,
        storage: str,
        name: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("info"),
                Arg(storage, "--storage={}"),
                Arg(name, "--name={}"),
            )
        ).to_dict()

    @staticmethod
    def list(
        session: Session,
        cluster: str,
        infobase: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("list"),
            )
        ).to_list()

    @staticmethod
    def create_full_backup(
        session: Session,
        cluster: str,
        infobase: str,
        server_path: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("create-full-backup"),
                Arg(server_path, "--server-path={}"),
            )
        )

    @staticmethod
    def create_diff_backup(
        session: Session,
        cluster: str,
        infobase: str,
        server_path: str,
        full_backup_server_path: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("create-diff-backup"),
                Arg(server_path, "--server-path={}"),
                Arg(full_backup_server_path, "--full-backup-server-path={}"),
            )
        )

    @staticmethod
    def load_full_backup(
        session: Session,
        cluster: str,
        infobase: str,
        server_path: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("load-full-backup"),
                Arg(server_path, "--server-path={}"),
            )
        )

    @staticmethod
    def load_diff_backup(
        session: Session,
        cluster: str,
        infobase: str,
        server_path: str,
        full_backup_server_path: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("load-diff-backup"),
                Arg(server_path, "--server-path={}"),
                Arg(full_backup_server_path, "--full-backup-server-path={}"),
            )
        )

    @staticmethod
    def clear_unused_space(
        session: Session,
        cluster: str,
        infobase: str,
        storage: str,
        name: str,
        by_universal_date: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("binary-data-storage"),
                Arg(cluster, "--cluster={}"),
                Arg(infobase, "--infobase={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg("clear-unused-space"),
                Arg(storage, "--storage={}"),
                Arg(name, "--name={}"),
                Arg(by_universal_date, "--by-universal-date={}"),
            )
        )
