from typing import TypeVar, Type

from .client import AsyncClient
from ..cmd.command import Command
from .. import errors
from ..utils import get_array_chunks, dict_entry_count

import asyncio
import re

T = TypeVar("T")
LIST_DICT_REGEX = r"(.*?)\s+:\s?(.*)\r"


class RawOutput:
    def __init__(self, output: str) -> None:
        self.output = output

    def to_str(self) -> str:
        return self.output.strip()

    def to_dict(self) -> dict[str, str | int]:
        matches: list[tuple[str, str]] = re.findall(LIST_DICT_REGEX, self.output)
        _dict: dict[str, str | int] = {}
        for prop in matches:
            if prop[1].isdecimal():
                _dict[prop[0].replace("-", "_")] = int(prop[1])
            else:
                _dict[prop[0].replace("-", "_")] = prop[1].replace('"', "")
        # for key in _dict:
        #     _dict[key] = any2b(_dict[key])
        return _dict

    def to_dataclass(self, dc: Type[T]) -> T:
        return dc(**self.to_dict())

    def to_list_of_dataclass(self, dc: Type[T]) -> list[T]:
        return [dc(**entry) for entry in self.to_list()]

    def to_list(self) -> list[dict[str, str | int]]:
        entry_count = dict_entry_count(self.output.splitlines())
        matches: list[tuple[str, str]] = re.findall(LIST_DICT_REGEX, self.output)
        if matches == []:
            return []
        chunks = get_array_chunks(matches, entry_count)
        _list: list[dict[str, str | int]] = []
        for chunk in chunks:
            _dict: dict[str, str | int] = {}
            for prop in chunk:
                if prop[1].isdecimal():
                    _dict[prop[0].replace("-", "_")] = int(prop[1])
                else:
                    _dict[prop[0].replace("-", "_")] = prop[1].replace('"', "")
            # for key in _dict:
            #     _dict[key] = any2b(_dict[key])
            _list.append(_dict)
        return _list


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
