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
    def group_device():
        return 'Working with the device.'

    @staticmethod
    @localization
    def group_emulator():
        return 'Working with the emulator virtualbox.'

    @staticmethod
    @localization
    def group_api():
        return 'Application Programming Interface.'
