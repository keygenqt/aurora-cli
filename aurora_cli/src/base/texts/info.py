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

from aurora_cli.src.base.utils.path import path_convert_relative_path


class TextInfo(Enum):
    @staticmethod
    def command_execute(command: str):
        return f'<blue>Command execute:</blue> `{command}`'

    @staticmethod
    def emulator_start_locked():
        return '<blue>The emulator is already running.</blue>'

    @staticmethod
    def emulator_recording_video_stop_already():
        return '<blue>The emulator recording video is already off.</blue>'

    @staticmethod
    def shh_download_start(path: str):
        path = path_convert_relative_path(path)
        if path and path.is_file():
            return f'<blue>Starting file download:</blue> {path}'

    @staticmethod
    def shh_download_progress():
        return '<blue>File download progress in percentage.</blue>'

    @staticmethod
    def ssh_install_rpm():
        return '<blue>Starting install RPM package...</blue>'

    @staticmethod
    def select_array_out(key: str, names: []):
        if names:
            return (f'<blue>Select</blue> {key} <blue>index:</blue>\n'
                    + '\n'.join([f'{i + 1}: {n}' for i, n in enumerate(names)]))

    @staticmethod
    def create_default_config_file(path: str):
        return f'<blue>A default configuration file has been created:</blue> {path}'
