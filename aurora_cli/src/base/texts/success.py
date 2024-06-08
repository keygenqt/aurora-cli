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


class TextSuccess(Enum):
    @staticmethod
    @localization
    def emulator_start_success():
        return '<green>Emulator started successfully.</green>'

    @staticmethod
    @localization
    def emulator_screenshot_success(path: str):
        return '<green>Screenshot taken successfully:</green> {}'.format(path)

    @staticmethod
    @localization
    def emulator_recording_video_start():
        return '<green>Video recording activated.</green>'

    @staticmethod
    @localization
    def emulator_recording_video_stop_with_save(path: str):
        return f'<green>Video recording has stopped. File saved:</green> {path}'

    @staticmethod
    @localization
    def emulator_recording_video_convert(path: str):
        return '<green>Video record convert successfully:</green> {}'.format(path)

    @staticmethod
    @localization
    def ssh_exec_command_success(execute: str, stdout: str = None, stderr: str = None):
        stdout = f'\n{stdout}' if stdout else ''
        stderr = f'\n{stderr}' if stderr else ''
        return f'<green>The command was executed successfully:</green> `{execute}`{stdout}{stderr}'

    @staticmethod
    @localization
    def ssh_uploaded_success(remote_path: str):
        return '<green>The file was successfully uploaded:</green> {}'.format(remote_path)

    @staticmethod
    @localization
    def ssh_install_rpm(file_name: str):
        return f'<green>Package</green> {file_name} <green>was installed successfully.</green>'

    @staticmethod
    @localization
    def ssh_run_package(package: str):
        return f'<green>Package</green> {package} <green>was run successfully.</green>'

    @staticmethod
    @localization
    def ssh_remove_rpm():
        return '<green>Package was successfully removed.</green>'

    @staticmethod
    @localization
    def validate_config_devices():
        return '<green>Section</green> devices <green>was validated successfully.</green>'

    @staticmethod
    @localization
    def validate_config_keys():
        return '<green>Section</green> keys <green>was validated successfully.</green>'

    @staticmethod
    @localization
    def validate_config_workdir():
        return '<green>Value</green> workdir <green>was validated successfully.</green>'

    @staticmethod
    @localization
    def shell_run_app_success(name: str):
        return f'<green>Application launched successfully:</green> {name}'

    @staticmethod
    @localization
    def check_url_download_success():
        return '<green>The file is ready for download.</green>'

    @staticmethod
    @localization
    def download_success():
        return '<green>The files were downloaded successfully.</green>'

    @staticmethod
    @localization
    def git_clone_success():
        return '<green>The project has been successfully cloned.</green>'

    @staticmethod
    @localization
    def flutter_install_success(path: str, version: str):
        return f'''
<green>Install Flutter</green> {version} <green>successfully!</green>

Add alias to ~/.bashrc for convenience:

    <blue>alias flutter-aurora={path}/bin/flutter</blue>

After that run the command:

    <blue>source $HOME/.bashrc</blue>

You can check the installation with the command:

    <blue>flutter-aurora --version</blue>

Good luck 👋'''

    @staticmethod
    @localization
    def flutter_remove_success(version: str):
        return f'<green>Remove Flutter</green> {version} <green>successfully!</green>'

    @staticmethod
    @localization
    def flutter_project_format_success():
        return '<green>The project was successfully formatted.</green>'

    @staticmethod
    @localization
    def flutter_project_build_success():
        return '<green>The project was successfully build.</green>'

    @staticmethod
    @localization
    def flutter_project_report_success():
        return '<green>Report generation was successful.</green>'

    @staticmethod
    @localization
    def psdk_sign_success():
        return '<green>The signature was completed successfully.</green>'
