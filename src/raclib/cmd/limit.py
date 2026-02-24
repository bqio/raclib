from .command import Command, Arg
from ..session import Session


class Limit:
    @staticmethod
    def list(
        session: Session,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("limit"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        ).to_list()

    @staticmethod
    def info(
        session: Session,
        cluster: str,
        limit: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("limit"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(limit, "--limit={}"),
            )
        ).to_dict()

    @staticmethod
    def update(
        session: Session,
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
        return session.call(
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
    def remove(
        session: Session,
        cluster: str,
        name: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("limit"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("remove"),
                Arg(name, "--name={}"),
            )
        )
