Команда позволяет проверить отформатирован ли проект по стандартам ОС Аврора.
Конфиг для `clang-format` берется с открытого репозитория на GitLab [omprussia](https://gitlab.com/omprussia).

#### Options

```shell
-p, --path TEXT  Путь к проекту. По умолчанию текущая директория.
-v, --verbose    Подробный вывод.
--help           Показать это сообщение и выйти.
```

#### Example

```shell
aurora-cli psdk project check-format
```
