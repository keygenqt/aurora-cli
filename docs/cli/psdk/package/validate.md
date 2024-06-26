Валидация пакетов RPM.

#### Options

```shell
-p, --path TEXT                 Путь к RPM-файлу.  [обязательно]
-pr, --profile [regular|extended|mdm|antivirus|auth] Выберите профиль.
-s, --select                    Выберите из доступных.
-i, --index INTEGER             Укажите индекс.
-v, --verbose                   Подробный вывод.
--help                          Показать это сообщение и выйти.
```

#### Example

```shell
aurora-cli psdk package validate
```
