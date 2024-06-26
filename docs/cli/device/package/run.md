Запуск приложения на устройстве. По умолчанию запуск происходит в песочнице.

!!! info

    Аргумент `--mode` позволяет запускать приложения в режиме отладки для Flutter приложений.
    Для этого приложение должно быть собрано с аргументом `--debug` и уже установлено на устройство.
    Подключиться к отладке можно через VS Code через отладку Dart или GDB.
    Не забудьте добавить custom-devices во Flutter, см. раздел **Flutter -> Custom Devices**.

#### Options

```shell
-p, --package TEXT     Имя пакета.  [обязательно]
-m, --mode [dart|gdb]  Режим запуска приложения.
-s, --select           Выберите из доступных.
-i, --index INTEGER    Укажите индекс.
-v, --verbose          Подробный вывод.
--help                 Показать это сообщение и выйти.
```

#### Example

```shell
aurora-cli device package run --package ru.auroraos.mypackage
```
