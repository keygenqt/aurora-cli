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
    def command_device_command():
        return 'Execute the command on the device.'

    @staticmethod
    @localization
    def command_device_upload():
        return 'Upload file to ~/Download directory device.'

    @staticmethod
    @localization
    def command_device_package_run():
        return 'Run package on device in container.'

    @staticmethod
    @localization
    def command_device_package_install():
        return 'Install RPM package on device.'

    @staticmethod
    @localization
    def command_device_package_remove():
        return 'Remove package from device.'

    @staticmethod
    @localization
    def command_emulator_start():
        return 'Start emulator.'

    @staticmethod
    @localization
    def command_emulator_screenshot():
        return 'Emulator take screenshot.'

    @staticmethod
    @localization
    def command_emulator_recording():
        return 'Recording video from emulator.'

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
        return 'Run package on emulator in container.'

    @staticmethod
    @localization
    def command_emulator_package_install():
        return 'Install RPM package on emulator.'

    @staticmethod
    @localization
    def command_emulator_package_remove():
        return 'Remove package from emulator.'

    @staticmethod
    @localization
    def command_flutter_available():
        return 'Get available version Flutter for Aurora OS.'

    @staticmethod
    @localization
    def command_flutter_installed():
        return 'Get version installed Flutter for Aurora OS.'

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
        return 'Compile a report flutter project.'

    @staticmethod
    @localization
    def command_project_format():
        return 'Formatting a project.'

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
        return 'Download and install Aurora Platform SDK.'

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
        return 'Get version installed Aurora SDK.'

    @staticmethod
    @localization
    def command_sdk_install():
        return 'Download and run install Aurora SDK.'

    @staticmethod
    @localization
    def command_sdk_tool():
        return 'Run maintenance tool (remove, update).'

    @staticmethod
    @localization
    def command_vscode_tuning():
        return 'Tuning Visual Studio Code.'

    @staticmethod
    @localization
    def command_flutter_custom_devices():
        return 'Add devices Aurora OS to Flutter.'
