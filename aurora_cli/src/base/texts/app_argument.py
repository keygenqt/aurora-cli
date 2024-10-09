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
    def argument_optional():
        return 'optional'

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
        return 'The command will be executed on the device.'

    @staticmethod
    @localization
    def argument_execute_emulator():
        return 'The command will be executed on the emulator.'

    @staticmethod
    @localization
    def argument_select():
        return 'Select from available.'

    @staticmethod
    @localization
    def argument_install():
        return 'Install on the device or the emulator.'

    @staticmethod
    @localization
    def argument_debug():
        return 'Build debug.'

    @staticmethod
    @localization
    def argument_run_mode():
        return 'Application launch mode.'

    @staticmethod
    @localization
    def argument_clean():
        return 'Build clean.'

    @staticmethod
    @localization
    def argument_pub_get():
        return 'Run pub get.'

    @staticmethod
    @localization
    def argument_build_runner():
        return 'Run build runner.'

    @staticmethod
    @localization
    def argument_run():
        return 'Run application on the device or the emulator.'

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
        return 'Download offline type installer.'

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

    @staticmethod
    @localization
    def argument_mode_build():
        return 'Mode build project.'

    @staticmethod
    @localization
    def argument_run_mode():
        return 'Application launch mode.'

    @staticmethod
    @localization
    def argument_host_device():
        return 'IP address device.'

    @staticmethod
    @localization
    def argument_flutter_version():
        return 'Installed version of Flutter.'

    @staticmethod
    @localization
    def argument_psdk_version():
        return 'Installed version of Aurora Platform SDK.'

    @staticmethod
    @localization
    def argument_target_name():
        return 'Target name installed version of Aurora Platform SDK.'

    @staticmethod
    @localization
    def argument_key_sign_name():
        return 'The name of key for sign package from config application.'

    @staticmethod
    @localization
    def argument_vscode_extension():
        return 'Name of the VS Code extension.'

    @staticmethod
    @localization
    def argument_language():
        return 'Application language.'

    @staticmethod
    @localization
    def argument_enable_verbose():
        return 'Enable/Disable --verbose by default.'

    @staticmethod
    @localization
    def argument_enable_save_select():
        return 'Enable/Disable saving --select.'

    @staticmethod
    @localization
    def argument_enable_hint():
        return 'Enable/Disable application hints.'

    @staticmethod
    @localization
    def argument_test_answer_time():
        return 'Response delay time.'

    @staticmethod
    @localization
    def argument_test_answer_code():
        return 'Response code (100, 200, 500).'

    @staticmethod
    @localization
    def argument_test_answer_iterate():
        return 'Number of response iterations.'

    @staticmethod
    @localization
    def argument_password():
        return 'Root password.'
