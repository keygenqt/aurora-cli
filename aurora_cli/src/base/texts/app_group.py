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


class TextGroup(Enum):
    @staticmethod
    @localization
    def group_main():
        return '''The application allows you to install tools for working with the Aurora OS and simplifies working with them.
More details about the tools can be found on the documentation page:

Flutter SDK  https://omprussia.gitlab.io/flutter/flutter
Aurora SDK   https://developer.auroraos.ru/doc/software_development/sdk
Platform SDK https://developer.auroraos.ru/doc/software_development/psdk

This is a third party tool written by enthusiasts!'''

    @staticmethod
    @localization
    def group_api():
        return 'Application Programming Interface.'

    @staticmethod
    @localization
    def group_build():
        return 'Building Qt & Flutter applications.'

    @staticmethod
    @localization
    def group_debug():
        return 'Debugging Qt & Flutter applications.'

    @staticmethod
    @localization
    def group_device():
        return 'Work with the device.'

    @staticmethod
    @localization
    def group_vscode():
        return 'Work with the Visual Studio Code.'

    @staticmethod
    @localization
    def subgroup_device_package():
        return 'Work with packages.'

    @staticmethod
    @localization
    def group_emulator():
        return 'Work with the emulator virtualbox.'

    @staticmethod
    @localization
    def subgroup_emulator_package():
        return 'Work with packages.'

    @staticmethod
    @localization
    def group_flutter():
        return 'Work with Flutter for Aurora OS.'

    @staticmethod
    @localization
    def subgroup_flutter_project():
        return 'Work with Flutter projects.'

    @staticmethod
    @localization
    def group_psdk():
        return 'Work with Platform Aurora SDK.'

    @staticmethod
    @localization
    def subgroup_psdk_package():
        return 'Work with packages.'

    @staticmethod
    @localization
    def subgroup_psdk_project():
        return 'Work with Aurora projects.'

    @staticmethod
    @localization
    def subgroup_psdk_sudoers():
        return 'Work with sudoers.'

    @staticmethod
    @localization
    def group_sdk():
        return 'Work with Aurora SDK.'

    @staticmethod
    @localization
    def group_sundry():
        return 'Additional functionality.'

    @staticmethod
    @localization
    def group_settings():
        return 'Additional application settings.'
