from .command import Command, Arg
from ..session import Session
from ..utils import b2ana


class Counter:
    @staticmethod
    def list(
        session: Session,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("counter"),
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
        counter: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("counter"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(counter, "--counter={}"),
            )
        ).to_dict()

    @staticmethod
    def update(
        session: Session,
        cluster: str,
        name: str,
        collection_time: str,
        group: str,
        filter_type: str,
        filter: str | None = None,
        duration: bool | None = None,
        cpu_time: bool | None = None,
        memory: bool | None = None,
        read: bool | None = None,
        write: bool | None = None,
        duration_dbms: bool | None = None,
        dbms_bytes: bool | None = None,
        service: bool | None = None,
        call: bool | None = None,
        number_of_active_sessions: bool | None = None,
        number_of_sessions: bool | None = None,
        descr: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("counter"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("update"),
                Arg(name, "--name={}"),
                Arg(collection_time, "--collection-time={}"),
                Arg(group, "--group={}"),
                Arg(filter_type, "--filter-type={}"),
                Arg(filter, "--filter={}"),
                Arg(b2ana(duration), "--duration={}"),
                Arg(b2ana(cpu_time), "--cpu-time={}"),
                Arg(b2ana(memory), "--memory={}"),
                Arg(b2ana(read), "--read={}"),
                Arg(b2ana(write), "--write={}"),
                Arg(b2ana(duration_dbms), "--duration-dbms={}"),
                Arg(b2ana(dbms_bytes), "--dbms-bytes={}"),
                Arg(b2ana(service), "--service={}"),
                Arg(b2ana(call), "--call={}"),
                Arg(b2ana(number_of_active_sessions), "--number-of-active-sessions={}"),
                Arg(b2ana(number_of_sessions), "--number-of-sessions={}"),
                Arg(descr, "--descr={}"),
            )
        )

    @staticmethod
    def values(
        session: Session,
        cluster: str,
        counter: str,
        object: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("counter"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("values"),
                Arg(counter, "--counter={}"),
                Arg(object, "--object={}"),
            )
        ).to_list()

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
                Arg("counter"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("remove"),
                Arg(name, "--name={}"),
            ),
        )

    @staticmethod
    def clear(
        session: Session,
        cluster: str,
        counter: str,
        object: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("counter"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("clear"),
                Arg(counter, "--counter={}"),
                Arg(object, "--object={}"),
            ),
        )

    @staticmethod
    def accumulated_values(
        session: Session,
        cluster: str,
        counter: str,
        object: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("counter"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("accumulated-values"),
                Arg(counter, "--counter={}"),
                Arg(object, "--object={}"),
            )
        ).to_list()
