Установка пакета на устройство с ОС Aurora 4 и 5 поколения, с помощью `pkcon`
или нового менеджера пакетов `APM` доступного на 5й версии ОС Аврора.

#### Options

```shell
-p, --path TEXT      Путь к RPM-файлу.  [обязательно]
-a, --apm            Использовать APM.
-s, --select         Выберите из доступных.
-i, --index INTEGER  Укажите индекс.
-v, --verbose        Подробный вывод.
--help               Показать это сообщение и выйти.
```

#### Example

```shell
aurora-cli device package install --path /path/to/file.rpm
```
