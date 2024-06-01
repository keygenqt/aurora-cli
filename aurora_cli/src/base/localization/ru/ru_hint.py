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
from enum import Enum

from aurora_cli.src.base.constants.other import VM_MANAGE


class TextHintRU(Enum):
    @staticmethod
    def emulator_run():
        return '<i>Запустить эмулятор можно следующей командой:</i> aurora-cli emulator start'

    @staticmethod
    def install_app(*args):
        application = 'virtualbox' if args[0] == VM_MANAGE else args[0]
        return f'<i>Вам необходимо установить это приложение:</i> sudo apt install {application}'

    @staticmethod
    def not_install_emulator():
        return '<i>Возможно у вас не установлен эмулятор, его можно поставить вместе с Aurora SDK.</i>'

    @staticmethod
    def emulator_recording_on():
        return '<i>Отключить запись можно в окне VirtualBox, внизу можно увидеть вращающуюся иконку.</i>'

    @staticmethod
    def route_error_hint():
        return '<i>Приложение имеет API для использование его в других приложениях, для людей предусмотрен CLI.</i>'

    @staticmethod
    def documentation_link():
        return ('<i>Более детально можно узнать в документации приложения:</i> '
                'https://keygenqt.github.io/aurora-cli')

    @staticmethod
    def device_config():
        return '<i>Возможно у вас неверно настроены параметры устройства в конфигурационном файле.</i>'

    @staticmethod
    def flutter_documentation_link():
        return ('<i>Более подробную информацию можно найти в документации Flutter:</i> '
                'https://omprussia.gitlab.io/flutter/flutter')

    @staticmethod
    def psdk_documentation_link():
        return ('<i>Более подробную информацию можно найти в документации Aurora Platform SDK:</i> '
                'https://developer.auroraos.ru/doc/software_development/psdk')

    @staticmethod
    def sdk_documentation_link():
        return ('<i>Более подробную информацию можно найти в документации Aurora SDK:</i> '
                'https://developer.auroraos.ru/doc/software_development/sdk')

    @staticmethod
    def flutter_install():
        return '<i>Вы можете установить Flutter с помощью следующей команды:</i> aurora-cli flutter install'

    @staticmethod
    def psdk_install():
        return '<i>Вы можете установить Aurora Platform SDK с помощью следующей команды:</i> aurora-cli psdk install'

    @staticmethod
    def sdk_install():
        return '<i>Вы можете установить Aurora SDK с помощью следующей команды:</i> aurora-cli sdk install'
