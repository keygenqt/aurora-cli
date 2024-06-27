Platform SDK работает из chroot и постоянно запрашивает `root` пароль.
От этого можно избавиться добавить настройки в `sudoers`.
Эта команда добавляет такие настройки.

#### Options

```shell
-s, --select         Выберите из доступных.
-i, --index INTEGER  Укажите индекс.
-v, --verbose        Подробный вывод.
--help               Показать это сообщение и выйти.
```

#### Example

```shell
aurora-cli psdk sudoers add
```
