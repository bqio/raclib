from ...cmd.command import Command, Arg, Flag
from ..session import AsyncSession


class AsyncProcess:
    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        process: str,
        licenses: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("process"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(process, "--process={}"),
                Flag(licenses, "--licenses"),
            )
        )
        return output.to_dict()

    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        server: str,
        licenses: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("process"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
                Arg(server, "--server={}"),
                Flag(licenses, "--licenses"),
            )
        )
        return output.to_list()
