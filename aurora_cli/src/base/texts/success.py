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
    def emulator_start_success():
        return '<green>Emulator started successfully.</green>'

    @staticmethod
    def emulator_screenshot_success(path: str):
        return '<green>Screenshot taken successfully:</green> {}'.format(path)

    @staticmethod
    def emulator_recording_video_start():
        return '<green>Video recording activated.</green>'

    @staticmethod
    def emulator_recording_video_stop_with_save(path: str):
        return f'<green>Video recording has stopped. File saved:</green> {path}'

    @staticmethod
    def emulator_recording_video_convert(path: str):
        return '<green>Video record convert successfully:</green> {}'.format(path)

    @staticmethod
    def ssh_exec_command_success(execute: str, stdout: str = None, stderr: str = None):
        stdout = f'\n{stdout}' if stdout else ''
        stderr = f'\n{stderr}' if stderr else ''
        return f'<green>The command was executed successfully:</green> `{execute}`{stdout}{stderr}'

    @staticmethod
    def ssh_uploaded_success(remote_path: str):
        return '<green>The file was successfully uploaded:</green> {}'.format(remote_path)

    @staticmethod
    def ssh_install_rpm(file_name: str):
        return f'<green>Package</green> {file_name} <green>was installed successfully.</green>'

    @staticmethod
    def ssh_run_package(package: str):
        return f'<green>Package</green> {package} <green>was run successfully.</green>'

    @staticmethod
    def ssh_remove_rpm():
        return '<green>Package was successfully removed.</green>'

    @staticmethod
    def validate_config_devices():
        return '<green>Section</green> devices <green>was validated successfully.</green>'

    @staticmethod
    def validate_config_keys():
        return '<green>Section</green> keys <green>was validated successfully.</green>'

    @staticmethod
    def validate_config_workdir():
        return '<green>Value</green> workdir <green>was validated successfully.</green>'
