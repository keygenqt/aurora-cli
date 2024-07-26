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


class TextInfoRu(Enum):
    @staticmethod
    def command_execute(command: str):
        return f'<blue>Выполнена команда:</blue> `{command}`'

    @staticmethod
    def emulator_start_locked():
        return '<blue>Эмулятор уже запущен.</blue>'

    @staticmethod
    def emulator_recording_video_stop_already():
        return '<blue>Эмулятор записи видео уже выключен.</blue>'

    @staticmethod
    def shh_download_start():
        return f'<blue>Начинаем загрузку файла...</blue>'

    @staticmethod
    def shh_upload_progress():
        return '<blue>Прогресс загрузки файла в процентах.</blue>'

    @staticmethod
    def ssh_start_install_rpm():
        return '<blue>Начинаем установку пакета RPM...</blue>'

    @staticmethod
    def download_progress():
        return '<blue>Прогресс загрузки файла в процентах.</blue>'

    @staticmethod
    def install_progress():
        return '<blue>Прогресс установки в процентах.</blue>'

    @staticmethod
    def git_clone_start(url: str):
        return f'<blue>Начато клонирование репозитория:</blue> {url}'

    @staticmethod
    def git_clone_progress(title: str):
        return f'<blue>Прогресс клонирования репозитория:</blue> {title}'

    @staticmethod
    def select_array_out(
            key: str,
            names: []
    ):
        if names:
            return (f'<blue>Выберите</blue> {key} <blue>индекс:</blue>\n'
                    + '\n'.join([f'{i + 1}: {n}' for i, n in enumerate(names)]))

    @staticmethod
    def create_default_config_file(path: str):
        return f'<blue>Был создан файл конфигурации по умолчанию:</blue> {path}'

    @staticmethod
    def available_versions_sdk(versions: []):
        return '<blue>Доступные версии Аврора SDK:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    def available_versions_psdk(versions: []):
        return '<blue>Доступные версии Аврора Platform SDK:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    def available_versions_flutter(versions: []):
        return '<blue>Доступные версии Flutter для ОС Аврора:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    def available_versions_plugins(versions: []):
        return '<blue>Доступные версии Flutter плагинов для ОС Аврора:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    def installed_versions_sdk(versions: []):
        return '<blue>Установленная версия Аврора SDK:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    def installed_versions_psdk(versions: []):
        return '<blue>Установленные версии Аврора Platform SDK:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    def installed_versions_flutter(versions: []):
        return '<blue>Установленные версии Flutter для ОС Аврора:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    def cache_clear():
        return '<blue>Кеш приложения был очищен.</blue>'

    @staticmethod
    def check_url_download_exist(path: str):
        return f'<blue>Файл уже существует:</blue> {path}'

    @staticmethod
    def flutter_project_format_cpp_done():
        return '<blue>Форматирование C++ окончено.</blue>'

    @staticmethod
    def flutter_project_format_dart_done():
        return '<blue>Форматирование Dart окончено.</blue>'

    @staticmethod
    def flutter_project_pub_get():
        return '<blue>Получение зависимостей проекта...</blue>'

    @staticmethod
    def flutter_gen_plugins_report():
        return '<blue>Генерация отчета по плагинам проекта...</blue>'

    @staticmethod
    def file_check_and_download():
        return f'<blue>Качаем необходимые файлы...</blue>'

    @staticmethod
    def psdk_sign_use_public_keys():
        return '<blue>Для подписи будут использованы публичные ключи.</blue>'

    @staticmethod
    def psdk_targets_empty(version: str):
        return f'<yellow>Список таргетов пуст:</yellow> {version}'

    @staticmethod
    def psdk_package_not_found():
        return f'<blue>Пакеты не найдены.</blue>'

    @staticmethod
    def psdk_package_search(values: []):
        return (f'<blue>Найдены пакеты:</blue>\n'
                + '\n'.join([f'{value["Name"]} ({value["Version"]})' for value in values]))

    @staticmethod
    def psdk_package_already_installed():
        return '<blue>Пакет уже установлен.</blue>'

    @staticmethod
    def psdk_sudoers_exist(
            version: str,
            path: str
    ):
        return f'<blue>Версия</blue> {version} <blue>уже указана в файле:</blue> {path}'

    @staticmethod
    def psdk_sudoers_not_found(
            version: str,
            path: str
    ):
        return f'<blue>Версия</blue> {version} <blue>не найдена в файле:</blue> {path}'

    @staticmethod
    def psdk_install_start():
        return '<blue>Установка Аврора Platform SDK.</blue>'

    @staticmethod
    def psdk_remove_start():
        return '<blue>Установка Аврора Platform SDK.</blue>'

    @staticmethod
    def psdk_download_start():
        return '<blue>Загрузка файлов Аврора Platform SDK.</blue>'

    @staticmethod
    def vscode_extensions_flutter(extensions: []):
        return '<blue>Будут установлены расширения для работы с Flutter:</blue>\n' + '\n'.join(extensions)

    @staticmethod
    def vscode_extensions_cpp(extensions: []):
        return '<blue>Будут установлены расширения для работы с C++:</blue>\n' + '\n'.join(extensions)

    @staticmethod
    def vscode_extensions_other(extensions: []):
        return '<blue>Будут установлены расширения для работы с VS Code:</blue>\n' + '\n'.join(extensions)

    @staticmethod
    def vscode_extensions_installing(extension: str):
        return f'<blue>Установка расширения:</blue> {extension}'

    @staticmethod
    def vscode_settings_update(path: str):
        return f'<blue>Конфигурационный файл обновлен:</blue> {path}'

    @staticmethod
    def vscode_settings_not_update():
        return '<blue>Конфигурационный файл не требует обновления.</blue>'

    @staticmethod
    def vscode_extensions_flutter_installed():
        return '<blue>Расширения для работы с Flutter уже установлены.</blue>'

    @staticmethod
    def vscode_extensions_cpp_installed():
        return '<blue>Расширения для работы с C++ уже установлены.</blue>'

    @staticmethod
    def vscode_extensions_other_installed():
        return '<blue>Расширения для работы с VS Code уже установлены.</blue>'

    @staticmethod
    def devices_not_found():
        return '<blue>Устройства не найдены.</blue>'

    @staticmethod
    def ssh_copy_id_password():
        return '<blue>Введите пароль подключения по ssh, его можно найти в настройках устройства.</blue>'

    @staticmethod
    def ssh_debug_without_project_gdb(bin_path: str, host: str, package: str):
        return ('<blue>Для подключения к GDB debug через VS Code, добавьте</blue>'
                ' launch.json '
                '<blue>с таким содержимым:</blue>'
                '\n{'
                '\n   "configurations": ['
                '\n       {'
                '\n           "name": "Flutter Aurora OS GDB Debug",'
                '\n           "type": "cppdbg",'
                '\n           "request": "launch",'
                f'\n           "program": "{bin_path}",'
                '\n           "MIMode": "gdb",'
                '\n           "miDebuggerPath": "/usr/bin/gdb-multiarch",'
                f'\n           "miDebuggerServerAddress": "{host}:2345",'
                '\n           "useExtendedRemote": true,'
                '\n           "cwd": "${workspaceRoot}",'
                '\n       }'
                '\n   ]'
                '\n}'
                '\n<blue>и добавьте файл инициализации</blue>'
                ' .gdbinit '
                '<blue>в корень проекта:</blue>'
                '\nhandle SIGILL pass nostop noprint'
                f'\nset remote exec-file /usr/bin/{package}\n'
                '\n<blue>Или просто запустите приложение из корня проекта, '
                'все добавится автоматически.</blue>')

    @staticmethod
    def ssh_debug_without_project_dart(dart_vm_url: str):
        return ('<blue>Для подключения к Dart debug через VS Code, добавьте</blue>'
                ' launch.json '
                '<blue>с таким содержимым:</blue>'
                '\n{'
                '\n   "configurations": ['
                '\n       {'
                '\n           "name": "Flutter Aurora OS Dart Debug",'
                '\n           "type": "dart",'
                '\n           "request": "attach",'
                f'\n           "vmServiceUri": "{dart_vm_url}",'
                '\n           "program": "lib/main.dart"'
                '\n       }'
                '\n   ]'
                '\n}'
                '\n<blue>Или просто запустите приложение из корня проекта, '
                'все добавится автоматически.</blue>')

    @staticmethod
    def devices_password_not_connect(host: str):
        return (f'<blue>Девайс,</blue>'
                f' {host} '
                f'<blue>подключенный с помощью пароля не будет добавлен, используйте ssh key в auth.</blue>')

    @staticmethod
    def devices_turn_on():
        return '<blue>Для получения необходимой информации об устройствах, они должны быть подключены.</blue>'

    @staticmethod
    def update_launch_json_gdb():
        return '<blue>Файл</blue> launch.json <blue>был обновлен, можно запускать GDB debug в VS Code.</blue>'

    @staticmethod
    def update_launch_json_dart():
        return '<blue>Файл</blue> launch.json <blue>был обновлен, можно запускать Dart debug в VS Code.</blue>'

    @staticmethod
    def ssh_run_debug_aurora():
        return '<yellow>Debug для Аврора приложения не предусмотрен, только для приложений Flutter.</yellow>'

    @staticmethod
    def run_debug_application():
        return '<blue>Приложение будет запущено вне песочницы.</blue>'

    @staticmethod
    def run_mode_debug_info():
        return '<blue>Приложение должно было быть собрано в debug режиме.</blue>'

    @staticmethod
    def search_installed_flutter_sdk(path: str):
        return f'<blue>Поиск в каталоге</blue> {path} <blue>Flutter SDK...</blue>'

    @staticmethod
    def search_installed_aurora_psdk_hint(path: str):
        return f'<blue>Поиск в каталоге</blue> {path} <blue>Aurora Platform SDK...</blue>'

    @staticmethod
    def search_installed_aurora_sdk_hint(path: str):
        return f'<blue>Поиск в каталоге</blue> {path} <blue>Aurora SDK...</blue>'

    @staticmethod
    def search_installed_aurora_psdk(path: str):
        return f'<blue>Поиск в каталоге</blue> {path} <blue>Aurora Platform SDK...</blue>'

    @staticmethod
    def search_installed_aurora_sdk(path: str):
        return f'<blue>Поиск в каталоге</blue> {path} <blue>Aurora SDK...</blue>'

    @staticmethod
    def install_debug_apm_dart_debug():
        return '<yellow>Через apm будет установлен только основной пакет, для Dart debug этого достаточно.</yellow>'

    @staticmethod
    def settings_list(values: dict):
        return ('<blue>Список текущих настроек:</blue>\n{}'
                .format('\n'.join([f'{key}: {value}' for key, value in values.items()])))

    @staticmethod
    def settings_item_empty():
        return 'Значение не установлено.'
