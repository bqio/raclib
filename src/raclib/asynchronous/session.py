from .client import AsyncClient
from ..cmd.command import Command
from .. import errors
from ..session import RawOutput

import asyncio


class AsyncSession:
    def __init__(
        self,
        async_client: AsyncClient,
        host: str = "localhost",
        port: int = 1545,
        debug: bool = False,
    ) -> None:
        self.client = async_client
        self.host = host
        self.port = port
        self._debug = debug

    async def async_exec(self, command: Command):
        args: list[str] = [
            f"{self.host}:{self.port}",
        ] + command.args
        if self._debug:
            print("[DEBUG]", args)
        try:
            process = await asyncio.create_subprocess_exec(
                self.client.rac_path,
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                stderr = stderr.decode(encoding="cp866")
                raise errors.handler(stderr)
            else:
                stdout = stdout.decode(encoding="cp866")
                if self._debug:
                    print(stdout)
                return RawOutput(stdout)
        except FileNotFoundError:
            raise errors.RACNotFoundError

    async def async_call(self, command: Command):
        await self.async_exec(command)
