Приложение имеет API интерфейс для использования его в других приложениях.
Интерфейс CLI (Command line interface) предназначен для удобного использования приложения через терминал,
а API (Application programming interface) предназначен для удобного использования приложения
во всевозможных скриптах, приложениях или расширениях для IDE.

По API можно вызвать справку в приложении через аргумент `--help`, так же, как и для других команд.
Команда имеет один аргумент - `--route`, он принимает URL в виде строки:

```shell
aurora-cli api --route '/device/command?host=192.168.2.15&execute=ls -1'
```

#### /device

Получить список устройств.

```shell title="/device/list"
No arguments
```

Выполните команду на устройстве.

```shell title="/device/command"
• host - IP-адрес устройства.
• execute - Команда, которая будет выполнена на устройстве.
```

Загрузите файл в каталог ~/Download устройства.

```shell title="/device/upload"
• host - IP-адрес устройства.
• path - Путь к файлу.
```

Запустите пакет на устройстве.

```shell title="/device/package/run"
• host - IP-адрес устройства.
• package - Имя пакета.
• mode [dart, gdb] (необязательный) - Режим запуска приложения.
• project (необязательный) - Путь к проекту. По умолчанию текущая директория.
```

Установите пакет RPM на устройство.

```shell title="/device/package/install"
• host - IP-адрес устройства.
• path - Путь к файлу.
• apm [по умолчанию = false, true] - Использовать APM.
```

Удалите пакет с устройства.

```shell title="/device/package/remove"
• host - IP-адрес устройства.
• package - Имя пакета.
• apm [по умолчанию = false, true] - Использовать APM.
```

#### /emulator

Запустите эмулятор.

```shell title="/emulator/start"
No arguments
```

Сделать скриншот эмулятора.

```shell title="/emulator/screenshot"
No arguments
```

Старт записи видео с эмулятора.

```shell title="/emulator/recording/start"
No arguments
```

Остановка записи видео с эмулятора.

```shell title="/emulator/recording/stop"
No arguments
```

Выполните команду на эмуляторе.

```shell title="/emulator/command"
• execute - Команда, которая будет выполнена на эмуляторе.
```

Загрузите файл в каталог ~/Download эмулятора.

```shell title="/emulator/upload"
• path - Путь к файлу.
```

Запустите пакет на эмуляторе.

```shell title="/emulator/package/run"
• package - Имя пакета.
• mode [dart, gdb] (необязательный) - Режим запуска приложения.
• project (необязательный) - Путь к проекту. По умолчанию текущая директория.
```

Установите пакет RPM на эмулятор.

```shell title="/emulator/package/install"
• path - Путь к файлу.
• apm [по умолчанию = false, true] - Использовать APM.
```

Удалите пакет с эмулятора.

```shell title="/emulator/package/remove"
• package - Имя пакета.
• apm [по умолчанию = false, true] - Использовать APM.
```

#### /flutter

Получите доступные версии Flutter для ОС Аврора.

```shell title="/flutter/available"
No arguments
```

Получите версии установленных Flutter для ОС Аврора.

```shell title="/flutter/installed"
No arguments
```

Загрузите и установите Flutter для ОС Аврора.

```shell title="/flutter/install"
• version - Установленная версия Flutter.
```

Удалите Flutter для ОС Аврора.

```shell title="/flutter/remove"
• version - Установленная версия Flutter.
```

Добавьте устройства с ОС Aurora во Flutter.

```shell title="/flutter/custom-devices"
• version - Установленная версия Flutter.
```

Форматирование проекта.

```shell title="/flutter/project/format"
• version - Установленная версия Flutter.
• path - Путь к проекту. По умолчанию текущая директория.
```

Сборка проекта.

```shell title="/flutter/project/build"
• version - Установленная версия Flutter.
• psdk - Установленная версия Aurora Platform SDK.
• target - Имя цели установленной версии Aurora Platform SDK.
• path - Путь к проекту. По умолчанию текущая директория.
• clean [по умолчанию = false, true] - Очистка сборки.
• install [по умолчанию = false, true] - Установите на устройство или эмулятор.
• apm [по умолчанию = false, true] - Использовать APM.
• run [по умолчанию = false, true] - Запустите приложение на устройстве или эмуляторе.
• verbose [по умолчанию = false, true] - Подробный вывод.
• mode [dart, gdb] (необязательный) - Режим сборки с отладкой.
• host (необязательный) - IP-адрес устройства.
• key (необязательный) - Название ключа для подписи пакета из конфигурации приложения.
```

Составить отчет проекта Flutter.

```shell title="/flutter/project/report"
• version - Установленная версия Flutter.
• path - Путь к проекту. По умолчанию текущая директория.
```

Генерируйте иконки разных размеров для приложения.

```shell title="/flutter/project/icons"
• image - Путь к изображению.
• path - Путь к проекту. По умолчанию текущая директория.
```

