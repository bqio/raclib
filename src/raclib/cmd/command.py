from enum import Enum
from typing import Protocol


class SupportsStr(Protocol):
    def __str__(self) -> str: ...


class Flag:
    def __init__(
        self,
        state: bool,
        value: str,
    ):
        self.value = value if state else None

    def __str__(self) -> str:
        return self.value if self.value is not None else ""

    def is_valid(self) -> bool:
        return self.value is not None


class Arg:
    def __init__(self, value: SupportsStr, fmt: str = "{}"):
        self.value = value.value if isinstance(value, Enum) else value
        self.fmt = fmt

    def __str__(self) -> str:
        return self.fmt.format(self.value)

    def is_valid(self) -> bool:
        return self.value is not None


class Command:
    def __init__(self, *args: Arg | Flag):
        self.args = [str(arg) for arg in args if arg.is_valid()]

    def __str__(self) -> str:
        return " ".join(self.args)
