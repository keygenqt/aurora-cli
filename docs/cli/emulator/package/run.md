Запуск приложения на эмуляторе. По умолчанию запуск происходит в песочнице.

!!! info

    Аргумент `--mode` позволяет запускать приложения в режиме отладки для Flutter приложений.
    Для этого приложение должно быть собрано с аргументом `--debug` и уже установлено на устройство.
    Подключиться к отладке можно через VS Code через отладку Dart или GDB.
    Не забудьте добавить custom-devices во Flutter, см. раздел **Flutter -> Custom Devices**.

#### Options

```shell
-p, --package TEXT     Имя пакета.  [обязательно]
-m, --mode [dart|gdb]  Режим запуска приложения.
-v, --verbose          Подробный вывод.
--help                 Показать это сообщение и выйти.
```

#### Example

```shell
aurora-cli emulator package run --package ru.auroraos.mypackage
```
