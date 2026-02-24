from .command import Command, Arg
from ..session import Session
from ..utils import b2yn


class Cluster:
    class Admin:
        @staticmethod
        def list(
            session: Session,
            cluster: str,
            cluster_user: str | None = None,
            cluster_pwd: str | None = None,
        ):
            return session.exec(
                Command(
                    Arg("cluster"),
                    Arg("admin"),
                    Arg(cluster, "--cluster={}"),
                    Arg(cluster_user, "--cluster-user={}"),
                    Arg(cluster_pwd, "--cluster-pwd={}"),
                    Arg("list"),
                )
            ).to_list()

        @staticmethod
        def register(
            session: Session,
            cluster: str,
            name: str,
            pwd: str | None = None,
            auth: str = "pwd",
            descr: str | None = None,
            os_user: str | None = None,
            cluster_user: str | None = None,
            cluster_pwd: str | None = None,
        ):
            return session.call(
                Command(
                    Arg("cluster"),
                    Arg("admin"),
                    Arg(cluster, "--cluster={}"),
                    Arg(cluster_user, "--cluster-user={}"),
                    Arg(cluster_pwd, "--cluster-pwd={}"),
                    Arg("register"),
                    Arg(name, "--name={}"),
                    Arg(pwd, "--pwd={}"),
                    Arg(descr, "--descr={}"),
                    Arg(auth, "--auth={}"),
                    Arg(os_user, "--os-user={}"),
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
                    Arg("cluster"),
                    Arg("admin"),
                    Arg(cluster, "--cluster={}"),
                    Arg(cluster_user, "--cluster-user={}"),
                    Arg(cluster_pwd, "--cluster-pwd={}"),
                    Arg("remove"),
                    Arg(name, "--name={}"),
                ),
            )

    @staticmethod
    def info(session: Session, cluster: str):
        return session.exec(
            Command(
                Arg("cluster"),
                Arg("info"),
                Arg(cluster, "--cluster={}"),
            )
        ).to_dict()

    @staticmethod
    def list(session: Session):
        return session.exec(
            Command(
                Arg("cluster"),
                Arg("list"),
            )
        ).to_list()

    @staticmethod
    def insert(
        session: Session,
        host: str,
        port: int,
        name: str | None = None,
        expiration_timeout: int = 60,
        lifetime_limit: int = 0,
        max_memory_size: int | None = None,
        max_memory_time_limit: int | None = None,
        security_level: str = "disabled",
        session_fault_tolerance_level: int = 0,
        load_balancing_mode: str = "performance",
        errors_count_threshold: int | None = None,
        kill_problem_processes: bool = True,
        kill_by_memory_with_dump: bool = False,
        allow_access_right_audit_events_recording: bool = False,
        ping_period: int = 0,
        ping_timeout: int = 0,
        agent_user: str | None = None,
        agent_pwd: str | None = None,
    ):
        cluster = session.exec(
            Command(
                Arg("cluster"),
                Arg("insert"),
                Arg(host, "--host={}"),
                Arg(port, "--port={}"),
                Arg(name, "--name={}"),
                Arg(expiration_timeout, "--expiration-timeout={}"),
                Arg(lifetime_limit, "--lifetime-limit={}"),
                Arg(max_memory_size, "--max-memory-size={}"),
                Arg(max_memory_time_limit, "--max-memory-time-limit={}"),
                Arg(security_level, "--security-level={}"),
                Arg(
                    session_fault_tolerance_level, "--session-fault-tolerance-level={}"
                ),
                Arg(load_balancing_mode, "--load-balancing-mode={}"),
                Arg(errors_count_threshold, "--errors-count-threshold={}"),
                Arg(b2yn(kill_problem_processes), "--kill-problem-processes={}"),
                Arg(b2yn(kill_by_memory_with_dump), "--kill-by-memory-with-dump={}"),
                Arg(
                    b2yn(allow_access_right_audit_events_recording),
                    "--allow-access-right-audit-events-recording={}",
                ),
                Arg(ping_period, "--ping-period={}"),
                Arg(ping_timeout, "--ping-timeout={}"),
                Arg(agent_user, "--agent-user={}"),
                Arg(agent_pwd, "--agent-pwd={}"),
            )
        ).to_dict()
        return str(cluster["cluster"])

    @staticmethod
    def update(
        session: Session,
        cluster: str,
        name: str | None = None,
        expiration_timeout: int | None = None,
        lifetime_limit: int | None = None,
        max_memory_size: int | None = None,
        max_memory_time_limit: int | None = None,
        security_level: str | None = None,
        session_fault_tolerance_level: int | None = None,
        load_balancing_mode: str | None = None,
        errors_count_threshold: int | None = None,
        kill_problem_processes: bool | None = None,
        kill_by_memory_with_dump: bool | None = None,
        allow_access_right_audit_events_recording: bool | None = None,
        ping_period: int | None = None,
        ping_timeout: int | None = None,
        agent_user: str | None = None,
        agent_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("cluster"),
                Arg("update"),
                Arg(cluster, "--cluster={}"),
                Arg(name, "--name={}"),
                Arg(expiration_timeout, "--expiration-timeout={}"),
                Arg(lifetime_limit, "--lifetime-limit={}"),
                Arg(max_memory_size, "--max-memory-size={}"),
                Arg(max_memory_time_limit, "--max-memory-time-limit={}"),
                Arg(security_level, "--security-level={}"),
                Arg(
                    session_fault_tolerance_level, "--session-fault-tolerance-level={}"
                ),
                Arg(load_balancing_mode, "--load-balancing-mode={}"),
                Arg(errors_count_threshold, "--errors-count-threshold={}"),
                Arg(b2yn(kill_problem_processes), "--kill-problem-processes={}"),
                Arg(b2yn(kill_by_memory_with_dump), "--kill-by-memory-with-dump={}"),
                Arg(
                    b2yn(allow_access_right_audit_events_recording),
                    "--allow-access-right-audit-events-recording={}",
                ),
                Arg(ping_period, "--ping-period={}"),
                Arg(ping_timeout, "--ping-timeout={}"),
                Arg(agent_user, "--agent-user={}"),
                Arg(agent_pwd, "--agent-pwd={}"),
            )
        )

    @staticmethod
    def remove(
        session: Session,
        cluster: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("cluster"),
                Arg("remove"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
            )
        )
