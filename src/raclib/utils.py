from typing import TypeVar

T = TypeVar("T")


def get_array_chunks(arr: list[tuple[str, str]], n: int) -> list[list[tuple[str, str]]]:
    return [arr[i : i + n] for i in range(0, len(arr), n)]


def dict_entry_count(lines: list[str]) -> int:
    return next((i for i, line in enumerate(lines) if line == ""), len(lines))


def b2yn(b: bool | None) -> str | None:
    match b:
        case True:
            return "yes"
        case False:
            return "no"
        case None:
            return None


def b2of(b: bool | None) -> str | None:
    match b:
        case True:
            return "on"
        case False:
            return "off"
        case None:
            return None


def b2da(b: bool | None) -> str | None:
    match b:
        case True:
            return "allow"
        case False:
            return "deny"
        case None:
            return None


def b2ana(b: bool | None) -> str | None:
    match b:
        case True:
            return "analyze"
        case False:
            return "not-analyze"
        case None:
            return None


def any2b(an: str | int) -> bool | str | int:
    match an:
        case "yes":
            return True
        case "no":
            return False
        case "on":
            return True
        case "off":
            return False
        case "allow":
            return True
        case "deny":
            return False
        case "analyze":
            return True
        case "not-analyze":
            return False
        case _:
            return an
