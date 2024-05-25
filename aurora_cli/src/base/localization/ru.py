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
        case 'emulator_start_locked':
            return ru_emulator_start_locked()
        case 'command_execute':
            return ru_command_execute(*args, **kwargs)
    return None


def ru_emulator_start_locked():
    return '<blue>Эмулятор уже запущен.</blue>'


def ru_command_execute(command: str):
    return f'<blue>Выполненная команда:</blue> `{command}`'
