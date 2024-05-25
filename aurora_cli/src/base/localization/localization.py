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
from aurora_cli.src.base.localization.ru import ru_click_help, ru_localization, ru_click_usage_error
from aurora_cli.src.base.utils.app import app_language
from aurora_cli.src.base.utils.capturing_stderr import CapturingStderr


def localization(func):
    def wrapped(*args, **kwargs) -> str:
        def wrapped_context():
            if app_language() == 'ru':
                return ru_localization(func.__name__, *args, **kwargs)

        value = wrapped_context()
        if value:
            return value
        return func(*args, **kwargs)

    return wrapped


def localization_help(text: str):
    if app_language() == 'ru':
        print(ru_click_help(text))
    else:
        print(text)


def localization_usage_error():
    def click_localization_usage_error(text: str):
        if app_language() == 'ru':
            print(ru_click_usage_error(text))

    return CapturingStderr(callback=click_localization_usage_error)