#### /psdk

Получить список доступных версий Аврора Platform SDK.

```shell title="/psdk/available"
No arguments
```

Получите список установленных Аврора Platform SDK.

```shell title="/psdk/installed"
No arguments
```

Получить список таргетов Аврора Platform SDK.

```shell title="/psdk/targets"
• version - Установленная версия Aurora Platform SDK.
```

Загрузите и установите Аврора Platform SDK.

```shell title="/psdk/install"
• version - Установленная версия Aurora Platform SDK.
```

Удалить Аврора Platform SDK.

```shell title="/psdk/remove"
• version - Установленная версия Aurora Platform SDK.
```

Удалить снимок таргета.

```shell title="/psdk/clear"
• version - Установленная версия Aurora Platform SDK.
• target - Имя цели установленной версии Aurora Platform SDK.
```

Добавьте разрешения sudoers Аврора Platform SDK.

```shell title="/psdk/sudoers/add"
• version - Установленная версия Aurora Platform SDK.
```

Удалите разрешения sudoers Аврора Platform SDK.

```shell title="/psdk/sudoers/remove"
• version - Установленная версия Aurora Platform SDK.
```

Найдите установленный пакет в таргете.

```shell title="/psdk/package/search"
• version - Установленная версия Aurora Platform SDK.
• target - Имя цели установленной версии Aurora Platform SDK.
• package - Имя пакета.
```

Установите пакеты RPM в таргет.

```shell title="/psdk/package/install"
• version - Установленная версия Aurora Platform SDK.
• target - Имя цели установленной версии Aurora Platform SDK.
• path - Путь к RPM-файлу.
```

Удалить пакет из таргета.

```shell title="/psdk/package/remove"
• version - Установленная версия Aurora Platform SDK.
• target - Имя цели установленной версии Aurora Platform SDK.
• package - Имя пакета.
```

Валидация пакетов RPM.

```shell title="/psdk/package/validate"
• version - Установленная версия Aurora Platform SDK.
• target - Имя цели установленной версии Aurora Platform SDK.
• path - Путь к RPM-файлу.
• profile [regular, extended, mdm, antivirus, auth] - Выберите профиль.
```

Подписать пакет RPM ключевой парой (с переподпиской).

```shell title="/psdk/package/sign"
• version - Установленная версия Aurora Platform SDK.
• path - Путь к RPM-файлу.
• key (необязательный) - Название ключа для подписи пакета из конфигурации приложения.
```

Форматирование проекта.

```shell title="/psdk/project/format"
• path - Путь к проекту. По умолчанию текущая директория.
```

Сборка проекта.

```shell title="/psdk/project/build"
• version - Установленная версия Aurora Platform SDK.
• target - Имя цели установленной версии Aurora Platform SDK.
• path - Путь к проекту. По умолчанию текущая директория.
• clean [по умолчанию = false, true] - Очистка сборки.
• install [по умолчанию = false, true] - Установите на устройство или эмулятор.
• apm [по умолчанию = false, true] - Использовать APM.
• run [по умолчанию = false, true] - Запустите приложение на устройстве или эмуляторе.
• debug [по умолчанию = false, true] - Режим сборки с отладкой.
• verbose [по умолчанию = false, true] - Подробный вывод.
• host (необязательный) - IP-адрес устройства.
• key (необязательный) - Название ключа для подписи пакета из конфигурации приложения.
```

Генерируйте иконки разных размеров для приложения.

```shell title="/psdk/project/icons"
• image - Путь к изображению.
• path - Путь к проекту. По умолчанию текущая директория.
```

#### /sdk

Получите доступные версии Аврора SDK.

```shell title="/sdk/available"
No arguments
```

Получите версию установленной Аврора SDK.

```shell title="/sdk/installed"
No arguments
```

Загрузите и запустите установку Аврора SDK.

```shell title="/sdk/install"
• version - Установленная версия Aurora Platform SDK.
• offline [по умолчанию = false, true] - Загрузите установщик offline типа.
```

Запустите инструмент обслуживания (удаление, обновление).

```shell title="/sdk/tool"
No arguments
```

#### /vscode

Получить список расширений VS Code.

```shell title="/vscode/extensions/list"
No arguments
```

Получить список расширений Flutter, необходимых для работы с VS Code.

```shell title="/vscode/extensions/check/flutter"
No arguments
```

Получить список расширений C++, необходимых для работы с VS Code.

```shell title="/vscode/extensions/check/cpp"
No arguments
```

Получить список других расширений, необходимых для работы с VS Code.

```shell title="/vscode/extensions/check/other"
No arguments
```

Установка расширения VS Code.

```shell title="/vscode/extensions/install"
• extension - Название расширения VS Code.
```

Обновить настройки VS Code.

```shell title="/vscode/settings/update"
No arguments
```
