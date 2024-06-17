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


class TextSuccessRu(Enum):
    @staticmethod
    def emulator_start_success():
        return '<green>Эмулятор успешно запущен.</green>'

    @staticmethod
    def emulator_screenshot_success(path: str):
        return '<green>Скриншот успешно сделан:</green> {}'.format(path)

    @staticmethod
    def emulator_recording_video_start():
        return '<green>Запись видео активирована.</green>'

    @staticmethod
    def emulator_recording_video_stop_with_save(path: str):
        return f'<green>Запись видео остановлена. Файл сохранен:</green> {path}'

    @staticmethod
    def emulator_recording_video_convert(path: str):
        return '<green>Видеозапись успешно конвертирована:</green> {}'.format(path)

    @staticmethod
    def ssh_exec_command_success(
            execute: str,
            stdout: str = None,
            stderr: str = None
    ):
        stdout = f'\n{stdout}' if stdout else ''
        stderr = f'\n{stderr}' if stderr else ''
        return f'<green>Команда выполнена успешно:</green> `{execute}`{stdout}{stderr}'

    @staticmethod
    def ssh_uploaded_success(remote_path: str):
        return f'<green>Файл был успешно загружен:</green> {remote_path}'

    @staticmethod
    def ssh_install_rpm(file_name: str):
        return f'<green>Пакет</green> {file_name} <green>был успешно установлен.</green>'

    @staticmethod
    def ssh_run_package(package: str):
        return f'<green>Пакет</green> {package} <green>был запущен успешно.</green>'

    @staticmethod
    def ssh_remove_rpm():
        return '<green>Пакет успешно удален.</green>'

    @staticmethod
    def validate_config_devices():
        return '<green>Раздел</green> devices <green>прошел валидацию.</green>'

    @staticmethod
    def validate_config_keys():
        return '<green>Раздел</green> keys <green>прошел валидацию.</green>'

    @staticmethod
    def validate_config_workdir():
        return '<green>Значение</green> workdir <green>прошло валидацию.</green>'

    @staticmethod
    def shell_run_app_success(name: str):
        return f'<green>Приложение запущено успешно:</green> {name}'

    @staticmethod
    def check_url_download_success(url: str):
        return f'<green>Файл будет скачан:</green> {url}'

    @staticmethod
    def download_success():
        return '<green>Файлы скачаны успешно.</green>'

    @staticmethod
    def git_clone_success():
        return '<green>Проект успешно клонирован.</green>'

    @staticmethod
    def flutter_install_success(
            path: str,
            version: str
    ):
        return f'''
<green>Установка Flutter</green> {version} <green>прошла успешно!</green>

Добавьте alias to ~/.bashrc для удобства:

    <blue>alias flutter-aurora={path}/bin/flutter</blue>

После этого выполните команду:

    <blue>source $HOME/.bashrc</blue>

И для проверки работы Flutter выполните:

    <blue>flutter-aurora --version</blue>

Удачи 👋'''

    @staticmethod
    def flutter_remove_success(version: str):
        return f'<green>Удаление Flutter</green> "{version}" <green>прошло успешно.</green>'

    @staticmethod
    def project_format_success():
        return '<green>Проект успешно отформатирован.</green>'

    @staticmethod
    def flutter_project_report_success(path: str):
        return f'<green>Генерация отчета прошла успешно.</green> {path}'

    @staticmethod
    def psdk_sign_success(file_name: str):
        return f'<green>Подпись выполнена успешно:</green> {file_name}'

    @staticmethod
    def psdk_targets_get_success(
            version: str,
            targets: []
    ):
        return f'<green>Список таргетов:</green> {version}\n' + '\n'.join(targets)

    @staticmethod
    def psdk_package_install_success():
        return '<green>Установка пакета прошла успешно.</green>'

    @staticmethod
    def psdk_package_remove_success():
        return '<green>Удаление пакета прошло успешно.</green>'

    @staticmethod
    def psdk_clear_success():
        return '<green>Удаление снимка прошло успешно.</green>'

    @staticmethod
    def psdk_validate_success():
        return '<green>Пакет прошел валидацию успешно.</green>'

    @staticmethod
    def psdk_sudoers_add_success(
            version: str,
            path: str
    ):
        return f'<green>Версия</green> {version} <green>добавлена в файл:</green> {path}'

    @staticmethod
    def psdk_sudoers_remove_success(
            version: str,
            path: str
    ):
        return f'<green>Версия</green> {version} <green>удалена из файла:</green> {path}'

    @staticmethod
    def tar_unpack_success():
        return '<green>Распаковка прошла успешно.</green>'

    @staticmethod
    def psdk_tooling_install_success():
        return '<green>Установка инструмента прошла успешно.</green>'

    @staticmethod
    def psdk_target_install_success():
        return f'<green>Установка цели прошла успешно.</green>'

    @staticmethod
    def psdk_install_success(
            path: str,
            version: str
    ):
        return f'''
<green>Установка Аврора Platform SDK</green> {version} <green>прошла успешно!</green>

Вам следует обновить ~/.bashrc, включив в него экспорт:

    <blue>export PSDK_DIR={path}/sdks/aurora_psdk</blue>

Добавьте псевдоним для удобства:

    <blue>alias aurora_psdk={path}/sdks/aurora_psdk/sdk-chroot</blue>

После этого выполните команду:

    <blue>source ~/.bashrc</blue>

Проверить установку можно командой:

    <blue>aurora_psdk sdk-assistant list</blue>

Файлы скачаны в папку ~/Загрузки, если они вам больше не нужны, удалите их.

Удачи 👋'''

    @staticmethod
    def psdk_remove_success(version: str):
        return f'<green>Аврора Platform SDK</green> {version} <green>успешно удалена.</green>'

    @staticmethod
    def image_resize_success(path: str):
        return f'<green>Изображения были успешно созданы:</green> {path}'

    @staticmethod
    def flutter_clear_success():
        return '<green>Очистка проекта прошла успешно.</green>'

    @staticmethod
    def flutter_get_pub_success():
        return '<green>Получение зависимостей прошло успешно.</green>'

    @staticmethod
    def flutter_run_build_runner_success():
        return '<green>Успешно выполнил работу build_runner.</green>'

    @staticmethod
    def flutter_build_success(paths: []):
        new_line = '\n' if len(paths) > 1 else ''
        return f'<green>Сборка проекта прошла успешно:</green> {new_line}' + ''.join(paths)

    @staticmethod
    def flutter_enable_custom_device_success():
        return '<green>Успешно активированы кастомные устройства.</green>'

    @staticmethod
    def vscode_extension_install_success(version: str):
        return f'<green>Расширение</green> {version} <green>было успешно установлено.</green>'

    @staticmethod
    def ssh_copy_id_success():
        return '<green>Ключ успешно зарегистрирован на устройстве.</green>'
