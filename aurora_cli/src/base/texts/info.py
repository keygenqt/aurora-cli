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


class TextInfo(Enum):
    @staticmethod
    @localization
    def command_execute(command: str):
        return f'<blue>Command execute:</blue> `{command}`'

    @staticmethod
    @localization
    def command_execute_time(seconds: float):
        return f'<blue>Run time seconds:</blue> {seconds:.2f}'

    @staticmethod
    @localization
    def emulator_start_locked():
        return '<blue>The emulator has already run.</blue>'

    @staticmethod
    @localization
    def emulator_recording_video_stop_already():
        return '<blue>The emulator recording video has already turned off.</blue>'

    @staticmethod
    @localization
    def shh_upload_start():
        return f'<blue>Starting file upload.</blue>'

    @staticmethod
    @localization
    def shh_upload_progress():
        return '<blue>File upload progress in percentage.</blue>'

    @staticmethod
    @localization
    def download_progress():
        return '<blue>File download progress in percentage.</blue>'

    @staticmethod
    @localization
    def install_progress():
        return '<blue>Install progress in percentage.</blue>'

    @staticmethod
    @localization
    def git_clone_progress(title: str):
        return f'<blue>Repository cloning progress:</blue> {title}'

    @staticmethod
    @localization
    def git_clone_start(url: str):
        return f'<blue>Cloning of the repository has begun:</blue> {url}'

    @staticmethod
    @localization
    def ssh_start_install_rpm():
        return '<blue>Starting install RPM package...</blue>'

    @staticmethod
    @localization
    def select_array_out(
            key: str,
            names: []
    ):
        if names:
            return (f'<blue>Select</blue> {key} <blue>index:</blue>\n'
                    + '\n'.join([f'{i + 1}: {n}' for i, n in enumerate(names)]))

    @staticmethod
    @localization
    def create_default_config_file(path: str):
        return f'<blue>A default configuration file has been created:</blue> {path}'

    @staticmethod
    @localization
    def available_versions_sdk(versions: []):
        return '<blue>Available versions Aurora SDK:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    @localization
    def available_versions_psdk(versions: []):
        return '<blue>Available versions Aurora Platform SDK:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    @localization
    def available_versions_flutter(versions: []):
        return '<blue>Available versions Flutter for Aurora OS:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    @localization
    def available_versions_plugins(versions: []):
        return '<blue>Available versions Flutter Plugins for Aurora OS:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    @localization
    def installed_versions_sdk(versions: []):
        return '<blue>Installed version Aurora SDK:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    @localization
    def installed_versions_psdk(versions: []):
        return '<blue>Installed versions Aurora Platform SDK:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    @localization
    def installed_versions_flutter(versions: []):
        return '<blue>Installed versions Flutter for Aurora OS:</blue>\n{}'.format('\n'.join(versions))

    @staticmethod
    @localization
    def cache_clear():
        return '<blue>The application cache has been cleared.</blue>'

    @staticmethod
    @localization
    def check_url_download_exist(path: str):
        return f'<blue>File has already existed:</blue> {path}'

    @staticmethod
    @localization
    def flutter_project_format_cpp_done():
        return '<blue>Aurora formatting is completed.</blue>'

    @staticmethod
    @localization
    def flutter_project_format_dart_done():
        return '<blue>Dart formatting is completed.</blue>'

    @staticmethod
    @localization
    def flutter_project_pub_get():
        return '<blue>Retrieving project dependencies...</blue>'

    @staticmethod
    @localization
    def flutter_gen_plugins_report():
        return '<blue>Generating a report on project plugins...</blue>'

    @staticmethod
    @localization
    def file_check_and_download():
        return '<blue>Download the necessary files...</blue>'

    @staticmethod
    @localization
    @hint(Hint.psdk_keys_info, Hint.psdk_documentation_keys_link)
    def psdk_sign_use_public_keys():
        return '<blue>Public keys will be used for signing.</blue>'

    @staticmethod
    @localization
    def psdk_targets_empty(version: str):
        return f'<yellow>Target list is empty:</yellow> {version}'

    @staticmethod
    @localization
    def psdk_package_not_found():
        return '<blue>Packages are not found.</blue>'

    @staticmethod
    @localization
    def psdk_package_search(values: []):
        return (f'<blue>Packages are found:</blue>\n'
                + '\n'.join([f'{value["Name"]} ({value["Version"]})' for value in values]))

    @staticmethod
    @localization
    def psdk_package_already_installed():
        return '<blue>The package has already installed.</blue>'

    @staticmethod
    @localization
    def psdk_sudoers_exist(
            version: str,
            path: str
    ):
        return f'<blue>Version</blue> {version} <blue>has already specified in the file:</blue> {path}'

    @staticmethod
    @localization
    def psdk_sudoers_not_found(version: str, path: str):
        return f'<blue>Version</blue> {version} <blue>is not found in file:</blue> {path}'

    @staticmethod
    @localization
    def psdk_install_start():
        return f'<blue>Installation Aurora Platform SDK is started.</blue>'

    @staticmethod
    @localization
    def psdk_remove_start():
        return f'<blue>Removing Aurora Platform SDK is started.</blue>'

    @staticmethod
    @localization
    def psdk_download_start():
        return f'<blue>The download of Aurora Platform SDK files has begun.</blue>'

    @staticmethod
    @localization
    def vscode_extensions_flutter(extensions: []):
        return '<blue>Extensions for work with Flutter will be installed:</blue>\n' + '\n'.join(extensions)

    @staticmethod
    @localization
    def vscode_extensions_cpp(extensions: []):
        return '<blue>Extensions for work with C++ will be installed:</blue>\n' + '\n'.join(extensions)

    @staticmethod
    @localization
    def vscode_extensions_other(extensions: []):
        return '<blue>Extensions for work with VS Code will be installed:</blue>\n' + '\n'.join(extensions)

    @staticmethod
    @localization
    def vscode_extensions_installing(extension: str):
        return f'<blue>Installing extension:</blue> {extension}'

    @staticmethod
    @localization
    def vscode_settings_update(path: str):
        return f'<blue>The configuration file has been updated:</blue> {path}'

    @staticmethod
    @localization
    def vscode_settings_not_update():
        return '<blue>The configuration file does not updates.</blue>'

    @staticmethod
    @localization
    def vscode_extensions_flutter_installed():
        return '<blue>Extensions for work with Flutter has already installed.</blue>'

    @staticmethod
    @localization
    def vscode_extensions_cpp_installed():
        return '<blue>Extensions for work with C++ has already installed.</blue>'

    @staticmethod
    @localization
    def vscode_extensions_other_installed():
        return '<blue>Extensions for work with VS Code has already installed.</blue>'

    @staticmethod
    @localization
    def devices_not_found():
        return '<blue>Any devices are not found.</blue>'

    @staticmethod
    @localization
    def ssh_copy_id_password():
        return '<blue>Enter the ssh connection password, it can be found in the device settings.</blue>'

    @staticmethod
    @localization
    def ssh_debug_without_project_gdb(binary: str, host: str, package: str):
        return ('<blue>To connect to the GDB debug via vscode, add</blue>'
                ' launch.json '
                '<blue>with the following content:</blue>'
                '\n{'
                '\n   "configurations": ['
                '\n       {'
                '\n           "name": "Flutter Aurora OS GDB Debug",'
                '\n           "type": "cppdbg",'
                '\n           "request": "launch",'
                f'\n           "program": "{binary}",'
                '\n           "MIMode": "gdb",'
                '\n           "miDebuggerPath": "/usr/bin/gdb-multiarch",'
                f'\n           "miDebuggerServerAddress": "{host}:2345",'
                '\n           "useExtendedRemote": true,'
                '\n           "cwd": "${workspaceRoot}",'
                '\n       }'
                '\n   ]'
                '\n}'
                '\n<blue>and for GDB debug add init file</blue>'
                ' .gdbinit '
                '<blue>to root project:</blue>'
                '\nhandle SIGILL pass nostop noprint'
                f'\nset remote exec-file /usr/bin/{package}\n'
                '\n<blue>Or just run the application from the root of the project, '
                'everything will be added automatically.</blue>')

    @staticmethod
    @localization
    def ssh_debug_without_project_dart(dart_vm_url: str):
        return ('<blue>To connect to the Dart debug via vscode, add</blue>'
                ' launch.json '
                '<blue>with the following content:</blue>'
                '\n{'
                '\n   "configurations": ['
                '\n       {'
                '\n           "name": "Flutter Aurora OS Dart Debug",'
                '\n           "type": "dart",'
                '\n           "request": "attach",'
                f'\n           "vmServiceUri": "{dart_vm_url}",'
                '\n           "program": "lib/main.dart"'
                '\n       }'
                '\n   ]'
                '\n}'
                '\n<blue>Or just run the application from the root of the project, '
                'everything will be added automatically.</blue>')

    @staticmethod
    @localization
    def devices_password_not_connect(host: str):
        return (f'<blue>The device</blue>'
                f' {host} '
                f'<blue>connected using a password will not be added, use ssh key in auth.</blue>')

    @staticmethod
    @localization
    def devices_turn_on():
        return '<blue>To obtain the necessary information about the devices, they must be connected...</blue>'

    @staticmethod
    @localization
    def update_launch_json_gdb():
        return '<blue>File</blue> launch.json <blue>has been updated, you can run the GDB debug in VS Code.</blue>'

    @staticmethod
    @localization
    def update_launch_json_dart():
        return '<blue>File</blue> launch.json <blue>has been updated, you can run the Dart debug in VS Code.</blue>'

    @staticmethod
    @localization
    @hint(Hint.debug_aurora)
    def ssh_run_debug_aurora():
        return '<yellow>There is no debugging for the Aurora application, only for Flutter.</yellow>'

    @staticmethod
    @localization
    def run_debug_application():
        return '<blue>The application will run outside the sandbox.</blue>'

    @staticmethod
    @localization
    def run_mode_debug_info():
        return '<blue>The Flutter application had to be built in debug mode.</blue>'

    @staticmethod
    @localization
    def search_installed_flutter_sdk(path: str):
        return f'<blue>Directory search</blue> {path} <blue>Flutter SDK...</blue>'

    @staticmethod
    @localization
    @hint(Hint.workdir)
    def search_installed_aurora_psdk_hint(path: str):
        return f'<blue>Directory search</blue> {path} <blue>Aurora Platform SDK...</blue>'

    @staticmethod
    @localization
    @hint(Hint.workdir)
    def search_installed_aurora_sdk_hint(path: str):
        return f'<blue>Directory search</blue> {path} <blue>Aurora SDK...</blue>'

    @staticmethod
    @localization
    def search_installed_aurora_psdk(path: str):
        return f'<blue>Directory search</blue> {path} <blue>Aurora Platform SDK...</blue>'

    @staticmethod
    @localization
    def search_installed_aurora_sdk(path: str):
        return f'<blue>Directory search</blue> {path} <blue>Aurora SDK...</blue>'

    @staticmethod
    @localization
    def install_debug_apm_dart_debug():
        return '<yellow>Only the main package will be installed via apm; this is enough for Dart debug.</yellow>'

    @staticmethod
    @localization
    @hint(Hint.settings_hint)
    def settings_list(values: dict):
        return ('<blue>List of current settings:</blue>\n{}'
                .format('\n'.join([f'{key}: {value}' for key, value in values.items()])))

    @staticmethod
    @localization
    def settings_item_empty():
        return 'Value not set.'
