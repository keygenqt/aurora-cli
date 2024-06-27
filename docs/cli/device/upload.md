Эта команда позволяет загружать файлы на устройство.
Загрузка происходит в директорию `~/Download`.

#### Options

```shell
-p, --path TEXT      Путь к файлу.  [обязательно]
-s, --select         Выберите из доступных.
-i, --index INTEGER  Укажите индекс.
-v, --verbose        Подробный вывод.
--help               Показать это сообщение и выйти.
```

#### Example

```shell
aurora-cli device upload --path /path/to/file
```
