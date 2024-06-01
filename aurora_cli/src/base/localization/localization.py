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
from aurora_cli.src.base.localization.ru.ru import ru_localization, ru_click_help, ru_click_usage_error, ru_abort
from aurora_cli.src.base.utils.app import app_language


def localization(func):
    def wrapped(*args, **kwargs) -> str:
        def wrapped_context():
            if app_language() == 'ru':
                return ru_localization(func.__name__, *args, **kwargs)

        orig_value = func(*args, **kwargs)
        value = wrapped_context()
        if value:
            hint = ''
            hints = '<hint>'.join(orig_value.split('<hint>')[1:])
            if '<hint>' in orig_value:
                hint = f'''\n<hint>{hints}'''
            return f'{value}{hint}'
        return orig_value

    return wrapped


def localization_help(text: str):
    text = text.strip()
    if app_language() == 'ru':
        print(ru_click_help(text))
    else:
        print(text)


def localization_usage_error(text: str):
    text = text.strip()
    if app_language() == 'ru':
        print(ru_click_usage_error(text))
    else:
        print(text)


def localization_abort(text: str):
    text = text.strip()
    if app_language() == 'ru':
        print(ru_abort(text))
    else:
        print(text)
