from .command import Command, Arg
from ..session import Session


class Connection:
    @staticmethod
    def info(
        session: Session,
        cluster: str,
        connection: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("connection"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(connection, "--connection={}"),
            )
        ).to_dict()

    @staticmethod
    def list(
        session: Session,
        cluster: str,
        process: str | None = None,
        infobase: str | None = None,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("connection"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
                Arg(process, "--process={}"),
                Arg(infobase, "--infobase={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
            )
        ).to_list()

    @staticmethod
    def disconnect(
        session: Session,
        cluster: str,
        process: str,
        connection: str,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("connection"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("disconnect"),
                Arg(process, "--process={}"),
                Arg(connection, "--connection={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
            )
        )
