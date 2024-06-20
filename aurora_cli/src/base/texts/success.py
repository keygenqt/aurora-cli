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
        return f'<green>Screenshot taken successfully:</green> {path}'

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
        return f'<green>Video record convert successfully:</green> {path}'

    @staticmethod
    @localization
    def ssh_exec_command_success(
            execute: str,
            stdout: str = None,
            stderr: str = None
    ):
        stdout = f'\n{stdout}' if stdout else ''
        stderr = f'\n{stderr}' if stderr else ''
        return f'<green>The command was executed successfully:</green> `{execute}`{stdout}{stderr}'

    @staticmethod
    @localization
    def ssh_uploaded_success(remote_path: str):
        return f'<green>The file was successfully uploaded:</green> {remote_path}'

    @staticmethod
    @localization
    def ssh_download_success(local_path: str):
        return f'<green>The file was successfully download:</green> {local_path}'

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
    def check_url_download_success(url: str):
        return f'<green>File ready download:</green> {url}'

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
    def flutter_install_success(
            path: str,
            version: str
    ):
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
    def project_format_success():
        return '<green>The project was successfully formatted.</green>'

    @staticmethod
    @localization
    def flutter_project_report_success(path: str):
        return f'<green>Report generation was successful:</green> {path}'

    @staticmethod
    @localization
    def psdk_sign_success(file_name: str):
        return f'<green>The signature was completed successfully:</green> {file_name}'

    @staticmethod
    @localization
    def psdk_targets_get_success(
            version: str,
            targets: []
    ):
        return f'<green>List of targets:</green> {version}\n' + '\n'.join(targets)

    @staticmethod
    @localization
    def psdk_package_install_success():
        return '<green>The package installation was successful.</green>'

    @staticmethod
    @localization
    def psdk_package_remove_success():
        return '<green>The package removal was successful.</green>'

    @staticmethod
    @localization
    def psdk_clear_success():
        return '<green>The snapshot removal was successful.</green>'

    @staticmethod
    @localization
    def psdk_validate_success():
        return '<green>The package was validated successfully.</green>'

    @staticmethod
    @localization
    def psdk_sudoers_add_success(
            version: str,
            path: str
    ):
        return f'<green>Version</green> {version} <green>added to file:</green> {path}'

    @staticmethod
    @localization
    def psdk_sudoers_remove_success(
            version: str,
            path: str
    ):
        return f'<green>Version</green> {version} <green>remove from file:</green> {path}'

    @staticmethod
    @localization
    def tar_unpack_success():
        return '<green>Unpacking was successful.</green>'

    @staticmethod
    @localization
    def psdk_tooling_install_success():
        return '<green>The tooling installation was successful.</green>'

    @staticmethod
    @localization
    def psdk_target_install_success():
        return f'<green>The target installation was successful.</green>'

    @staticmethod
    @localization
    def psdk_install_success(
            path: str,
            version: str
    ):
        return f'''
<green>Install Aurora Platform SDK</green> {version} <green>successfully!</green>

You should update your ~/.bashrc to include export:

    <blue>export PSDK_DIR={path}/sdks/aurora_psdk</blue>

Add alias for convenience:

    <blue>alias aurora_psdk={path}/sdks/aurora_psdk/sdk-chroot</blue>

After that run the command:

    <blue>source ~/.bashrc</blue>

You can check the installation with the command:

    <blue>aurora_psdk sdk-assistant list</blue>

The files have been downloaded to the ~/Downloads folder, if you no longer need them, delete them.

Good luck 👋'''

    @staticmethod
    @localization
    def psdk_remove_success(version: str):
        return f'<green>Aurora Platform SDK</green> {version} <green>remove was successful.</green>'

    @staticmethod
    @localization
    def image_resize_success(path: str):
        return f'<green>The images were successfully created:</green> {path}'

    @staticmethod
    @localization
    def flutter_clear_success():
        return '<green>The project cleanup was successful.</green>'

    @staticmethod
    @localization
    def flutter_get_pub_success():
        return '<green>Getting dependencies was successful.</green>'

    @staticmethod
    @localization
    def flutter_run_build_runner_success():
        return '<green>The build_runner completed the job successfully.</green>'

    @staticmethod
    @localization
    def flutter_build_success(paths: []):
        new_line = '\n' if len(paths) > 1 else ''
        return f'<green>The project build was successful:</green> {new_line}' + '\n'.join(paths)

    @staticmethod
    @localization
    def flutter_enable_custom_device_success():
        return '<green>Custom devices have been successfully activated.</green>'

    @staticmethod
    @localization
    def vscode_extension_install_success(version: str | None = None):
        if version:
            return f'<green>Extension</green> {version} <green>was successfully installed.</green>'
        else:
            return f'<green>Extension was successfully installed.</green>'

    @staticmethod
    @localization
    def ssh_copy_id_success():
        return '<green>The key has been successfully registered on the device.</green>'

    @staticmethod
    @localization
    def ssh_forward_port_success():
        return '<green>The port was successfully forwarded.</green>'

    @staticmethod
    @localization
    def ssh_gdb_server_start_success():
        return '<green>The server GDB has started successfully.</green>'

    @staticmethod
    @localization
    def devices_add_to_config_emulator():
        return '<green>Aurora Emulator was successfully added to custom-devices Flutter.</green>'

    @staticmethod
    @localization
    def devices_add_to_config_devices(host: str):
        return (f'<green>Aurora Device</green>'
                f' {host} '
                f'<green>was successfully added to custom-devices Flutter.</green>')
