from .command import Command, Arg, Flag
from ..session import Session
from ..utils import b2of, b2da, b2yn


class Infobase:
    @staticmethod
    def info(
        session: Session,
        cluster: str,
        infobase: str | None = None,
        name: str | None = None,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.exec(
            Command(
                Arg("infobase"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("info"),
                Arg(infobase, "--infobase={}"),
                Arg(name, "--name={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
            )
        ).to_dict()

    class Summary:
        @staticmethod
        def info(
            session: Session,
            cluster: str,
            infobase: str | None = None,
            name: str | None = None,
            cluster_user: str | None = None,
            cluster_pwd: str | None = None,
        ):
            return session.exec(
                Command(
                    Arg("infobase"),
                    Arg(cluster, "--cluster={}"),
                    Arg(cluster_user, "--cluster-user={}"),
                    Arg(cluster_pwd, "--cluster-pwd={}"),
                    Arg("summary"),
                    Arg("info"),
                    Arg(infobase, "--infobase={}"),
                    Arg(name, "--name={}"),
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
                    Arg("infobase"),
                    Arg(cluster, "--cluster={}"),
                    Arg(cluster_user, "--cluster-user={}"),
                    Arg(cluster_pwd, "--cluster-pwd={}"),
                    Arg("summary"),
                    Arg("list"),
                )
            ).to_list()

        @staticmethod
        def update(
            session: Session,
            cluster: str,
            infobase: str | None = None,
            name: str | None = None,
            descr: str | None = None,
            cluster_user: str | None = None,
            cluster_pwd: str | None = None,
        ):
            return session.call(
                Command(
                    Arg("infobase"),
                    Arg(cluster, "--cluster={}"),
                    Arg(cluster_user, "--cluster-user={}"),
                    Arg(cluster_pwd, "--cluster-pwd={}"),
                    Arg("summary"),
                    Arg("update"),
                    Arg(infobase, "--infobase={}"),
                    Arg(name, "--name={}"),
                    Arg(descr, "--descr={}"),
                )
            )

    @staticmethod
    def create(
        session: Session,
        cluster: str,
        name: str,
        dbms: str,
        db_server: str,
        db_name: str,
        locale: str,
        db_user: str | None = None,
        db_pwd: str | None = None,
        descr: str | None = None,
        date_offset: str = "0",
        security_level: str = "disabled",
        scheduled_jobs_deny: bool = False,
        license_distribution: bool = True,
        create_database: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        infobase = session.exec(
            Command(
                Arg("infobase"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("create"),
                Flag(create_database, "--create-database"),
                Arg(name, "--name={}"),
                Arg(dbms, "--dbms={}"),
                Arg(db_server, "--db-server={}"),
                Arg(db_name, "--db-name={}"),
                Arg(locale, "--locale={}"),
                Arg(db_user, "--db-user={}"),
                Arg(db_pwd, "--db-pwd={}"),
                Arg(descr, "--descr={}"),
                Arg(date_offset, "--date-offset={}"),
                Arg(security_level, "--security-level={}"),
                Arg(b2of(scheduled_jobs_deny), "--scheduled-jobs-deny={}"),
                Arg(b2da(license_distribution), "--license-distribution={}"),
            )
        ).to_dict()
        return str(infobase["infobase"])

    @staticmethod
    def update(
        session: Session,
        cluster: str,
        infobase: str | None = None,
        name: str | None = None,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        dbms: str | None = None,
        db_server: str | None = None,
        db_name: str | None = None,
        db_user: str | None = None,
        db_pwd: str | None = None,
        descr: str | None = None,
        denied_from: str | None = None,
        denied_message: str | None = None,
        denied_parameter: str | None = None,
        denied_to: str | None = None,
        permission_code: str | None = None,
        sessions_deny: bool | None = None,
        scheduled_jobs_deny: bool | None = None,
        license_distribution: bool | None = None,
        external_session_manager_connection_string: str | None = None,
        external_session_manager_required: bool | None = None,
        reserve_working_processes: bool | None = None,
        security_profile_name: str | None = None,
        safe_mode_security_profile_name: str | None = None,
        disable_local_speech_to_text: bool | None = None,
        configuration_unload_delay_by_working_process_without_active_users: (
            int | None
        ) = None,
        minimum_scheduled_jobs_start_period_without_active_users: int | None = None,
        maximum_scheduled_jobs_start_shift_without_active_users: int | None = None,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("infobase"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("update"),
                Arg(infobase, "--infobase={}"),
                Arg(name, "--name={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Arg(dbms, "--dbms={}"),
                Arg(db_server, "--db-server={}"),
                Arg(db_name, "--db-name={}"),
                Arg(db_user, "--db-user={}"),
                Arg(db_pwd, "--db-pwd={}"),
                Arg(descr, "--descr={}"),
                Arg(denied_from, "--denied-from={}"),
                Arg(denied_message, "--denied-message={}"),
                Arg(denied_parameter, "--denied-parameter={}"),
                Arg(denied_to, "--denied-to={}"),
                Arg(permission_code, "--permission-code={}"),
                Arg(b2of(sessions_deny), "--sessions-deny={}"),
                Arg(b2of(scheduled_jobs_deny), "--scheduled-jobs-deny={}"),
                Arg(b2da(license_distribution), "--license-distribution={}"),
                Arg(
                    external_session_manager_connection_string,
                    "--external-session-manager-connection-string={}",
                ),
                Arg(
                    b2yn(external_session_manager_required),
                    "--external-session-manager-required={}",
                ),
                Arg(b2yn(reserve_working_processes), "--reserve-working-processes={}"),
                Arg(security_profile_name, "--security-profile-name={}"),
                Arg(
                    safe_mode_security_profile_name,
                    "--safe-mode-security-profile-name={}",
                ),
                Arg(
                    b2yn(disable_local_speech_to_text),
                    "--disable-local-speech-to-text={}",
                ),
                Arg(
                    configuration_unload_delay_by_working_process_without_active_users,
                    "--configuration-unload-delay-by-working-process-without-active-users={}",
                ),
                Arg(
                    minimum_scheduled_jobs_start_period_without_active_users,
                    "--minimum-scheduled-jobs-start-period-without-active-users={}",
                ),
                Arg(
                    maximum_scheduled_jobs_start_shift_without_active_users,
                    "--maximum-scheduled-jobs-start-shift-without-active-users={}",
                ),
            )
        )

    @staticmethod
    def drop(
        session: Session,
        cluster: str,
        infobase: str | None = None,
        name: str | None = None,
        infobase_user: str | None = None,
        infobase_pwd: str | None = None,
        drop_database: bool = False,
        clear_database: bool = False,
        cluster_user: str | None = None,
        cluster_pwd: str | None = None,
    ):
        return session.call(
            Command(
                Arg("infobase"),
                Arg(cluster, "--cluster={}"),
                Arg(cluster_user, "--cluster-user={}"),
                Arg(cluster_pwd, "--cluster-pwd={}"),
                Arg("drop"),
                Arg(infobase, "--infobase={}"),
                Arg(name, "--name={}"),
                Arg(infobase_user, "--infobase-user={}"),
                Arg(infobase_pwd, "--infobase-pwd={}"),
                Flag(drop_database, "--drop-database"),
                Flag(clear_database, "--clear-database"),
            )
        )
