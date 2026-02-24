# raclib

Библиотека на языке Python, которая позволяет взаимодействовать с сервером администрирования 1С через утилиту RAC, предоставляя соответствующие сущности.

## Установка

```bash
pip install raclib
```

## API

https://bqio.github.io/raclib/

## Примеры

Получение списка кластеров.

```python
import raclib as rc

client = rc.Client("/opt/1cv8/x86_64/<version>/rac")
session = rc.Session(client)

print(rc.Cluster.list(session))
```

Получение списка информационных баз кластера.

```python
import raclib as rc

client = rc.Client("/opt/1cv8/x86_64/<version>/rac")
session = rc.Session(client)
cluster = rc.Cluster.list(session)[0]["cluster"]

print(rc.Infobase.Summary.list(session, cluster))
```

Создание информационной базы.

```python
import raclib as rc

client = rc.Client("/opt/1cv8/x86_64/<version>/rac")
session = rc.Session(client)
cluster = rc.Cluster.list(session)[0]["cluster"]

infobase = rc.Infobase.create(
    session, cluster, "Тестовая база", "PostgreSQL", "localhost", "TestIB", "ru_RU"
)

print(infobase)
```

Пример `async` реализации.

```python
from raclib import AsyncClient, AsyncSession, AsyncCluster

import os
import asyncio

client = AsyncClient(os.environ.get("RAC_PATH"))

session1 = AsyncSession(client, "server1")
session2 = AsyncSession(client, "server2")
session3 = AsyncSession(client, "server3")
session4 = AsyncSession(client, "server4")
session5 = AsyncSession(client, "server5")


async def main():
    tasks = (
        AsyncCluster.list(session1),
        AsyncCluster.list(session2),
        AsyncCluster.list(session3),
        AsyncCluster.list(session4),
        AsyncCluster.list(session5),
    )

    results = await asyncio.gather(*tasks)

    for result in results:
        print(result)  # В 3 раза быстрее, чем синхронный


if __name__ == "__main__":
    asyncio.run(main())
```
