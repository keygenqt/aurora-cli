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


class TextErrorRu(Enum):
    @staticmethod
    def shell_exec_command_empty():
        return '<red>Ошибка чтения аргументов оболочки.</red>'

    @staticmethod
    def emulator_not_found():
        return '<red>Эмулятор с ОС Аврора не найден.</red>'

    @staticmethod
    def emulator_not_found_running():
        return '<red>Ни одного работающего эмулятора с ОС Аврора не обнаружено.</red>'

    @staticmethod
    def emulator_start_error():
        return '<red>Не удалось запустить эмулятор.</red>'

    @staticmethod
    def emulator_path_not_found():
        return '<red>Не удалось найти путь к эмулятору.</red>'

    @staticmethod
    def route_not_found():
        return '<red>Маршрут не найден.</red>'

    @staticmethod
    def emulator_screenshot_error():
        return '<red>Не удалось сделать скриншот.</red>'

    @staticmethod
    def emulator_already_running_recording():
        return '<red>Эмулятор записи видео уже включен.</red>'

    @staticmethod
    def emulator_not_running_recording():
        return '<red>Не удалось запустить запись видео.</red>'

    @staticmethod
    def emulator_recording_video_start_error():
        return '<red>Не удалось активировать запись видео.</red>'

    @staticmethod
    def emulator_recording_video_stop_error():
        return '<red>Не удалось отключить запись видео.</red>'

    @staticmethod
    def emulator_recording_video_file_not_found():
        return '<red>Не удалось найти файл видеозаписи.</red>'

    @staticmethod
    def emulator_recording_video_convert_error():
        return '<red>Не удалось преобразовать видеозапись.</red>'

    @staticmethod
    def ssh_connect_emulator_error():
        return '<red>Ошибка подключения к эмулятору через SSH.</red>'

    @staticmethod
    def ssh_connect_device_error():
        return '<red>Ошибка подключения к устройству через SSH.</red>'

    @staticmethod
    def ssh_run_application_error(package: str):
        return f'<red>При запуске приложения произошла ошибка:</red> {package}'

    @staticmethod
    def ssh_upload_error():
        return '<red>Не удалось загрузить файл.</red>'

    @staticmethod
    def ssh_download_error():
        return '<red>Не удалось загрузить файл.</red>'

    @staticmethod
    def file_not_found_error(path: str):
        return f'<red>Файл не найден:</red> {path}'

    @staticmethod
    def file_already_exists_error(path: str):
        return f'<red>Файл уже существует:</red> {path}'

    @staticmethod
    def file_read_error(path: str):
        return f'<red>Ошибка чтения файла:</red> {path}'

    @staticmethod
    def ssh_install_rpm_error():
        return '<red>Ошибка установки пакета RPM.</red>'

    @staticmethod
    def ssh_remove_rpm_error():
        return '<red>Произошла ошибка при удалении пакета.</red>'

    @staticmethod
    def validate_config_error():
        return '<red>Файл конфигурации не прошел валидацию.</red>'

    @staticmethod
    def validate_config_devices_not_found():
        return '<red>Раздел</red> devices <red>не найден.</red>'

    @staticmethod
    def validate_config_devices():
        return '<red>Раздел</red> devices <red>неправильный.</red>'

    @staticmethod
    def validate_config_keys_not_found():
        return '<red>Раздел</red> keys <red>не найден.</red>'

    @staticmethod
    def validate_config_keys():
        return '<red>Раздел</red> keys <red>неправильный.</red>'

    @staticmethod
    def validate_config_key_not_found(path: str):
        return f'<red>Не найден файла ключа:</red> {path}'

    @staticmethod
    def validate_config_cert_not_found(path: str):
        return f'<red>Не найден файл сертификата:</red> {path}'

    @staticmethod
    def validate_config_workdir_not_found():
        return '<red>Не удалось найти и создать</red> workdir <red>директорию.</red>'

    @staticmethod
    def validate_config_workdir_error_create(path: str):
        return f'<red>Директория</red> {path} <red>не найдена.</red>'

    @staticmethod
    def validate_config_arg_path(path: str):
        return f'<red>Указанный файл конфигурации не существует:</red> {path}'

    @staticmethod
    def config_arg_path_load_error(path: str):
        return f'<red>Чтение файла конфигурации завершилось с ошибкой:</red> {path}'

    @staticmethod
    def index_error():
        return '<red>Введен неверный индекс.</red>'

    @staticmethod
    def index_and_select_at_the_same_time():
        return '<red>Выберите один аргумент</red> --select <red>или</red> --index<red>.</red>'

    @staticmethod
    def dependency_not_found(dependency: str):
        return f'<red>Зависимость</red> {dependency} <red>не найдена и необходима для запуска этой команды.</red>'

    @staticmethod
    def request_error():
        return '<red>Ошибка подключения к интернету. Проверьте соединение.</red>'

    @staticmethod
    def request_empty_error():
        return '<red>Запрос дал пустой результат. Произошла ошибка...</red>'

    @staticmethod
    def just_empty_error():
        return '<yellow>Ничего не найдено.</yellow>'

    @staticmethod
    def config_value_empty_error():
        return '<yellow>Не найдены элементы для выбора, проверьте конфигурационный файл.</yellow>'

    @staticmethod
    def flutter_already_installed_error(version: str):
        return f'<red>Flutter уже установлен:</red> {version}'

    @staticmethod
    def flutter_not_found_error(version: str = ''):
        if version:
            return f'<red>Не найдено: Flutter SDK. Версия:</red> {version}'
        else:
            return '<red>Не найдено: Flutter SDK.</red>'

    @staticmethod
    def psdk_not_found_error(version: str = ''):
        if version:
            return f'<red>Не найдено: Аврора Platform SDK. Версия:</red> {version}'
        else:
            return '<red>Не найдено: Аврора Platform SDK.</red>'

    @staticmethod
    def sdk_not_found_error(version: str = ''):
        if version:
            return f'<red>Не найдено: Аврора SDK. Версия:</red> {version}'
        else:
            return '<red>Не найдено: Аврора SDK.</red>'

    @staticmethod
    def sdk_already_installed_error():
        return '<red>Аврора SDK уже установлено.</red>'

    @staticmethod
    def psdk_already_installed_error(version: str):
        return f'<red>Аврора Platform SDK</red> {version} <red>уже установлено.</red>'

    @staticmethod
    def device_not_found_error(host: str):
        return f'<red>Не найдено: Устройство. Host: </red> {host}'

    @staticmethod
    def shell_run_app_error(name: str):
        return f'<red>Не удалось запустить приложение:</red> {name}'

    @staticmethod
    def download_error():
        return '<red>Скачивание завершилось с ошибкой.</red>'

    @staticmethod
    def start_download_error():
        return '<red>Не удалось начать скачивание.</red>'

    @staticmethod
    def abort_download_error():
        return '<red>Загрузка прервана.</red>'

    @staticmethod
    def check_url_download_error(url: str):
        return f'<red>Не удалось получить информацию о файле по URL:</red> {url}'

    @staticmethod
    def check_url_download_dir_error(path: str):
        return f'<red>В папке назначения имя уже занято:</red> {path}'

    @staticmethod
    def check_url_download_exist_error(path: str):
        return f'<red>Найден неизвестный файл с таким же названием:</red> {path}'

    @staticmethod
    def get_install_info_error():
        return '<red>Не удалось получить информацию об установочных файлах.</red>'

    @staticmethod
    def git_clone_error():
        return '<red>Не удалось выполнить клонирование репозитория.</red>'

    @staticmethod
    def flutter_project_not_found(path: str):
        return f'<red>Проект Flutter c поддержкой ОС Аврора не найден:</red> {path}'

    @staticmethod
    def psdk_project_not_found(path: str):
        return f'<red>Проект Аврора не найден:</red> {path}'

    @staticmethod
    def project_format_error():
        return f'<red>Произошла ошибка при форматировании проекта.</red>'

    @staticmethod
    def psdk_sign_error():
        return '<red>Возникла ошибка при подписи.</red>'

    @staticmethod
    def psdk_targets_get_error():
        return '<red>Произошла ошибка при получении таргетов.</red>'

    @staticmethod
    def exec_command_error():
        return '<red>Произошла ошибка при выполнении команды.</red>'

    @staticmethod
    def psdk_validate_error():
        return '<red>Пакет не прошел валидацию.</red>'

    @staticmethod
    def image_size_icon_error(
            width: int,
            height: int
    ):
        return '<red>Минимальный размер изображения {}x{}.</red>'.format(width, height)

    @staticmethod
    def search_application_id_error():
        return '<red>Не удалось прочитать идентификатор приложения.</red>'

    @staticmethod
    def arch_not_found():
        return '<red>Тип архитектуры не найден.</red>'

    @staticmethod
    def debug_apm_error():
        return '<red>Установка debug пакетов для apm не доступна.</red>'

    @staticmethod
    def debug_mode_error():
        return '<red>Для запуска приложения в этом режиме требуется сборка с флагом:</red> --debug'

    @staticmethod
    def debug_apm_gdb_error():
        return '<red>Установка через</red> --apm <red>не поддерживаем debug по GDB.</red>'

    @staticmethod
    def run_without_install_error():
        return '<red>Не указан флаг установки</red> --install (-i)'

    @staticmethod
    def flutter_read_json_error():
        return '<red>Не удалось получить данные пакетов.</red>'

    @staticmethod
    def flutter_read_yaml_error():
        return '<red>Не удалось прочитать pubspec файл.</red>'

    @staticmethod
    def vscode_extension_install_error():
        return '<red>Не удалось установить расширение.</red>'

    @staticmethod
    def ssh_copy_id_without_key():
        return '<red>В поле auth устройства, укажите путь к ssh ключу в файле конфигурации приложения.</red>'

    @staticmethod
    def ssh_copy_id_error():
        return '<red>Не удалось зарегистрировать ключ на устройстве.</red>'

    @staticmethod
    def ssh_run_debug_error():
        return '<red>Для запуска приложения в режиме debug подключение должно быть через ssh ключ.</red>'

    @staticmethod
    def ssh_forward_port_error():
        return '<red>Не удалось пробросить ssh порты.</red>'

    @staticmethod
    def run_emulator_arch_error():
        return '<red>Архитектура для установки приложения на эмулятор не подходит.</red>'

    @staticmethod
    def repo_search_error():
        return '<red>Не удалось найти версию для установки в репозитории.</red>'

    @staticmethod
    def get_data_error():
        return '<red>Не удалось получить данные.</red>'