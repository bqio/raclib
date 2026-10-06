# Справочник API

Полное описание публичных классов и методов, сгенерированное из докстрингов.

## Как устроен API

Все сущности 1С — это классы со **статическими методами**, первым аргументом
которых всегда идёт сессия:

```python
rc.Cluster.list(session)
rc.Infobase.create(session, cluster, name="TestIB", ...)
```

Методы делятся на две группы:

| Назначение | Что возвращают | Примеры |
| --- | --- | --- |
| Чтение | `dict` или `list[dict]` | `info`, `list`, `values` |
| Изменение | `None` или `str` с идентификатором | `insert`, `update`, `remove`, `create` |

Методы создания (`Cluster.insert`, `Server.insert`, `Infobase.create`,
`Rule.insert`) возвращают **строку** с идентификатором созданного объекта.

## Формат словарей

RAC печатает вывод в виде `ключ : значение`. Библиотека преобразует его так:

- дефисы в именах полей заменяются на подчёркивания:
  `expiration-timeout` → `expiration_timeout`;
- значения в кавычках теряют кавычки;
- десятичные числа приводятся к `int`, остальное остаётся строкой;
- записи разделяются по повтору первого ключа, а не по пустым строкам.

!!! note "Типы значений зависят от версии 1С"

    Приведение к `int` срабатывает только для десятичных чисел. Если RAC вернул
    отрицательное число или число с плавающей точкой, значение останется
    строкой. Не полагайтесь на тип без проверки.

## Разделы

- **[Кластеры и серверы](cluster.md)** — `Cluster`, `Server`, `Rule`, `Agent`.
- **[Информационные базы](infobase.md)** — `Infobase`, `BinaryDataStorage`.
- **[Сеансы и процессы](runtime.md)** — `UserSession`, `Connection`, `Process`,
  `Lock`, `Manager`, `Service`, `ServiceSetting`.
- **[Ограничения и счётчики](resources.md)** — `Counter`, `Limit`.
- **[Профили безопасности](security.md)** — `Profile` и его правила ACL.
- **[Утилиты](utils.md)** — `Client`, `Session`, `RawOutput`, `raclib.errors`.

## Асинхронная ветка

Асинхронные двойники лежат в `raclib.asynchronous` и повторяют синхронный API
с префиксом `Async`:

| Синхронный | Асинхронный |
| --- | --- |
| `raclib.Client` | `raclib.asynchronous.AsyncClient` |
| `raclib.Session` | `raclib.asynchronous.AsyncSession` |
| `raclib.Cluster` | `raclib.asynchronous.AsyncCluster` |
| `raclib.Infobase` | `raclib.asynchronous.AsyncInfobase` |
| ... | ... |

Сигнатуры методов совпадают, отличается только способ вызова: асинхронные
методы нужно `await`-ить. Подробности — в разделе
[Асинхронный режим](../guides/async.md).
