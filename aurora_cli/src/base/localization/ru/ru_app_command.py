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
    def command_device_list():
        return 'Получить список устройств.'

    @staticmethod
    def command_device_info():
        return 'Получить информацию об устройстве.'

    @staticmethod
    def command_device_command():
        return 'Выполните команду на устройстве.'

    @staticmethod
    def command_device_upload():
        return 'Загрузите файл в каталог ~/Download устройства.'

    @staticmethod
    def command_device_ssh_copy_id():
        return 'Запустите пакет на устройстве.'

    @staticmethod
    def command_device_package_run():
        return 'Запустите пакет на устройстве.'

    @staticmethod
    def command_device_package_install():
        return 'Установите пакет RPM на устройство.'

    @staticmethod
    def command_device_package_remove():
        return 'Удалите пакет с устройства.'

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
    def command_emulator_recording_start():
        return 'Старт записи видео с эмулятора.'

    @staticmethod
    def command_emulator_recording_stop():
        return 'Остановка записи видео с эмулятора.'

    @staticmethod
    def command_emulator_info():
        return 'Получить информацию об эмуляторе.'

    @staticmethod
    def command_emulator_command():
        return 'Выполните команду на эмуляторе.'

    @staticmethod
    def command_emulator_upload():
        return 'Загрузите файл в каталог ~/Download эмулятора.'

    @staticmethod
    def command_emulator_package_run():
        return 'Запустите пакет на эмуляторе.'

    @staticmethod
    def command_emulator_package_install():
        return 'Установите пакет RPM на эмулятор.'

    @staticmethod
    def command_emulator_package_remove():
        return 'Удалите пакет с эмулятора.'

    @staticmethod
    def command_flutter_available():
        return 'Получите доступные версии Flutter для ОС Аврора.'

    @staticmethod
    def command_flutter_installed():
        return 'Получите версии установленных Flutter для ОС Аврора.'

    @staticmethod
    def command_flutter_install():
        return 'Загрузите и установите Flutter для ОС Аврора.'

    @staticmethod
    def command_flutter_remove():
        return 'Удалите Flutter для ОС Аврора.'

    @staticmethod
    def command_flutter_project_report():
        return 'Составить отчет проекта Flutter.'

    @staticmethod
    def command_project_format():
        return 'Форматирование проекта.'

    @staticmethod
    def command_project_build():
        return 'Сборка проекта.'

    @staticmethod
    def command_project_debug():
        return 'Сборка debug и запуск проекта.'

    @staticmethod
    def command_project_icon():
        return 'Генерируйте иконки разных размеров для приложения.'

    @staticmethod
    def command_psdk_available():
        return 'Получить список доступных версий Аврора Platform SDK.'

    @staticmethod
    def command_psdk_installed():
        return 'Получите список установленных Аврора Platform SDK.'

    @staticmethod
    def command_psdk_install():
        return 'Установите Аврора Platform SDK.'

    @staticmethod
    def command_psdk_download():
        return 'Загрузите Аврора Platform SDK.'

    @staticmethod
    def command_psdk_remove():
        return 'Удалить Аврора Platform SDK.'

    @staticmethod
    def command_psdk_clear():
        return 'Удалить снимок таргета.'

    @staticmethod
    def command_psdk_package_search():
        return 'Найдите установленный пакет в таргете.'

    @staticmethod
    def command_psdk_package_install():
        return 'Установите пакеты RPM в таргет.'

    @staticmethod
    def command_psdk_package_remove():
        return 'Удалить пакет из таргета.'

    @staticmethod
    def command_psdk_sign():
        return 'Подписать пакет RPM ключевой парой (с переподпиской).'

    @staticmethod
    def command_psdk_sudoers_add():
        return 'Добавьте разрешения sudoers Аврора Platform SDK.'

    @staticmethod
    def command_psdk_sudoers_remove():
        return 'Удалите разрешения sudoers Аврора Platform SDK.'

    @staticmethod
    def command_psdk_info():
        return 'Получить информацию о Аврора Platform SDK.'

    @staticmethod
    def command_psdk_targets():
        return 'Получить список таргетов Аврора Platform SDK.'

    @staticmethod
    def command_psdk_validate():
        return 'Валидация пакетов RPM.'

    @staticmethod
    def command_sdk_available():
        return 'Получите доступные версии Аврора SDK.'

    @staticmethod
    def command_sdk_installed():
        return 'Получите версию установленной Аврора SDK.'

    @staticmethod
    def command_sdk_install():
        return 'Загрузите и запустите установку Аврора SDK.'

    @staticmethod
    def command_sdk_tool():
        return 'Запустите инструмент обслуживания (удаление, обновление).'

    @staticmethod
    def command_vscode_tuning():
        return 'Настройка Visual Studio Code.'

    @staticmethod
    def command_flutter_custom_devices():
        return 'Добавьте устройства с ОС Aurora во Flutter.'

    @staticmethod
    def command_vscode_info():
        return 'Информация о VS Code.'

    @staticmethod
    def command_vscode_extensions_list():
        return 'Получить список расширений VS Code.'

    @staticmethod
    def command_vscode_extension_install():
        return 'Установка расширения VS Code.'

    @staticmethod
    def command_vscode_settings_update():
        return 'Обновить настройки VS Code.'

    @staticmethod
    def command_settings_list():
        return 'Вывести дополнительные настройки приложения.'

    @staticmethod
    def command_settings_clear():
        return 'Очистить дополнительные настройки приложения.'

    @staticmethod
    def command_settings_localization():
        return 'Установить язык приложения.'

    @staticmethod
    def command_settings_verbose():
        return 'Управление параметром --verbose.'

    @staticmethod
    def command_settings_select():
        return 'Управление параметром --select.'

    @staticmethod
    def command_settings_hint():
        return 'Управление подсказками приложения.'

    @staticmethod
    def command_test_answer():
        return 'Тестовые ответы API.'

    @staticmethod
    def command_app_info():
        return 'Получить информацию о приложении.'

    @staticmethod
    def command_app_versions():
        return 'Получить информацию версиях приложения.'

    @staticmethod
    def command_app_auth_check():
        return 'Проверить доступ к root пользователю.'

    @staticmethod
    def command_app_auth_root():
        return 'Авторизация в sudo.'