from .command import Command, Arg, Flag
from ..session import Session


class UserSession:
    @staticmethod
    def info(
        session: Session,
        cluster: str,
        user_session: str,
        licenses: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("session"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(user_session, "--session={}"),
                Flag(licenses, "--licenses"),
            )
        ).to_dict()

    @staticmethod
    def list(
        session: Session,
        cluster: str,
        infobase: str | None = None,
        licenses: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("session"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
                Arg(infobase, "--infobase={}"),
                Flag(licenses, "--licenses"),
            )
        ).to_list()

    @staticmethod
    def terminate(
        session: Session,
        cluster: str,
        user_session: str,
        error_message: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
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
    def interrupt_current_server_call(
        session: Session,
        cluster: str,
        user_session: str,
        error_message: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
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
