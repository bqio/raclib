from .command import Command, Arg
from ..session import Session


class Manager:
    @staticmethod
    def info(
        session: Session,
        cluster: str,
        manager: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("manager"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(manager, "--manager={}"),
            )
        ).to_dict()

    @staticmethod
    def list(
        session: Session,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("manager"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        ).to_list()
