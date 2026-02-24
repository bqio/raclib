from ...cmd.command import Command, Arg, Flag
from ..session import AsyncSession


class AsyncUserSession:
    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        user_session: str,
        licenses: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("session"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(user_session, "--session={}"),
                Flag(licenses, "--licenses"),
            )
        )
        return output.to_dict()

    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        infobase: str | None = None,
        licenses: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("session"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
                Arg(infobase, "--infobase={}"),
                Flag(licenses, "--licenses"),
            )
        )
        return output.to_list()

    @staticmethod
    async def terminate(
        session: AsyncSession,
        cluster: str,
        user_session: str,
        error_message: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
            Command(
                Arg("session"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("terminate"),
                Arg(user_session, "--session={}"),
                Arg(error_message, "--error-message={}"),
            )
        )

    @staticmethod
    async def interrupt_current_server_call(
        session: AsyncSession,
        cluster: str,
        user_session: str,
        error_message: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
            Command(
                Arg("session"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("interrupt-current-server-call"),
                Arg(user_session, "--session={}"),
                Arg(error_message, "--error-message={}"),
            )
        )
