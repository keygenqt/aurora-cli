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
import functools
from enum import Enum

from aurora_cli.src.base.constants.other import VM_MANAGE
from aurora_cli.src.base.localization.localization import localization


class Hint(Enum):
    emulator_run = 'emulator_run'
    install_app = 'install_app'
    not_install_emulator = 'not_install_emulator'
    emulator_recording_on = 'emulator_recording_on'


def hint(*hints: Hint):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            value = function(*args, **kwargs)
            for key in hints:
                for key_fun in TextHint.__dict__:
                    if key.value == key_fun:
                        hint_fun = getattr(TextHint, key_fun)
                        value = '{text}\n<hint>{hint}</hint>'.format(
                            text=value,
                            hint=hint_fun(*args, **kwargs)
                        )
            return value

        return wrapper

    return decorator


class TextHint(Enum):
    @staticmethod
    @localization
    def emulator_run():
        return '<i>You can start the emulator with the following command:</i> aurora-cli emulator start'

    @staticmethod
    @localization
    def install_app(*args):
        application = 'virtualbox' if args[0] == VM_MANAGE else args[0]
        return f'<i>You need to install this application:</i> sudo apt install {application}'

    @staticmethod
    @localization
    def not_install_emulator():
        return '<i>You may not have an emulator installed; it can be installed with the Aurora SDK.</i>'

    @staticmethod
    @localization
    def emulator_recording_on():
        return '<i>You can disable recording in the VirtualBox window; you can see a rotating icon at the bottom.</i>'
