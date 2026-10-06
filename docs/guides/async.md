# Асинхронный режим

Асинхронная ветка нужна, когда команд много и они уходят на разные серверы:
`rac` — внешний процесс, поэтому ожидание ответа можно совместить. Набор
методов полностью совпадает с синхронным, меняется только способ вызова.

```python
import asyncio

from raclib import AsyncClient, AsyncCluster, AsyncSession

client = AsyncClient("/opt/1cv8/x86_64/8.3.24.1548/rac")

servers = ["server1", "server2", "server3", "server4", "server5"]


async def main():
    sessions = [AsyncSession(client, host, timeout=30) for host in servers]
    results = await asyncio.gather(*(AsyncCluster.list(s) for s in sessions))

    for host, clusters in zip(servers, results):
        print(host, clusters)


asyncio.run(main())
```

## Что отличается от синхронной ветки

| | Синхронная | Асинхронная |
| --- | --- | --- |
| Клиент | `Client` | `AsyncClient` |
| Сессия | `Session` | `AsyncSession` |
| Команды | `Cluster.list(session)` | `await AsyncCluster.list(session)` |
| Метод сессии | `session.exec(...)` | `await session.async_exec(...)` |
| Ограничение параллелизма | — | `max_concurrency` |

`Session` и `AsyncSession` принимают одинаковые параметры
(`host`, `port`, `timeout`, `encoding`, `debug`), у асинхронной дополнительно
есть `max_concurrency`. `AsyncSession` также поддерживает псевдонимы
`exec`/`call`, поэтому код, написанный под синхронную сессию, переносится
почти без изменений:

```python
output = await session.exec("cluster list")   # работает наравне с async_exec
```

## Ограничение параллелизма

!!! warning "`asyncio.gather` без ограничения создаёт процесс на каждую задачу"

    Каждая команда — это отдельный процесс `rac`. На двух сотнях кластеров
    `asyncio.gather` запустит двести процессов одновременно, что исчерпает
    память и дескрипторы.

Параметр `max_concurrency` ограничивает число одновременных запусков через
семафор:

```python
session = AsyncSession(client, host, timeout=30, max_concurrency=8)
```

Ограничение действует **в рамках одной сессии**. Если у вас много сессий,
задайте его на каждой:

```python
sessions = [
    AsyncSession(client, host, timeout=30, max_concurrency=8)
    for host in servers
]
```

## Типовые сценарии

### Обход всех серверов

```python
async def clusters_of(host: str):
    session = AsyncSession(client, host, timeout=30)
    return host, await AsyncCluster.list(session)


async def main():
    results = await asyncio.gather(
        *(clusters_of(host) for host in servers), return_exceptions=True
    )

    for result in results:
        if isinstance(result, Exception):
            print("не удалось:", result)
        else:
            print(result)
```

`return_exceptions=True` не даёт одной недоступной машине сорвать весь обход.

### Собрать сеансы по всем базам

```python
async def sessions_of(host: str) -> list[dict]:
    session = AsyncSession(client, host, timeout=30, max_concurrency=8)
    cluster = (await AsyncCluster.list(session))[0]["cluster"]

    infobases = await AsyncInfobase.Summary.list(session, cluster)
    batches = await asyncio.gather(
        *(
            AsyncUserSession.list(session, cluster, infobase=ib["infobase"])
            for ib in infobases
        )
    )
    return [item for batch in batches for item in batch]
```

Здесь семафор работает дважды: он ограничивает и число баз в обработке, и
число одновременных процессов `rac`.

### Периодический мониторинг

```python
async def watch(interval: int = 60) -> None:
    session = AsyncSession(client, "cluster.example.com", timeout=30)

    while True:
        cluster = (await AsyncCluster.list(session))[0]["cluster"]
        locks = await AsyncLock.list(session, cluster)

        if locks:
            print(f"блокировок: {len(locks)}")

        await asyncio.sleep(interval)
```

## Таймауты

`timeout` в асинхронной ветке работает так же, как в синхронной, но с важным
отличием: по истечении таймаута процесс `rac` **принудительно завершается**,
чтобы не остались висящие процессы. Поднимается
`raclib.errors.RACTimeoutError`.

```python
try:
    await AsyncCluster.list(session)
except errors.RACTimeoutError:
    print("сервер не ответил")
```

Дополнительно можно ограничить всю операцию целиком средствами `asyncio`:

```python
await asyncio.wait_for(AsyncCluster.list(session), timeout=15)
```

## Ограничение окружения

`asyncio` создаёт каналы для подпроцессов через именованные pipe-объекты.
Некоторые ограниченные среды (контейнеры с урезанными правами, песочницы) их
запрещают — тогда запуск упадёт с `PermissionError` ещё до старта `rac`. Это
ограничение среды, а не библиотеки: в таком окружении используйте синхронную
ветку.
