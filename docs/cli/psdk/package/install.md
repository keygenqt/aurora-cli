Эта команда позволяет установить RPM пакет в таргет Platform SDK.

#### Options

```shell
-p, --path TEXT      Путь к RPM-файлу.  [обязательно]
-s, --select         Выберите из доступных.
-i, --index INTEGER  Укажите индекс.
-v, --verbose        Подробный вывод.
--help               Показать это сообщение и выйти.
```

#### Example

```shell
aurora-cli psdk package install --path /path/to/package.rpm
```
