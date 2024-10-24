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


class TextCommand(Enum):
    @staticmethod
    @localization
    def command_device_list():
        return 'Get list devices.'

    @staticmethod
    @localization
    def command_device_info():
        return 'Get info device.'

    @staticmethod
    @localization
    def command_device_command():
        return 'Execute the command on the device.'

    @staticmethod
    @localization
    def command_device_upload():
        return 'Upload file to ~/Download directory device.'

    @staticmethod
    @localization
    def command_device_ssh_copy_id():
        return 'Скопируйте ключи SSH на устройство.'

    @staticmethod
    @localization
    def command_device_package_run():
        return 'Run package on the device.'

    @staticmethod
    @localization
    def command_device_package_install():
        return 'Install RPM package on the device.'

    @staticmethod
    @localization
    def command_device_package_remove():
        return 'Remove package from the device.'

    @staticmethod
    @localization
    def command_emulator_start():
        return 'Start the emulator.'

    @staticmethod
    @localization
    def command_emulator_screenshot():
        return 'Take a screenshot of the emulator.'

    @staticmethod
    @localization
    def command_emulator_recording():
        return 'Recording video from the emulator.'

    @staticmethod
    @localization
    def command_emulator_recording_start():
        return 'Start recording video from the the emulator.'

    @staticmethod
    @localization
    def command_emulator_recording_stop():
        return 'Stop video recording from the the emulator.'

    @staticmethod
    @localization
    def command_emulator_info():
        return 'Get info emulator.'

    @staticmethod
    @localization
    def command_emulator_command():
        return 'Execute the command on the emulator.'

    @staticmethod
    @localization
    def command_emulator_upload():
        return 'Upload file to ~/Download directory emulator.'

    @staticmethod
    @localization
    def command_emulator_package_run():
        return 'Run package on the emulator.'

    @staticmethod
    @localization
    def command_emulator_package_install():
        return 'Install RPM package on the emulator.'

    @staticmethod
    @localization
    def command_emulator_package_remove():
        return 'Remove package from the emulator.'

    @staticmethod
    @localization
    def command_flutter_available():
        return 'Get available version Flutter for Aurora OS.'

    @staticmethod
    @localization
    def command_flutter_installed():
        return 'Get versions of installed Flutter for Aurora OS.'

    @staticmethod
    @localization
    def command_flutter_install():
        return 'Download and install Flutter for Aurora OS.'

    @staticmethod
    @localization
    def command_flutter_remove():
        return 'Remove Flutter for Aurora OS.'

    @staticmethod
    @localization
    def command_flutter_project_report():
        return 'Compile a report of flutter project.'

    @staticmethod
    @localization
    def command_project_format():
        return 'Project formatting.'

    @staticmethod
    @localization
    def command_project_build():
        return 'Build a project.'

    @staticmethod
    @localization
    def command_project_debug():
        return 'Build debug and run a project.'

    @staticmethod
    @localization
    def command_project_icon():
        return 'Gen multiple size icons for application.'

    @staticmethod
    @localization
    def command_psdk_available():
        return 'Get available version Aurora Platform SDK.'

    @staticmethod
    @localization
    def command_psdk_installed():
        return 'Get installed list Aurora Platform SDK.'

    @staticmethod
    @localization
    def command_psdk_install():
        return 'Install Aurora Platform SDK.'

    @staticmethod
    @localization
    def command_psdk_download():
        return 'Download Aurora Platform SDK.'

    @staticmethod
    @localization
    def command_psdk_remove():
        return 'Remove Aurora Platform SDK.'

    @staticmethod
    @localization
    def command_psdk_clear():
        return 'Remove snapshot target.'

    @staticmethod
    @localization
    def command_psdk_package_search():
        return 'Search installed package in target.'

    @staticmethod
    @localization
    def command_psdk_package_install():
        return 'Install RPM packages to target.'

    @staticmethod
    @localization
    def command_psdk_package_remove():
        return 'Remove package from target.'

    @staticmethod
    @localization
    def command_psdk_sign():
        return 'Sign (with re-sign) RPM package.'

    @staticmethod
    @localization
    def command_psdk_sudoers_add():
        return 'Add sudoers permissions Aurora Platform SDK.'

    @staticmethod
    @localization
    def command_psdk_sudoers_remove():
        return 'Remove sudoers permissions Aurora Platform SDK.'

    @staticmethod
    @localization
    def command_psdk_info():
        return 'Get info about Aurora Platform SDK.'

    @staticmethod
    @localization
    def command_psdk_targets():
        return 'Get list targets Aurora Platform SDK.'

    @staticmethod
    @localization
    def command_psdk_validate():
        return 'Validate RPM packages.'

    @staticmethod
    @localization
    def command_sdk_available():
        return 'Get available version Aurora SDK.'

    @staticmethod
    @localization
    def command_sdk_installed():
        return 'Get version of the installed Aurora SDK.'

    @staticmethod
    @localization
    def command_sdk_install():
        return 'Download and run Aurora SDK installation.'

    @staticmethod
    @localization
    def command_sdk_tool():
        return 'Run maintenance tool (remove, update).'

    @staticmethod
    @localization
    def command_vscode_tuning():
        return 'Installing VS Code extensions that are necessary for work.'

    @staticmethod
    @localization
    def command_flutter_custom_devices():
        return 'Add devices with Aurora OS to Flutter.'

    @staticmethod
    @localization
    def command_vscode_info():
        return 'Information about VS Code.'

    @staticmethod
    @localization
    def command_vscode_extensions_list():
        return 'Get a list of VS Code extensions.'

    @staticmethod
    @localization
    def command_vscode_extension_install():
        return 'Install VS Code extension.'

    @staticmethod
    @localization
    def command_vscode_settings_update():
        return 'Update VS Code settings.'

    @staticmethod
    @localization
    def command_settings_list():
        return 'Display additional application settings.'

    @staticmethod
    @localization
    def command_settings_clear():
        return 'Clear advanced application settings.'

    @staticmethod
    @localization
    def command_settings_localization():
        return 'Set the application language.'

    @staticmethod
    @localization
    def command_settings_verbose():
        return 'Controlling the --verbose parameter.'

    @staticmethod
    @localization
    def command_settings_select():
        return 'Controlling the --select parameter.'

    @staticmethod
    @localization
    def command_settings_hint():
        return 'Manage application hints.'

    @staticmethod
    @localization
    def command_test_answer():
        return 'Test answers API.'

    @staticmethod
    @localization
    def command_app_info():
        return 'Get information about the application.'

    @staticmethod
    @localization
    def command_app_versions():
        return 'Get information about versions the application.'

    @staticmethod
    @localization
    def command_app_auth_check():
        return 'Check access to root user.'

    @staticmethod
    @localization
    def command_app_auth_root():
        return 'Authorization in sudo.'
