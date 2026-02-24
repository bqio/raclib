from ...cmd.command import Command, Arg
from ..session import AsyncSession


class AsyncManager:
    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        manager: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("manager"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(manager, "--manager={}"),
            )
        )
        return output.to_dict()

    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("manager"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        )
        return output.to_list()
