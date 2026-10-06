"""Асинхронный двойник :class:`raclib.client.Client`.

Класс общий для обеих веток и объявлен в :mod:`raclib._shared`; здесь
оставлен реэкспорт под именем ``AsyncClient`` для единообразия API.
"""

from .._shared import Client as AsyncClient

__all__ = ["AsyncClient"]
