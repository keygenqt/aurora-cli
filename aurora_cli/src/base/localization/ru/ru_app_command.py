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


class TextCommandRu(Enum):
    @staticmethod
    def command_device_command():
        return 'Выполните команду на устройстве.'

    @staticmethod
    def command_device_upload():
        return 'Загрузите файл в каталог ~/Download устройства.'

    @staticmethod
    def command_device_package_run():
        return 'Запустите пакет на устройстве в контейнере.'

    @staticmethod
    def command_device_package_install():
        return 'Установите пакет RPM на устройство.'

    @staticmethod
    def command_device_package_remove():
        return 'Удалите пакет RPM с устройства.'

    @staticmethod
    def command_emulator_start():
        return 'Запустите эмулятор.'

    @staticmethod
    def command_emulator_screenshot():
        return 'Сделать скриншот эмулятора.'

    @staticmethod
    def command_emulator_recording():
        return 'Запись видео с эмулятора.'

    @staticmethod
    def command_emulator_command():
        return 'Выполните команду на эмуляторе.'

    @staticmethod
    def command_emulator_upload():
        return 'Загрузите файл на эмулятор в каталог ~/Download.'

    @staticmethod
    def command_emulator_package_run():
        return 'Запустите пакет на эмуляторе в контейнере.'

    @staticmethod
    def command_emulator_package_install():
        return 'Установите пакет RPM на эмулятор.'

    @staticmethod
    def command_emulator_package_remove():
        return 'Удалите пакет RPM с эмулятора.'
