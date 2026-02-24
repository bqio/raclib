from .command import Command, Arg
from ..session import Session


class ServiceSetting:
    @staticmethod
    def info(
        session: Session,
        cluster: str,
        server: str,
        setting: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(setting, "--setting={}"),
            )
        ).to_dict()

    @staticmethod
    def list(
        session: Session,
        cluster: str,
        server: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        ).to_list()

    @staticmethod
    def insert(
        session: Session,
        cluster: str,
        server: str,
        service_name: str,
        infobase_name: str | None = None,
        service_data_dir: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
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
    def update(
        session: Session,
        cluster: str,
        server: str,
        setting: str,
        service_data_dir: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
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
    def get_service_data_dirs_for_transfer(
        session: Session,
        cluster: str,
        server: str,
        service_name: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("get-service-data-dirs-for-transfer"),
                Arg(service_name, "--service-name={}"),
            )
        ).to_list()

    @staticmethod
    def remove(
        session: Session,
        cluster: str,
        server: str,
        setting: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
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
    def apply(
        session: Session,
        cluster: str,
        server: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("service-setting"),
                Arg(cluster, "--cluster={}"),
                Arg(server, "--server={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("apply"),
            )
        )
