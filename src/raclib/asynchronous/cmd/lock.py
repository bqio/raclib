from ...cmd.command import Command, Arg
from ..session import AsyncSession


class AsyncLock:
    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        infobase: str | None = None,
        connection: str | None = None,
        infobase_session: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
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
        )
        return output.to_list()
