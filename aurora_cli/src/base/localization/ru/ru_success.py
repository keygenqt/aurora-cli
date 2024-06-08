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
    def ssh_exec_command_success(execute: str, stdout: str = None, stderr: str = None):
        stdout = f'\n{stdout}' if stdout else ''
        stderr = f'\n{stderr}' if stderr else ''
        return f'<green>Команда выполнена успешно:</green> `{execute}`{stdout}{stderr}'

    @staticmethod
    def ssh_uploaded_success(remote_path: str):
        return '<green>Файл был успешно загружен:</green> {}'.format(remote_path)

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
    def check_url_download_success():
        return '<green>Файл готов к скачиванию.</green>'

    @staticmethod
    def download_success():
        return '<green>Файлы скачаны успешно.</green>'

    @staticmethod
    def git_clone_success():
        return '<green>Проект успешно клонирован.</green>'

    @staticmethod
    def flutter_install_success(path: str, version: str):
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
    def flutter_project_format_success():
        return '<green>Проект успешно отформатирован.</green>'

    @staticmethod
    def flutter_project_build_success():
        return '<green>Сборка проекта прошла успешно.</green>'

    @staticmethod
    def flutter_project_report_success():
        return '<green>Генерация отчета прошла успешно.</green>'

    @staticmethod
    def psdk_sign_success():
        return '<green>Подпись выполнена успешно.</green>'
