# Сеансы, соединения и блокировки

Эти три сущности описывают, кто прямо сейчас работает с базой, и позволяют
вмешаться в работу **без перезапуска сервера**.

## Сеансы пользователей

```python
import raclib as rc

session = rc.Session(rc.Client("/opt/1cv8/x86_64/8.3.24.1548/rac"), timeout=30)
cluster = rc.Cluster.list(session)[0]["cluster"]

for user_session in rc.UserSession.list(session, cluster):
    print(user_session["session"], user_session["user-name"], user_session["app-id"])
```

Список можно сузить до одной базы:

```python
rc.UserSession.list(session, cluster, infobase=infobase_id)
```

### Информация о сеансе и лицензиях

```python
info = rc.UserSession.info(session, cluster, user_session_id, licenses=True)
print(info["user-name"], info["host"], info["licenses"])
```

Флаг `licenses=True` добавляет в вывод сведения о занятых лицензиях. Он есть у
`UserSession.info`, `UserSession.list`, `Process.info` и `Process.list`.

### Завершить сеанс

```python
rc.UserSession.terminate(
    session,
    cluster,
    user_session_id,
    error_message="Сервер будет перезапущен через 5 минут. Сохраните данные.",
)
```

Пользователь увидит переданное сообщение. Если оставить `error_message` пустым,
будет показано стандартное сообщение 1С.

### Прервать серверный вызов

Если сеанс завис на долгом вызове и завершать его целиком не нужно:

```python
rc.UserSession.interrupt_current_server_call(
    session, cluster, user_session_id, error_message="Операция прервана администратором"
)
```

В отличие от `terminate` сеанс пользователя сохраняется — прерывается только
текущий серверный вызов.

!!! warning "Это не «убить процесс»"

    `terminate` и `interrupt_current_server_call` выполняются на стороне
    сервера 1С и завершают сеанс корректно. Рабочий процесс при этом остаётся
    жив и продолжает обслуживать другие сеансы.

## Соединения

Соединение — это канал между клиентом и информационной базой. Один сеанс может
иметь несколько соединений.

```python
# Все соединения кластера
rc.Connection.list(session, cluster)

# Соединения конкретного рабочего процесса
rc.Connection.list(session, cluster, process=process_id)

# Соединения конкретной базы
rc.Connection.list(session, cluster, infobase=infobase_id)

# Сведения об одном соединении
info = rc.Connection.info(session, cluster, connection_id)
print(info["infobase"], info["user-name"], info["application"])
```

### Разорвать соединение

```python
rc.Connection.disconnect(session, cluster, process_id, connection_id)
```

Для разрыва нужны **оба** идентификатора: рабочий процесс и само соединение.

## Рабочие процессы

Прежде чем разрывать соединения и искать блокировки, посмотрите, какие процессы
запущены на сервере:

```python
for server in rc.Server.list(session, cluster):
    server_id = server["server"]

    for process in rc.Process.list(session, cluster, server_id, licenses=True):
        print(process["process"], process["pid"], process["avg-call-time"])
```

Сведения об одном процессе:

```python
info = rc.Process.info(session, cluster, process_id)
```

## Блокировки

Блокировки показывают, кто кого ждёт. Это первый инструмент при жалобах на
«зависшую» базу.

```python
locks = rc.Lock.list(session, cluster)
for lock in locks:
    print(lock["session"], lock["object"], lock["desc"])
```

Список можно сузить:

```python
rc.Lock.list(session, cluster, infobase=infobase_id)
rc.Lock.list(session, cluster, connection=connection_id)
rc.Lock.list(session, cluster, infobase_session=user_session_id)
```

## Менеджеры кластера

Менеджеры отвечают за обслуживание информационных баз. Их состояние полезно при
диагностике проблем с конкретной базой:

```python
for manager in rc.Manager.list(session, cluster):
    print(manager["manager"], manager["infobase"], manager["state"])
```

## Службы на рабочем сервере

1С позволяет запускать на рабочем сервере отдельные службы (например,
серверные вызовы и задания) со своими каталогами данных.

```python
# Настройки служб сервера
for setting in rc.ServiceSetting.list(session, cluster, server_id):
    print(setting)

# Список зарегистрированных служб кластера
rc.Service.list(session, cluster)

# Куда переносить данные службы при переезде на другой сервер
dirs = rc.ServiceSetting.get_service_data_dirs_for_transfer(
    session, cluster, server_id, service_name="JobService"
)

# Применить изменения настроек
rc.ServiceSetting.apply(session, cluster, server_id)
```

```python
rc.ServiceSetting.insert(
    session,
    cluster,
    server_id,
    service_name="JobService",
    infobase_name="TestIB",
    service_data_dir="/srv/1c/services/job",
)

rc.ServiceSetting.update(
    session, cluster, server_id, setting_id, service_data_dir="/srv/1c/services/job2"
)

rc.ServiceSetting.remove(session, cluster, server_id, setting_id)
```
