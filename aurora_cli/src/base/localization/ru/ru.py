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

from aurora_cli.src.base.localization.ru.ru_app_argument import TextArgumentRu
from aurora_cli.src.base.localization.ru.ru_app_command import TextCommandRu
from aurora_cli.src.base.localization.ru.ru_app_group import TextGroupRu
from aurora_cli.src.base.localization.ru.ru_error import TextErrorRu
from aurora_cli.src.base.localization.ru.ru_hint import TextHintRU
from aurora_cli.src.base.localization.ru.ru_info import TextInfoRu
from aurora_cli.src.base.localization.ru.ru_prompt import TextPromptRu
from aurora_cli.src.base.localization.ru.ru_success import TextSuccessRu


def _ru_search(cls, key_fun: str):
    for key_fun_ru in cls.__dict__:
        if key_fun == key_fun_ru:
            return getattr(cls, key_fun_ru)


def ru_localization(key_fun: str, *args, **kwargs):
    ru_cls = [
        TextArgumentRu,
        TextCommandRu,
        TextGroupRu,
        TextErrorRu,
        TextInfoRu,
        TextPromptRu,
        TextSuccessRu,
        TextHintRU,
    ]
    for cls in ru_cls:
        func = _ru_search(cls, key_fun)
        if func:
            return func(*args, **kwargs)
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


def ru_abort(text: str) -> str:
    return (text
            .replace('Aborted! Closing...', 'Прервано! Закрытие...')
            .replace('Goodbye 👋', 'До свидания 👋'))


def ru_git_clone(text: str) -> str:
    return (text
            .replace('Counting', 'Подсчет')
            .replace('Compressing', 'Сжатие')
            .replace('Receiving', 'Получение')
            .replace('Resolving', 'Разрешение'))
