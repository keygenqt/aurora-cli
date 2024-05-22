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


class TextSuccess(Enum):
    @staticmethod
    def emulator_start_success() -> str:
        return '<green>Emulator started successfully.</green>'

    @staticmethod
    def emulator_screenshot_success(path: str) -> str:
        return '<green>Screenshot taken successfully:</green> {}'.format(path)

    @staticmethod
    def emulator_recording_video_start() -> str:
        return '<green>Video recording activated.</green>'

    @staticmethod
    def emulator_recording_video_stop() -> str:
        return '<green>Video recording is deactivated.</green>'

    @staticmethod
    def emulator_recording_video_convert(path: str) -> str:
        return '<green>Video record convert successfully:</green> {}'.format(path)

    @staticmethod
    def ssh_exec_command_success(execute: str, stdout: str = None, stderr: str = None) -> str:
        stdout = f'\n{stdout}' if stdout else ''
        stderr = f'\n{stderr}' if stderr else ''
        return f'<green>The command was executed successfully:</green> `{execute}`{stdout}{stderr}'

    @staticmethod
    def ssh_uploaded_success(remote_path: str) -> str:
        return '<green>The file was successfully uploaded:</green> {}'.format(remote_path)

    @staticmethod
    def ssh_install_rpm(file_name: str) -> str:
        return f'<green>Package</green> {file_name} <green>was installed successfully.</green>'

    @staticmethod
    def ssh_remove_rpm() -> str:
        return '<green>Package was successfully removed.</green>'

    @staticmethod
    def validate_config_devices() -> str:
        return '<green>Section</green> devices <green>was validated successfully.</green>'

    @staticmethod
    def validate_config_keys() -> str:
        return '<green>Section</green> keys <green>was validated successfully.</green>'

    @staticmethod
    def validate_config_workdir() -> str:
        return '<green>Value</green> workdir <green>was validated successfully.</green>'
