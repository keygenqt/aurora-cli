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

from aurora_cli.src.base.texts.tint import tint


class TextError(Enum):
    @staticmethod
    def shell_exec_command_empty():
        return '<red>Error reading shell arguments.</red>'

    @staticmethod
    def emulator_not_found():
        return '<red>Emulator with Aurora OS not found.</red>'

    @staticmethod
    @tint
    def emulator_not_found_running():
        return '<red>No running emulator with Aurora OS was found.</red>'

    @staticmethod
    def emulator_start_error():
        return '<red>Failed to start the emulator.</red>'

    @staticmethod
    def emulator_path_not_found():
        return '<red>Could not find path to emulator.</red>'

    @staticmethod
    def route_not_found():
        return '<red>Route not found.</red>'

    @staticmethod
    def emulator_screenshot_error():
        return '<red>Failed to take screenshot.</red>'

    @staticmethod
    def emulator_already_running_recording():
        return '<red>The emulator recording video is already on.</red>'

    @staticmethod
    def emulator_not_running_recording():
        return '<red>The emulator recording not started.</red>'

    @staticmethod
    def emulator_recording_video_start_error():
        return '<red>Failed to activate video recording.</red>'

    @staticmethod
    def emulator_recording_video_stop_error():
        return '<red>Failed to deactivate video recording.</red>'

    @staticmethod
    def emulator_recording_video_file_not_found():
        return '<red>Could not find video recording.</red>'

    @staticmethod
    def emulator_recording_video_convert_error():
        return '<red>Could not convert video recording.</red>'

    @staticmethod
    def ssh_connect_emulator_error():
        return '<red>Error connecting to emulator via SSH.</red>'

    @staticmethod
    def ssh_connect_device_error():
        return '<red>Error connecting to device via SSH.</red>'

    @staticmethod
    def ssh_run_application_error(package: str):
        return f'<red>An error occurred while starting the application:</red> {package}'

    @staticmethod
    def ssh_upload_error():
        return '<red>Failed to upload files.</red>'

    @staticmethod
    def ssh_upload_file_not_found(path: str):
        return f'<red>File not found for download:</red> {path}'

    @staticmethod
    def ssh_install_rpm_error():
        return '<red>Error installing RPM package.</red>'

    @staticmethod
    def ssh_remove_rpm_error():
        return '<red>An error occurred while deleting the package.</red>'

    @staticmethod
    def validate_config_error():
        return '<red>The configuration file failed verification.</red>'

    @staticmethod
    @tint
    def validate_config_devices_not_found():
        return '<red>Section</red> devices <red>not found.</red>'

    @staticmethod
    @tint
    def validate_config_devices():
        return '<red>Section</red> devices <red>incorrect.</red>'

    @staticmethod
    @tint
    def validate_config_keys_not_found():
        return '<red>Section</red> keys <red>not found.</red>'

    @staticmethod
    @tint
    def validate_config_keys():
        return '<red>Section</red> keys <red>incorrect.</red>'

    @staticmethod
    def validate_config_key_not_found(path: str):
        return f'<red>Not found file key:</red> {path}'

    @staticmethod
    def validate_config_cert_not_found(path: str):
        return f'<red>Not found file cert:</red> {path}'

    @staticmethod
    @tint
    def validate_config_workdir_not_found():
        return '<red>It was not possible to find and create the</red> workdir <red>folder.</red>'

    @staticmethod
    def validate_config_workdir_error_create(path: str):
        return f'<red>Folder</red> {path} <red>not found.</red>'

    @staticmethod
    def validate_config_arg_path(path: str):
        return f'<red>The specified configuration file does not exist:</red> {path}'

    @staticmethod
    @tint
    def config_arg_path_load_error(path: str):
        return f'<red>Configuration file cannot be read:</red> {path}'

    @staticmethod
    def index_error():
        return '<red>Invalid index entered.</red>'

    @staticmethod
    def index_and_select_at_the_same_time():
        return '<red>Select one thing</red> --select <red>or</red> --index<red>.</red>'

    @staticmethod
    @tint
    def dependency_not_found(dependency: str):
        return f'<red>Dependency</red> {dependency} <red>was not found and is required to run this command.</red>'
