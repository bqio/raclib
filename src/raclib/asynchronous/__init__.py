"""Асинхронная ветка raclib.

Командные модули этого пакета **генерируются** из синхронной ветки скриптом
``tools/generate_async.py``; вручную поддерживаются только ``_transport.py``,
``errors.py``, ``client.py``, ``session.py`` и этот файл. Правки команд вносите
в ``src/raclib/cmd/`` и запускайте генератор, иначе CI сообщит о расхождении.
"""

from .._shared import Client as AsyncClient
from .._shared import RawOutput
from ..errors import RACNotFoundError, RACTimeoutError
from .cmd.agent import AsyncAgent
from .cmd.bindatastorage import AsyncBinaryDataStorage
from .cmd.cluster import AsyncCluster
from .cmd.connection import AsyncConnection
from .cmd.counter import AsyncCounter
from .cmd.infobase import AsyncInfobase
from .cmd.limit import AsyncLimit
from .cmd.lock import AsyncLock
from .cmd.manager import AsyncManager
from .cmd.process import AsyncProcess
from .cmd.profile import AsyncProfile
from .cmd.rule import AsyncRule
from .cmd.server import AsyncServer
from .cmd.service import AsyncService
from .cmd.servicesetting import AsyncServiceSetting
from .cmd.session import AsyncUserSession
from .session import AsyncSession

__all__ = [
    "AsyncClient",
    "AsyncSession",
    "RawOutput",
    "RACNotFoundError",
    "RACTimeoutError",
    "AsyncAgent",
    "AsyncBinaryDataStorage",
    "AsyncCluster",
    "AsyncConnection",
    "AsyncCounter",
    "AsyncInfobase",
    "AsyncLimit",
    "AsyncLock",
    "AsyncManager",
    "AsyncProcess",
    "AsyncProfile",
    "AsyncRule",
    "AsyncServer",
    "AsyncService",
    "AsyncServiceSetting",
    "AsyncUserSession",
]
