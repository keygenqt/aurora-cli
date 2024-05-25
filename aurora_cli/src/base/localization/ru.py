"""
Copyright 2024 Vitaliy Zarubin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


def ru_localization(key_fun: str, *args, **kwargs):
    match key_fun:
        # Groups
        case 'group_main':
            return ru_group_main()
        case 'group_device':
            return ru_group_device()
        case 'group_emulator':
            return ru_group_emulator()
        case 'group_api':
            return ru_group_api()
        # Arguments
        case 'argument_config':
            return ru_argument_config()
        # Other
        case 'emulator_start_locked':
            return ru_emulator_start_locked()
        case 'command_execute':
            return ru_command_execute(*args, **kwargs)
    return None


def ru_click_help(text: str) -> str:
    return (text
            .replace('Show the version and exit.', 'Показать версию и выйти.')
            .replace('Show this message and exit.', 'Показать это сообщение и выйти.')
            .replace('Usage:', 'Применение:')
            .replace('Options:', 'Параметры:')
            .replace('Commands:', 'Команды:'))


def ru_click_usage_error(text: str) -> str:
    return (text
            .replace('Usage:', 'Применение:')
            .replace('Try', 'Попробуй')
            .replace('for help', 'для помощи')
            .replace('Error: No such option', 'Ошибка: Нет такой опции')
            .replace('Error: Missing option', 'Ошибка: отсутствует опция')
            .replace('Error: No such command', 'Ошибка: нет такой команды'))


def ru_group_main():
    return '''Приложение позволяет устанавливать инструменты для работы с ОС Аврора и упрощает работу с ними.
Более подробную информацию об инструментах можно найти на странице документации:

Flutter SDK  https://omprussia.gitlab.io/flutter/flutter
Aurora SDK   https://developer.auroraos.ru/doc/software_development/sdk
Platform SDK https://developer.auroraos.ru/doc/software_development/psdk

Это сторонний инструмент, написанный энтузиастами!'''


def ru_group_device():
    return 'Работа с устройством.'


def ru_group_emulator():
    return 'Работа с эмулятором.'


def ru_group_api():
    return 'Программный интерфейс для приложений.'


def ru_argument_config():
    return 'Укажите путь к конфигурации.'


def ru_emulator_start_locked():
    return '<blue>Эмулятор уже запущен.</blue>'


def ru_command_execute(command: str):
    return f'<blue>Выполненная команда:</blue> `{command}`'
