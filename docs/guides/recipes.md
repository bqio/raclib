# Рецепты

Готовые куски кода под частые задачи. Все примеры предполагают, что сессия уже
создана:

```python
import raclib as rc
from raclib import errors

session = rc.Session(
    rc.Client("/opt/1cv8/x86_64/8.3.24.1548/rac"),
    host="cluster.example.com",
    timeout=30,
)
cluster = rc.Cluster.list(session)[0]["cluster"]
```

## Вывести все базы с числом сеансов

```python
summary = rc.Infobase.Summary.list(session, cluster)
summary.sort(key=lambda item: int(item.get("session-count", 0)), reverse=True)

for item in summary:
    print(f'{item["name"]:<30} сеансов: {item.get("session-count", 0)}')
```

## Завершить сеансы конкретного пользователя

```python
user = "ivanov"

for item in rc.UserSession.list(session, cluster):
    if item.get("user-name") != user:
        continue

    rc.UserSession.terminate(
        session,
        cluster,
        item["session"],
        error_message="Ваш сеанс завершён администратором",
    )
    print("завершён сеанс", item["session"])
```

## Найти виновника блокировок

```python
locks = rc.Lock.list(session, cluster)

# Группируем блокировки по сеансу, который их удерживает.
by_session: dict[str, list[dict]] = {}
for lock in locks:
    by_session.setdefault(str(lock["session"]), []).append(lock)

for user_session, items in sorted(by_session.items(), key=lambda kv: -len(kv[1])):
    print(f"сеанс {user_session}: блокировок {len(items)}")
```

## Разорвать все соединения базы

Полезно перед выводом базы на обслуживание.

```python
infobase_id = rc.Infobase.info(session, cluster, name="TestIB")["infobase"]

for server in rc.Server.list(session, cluster):
    for process in rc.Process.list(session, cluster, server["server"]):
        connections = rc.Connection.list(
            session, cluster, process=process["process"], infobase=infobase_id
        )
        for connection in connections:
            rc.Connection.disconnect(
                session, cluster, process["process"], connection["connection"]
            )
            print("разорвано соединение", connection["connection"])
```

## Вывести базу на обслуживание

Последовательность, которая не даст пользователям «зайти посередине»:
сначала запрещаем новые сеансы, затем завершаем существующие.

```python
infobase_id = rc.Infobase.info(session, cluster, name="TestIB")["infobase"]

# 1. Запретить новые сеансы и регламентные задания
rc.Infobase.update(
    session,
    cluster,
    infobase_id,
    sessions_deny=True,
    scheduled_jobs_deny=True,
    descr="Обслуживание до 04:00",
)

# 2. Завершить текущие сеансы
for item in rc.UserSession.list(session, cluster, infobase=infobase_id):
    rc.UserSession.terminate(
        session, cluster, item["session"], error_message="База на обслуживании"
    )

# 3. ... работы ...

# 4. Вернуть доступ
rc.Infobase.update(
    session, cluster, infobase_id, sessions_deny=False, scheduled_jobs_deny=False
)
```

## Настроить счётчик производительности

```python
rc.Counter.update(
    session,
    cluster,
    name="cpu-time",
    collection_time="0",
    group="process",
    filter_type="processor",
    duration=True,
    cpu_time=True,
    memory=True,
    descr="Базовые метрики процессов",
)

for value in rc.Counter.values(session, cluster, "cpu-time"):
    print(value)
```

Включённые метрики передаются как `True`, выключенные — как `False`,
неизменяемые — как `None`. В RAC это `analyze` / `not-analyze`.

## Ограничить ресурсы проблемной базы

```python
rc.Limit.update(
    session,
    cluster,
    name="memory-per-process",
    action="restart",           # или "ignore"
    memory=2_000_000,           # порог в единицах счётчика (КБ)
    error_message="Превышен лимит памяти, процесс перезапущен",
    descr="Защита от утечек памяти",
)
```

## Профиль безопасности с доступом к каталогу

Профиль безопасности ограничивает доступ к внешним ресурсам для кода в
безопасном режиме.

```python
rc.Profile.update(
    session,
    cluster,
    name="safe-profile",
    descr="Профиль для внешних обработок",
    config="deny",
    priv="deny",
    crypto="deny",
)

# Разрешить чтение из одного каталога
rc.Profile.ACL.Directory.update(
    session,
    cluster,
    name="safe-profile",
    alias="reports",
    physicalPath="/srv/1c/reports",
    allowedRead=True,
    allowedWrite=False,
)
```

Правила есть и для других типов ресурсов: `Profile.ACL.COM`,
`Profile.ACL.Addin` (внешние компоненты), `Profile.ACL.Module`,
`Profile.ACL.App`, `Profile.ACL.Inet` (интернет-ресурсы). Структура вызовов у
них одинаковая: `list`, `update`, `remove`.

## Собрать отчёт по всем кластерам

```python
import json

report = []
for cluster_item in rc.Cluster.list(session):
    cluster_id = cluster_item["cluster"]

    report.append(
        {
            "cluster": cluster_item["name"],
            "servers": len(rc.Server.list(session, cluster_id)),
            "infobases": len(rc.Infobase.Summary.list(session, cluster_id)),
            "sessions": len(rc.UserSession.list(session, cluster_id)),
        }
    )

print(json.dumps(report, ensure_ascii=False, indent=2))
```

## Устойчивый скрипт: одна ошибка не срывает обход

```python
import sys

results = {}

for cluster_item in rc.Cluster.list(session):
    cluster_id = cluster_item["cluster"]
    try:
        results[cluster_id] = rc.Infobase.Summary.list(session, cluster_id)
    except errors.RACTimeoutError:
        print(f"кластер {cluster_id}: таймаут", file=sys.stderr)
    except errors.ClusterNotFoundError:
        print(f"кластер {cluster_id}: не найден", file=sys.stderr)
    except errors.UnknownError as exc:
        print(f"кластер {cluster_id}: ошибка RAC: {exc}", file=sys.stderr)
```

## Разобрать вывод в `dataclass`

Если хочется работать с объектами, а не словарями:

```python
from dataclasses import dataclass


@dataclass
class ClusterRow:
    cluster: str
    name: str
    host: str
    port: int
    expiration_timeout: int
    lifetime_limit: int
    security_level: int


output = session.exec("cluster list")
clusters = output.to_list_of_dataclass(ClusterRow)

print(clusters[0].name)
```

!!! warning "Все поля вывода должны быть объявлены"

    `to_dataclass` передаёт в конструктор **все** ключи из вывода RAC. Если
    в датаклассе не объявить какое-то поле, будет `TypeError`. Для устойчивости
    к версиям 1С объявляйте поля с значениями по умолчанию или оставайтесь на
    словарях.
