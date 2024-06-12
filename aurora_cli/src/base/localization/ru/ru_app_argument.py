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


class TextArgumentRu(Enum):
    @staticmethod
    def argument_config():
        return 'Указать путь конфигурации.'

    @staticmethod
    def argument_verbose():
        return 'Подробный вывод.'

    @staticmethod
    def argument_execute_device():
        return 'Команда, которая будет выполнена на устройстве.'

    @staticmethod
    def argument_execute_emulator():
        return 'Команда, которая будет выполнена на эмуляторе.'

    @staticmethod
    def argument_select():
        return 'Выберите из доступных.'

    @staticmethod
    def argument_index():
        return 'Укажите индекс.'

    @staticmethod
    def argument_path():
        return 'Путь к файлу.'

    @staticmethod
    def argument_path_rpm():
        return 'Путь к RPM-файлу.'

    @staticmethod
    def argument_package_name():
        return 'Имя пакета.'

    @staticmethod
    def argument_apm():
        return 'Использовать APM.'

    @staticmethod
    def argument_exit_after_run():
        return 'Выйти после запуска.'

    @staticmethod
    def argument_sdk_installer_type():
        return 'Загрузите установщик offline типа (online = по умолчанию).'

    @staticmethod
    def argument_validate_profile():
        return 'Выберите профиль.'

    @staticmethod
    def argument_path_to_project():
        return 'Путь к проекту. По умолчанию текущая директория.'

    @staticmethod
    def argument_path_to_image():
        return 'Путь к изображению.'

    @staticmethod
    def argument_clear_cache():
        return 'Очистить кэшированные данные.'
