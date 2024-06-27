Platform SDK имеет возможность валидировать RPM пакет для обнаружения проблем.
Пакет должен соответствовать
[требованиям](https://developer.auroraos.ru/doc/5.1.0/software_development/guidelines/rpm_requirements).
Эта команда упрощает задачу по валидации пакета.

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
aurora-cli psdk package validate --path /path/to/package.rpm --profile regular
```
