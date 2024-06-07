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


class TextArgument(Enum):
    @staticmethod
    @localization
    def argument_config():
        return 'Specify config path.'

    @staticmethod
    @localization
    def argument_verbose():
        return 'Command output.'

    @staticmethod
    @localization
    def argument_execute_device():
        return 'The command to be executed on the device.'

    @staticmethod
    @localization
    def argument_execute_emulator():
        return 'The command to be executed on the emulator.'

    @staticmethod
    @localization
    def argument_select():
        return 'Select from available.'

    @staticmethod
    @localization
    def argument_index():
        return 'Specify index.'

    @staticmethod
    @localization
    def argument_path():
        return 'Path to file.'

    @staticmethod
    @localization
    def argument_path_rpm():
        return 'Path to RPM file.'

    @staticmethod
    @localization
    def argument_package_name():
        return 'Package name.'

    @staticmethod
    @localization
    def argument_apm():
        return 'Use APM.'

    @staticmethod
    @localization
    def argument_exit_after_run():
        return 'Exit after run.'

    @staticmethod
    @localization
    def argument_sdk_installer_type():
        return 'Download offline type installer (online = default).'

    @staticmethod
    @localization
    def argument_validate_profile():
        return 'Select profile.'

    @staticmethod
    @localization
    def argument_path_to_project():
        return 'Path to project. The default is the current directory.'

    @staticmethod
    @localization
    def argument_path_to_image():
        return 'Path to image.'

    @staticmethod
    @localization
    def argument_clear_cache():
        return 'Clear cached data.'
