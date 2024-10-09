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

from aurora_cli.src.base.localization.localization import localization
from aurora_cli.src.base.texts.hint import hint, Hint


class TextError(Enum):
    @staticmethod
    @localization
    def shell_exec_command_empty():
        return '<red>Reading shell arguments error.</red>'

    @staticmethod
    @localization
    @hint(Hint.not_install_emulator)
    def emulator_not_found():
        return '<red>Emulator with Aurora OS is not found.</red>'

    @staticmethod
    @localization
    @hint(Hint.emulator_run)
    def emulator_not_found_running():
        return '<red>No running emulator with Aurora OS is found.</red>'

    @staticmethod
    @localization
    def emulator_start_error():
        return '<red>Failed to start the emulator.</red>'

    @staticmethod
    @localization
    def emulator_path_not_found():
        return '<red>Could not find path to emulator.</red>'

    @staticmethod
    @localization
    @hint(Hint.route_error_hint, Hint.documentation_link)
    def route_not_found():
        return '<red>Route is not found.</red>'

    @staticmethod
    @localization
    def emulator_screenshot_error():
        return '<red>Failed to take screenshot.</red>'

    @staticmethod
    @localization
    @hint(Hint.emulator_recording_on)
    def emulator_already_running_recording():
        return '<red>The emulator recording video is already on.</red>'

    @staticmethod
    @localization
    def emulator_not_running_recording():
        return '<red>The emulator recording is not started.</red>'

    @staticmethod
    @localization
    def emulator_recording_video_start_error():
        return '<red>Failed to activate video recording.</red>'

    @staticmethod
    @localization
    def emulator_recording_video_stop_error():
        return '<red>Failed to deactivate video recording.</red>'

    @staticmethod
    @localization
    def emulator_recording_video_file_not_found():
        return '<red>Could not find video recording.</red>'

    @staticmethod
    @localization
    def emulator_recording_video_convert_error():
        return '<red>Could not convert video recording.</red>'

    @staticmethod
    @localization
    def ssh_connect_emulator_error():
        return '<red>Connecting to emulator via SSH error.</red>'

    @staticmethod
    @localization
    @hint(Hint.device_config, Hint.documentation_link)
    def ssh_connect_device_error():
        return '<red>Connecting to device via SSH error.</red>'

    @staticmethod
    @localization
    def ssh_run_application_error(package: str):
        return f'<red>An error occurred while starting the application:</red> {package}'

    @staticmethod
    @localization
    def ssh_upload_error():
        return '<red>Failed to upload file.</red>'

    @staticmethod
    @localization
    def ssh_download_error():
        return '<red>Failed to download file.</red>'

    @staticmethod
    @localization
    def file_not_found_error(path: str):
        return f'<red>File is not found:</red> {path}'

    @staticmethod
    @localization
    def file_already_exists_error(path: str):
        return f'<red>The file has already existed:</red> {path}'

    @staticmethod
    @localization
    def file_read_error(path: str):
        return f'<red>Reading file error:</red> {path}'

    @staticmethod
    @localization
    @hint(Hint.use_apm, Hint.use_verbose)
    def ssh_install_rpm_error():
        return '<red>Installing RPM package error.</red>'

    @staticmethod
    @localization
    def ssh_remove_rpm_error():
        return '<red>An error occurred while deleting the package.</red>'

    @staticmethod
    @localization
    @hint(Hint.documentation_link)
    def validate_config_error():
        return '<red>The configuration file failed verification.</red>'

    @staticmethod
    @localization
    def validate_config_devices_not_found():
        return '<red>Section</red> devices <red>is not found.</red>'

    @staticmethod
    @localization
    def validate_config_devices():
        return '<red>Section</red> devices <red>is incorrect.</red>'

    @staticmethod
    @localization
    def validate_config_keys_not_found():
        return '<red>Section</red> keys <red>is not found.</red>'

    @staticmethod
    @localization
    def validate_config_keys():
        return '<red>Section</red> keys <red>is incorrect.</red>'

    @staticmethod
    @localization
    def validate_config_key_not_found(path: str):
        return f'<red>File key is not found:</red> {path}'

    @staticmethod
    @localization
    def validate_config_cert_not_found(path: str):
        return f'<red>File cert is not found:</red> {path}'

    @staticmethod
    @localization
    def validate_config_workdir_not_found():
        return '<red>It is not possible to find and create the</red> workdir <red>folder.</red>'

    @staticmethod
    @localization
    def validate_config_workdir_error_create(path: str):
        return f'<red>Folder is not found:</red> {path}'

    @staticmethod
    @localization
    def validate_config_arg_path(path: str):
        return f'<red>The specified configuration file does not exist:</red> {path}'

    @staticmethod
    @localization
    def config_arg_path_load_error(path: str):
        return f'<red>Configuration file cannot be read:</red> {path}'

    @staticmethod
    @localization
    def index_error():
        return '<red>Invalid index entered.</red>'

    @staticmethod
    @localization
    def index_and_select_at_the_same_time():
        return '<red>Select one thing</red> --select <red>or</red> --index<red>.</red>'

    @staticmethod
    @localization
    @hint(Hint.install_app)
    def dependency_not_found(dependency: str):
        return f'<red>Dependency</red> {dependency} <red>is not found and is required to run this command.</red>'

    @staticmethod
    @localization
    def request_error():
        return '<red>Internet connection error. Check the connection.</red>'

    @staticmethod
    @localization
    def request_empty_error():
        return '<red>The request returned an empty result. An error has occurred...</red>'

    @staticmethod
    @localization
    def just_empty_error():
        return '<yellow>Nothing is found.</yellow>'

    @staticmethod
    @localization
    def config_value_empty_error():
        return '<yellow>No items is found to select, check the configuration file.</yellow>'

    @staticmethod
    @localization
    @hint(Hint.use_select)
    def flutter_already_installed_error(version: str):
        return f'<red>Flutter has already installed:</red> {version}'

    @staticmethod
    @localization
    @hint(Hint.flutter_install, Hint.flutter_documentation_link)
    def flutter_not_found_error(version: str = ''):
        if version:
            return f'<red>Not found: Flutter SDK. Version:</red> {version}'
        else:
            return '<red>Not found: Flutter SDK.</red>'

    @staticmethod
    @localization
    @hint(Hint.psdk_install, Hint.psdk_documentation_link)
    def psdk_not_found_error(version: str = ''):
        if version:
            return f'<red>Not found: Aurora Platform SDK. Version:</red> {version}'
        else:
            return '<red>Not found: Aurora Platform SDK.</red>'

    @staticmethod
    @localization
    @hint(Hint.sdk_install, Hint.sdk_documentation_link)
    def sdk_not_found_error(version: str = ''):
        if version:
            return f'<red>Not found: Aurora SDK. Version:</red> {version}'
        else:
            return '<red>Not found: Aurora SDK.</red>'

    @staticmethod
    @localization
    @hint(Hint.sdk_reinstall)
    def sdk_already_installed_error():
        return '<red>Aurora SDK has already installed.</red>'

    @staticmethod
    @localization
    @hint(Hint.use_select)
    def psdk_already_installed_error(version: str):
        return f'<red>Aurora Platform SDK</red> {version} <red>has already installed.</red>'

    @staticmethod
    @localization
    def device_not_found_error(host: str):
        return f'<red>Not found: Device. Host: </red> {host}'

    @staticmethod
    @localization
    def shell_run_app_error(name: str):
        return f'<red>Application failed to start:</red> {name}'

    @staticmethod
    @localization
    @hint(Hint.hint_download_error)
    def download_error():
        return '<red>The download completed with an error.</red>'

    @staticmethod
    @localization
    @hint(Hint.hint_download_error)
    def start_download_error():
        return '<red>Failed to start downloading.</red>'

    @staticmethod
    @localization
    def abort_download_error():
        return '<red>The download is interrupted.</red>'

    @staticmethod
    @localization
    @hint(Hint.hint_check_download_error)
    def check_url_download_error(url: str):
        return f'<red>Failed to get file information by URL:</red> {url}'

    @staticmethod
    @localization
    @hint(Hint.hint_check_download_error)
    def check_url_download_dir_error(path: str):
        return f'<red>The name in the destination folder has already taken:</red> {path}'

    @staticmethod
    @localization
    @hint(Hint.hint_check_download_error)
    def check_url_download_exist_error(path: str):
        return f'<red>An unknown file with the same name is found:</red> {path}'

    @staticmethod
    @localization
    def get_install_info_error():
        return '<red>Failed to obtain installation files information.</red>'

    @staticmethod
    @localization
    def git_clone_error():
        return '<red>Failed to clone the repository.</red>'

    @staticmethod
    @localization
    @hint(Hint.flutter_project_add_target)
    def flutter_project_not_found(path: str):
        return f'<red>Flutter project with support Aurora OS is not found:</red> {path}'

    @staticmethod
    @localization
    def psdk_project_not_found(path: str):
        return f'<red>Aurora project is not found:</red> {path}'

    @staticmethod
    @localization
    @hint(Hint.use_verbose)
    def project_format_error():
        return '<red>An error occurred while formatting the project.</red>'

    @staticmethod
    @localization
    @hint(Hint.use_verbose)
    def psdk_sign_error():
        return '<red>An error occurred while signing.</red>'

    @staticmethod
    @localization
    @hint(Hint.use_verbose)
    def psdk_targets_get_error():
        return '<red>An error occurred while receiving targets.</red>'

    @staticmethod
    @localization
    @hint(Hint.use_verbose)
    def exec_command_error():
        return '<red>An error occurred when execution command.</red>'

    @staticmethod
    @localization
    @hint(Hint.use_verbose)
    def psdk_validate_error():
        return '<red>The package has not been validated.</red>'

    @staticmethod
    @localization
    def image_size_icon_error(
            width: int,
            height: int
    ):
        return f'<red>Minimum icon size is {width}x{height}.</red>'

    @staticmethod
    @localization
    def search_application_id_error():
        return '<red>Failed to read application ID.</red>'

    @staticmethod
    @localization
    def arch_not_found():
        return '<red>Architecture type is not found.</red>'

    @staticmethod
    @localization
    def debug_apm_error():
        return '<red>Installation of debug packages for apm is not available.</red>'

    @staticmethod
    @localization
    def debug_mode_error():
        return '<red>To run the application in this mode,</red> --debug <red>build is required.</red>'

    @staticmethod
    @localization
    def debug_apm_gdb_error():
        return '<red>Installation via</red> --apm <red> do not support debug GDB.</red>'

    @staticmethod
    @localization
    def run_without_install_error():
        return '<red>Installation flag not specified</red> --install (-i)'

    @staticmethod
    @localization
    def flutter_read_json_error():
        return '<red>Failed to retrieve package data.</red>'

    @staticmethod
    @localization
    def flutter_read_yaml_error():
        return '<red>Failed to read pubspec file.</red>'

    @staticmethod
    @localization
    def vscode_extension_install_error():
        return '<red>Failed to install extension.</red>'

    @staticmethod
    @localization
    @hint(Hint.ssh_key)
    def ssh_copy_id_without_key():
        return '<red>In the device auth field, specify path to the ssh key in the application configuration file.</red>'

    @staticmethod
    @localization
    def ssh_copy_id_error():
        return '<red>Failed to register the key on the device.</red>'

    @staticmethod
    @localization
    @hint(Hint.ssh_copy_id)
    def ssh_run_debug_error():
        return '<red>To run the application in debug mode, the connection must be via ssh key.</red>'

    @staticmethod
    @localization
    @hint(Hint.ssh_forward_port)
    def ssh_forward_port_error():
        return '<red>Failed to forward ssh ports.</red>'

    @staticmethod
    @localization
    def run_emulator_arch_error():
        return '<red>The architecture for installing the application on the emulator is not suitable.</red>'

    @staticmethod
    @localization
    def repo_search_error():
        return '<red>Could not find a version to install in the repository.</red>'

    @staticmethod
    @localization
    def get_data_error():
        return '<red>Failed to retrieve data.</red>'