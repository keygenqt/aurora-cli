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
    def argument_run_mode():
        return 'Application launch mode.'

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
    def argument_path_phrase():
        return 'PEM password phrase.'

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
    def argument_reinstall():
        return 'Reinstall an already installed package.'

    @staticmethod
    @localization
    def argument_keep_user_data():
        return 'Keep user data.'

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

    @staticmethod
    @localization
    def argument_vnc_password():
        return 'VNC password.'

    @staticmethod
    @localization
    def argument_vnc_port():
        return 'VNC port.'

    @staticmethod
    @localization
    def argument_app_id():
        return 'Select the application ID.'

    @staticmethod
    @localization
    def argument_arch():
        return 'Select the application architecture.'

    @staticmethod
    @localization
    def argument_app_device_index():
        return 'Select the device index.'

    @staticmethod
    @localization
    def argument_app_sign_index():
        return 'Select the sign key index.'

    @staticmethod
    @localization
    def argument_apps_filter():
        return 'Filter projects by group.'

    @staticmethod
    @localization
    def argument_apps_search():
        return 'Search projects.'