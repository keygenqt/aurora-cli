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
        return 'Remove RPM package from device.'

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
        return 'Remove RPM package from emulator.'
