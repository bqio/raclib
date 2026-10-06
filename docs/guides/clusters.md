# Кластеры

Кластер — верхний уровень иерархии 1С: в нём живут рабочие серверы,
информационные базы, сеансы и настройки. Почти любая операция начинается с
идентификатора кластера.

## Получить список кластеров

```python
import raclib as rc

session = rc.Session(rc.Client("/opt/1cv8/x86_64/8.3.24.1548/rac"), timeout=30)

for cluster in rc.Cluster.list(session):
    print(cluster["cluster"], cluster["name"], cluster["host"])
```

Метод возвращает `list[dict]`. Ключи соответствуют полям вывода RAC, дефисы
заменены на подчёркивания, а числовые значения приведены к `int`:

```python
[
    {
        "cluster": "6a4c0b3f-1111-2222-3333-444455556666",
        "name": "Production",
        "host": "rac1.local",
        "port": 1541,
        "expiration_timeout": 60,
        "lifetime_limit": 0,
    },
]
```

## Параметры кластера

```python
cluster_id = rc.Cluster.list(session)[0]["cluster"]
info = rc.Cluster.info(session, cluster_id)

print(info["security_level"], info["load_balancing_mode"])
```

### Изменить параметры

Меняются только явно переданные параметры: `None` означает «оставить как есть».

```python
rc.Cluster.update(
    session,
    cluster_id,
    name="Production (обновлён)",
    expiration_timeout=120,
    load_balancing_mode="memory",
    kill_problem_processes=True,
)
```

!!! note "Сбросить параметр в значение по умолчанию нельзя"

    `Cluster.update` не различает «не задано» и «очистить»: значение `None`
    пропускается. Чтобы вернуть параметр к значению по умолчанию, задайте его
    явно тем же значением, что используется в RAC.

### Логические параметры

Параметры вида `kill_problem_processes` принимают `bool`, а в RAC
преобразуются в `yes`/`no`:

| Python | В команде `rac` |
| --- | --- |
| `True` | `--kill-problem-processes=yes` |
| `False` | `--kill-problem-processes=no` |
| `None` | параметр не передаётся |

## Рабочие серверы

```python
for server in rc.Server.list(session, cluster_id):
    print(server["server"], server["name"], server["port_range"])
```

### Зарегистрировать сервер

Сервер должен быть доступен по сети: RAC обращается к его агенту.

```python
server_id = rc.Server.insert(
    session,
    cluster_id,
    agent_host="rac2.local",
    agent_port=1541,
    port_range="1560:1591",
    name="Worker 2",
    using="normal",
    infobases_limit=10,
)

print(server_id)   # идентификатор зарегистрированного сервера
```

Методы `insert` (`Cluster.insert`, `Server.insert`, `Rule.insert`) возвращают
строку с идентификатором созданного объекта, а не словарь.

### Удалить сервер

```python
rc.Server.remove(session, cluster_id, server_id)
```

Центральный сервер кластера удалить нельзя — RAC ответит ошибкой, и библиотека
поднимет `raclib.errors.ServerIsMainError`.

## Требования размещения

Требования определяют, какие информационные базы могут выполняться на
конкретном рабочем сервере.

```python
rule_id = rc.Rule.insert(
    session,
    cluster_id,
    server_id,
    position=1,
    object_type="Infobase",
    infobase_name="TestIB",
    rule_type="Assign",
)

rc.Rule.apply(session, cluster_id)          # применить требования
rc.Rule.remove(session, cluster_id, server_id, rule_id)
```

## Администраторы кластера

```python
rc.Cluster.Admin.register(
    session,
    cluster_id,
    name="admin2",
    pwd="secret",
    auth="pwd",
    descr="Дежурный администратор",
)

for admin in rc.Cluster.Admin.list(session, cluster_id):
    print(admin["name"], admin["auth"])
```

!!! warning "Последнего администратора удалить нельзя"

    RAC не позволит удалить последнего администратора с разрешённой
    аутентификацией по паролю — библиотека поднимет
    `raclib.errors.AgentAdminCreateError`.

## Создать и удалить кластер

```python
new_cluster = rc.Cluster.insert(
    session,
    host="rac1.local",
    port=1540,
    name="Test cluster",
    security_level="basic",
    agent_user="agent-admin",
    agent_pwd="agent-secret",
)
```

Для создания кластера нужны права администратора **агента** кластера, поэтому
передаются `agent_user`/`agent_pwd`, а не `cluster_user`/`cluster_pwd`.

```python
rc.Cluster.remove(session, new_cluster, cluster_user="admin", cluster_pwd="secret")
```

!!! danger "Удаление кластера необратимо"

    Вместе с кластером удаляются его настройки, рабочие серверы и регистрация
    информационных баз. Сами базы данных на сервере СУБД при этом **не**
    удаляются.
