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


class TextGroupRu(Enum):
    @staticmethod
    def group_main():
        return '''Приложение позволяет устанавливать инструменты для работы с ОС Аврора и упрощает работу с ними.
Более подробную информацию об инструментах можно найти на странице документации:

Flutter SDK  https://omprussia.gitlab.io/flutter/flutter
Aurora SDK   https://developer.auroraos.ru/doc/software_development/sdk
Platform SDK https://developer.auroraos.ru/doc/software_development/psdk

Это сторонний инструмент, написанный энтузиастами!'''

    @staticmethod
    def group_device():
        return 'Работа с устройством.'

    @staticmethod
    def group_emulator():
        return 'Работа с эмулятором в virtualbox.'

    @staticmethod
    def group_api():
        return 'Программный интерфейс для приложений.'
