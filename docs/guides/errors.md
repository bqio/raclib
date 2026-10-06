# Обработка ошибок

Все ошибки RAC разбираются в типизированные исключения из `raclib.errors`.
Ловить текст из `stderr` не нужно — исключение уже содержит готовое описание.

```python
import raclib as rc
from raclib import errors

session = rc.Session(rc.Client("/opt/1cv8/x86_64/8.3.24.1548/rac"), timeout=30)

try:
    rc.Cluster.info(session, "unknown-cluster-id")
except errors.ClusterNotFoundError:
    print("Кластер не найден")
except errors.RACTimeoutError:
    print("Сервер администрирования не ответил за отведённое время")
except errors.RACNotFoundError:
    print("Не найден или не запускается исполняемый файл rac")
except errors.UnknownError as exc:
    print("Незнакомая ошибка RAC:", exc)
```

## Какие исключения бывают

### Проблемы с запуском `rac`

Бросаются **до** запуска команды или вместо её результата.

| Исключение | Когда |
| --- | --- |
| `RACNotFoundError` | файл `rac` не найден, не исполняем или путь указывает на каталог |
| `RACTimeoutError` | `rac` не ответил за `timeout` секунд, заданный в сессии |

`RACNotFoundError` наследуется от `FileNotFoundError`, `RACTimeoutError` — от
`TimeoutError`, поэтому оба можно поймать стандартными исключениями Python.

### Ошибки аутентификации

| Исключение | Что проверить |
| --- | --- |
| `ClusterCredentialsError` | `cluster_user` / `cluster_pwd` |
| `AgentCredentialsError` | `agent_user` / `agent_pwd` |
| `CentralServerCredentialsError` | права администратора центрального сервера |
| `InfobaseCredentialsError` | `infobase_user` / `infobase_pwd` |

### Объект не найден

`ClusterNotFoundError`, `InfobaseNotFoundError`, `CounterNotFoundError`,
`LimitNotFoundError`, `RuleNotFoundError` — обычно означают опечатку в
идентификаторе или попытку работать с объектом из другого кластера.

### Конфликты и ограничения сервера

| Исключение | Причина |
| --- | --- |
| `ServerIsMainError` | попытка удалить центральный сервер кластера |
| `ServerAlreadyExistsError` | такой рабочий сервер уже зарегистрирован |
| `InfobaseAlreadyExistsError` | база уже зарегистрирована в кластере |
| `ServerIPRangeError` | левая граница диапазона IP-портов больше правой |
| `PortConflictError` | конфликт IP-портов при запуске рабочего процесса |
| `AgentAdminCreateError` | попытка удалить последнего администратора с паролем |
| `UnknownHostError` | компьютер отсутствует в сети или недоступен |

### Проблемы с базой данных

| Исключение | Что делать |
| --- | --- |
| `InfobaseDatabaseNotFoundError` | передать `create_database=True` в `Infobase.create` |
| `CreateInfobaseParamsError` | проверить `dbms`, `db_server`, `db_name`, `db_user`, `db_pwd` |
| `DatabaseConnectionError` | сервер баз данных не обнаружен — проверить доступность |
| `DatabaseError` | операция с базой не выполнена, подробности в тексте исключения |

### Прочее

| Исключение | Причина |
| --- | --- |
| `IncorrectVersionError` | версии `rac` и сервера 1С различаются |
| `ParamError` | RAC не принял параметр команды |
| `ConnectionError` | не удалось соединиться с сервером администрирования |
| `UnknownError` | ошибка, которой нет в таблице соответствий |

## `UnknownError`

Таблица соответствий покрывает типовые сообщения RAC, но она построена на
локализованном тексте и не может быть исчерпывающей: новая версия 1С или
англоязычная локаль сервера дадут незнакомую формулировку. В этом случае
поднимается `UnknownError`, который **сохраняет исходный текст RAC**:

```python
try:
    rc.Counter.update(session, cluster, name="cpu", collection_time="0", group="process", filter_type="processor")
except errors.UnknownError as exc:
    print(exc)          # строки, которые вернул RAC
    print(exc.stderr)   # исходный stderr целиком
```

Если вы получили `UnknownError` на штатной ситуации — это повод добавить шаблон
в таблицу `raclib.errors.errors`.

## Общий обработчик

Для скриптов удобно один раз преобразовать всё в понятный вывод:

```python
import sys
import raclib as rc
from raclib import errors

session = rc.Session(rc.Client(RAC), timeout=30)

try:
    rc.Cluster.remove(session, cluster_id, cluster_user="admin", cluster_pwd="secret")
except errors.ClusterCredentialsError:
    sys.exit("Неверные учётные данные администратора кластера")
except errors.ClusterNotFoundError:
    sys.exit("Кластер не найден")
except (errors.RACNotFoundError, errors.RACTimeoutError) as exc:
    sys.exit(f"RAC недоступен: {exc}")
except errors.UnknownError as exc:
    sys.exit(f"Ошибка RAC: {exc}")
```
