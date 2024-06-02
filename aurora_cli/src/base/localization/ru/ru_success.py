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
