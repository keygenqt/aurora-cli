Удаление пакета с устройства на ОС Aurora 4 и 5 поколения с помощью `pkcon`
или нового менеджера пакетов `APM`, доступного на 5й версии ОС Аврора.

!!! warning

    Пакетные менеджеры `pkcon` & `APM` не взаимодействуют между собой. Установленный пакет через `pkcon` нельзя удалить через `APM`.

#### Options

```shell
-p, --package TEXT   Имя пакета.  [обязательно]
-a, --apm            Использовать APM.
-s, --select         Выберите из доступных.
-i, --index INTEGER  Укажите индекс.
-v, --verbose        Подробный вывод.
--help               Показать это сообщение и выйти.
```

#### Example

```shell
aurora-cli device package remove --package ru.auroraos.mypackage
```
