# Информационные базы

## Список баз кластера

Полный список с параметрами каждой базы:

```python
import raclib as rc

session = rc.Session(rc.Client("/opt/1cv8/x86_64/8.3.24.1548/rac"), timeout=30)
cluster = rc.Cluster.list(session)[0]["cluster"]

for infobase in rc.Infobase.Summary.list(session, cluster):
    print(infobase["infobase"], infobase["name"], infobase["db_name"])
```

`Infobase.Summary` — это сводки: они содержат суммарные показатели по базе
(число сеансов, соединений, занятые ресурсы). Параметры конкретной базы — у
`Infobase.info`:

```python
info = rc.Infobase.info(session, cluster, name="TestIB")
print(info["dbms"], info["db_server"], info["db_name"])
```

Базу можно указать либо идентификатором (`infobase=`), либо именем (`name=`).

## Создать базу

```python
infobase_id = rc.Infobase.create(
    session,
    cluster,
    name="TestIB",
    dbms="PostgreSQL",
    db_server="db.example.com",
    db_name="TestIB",
    locale="ru_RU",
    db_user="postgres",
    db_pwd="pg-secret",
    descr="Тестовая база",
)

print(infobase_id)
```

Метод возвращает строку с идентификатором созданной базы.

### `create_database`: регистрация или создание

По умолчанию база **только регистрируется** в кластере: предполагается, что
база данных на сервере СУБД уже существует. Если её нет, RAC ответит ошибкой, и
библиотека поднимет `raclib.errors.InfobaseDatabaseNotFoundError` с подсказкой:

```python
rc.Infobase.create(
    session,
    cluster,
    name="TestIB",
    dbms="PostgreSQL",
    db_server="db.example.com",
    db_name="TestIB",
    locale="ru_RU",
    db_user="postgres",
    db_pwd="pg-secret",
    create_database=True,     # создать базу данных на сервере СУБД
)
```

| `create_database` | Что произойдёт |
| --- | --- |
| `False` (по умолчанию) | база регистрируется в кластере, БД должна существовать |
| `True` | RAC создаст базу данных на сервере СУБД |

### Основные параметры

| Параметр | Значение |
| --- | --- |
| `dbms` | `PostgreSQL`, `MSSQLServer`, `IBMDB2`, `Oracle`, `File` |
| `db_server` | `host` или `host:port` |
| `db_name` | имя базы на сервере СУБД |
| `locale` | код локали, например `ru_RU` |
| `date_offset` | смещение даты в часах относительно времени сервера |
| `security_level` | `disabled`, `basic`, `integrity` |
| `scheduled_jobs_deny` | запретить регламентные задания |
| `license_distribution` | разрешить распределение лицензий |

## Изменить базу

```python
rc.Infobase.update(
    session,
    cluster,
    infobase_id,
    name="TestIB (prod)",
    sessions_deny=True,           # запретить новые сеансы
    scheduled_jobs_deny=True,
    descr="Выведена на обслуживание",
)
```

Логические параметры (`sessions_deny`, `scheduled_jobs_deny`,
`license_distribution`) преобразуются в `on`/`off`; параметр `None` не
передаётся, то есть остаётся прежним.

### Блокировка подключений по расписанию

```python
rc.Infobase.update(
    session,
    cluster,
    infobase_id,
    denied_from="2026-03-01 02:00:00",
    denied_to="2026-03-01 04:00:00",
    denied_message="База на обслуживании",
    permission_code="tech-window",   # код для входа в обход блокировки
)
```

## Удалить базу

```python
rc.Infobase.drop(session, cluster, infobase_id)
```

По умолчанию из кластера удаляется **только регистрация** базы: база данных на
сервере СУБД остаётся нетронутой. Чтобы удалить или очистить и её, нужны
учётные данные сервера СУБД:

```python
# Удалить и регистрацию, и саму базу данных
rc.Infobase.drop(
    session,
    cluster,
    infobase_id,
    db_user="postgres",
    db_pwd="pg-secret",
    drop_database=True,
)

# Очистить данные, оставив базу данных существовать
rc.Infobase.drop(
    session,
    cluster,
    infobase_id,
    db_user="postgres",
    db_pwd="pg-secret",
    clear_database=True,
)
```

!!! danger "Проверьте, что вам нужен `drop_database`"

    Без флага `drop_database` вы потеряете только запись о базе в кластере.
    С флагом — данные безвозвратно. Убедитесь, что у вас есть резервная копия.

## Хранилища двоичных данных

Если включено разделение данных, двоичные данные базы лежат в отдельном
хранилище. Для него доступны резервное копирование и восстановление:

```python
# Список хранилищ базы
for storage in rc.BinaryDataStorage.list(session, cluster, infobase_id):
    print(storage)

# Полная резервная копия в каталог на рабочем сервере
rc.BinaryDataStorage.create_full_backup(
    session, cluster, infobase_id, server_path="/backup/full"
)

# Differential-копия поверх полной
rc.BinaryDataStorage.create_diff_backup(
    session,
    cluster,
    infobase_id,
    server_path="/backup/diff",
    full_backup_server_path="/backup/full",
)

# Восстановление
rc.BinaryDataStorage.load_full_backup(
    session, cluster, infobase_id, server_path="/backup/full"
)

# Освободить место, занятое устаревшими версиями данных
rc.BinaryDataStorage.clear_unused_space(
    session,
    cluster,
    infobase_id,
    storage="<storage-id>",
    name="<object-name>",
    by_universal_date="0",
)
```

Все пути (`server_path`, `full_backup_server_path`) — это каталоги **на рабочем
сервере**, а не на машине, где выполняется ваш скрипт.
