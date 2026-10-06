# raclib

Библиотека на языке Python, которая позволяет взаимодействовать с сервером администрирования 1С через утилиту RAC, предоставляя соответствующие сущности.

Возможности:

* синхронный и асинхронный (`asyncio`) интерфейсы;
* разбор вывода RAC в словари или `dataclass`;
* понятные исключения вместо текста из `stderr`;
* настраиваемая кодировка вывода и таймаут запуска `rac`.

## Установка

```bash
pip install raclib
```

Требуется Python 3.12+. Внешних зависимостей нет.

## Быстрый старт

```python
import raclib as rc

client = rc.Client("/opt/1cv8/x86_64/<version>/rac")
session = rc.Session(client, timeout=30)

print(rc.Cluster.list(session))
```

### Кодировка и таймаут

`rac.exe` на Windows печатает в `cp866`, на Linux и macOS — в UTF-8. Библиотека
подбирает кодировку по платформе, но её можно задать явно, если сервер настроен
иначе:

```python
session = rc.Session(client, encoding="utf-8")
```

`timeout` (в секундах) ограничивает ожидание ответа. Без него зависший или
недоступный сервер администрирования повесит вызывающий поток, поэтому
указывать его настоятельно рекомендуется.

### Примеры

Получение списка информационных баз кластера.

```python
import raclib as rc

client = rc.Client("/opt/1cv8/x86_64/<version>/rac")
session = rc.Session(client, timeout=30)
cluster = rc.Cluster.list(session)[0]["cluster"]

print(rc.Infobase.Summary.list(session, cluster))
```

Создание информационной базы.

```python
import raclib as rc

client = rc.Client("/opt/1cv8/x86_64/<version>/rac")
session = rc.Session(client, timeout=60)
cluster = rc.Cluster.list(session)[0]["cluster"]

infobase = rc.Infobase.create(
    session, cluster, "Тестовая база", "PostgreSQL", "localhost", "TestIB", "ru_RU"
)

print(infobase)
```

### Асинхронный режим

```python
import asyncio
import os

from raclib import AsyncClient, AsyncCluster, AsyncSession

client = AsyncClient(os.environ["RAC_PATH"])

servers = ["server1", "server2", "server3", "server4", "server5"]


async def main():
    # max_concurrency ограничивает число одновременных процессов rac.
    sessions = [AsyncSession(client, host, timeout=30, max_concurrency=8)
                for host in servers]
    tasks = (AsyncCluster.list(session) for session in sessions)

    for result in await asyncio.gather(*tasks):
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

Без `max_concurrency` число одновременных процессов `rac` равно числу задач, что
на сотнях кластеров исчерпывает память и дескрипторы.

## Обработка ошибок

Все ошибки RAC разбираются в типизированные исключения из `raclib.errors`:

```python
import raclib as rc
from raclib import errors

session = rc.Session(rc.Client("/opt/1cv8/x86_64/<version>/rac"), timeout=30)

try:
    rc.Cluster.info(session, "unknown-cluster-id")
except errors.ClusterNotFoundError:
    print("Кластер не найден")
except errors.RACTimeoutError:
    print("Сервер администрирования не ответил")
except errors.RACNotFoundError:
    print("Не найден или не запускается исполняемый файл rac")
except errors.UnknownError as exc:
    print("Незнакомая ошибка RAC:", exc)
```

Полный список — в [справочнике по ошибкам](https://bqio.github.io/raclib/reference/utils/#raclib.errors.UnknownError).

## Документация

https://bqio.github.io/raclib/

| Раздел | О чём |
| --- | --- |
| [Установка и подключение](https://bqio.github.io/raclib/guides/install/) | путь к `rac`, параметры сессии, кодировка, таймаут, отладка |
| [Кластеры](https://bqio.github.io/raclib/guides/clusters/) | кластеры, рабочие серверы, требования размещения |
| [Информационные базы](https://bqio.github.io/raclib/guides/infobases/) | создание, изменение, удаление, резервные копии |
| [Сеансы и соединения](https://bqio.github.io/raclib/guides/sessions/) | сеансы, соединения, блокировки, процессы, службы |
| [Обработка ошибок](https://bqio.github.io/raclib/guides/errors/) | какие исключения бывают и что с ними делать |
| [Асинхронный режим](https://bqio.github.io/raclib/guides/async/) | `asyncio`, `max_concurrency`, таймауты |
| [Рецепты](https://bqio.github.io/raclib/guides/recipes/) | готовые сценарии: вывод базы на обслуживание, поиск блокировок |
| [Справочник API](https://bqio.github.io/raclib/reference/) | все классы и методы |

## Разработка

```bash
pip install -e ".[dev]"

python -m unittest discover -s tests -t .   # тесты без внешних зависимостей
pytest -q                                   # то же самое через pytest
ruff check src tests tools

python tools/generate_async.py              # перегенерировать асинхронную ветку
python tools/generate_async.py --check      # проверить, что она актуальна
python tools/add_docstrings.py --check      # проверить покрытие докстрингами
```

Документация собирается MkDocs Material:

```bash
pip install -e ".[docs]"
mkdocs serve            # предпросмотр на http://127.0.0.1:8000
mkdocs build --strict   # так же, как в CI
```

Подробности — в разделе [Разработка](https://bqio.github.io/raclib/contributing/).

### Асинхронная ветка генерируется

Каталог `src/raclib/asynchronous/` **не редактируется вручную**: командные модули
генерируются из синхронных исходников скриптом `tools/generate_async.py`.
Единственный источник правды для команд — `src/raclib/cmd/`.

Раньше обе ветки были ручными копиями и успели разойтись: регекс разбора вывода
в асинхронной ветке требовал `\r` в конце строки, поэтому на Linux `to_list()`
молча возвращал пустой список. Теперь такое расхождение ловит тест
`tests/test_generator.py`, а CI запускает `generate_async.py --check`.

Вручную поддерживаются только:

| Файл | Почему |
| --- | --- |
| `asynchronous/_transport.py` | запуск процесса через `asyncio`, а не `subprocess` |
| `asynchronous/session.py` | `await`, семафор, псевдонимы `exec`/`call` |
| `asynchronous/errors.py` | реэкспорт общего модуля ошибок |
| `asynchronous/__init__.py` | публичный API пакета |

Общая логика (разбор вывода, таблица ошибок, утилиты) лежит в
`src/raclib/_shared.py` и используется обеими ветками.
