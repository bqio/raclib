from .command import Command, Arg
from ..session import Session


class Lock:
    @staticmethod
    def list(
        session: Session,
        cluster: str,
        infobase: str | None = None,
        connection: str | None = None,
        infobase_session: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
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
        ).to_list()
