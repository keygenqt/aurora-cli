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
    def argument_optional():
        return 'необязательный'

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
    def argument_install():
        return 'Установите на устройство или эмулятор.'

    @staticmethod
    def argument_debug():
        return 'Режим сборки с отладкой.'

    @staticmethod
    def argument_run_mode():
        return 'Режим запуска приложения.'

    @staticmethod
    def argument_clean():
        return 'Очистка сборки.'

    @staticmethod
    def argument_pub_get():
        return 'Выполнить pub get.'

    @staticmethod
    def argument_build_runner():
        return 'Выполнить build runner.'

    @staticmethod
    def argument_run():
        return 'Запустите приложение на устройстве или эмуляторе.'

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
        return 'Загрузите установщик offline типа.'

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

    @staticmethod
    def argument_mode_build():
        return 'Тип сборки проекта.'

    @staticmethod
    def argument_run_mode():
        return 'Режим запуска приложения.'

    @staticmethod
    def argument_host_device():
        return 'IP-адрес устройства.'

    @staticmethod
    def argument_flutter_version():
        return 'Установленная версия Flutter.'

    @staticmethod
    def argument_psdk_version():
        return 'Установленная версия Aurora Platform SDK.'

    @staticmethod
    def argument_target_name():
        return 'Имя цели установленной версии Aurora Platform SDK.'

    @staticmethod
    def argument_key_sign_name():
        return 'Название ключа для подписи пакета из конфигурации приложения.'

    @staticmethod
    def argument_vscode_extension():
        return 'Название расширения VS Code.'

    @staticmethod
    def argument_language():
        return 'Язык приложения.'

    @staticmethod
    def argument_enable_verbose():
        return 'Включить/Выключить --verbose по умолчанию.'

    @staticmethod
    def argument_enable_save_select():
        return 'Включить/Выключить сохранение --select.'

    @staticmethod
    def argument_enable_hint():
        return 'Включить/Выключить подсказки в приложении.'

    @staticmethod
    def argument_test_answer_time():
        return 'Время задержки ответа.'

    @staticmethod
    def argument_test_answer_code():
        return 'Код ответа (100, 200, 500).'

    @staticmethod
    def argument_test_answer_iterate():
        return 'Количество итераций ответов.'

    @staticmethod
    def argument_password():
        return 'Root пароль.'