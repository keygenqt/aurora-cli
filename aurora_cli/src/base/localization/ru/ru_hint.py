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

from aurora_cli.src.base.utils.argv import argv_is_select, argv_is_verbose, argv_is_api, argv_is_apm


class TextHintRU(Enum):
    @staticmethod
    def emulator_run():
        return '<i>Запустить эмулятор можно следующей командой:</i> aurora-cli emulator start'

    @staticmethod
    def install_app():
        return f'<i>Вам необходимо установить приложение.</i>'

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
        return '<i>Возможно, у вас неверно настроены параметры устройства в конфигурационном файле.</i>'

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
    def psdk_documentation_keys_link():
        return ('<i>Более подробную информацию можно найти в документации:</i> '
                'https://developer.auroraos.ru/doc/software_development/guides/package_signing')

    @staticmethod
    def flutter_install():
        return '<i>Вы можете установить Flutter с помощью следующей команды:</i> aurora-cli flutter install'

    @staticmethod
    def psdk_install():
        return '<i>Вы можете установить Aurora Platform SDK с помощью следующей команды:</i> aurora-cli psdk install'

    @staticmethod
    def sdk_install():
        return '<i>Вы можете установить Aurora SDK с помощью следующей команды:</i> aurora-cli sdk install'

    @staticmethod
    def sdk_reinstall():
        return '<i>Если вы хотите установить новую версию, нужно удалить старую:</i> aurora-cli sdk tool'

    @staticmethod
    def hint_download_error():
        return '<i>Проверьте соединение с интернетом или просто попробуйте позже.</i>'

    @staticmethod
    def hint_check_download_error():
        return '<i>Скачивание не начнется пока не будут устранены все ошибки.</i>'

    @staticmethod
    def use_select():
        if argv_is_select() or argv_is_api():
            return ''
        return '<i>Для выбора других версий используйте флаг:</i> --select'

    @staticmethod
    def use_verbose():
        if argv_is_verbose() or argv_is_api():
            return ''
        return '<i>Для более подробного вывода используйте флаг:</i> --verbose'

    @staticmethod
    def use_apm():
        if argv_is_apm() or argv_is_api():
            return ''
        return '<i>Возможно вам стоит включить режим apm:</i> --apm'

    @staticmethod
    def psdk_keys_info():
        return '<i>В конфигурационный файл приложения вы можете добавить ваши ключи, если такие имеются.</i>'

    @staticmethod
    def ssh_key():
        return '<i>Для примера: auth: ~/.ssh/id_rsa. Создать ключ можно командой: ssh-keygen -t rsa</i>'

    @staticmethod
    def ssh_copy_id():
        return '<i>Для регистрации ключа на девайсе воспользуйтесь командой:</i> aurora-cli device ssh-copy-id'

    @staticmethod
    def ssh_forward_port():
        return '<i>Попробуйте удалить старое соединение:</i> rm ~/.ssh/known_hosts'

    @staticmethod
    def custom_devices():
        return ('<i>Для запуска debug потребуется добавить custom-devices, если вы еще этого не сделали:</i> '
                'aurora-cli flutter custom-devices')

    @staticmethod
    def debug_aurora():
        return ('<i>Для debug Аврора приложений воспользуйтесь Аврора SDK:</i> '
                'https://developer.auroraos.ru/doc/software_development/sdk')

    @staticmethod
    def workdir():
        return '<i>В конфигурационном файле можно указать</i> workdir <i>это облегчит поиск.</i>'

    @staticmethod
    def flutter_project_add_target():
        return ('<i>Возможно не была добавлена поддержка платформы: '
                '</i> flutter-aurora create --platforms=aurora --org={org} .')

    @staticmethod
    def settings_hint():
        return ('<i>Подробно с дополнительными настройками вы можете ознакомится на странице документации:</i> '
                'https://aurora-cli.keygenqt.com')
