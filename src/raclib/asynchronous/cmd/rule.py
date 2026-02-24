from ...cmd.command import Command, Arg, Flag
from ..session import AsyncSession


class AsyncRule:
    @staticmethod
    async def apply(
        session: AsyncSession,
        cluster: str,
        partial: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
            Command(
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("apply"),
                Flag(partial, "--partial"),
            )
        )

    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        server: str,
        rule: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(server, "--server={}"),
                Arg(rule, "--rule={}"),
            )
        )
        return output.to_dict()

    @staticmethod
    async def list(
        session: AsyncSession,
        cluster: str,
        server: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
                Arg(server, "--server={}"),
            )
        )
        return output.to_list()

    @staticmethod
    async def insert(
        session: AsyncSession,
        cluster: str,
        server: str,
        position: int,
        object_type: str | None = None,
        infobase_name: str | None = None,
        rule_type: str | None = None,
        application_ext: str | None = None,
        priority: int | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("insert"),
                Arg(server, "--server={}"),
                Arg(position, "--position={}"),
                Arg(object_type, "--object-type={}"),
                Arg(infobase_name, "--infobase-name={}"),
                Arg(rule_type, "--rule-type={}"),
                Arg(application_ext, "--application-ext={}"),
                Arg(priority, "--priority={}"),
            )
        )
        rule = output.to_dict()
        return str(rule["rule"])

    @staticmethod
    async def update(
        session: AsyncSession,
        cluster: str,
        server: str,
        rule: str,
        position: int,
        object_type: str | None = None,
        infobase_name: str | None = None,
        rule_type: str | None = None,
        application_ext: str | None = None,
        priority: int | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
            Command(
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("update"),
                Arg(server, "--server={}"),
                Arg(rule, "--rule={}"),
                Arg(position, "--position={}"),
                Arg(object_type, "--object-type={}"),
                Arg(infobase_name, "--infobase-name={}"),
                Arg(rule_type, "--rule-type={}"),
                Arg(application_ext, "--application-ext={}"),
                Arg(priority, "--priority={}"),
            ),
        )

    @staticmethod
    async def remove(
        session: AsyncSession,
        cluster: str,
        server: str,
        rule: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
            Command(
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("remove"),
                Arg(server, "--server={}"),
                Arg(rule, "--rule={}"),
            )
        )
