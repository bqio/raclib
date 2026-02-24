from ...cmd.command import Command, Arg
from ..session import AsyncSession


class AsyncServiceSetting:
    @staticmethod
    async def info(
        session: AsyncSession,
        cluster: str,
        server: str,
        setting: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(setting, "--setting={}"),
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
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        )
        return output.to_list()

    @staticmethod
    async def insert(
        session: AsyncSession,
        cluster: str,
        server: str,
        service_name: str,
        infobase_name: str | None = None,
        service_data_dir: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
            Command(
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("insert"),
                Arg(service_name, "--service-name={}"),
                Arg(infobase_name, "--infobase-name={}"),
                Arg(service_data_dir, "--service-data-dir={}"),
            )
        )

    @staticmethod
    async def update(
        session: AsyncSession,
        cluster: str,
        server: str,
        setting: str,
        service_data_dir: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
            Command(
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("update"),
                Arg(setting, "--setting={}"),
                Arg(service_data_dir, "--service-data-dir={}"),
            )
        )

    @staticmethod
    async def get_service_data_dirs_for_transfer(
        session: AsyncSession,
        cluster: str,
        server: str,
        service_name: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        output = await session.async_exec(
            Command(
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("get-service-data-dirs-for-transfer"),
                Arg(service_name, "--service-name={}"),
            )
        )
        return output.to_list()

    @staticmethod
    async def remove(
        session: AsyncSession,
        cluster: str,
        server: str,
        setting: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
            Command(
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("remove"),
                Arg(setting, "--setting={}"),
            )
        )

    @staticmethod
    async def apply(
        session: AsyncSession,
        cluster: str,
        server: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return await session.async_call(
            Command(
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("apply"),
            )
        )
