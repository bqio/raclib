# Утилиты

Транспорт и разбор вывода: то, что используется всеми сущностями.

## RacRecord

Тип одной записи вывода RAC — то, что возвращают все методы чтения:

```python
type RacRecord = dict[str, str | int]
```

Ключи соответствуют полям вывода RAC, дефисы заменены на подчёркивания,
десятичные значения приведены к `int`. Именно он указан в аннотациях методов
вида `-> list[RacRecord]` и `-> RacRecord`.

::: raclib._shared.RacRecord

## Client

::: raclib.Client
    options:
      members: true

## RawOutput

Результат выполнения команды. Позволяет получить сырой текст или разобрать его.

```python
output = session.exec("cluster list")

output.to_str()                   # исходный текст
output.to_list()                  # list[dict]
output.to_dict()                  # последняя запись
output.to_dataclass(MyRow)        # одна запись как dataclass
output.to_list_of_dataclass(Row)  # все записи как dataclass
```

::: raclib.RawOutput
    options:
      members: true

## Session

::: raclib.Session
    options:
      members: true

## Ошибки

Все исключения библиотеки. Разбор сообщений RAC выполняет `raclib.errors.handler`.

::: raclib.errors.RACNotFoundError

::: raclib.errors.RACTimeoutError

::: raclib.errors.UnknownError

::: raclib.errors.ClusterNotFoundError

::: raclib.errors.ClustersNotFoundError

::: raclib.errors.InfobaseNotFoundError

::: raclib.errors.AgentAdminNotFoundError

::: raclib.errors.AgentAdminsNotFoundError

::: raclib.errors.CounterNotFoundError

::: raclib.errors.LimitNotFoundError

::: raclib.errors.RuleNotFoundError

::: raclib.errors.InfobaseCredentialsError

::: raclib.errors.ClusterCredentialsError

::: raclib.errors.AgentCredentialsError

::: raclib.errors.CentralServerCredentialsError

::: raclib.errors.AgentAdminCreateError

::: raclib.errors.ConnectionError

::: raclib.errors.CreateInfobaseParamsError

::: raclib.errors.DatabaseConnectionError

::: raclib.errors.DatabaseError

::: raclib.errors.InfobaseDatabaseNotFoundError

::: raclib.errors.InfobaseAlreadyExistsError

::: raclib.errors.ServerAlreadyExistsError

::: raclib.errors.ServerIPRangeError

::: raclib.errors.ServerIsMainError

::: raclib.errors.ServerNotCentralError

::: raclib.errors.IncorrectVersionError

::: raclib.errors.ParamError

::: raclib.errors.PortConflictError

::: raclib.errors.UnknownHostError
