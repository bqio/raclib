from ...cmd.command import Command, Arg
from ..session import AsyncSession


class AsyncService:
    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("service"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        )
        return output.to_list()
