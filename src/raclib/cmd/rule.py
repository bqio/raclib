from .command import Command, Arg, Flag
from ..session import Session


class Rule:
    @staticmethod
    def apply(
        session: Session,
        cluster: str,
        partial: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
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
    def info(
        session: Session,
        cluster: str,
        server: str,
        rule: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(server, "--server={}"),
                Arg(rule, "--rule={}"),
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
                Arg("rule"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
                Arg(server, "--server={}"),
            )
        ).to_list()

    @staticmethod
    def insert(
        session: Session,
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
        rule = session.exec(
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
        ).to_dict()
        return str(rule["rule"])

    @staticmethod
    def update(
        session: Session,
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
        return session.call(
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
    def remove(
        session: Session,
        cluster: str,
        server: str,
        rule: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
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
