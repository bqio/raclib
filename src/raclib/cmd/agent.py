from .command import Command, Arg
from ..session import Session


class Agent:
    class Admin:
        @staticmethod
        def list(
            session: Session,
            agent_user: str | None = None,
            agent_pwd: str | None = None,
        ):
            return session.exec(
                Command(
                    Arg("agent"),
                    Arg(agent_user, "--agent-user={}"),
                    Arg(agent_pwd, "--agent-pwd={}"),
                    Arg("admin"),
                    Arg("list"),
                )
            ).to_list()

        @staticmethod
        def register(
            session: Session,
            name: str,
            pwd: str | None = None,
            auth: str = "pwd",
            descr: str | None = None,
            os_user: str | None = None,
            agent_user: str | None = None,
            agent_pwd: str | None = None,
        ):
            return session.call(
                Command(
                    Arg("agent"),
                    Arg(agent_user, "--agent-user={}"),
                    Arg(agent_pwd, "--agent-pwd={}"),
                    Arg("admin"),
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
            name: str,
            agent_user: str | None = None,
            agent_pwd: str | None = None,
        ):
            return session.call(
                Command(
                    Arg("agent"),
                    Arg(agent_user, "--agent-user={}"),
                    Arg(agent_pwd, "--agent-pwd={}"),
                    Arg("admin"),
                    Arg("remove"),
                    Arg(name, "--name={}"),
                ),
            )

    @staticmethod
    def version(session: Session):
        return session.exec(Command(Arg("agent"), Arg("version"))).to_str()
