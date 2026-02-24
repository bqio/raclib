from ...cmd.command import Command, Arg
from ..session import AsyncSession


class AsyncLimit:
    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("limit"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        )
        return output.to_list()

    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        limit: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("limit"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(limit, "--limit={}"),
            )
        )
        return output.to_dict()

    @staticmethod
    async def update(
        session: AsyncSession,
        cluster: str,
        name: str,
        action: str,
        counter: str | None = None,
        duration: int | None = None,
        cpu_time: int | None = None,
        memory: int | None = None,
        read: int | None = None,
        write: int | None = None,
        duration_dbms: int | None = None,
        dbms_bytes: int | None = None,
        service: int | None = None,
        call: int | None = None,
        number_of_active_sessions: int | None = None,
        number_of_sessions: int | None = None,
        error_message: str | None = None,
        descr: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
            Command(
                Arg("limit"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("update"),
                Arg(name, "--name={}"),
                Arg(action, "--action={}"),
                Arg(counter, "--counter={}"),
                Arg(duration, "--duration={}"),
                Arg(cpu_time, "--cpu-time={}"),
                Arg(memory, "--memory={}"),
                Arg(read, "--read={}"),
                Arg(write, "--write={}"),
                Arg(duration_dbms, "--duration-dbms={}"),
                Arg(dbms_bytes, "--dbms-bytes={}"),
                Arg(service, "--service={}"),
                Arg(call, "--call={}"),
                Arg(number_of_active_sessions, "--number-of-active-sessions={}"),
                Arg(number_of_sessions, "--number-of-sessions={}"),
                Arg(error_message, "--error-message={}"),
                Arg(descr, "--descr={}"),
            )
        )

    @staticmethod
    async def remove(
        session: AsyncSession,
        cluster: str,
        name: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
            Command(
                Arg("limit"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("remove"),
                Arg(name, "--name={}"),
            )
        )
