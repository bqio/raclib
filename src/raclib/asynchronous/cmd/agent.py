from ...cmd.command import Command, Arg
from ..session import AsyncSession


class AsyncAgent:
    class Admin:
        @staticmethod
        async def list(
            session: AsyncSession,
            agent_user: str | None = None,
            agent_pwd: str | None = None,
        ):
            output = await session.async_exec(
                Command(
                    Arg("agent"),
                    Arg(agent_user, "--agent-user={}"),
                    Arg(agent_pwd, "--agent-pwd={}"),
                    Arg("admin"),
                    Arg("list"),
                )
            )
            return output.to_list()

        @staticmethod
        async def register(
            session: AsyncSession,
            name: str,
            pwd: str | None = None,
            auth: str = "pwd",
            descr: str | None = None,
            os_user: str | None = None,
            agent_user: str | None = None,
            agent_pwd: str | None = None,
        ):
            return await session.async_call(
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
        async def remove(
            session: AsyncSession,
            name: str,
            agent_user: str | None = None,
            agent_pwd: str | None = None,
        ):
            return await session.async_call(
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
    async def version(session: AsyncSession):
        output = await session.async_exec(Command(Arg("agent"), Arg("version")))
        return output.to_str()
