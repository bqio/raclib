from ...cmd.command import Command, Arg
from ..session import AsyncSession


class AsyncConnection:
    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        connection: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("connection"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(connection, "--connection={}"),
            )
        )
        return output.to_dict()

    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        process: str | None = None,
        infobase: str | None = None,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("connection"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
                Arg(process, "--process={}"),
                Arg(infobase, "--infobase={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
            )
        )
        return output.to_list()

    @staticmethod
    async def disconnect(
        session: AsyncSession,
        cluster: str,
        process: str,
        connection: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
            Command(
                Arg("connection"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("disconnect"),
                Arg(process, "--process={}"),
                Arg(connection, "--connection={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
            )
        )
