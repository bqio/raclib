from ...cmd.command import Command, Arg
from ..session import AsyncSession


class AsyncBinaryDataStorage:
    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        infobase: str,
        storage: str,
        name: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
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
        )
        return output.to_dict()

    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        infobase: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
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
        )
        return output.to_list()

    @staticmethod
    async def create_full_backup(
        session: AsyncSession,
        cluster: str,
        infobase: str,
        server_path: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
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
    async def create_diff_backup(
        session: AsyncSession,
        cluster: str,
        infobase: str,
        server_path: str,
        full_backup_server_path: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
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
    async def load_full_backup(
        session: AsyncSession,
        cluster: str,
        infobase: str,
        server_path: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
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
    async def load_diff_backup(
        session: AsyncSession,
        cluster: str,
        infobase: str,
        server_path: str,
        full_backup_server_path: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
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
    async def clear_unused_space(
        session: AsyncSession,
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
        return await session.async_call(
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
