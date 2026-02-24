from .command import Command, Arg
from ..session import Session
from ..utils import b2yn


class Server:
    @staticmethod
    def info(
        session: Session,
        cluster: str,
        server: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("server"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(server, "--server={}"),
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
                Arg("server"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("list"),
            )
        ).to_list()

    @staticmethod
    def insert(
        session: Session,
        cluster: str,
        agent_host: str,
        agent_port: int,
        port_range: str,
        name: str | None = None,
        using: str = "main",
        infobases_limit: int = 8,
        memory_limit: int | None = None,
        connections_limit: int = 256,
        cluster_port: int | None = None,
        dedicate_managers: str = "all",
        safe_working_processess_memory_limit: int | None = None,
        safe_call_memory_limit: int | None = None,
        critical_total_memory: int | None = None,
        temporary_allowed_total_memory: int | None = None,
        temporary_allowed_total_memory_time_limit: int = 300,
        service_principal_name: str | None = None,
        restart_schedule: str | None = None,
        add_prohibiting_assignment_rule: bool | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        server = session.exec(
            Command(
                Arg("server"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("insert"),
                Arg(agent_host, "--agent-host={}"),
                Arg(agent_port, "--agent-port={}"),
                Arg(str(port_range), "--port-range={}"),
                Arg(name, "--name={}"),
                Arg(using, "--using={}"),
                Arg(infobases_limit, "--infobases-limit={}"),
                Arg(memory_limit, "--memory-limit={}"),
                Arg(connections_limit, "--connections-limit={}"),
                Arg(cluster_port, "--cluster-port={}"),
                Arg(dedicate_managers, "--dedicate-managers={}"),
                Arg(
                    safe_working_processess_memory_limit,
                    "--safe-working-processess-memory-limit={}",
                ),
                Arg(safe_call_memory_limit, "--safe-call-memory-limit={}"),
                Arg(critical_total_memory, "--critical-total-memory={}"),
                Arg(
                    temporary_allowed_total_memory,
                    "--temporary-allowed-total-memory={}",
                ),
                Arg(
                    temporary_allowed_total_memory_time_limit,
                    "--temporary-allowed-total-memory-time-limit={}",
                ),
                Arg(service_principal_name, "--service-principal-name={}"),
                Arg(
                    restart_schedule,
                    "--restart-schedule={}",
                ),
                Arg(
                    b2yn(add_prohibiting_assignment_rule),
                    "--add-prohibiting-assignment-rule={}",
                ),
            )
        ).to_dict()
        return str(server["server"])

    @staticmethod
    def update(
        session: Session,
        cluster: str,
        server: str,
        port_range: str | None = None,
        using: str | None = None,
        infobases_limit: int | None = None,
        memory_limit: int | None = None,
        connections_limit: int | None = None,
        dedicate_managers: str | None = None,
        safe_working_processess_memory_limit: int | None = None,
        safe_call_memory_limit: int | None = None,
        critical_total_memory: int | None = None,
        temporary_allowed_total_memory: int | None = None,
        temporary_allowed_total_memory_time_limit: int | None = None,
        service_principal_name: str | None = None,
        restart_schedule: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("server"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("update"),
                Arg(server, "--server={}"),
                Arg(using, "--using={}"),
                Arg(dedicate_managers, "--dedicate-managers={}"),
                Arg(port_range, "--port-range={}"),
                Arg(infobases_limit, "--infobases-limit={}"),
                Arg(memory_limit, "--memory-limit={}"),
                Arg(connections_limit, "--connections-limit={}"),
                Arg(
                    safe_working_processess_memory_limit,
                    "--safe-working-processess-memory-limit={}",
                ),
                Arg(safe_call_memory_limit, "--safe-call-memory-limit={}"),
                Arg(critical_total_memory, "--critical-total-memory={}"),
                Arg(
                    temporary_allowed_total_memory,
                    "--temporary-allowed-total-memory={}",
                ),
                Arg(
                    temporary_allowed_total_memory_time_limit,
                    "--temporary-allowed-total-memory-time-limit={}",
                ),
                Arg(service_principal_name, "--service-principal-name={}"),
                Arg(restart_schedule, "--restart-schedule={}"),
            )
        )

    @staticmethod
    def remove(
        session: Session,
        cluster: str,
        server: str,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("server"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("remove"),
                Arg(server, "--server={}"),
            )
        )
