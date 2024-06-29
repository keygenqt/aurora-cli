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

import functools
from enum import Enum

from aurora_cli.src.base.localization.localization import localization
from aurora_cli.src.base.utils.argv import argv_is_select, argv_is_verbose, argv_is_api, argv_is_apm
from aurora_cli.src.base.utils.cache_settings import CacheSettingsKey, cache_settings_get


class Hint(Enum):
    emulator_run = 'emulator_run'
    install_app = 'install_app'
    not_install_emulator = 'not_install_emulator'
    emulator_recording_on = 'emulator_recording_on'
    route_error_hint = 'route_error_hint'
    documentation_link = 'documentation_link'
    device_config = 'device_config'
    flutter_documentation_link = 'flutter_documentation_link'
    psdk_documentation_link = 'psdk_documentation_link'
    sdk_documentation_link = 'sdk_documentation_link'
    psdk_documentation_keys_link = 'psdk_documentation_keys_link'
    psdk_keys_info = 'psdk_keys_info'
    flutter_install = 'flutter_install'
    psdk_install = 'psdk_install'
    sdk_install = 'sdk_install'
    sdk_reinstall = 'sdk_reinstall'
    hint_download_error = 'hint_download_error'
    hint_check_download_error = 'hint_check_download_error'
    use_select = 'use_select'
    use_verbose = 'use_verbose'
    use_apm = 'use_apm'
    ssh_key = 'ssh_key'
    ssh_copy_id = 'ssh_copy_id'
    ssh_forward_port = 'ssh_forward_port'
    debug_aurora = 'debug_aurora'
    workdir = 'workdir'
    flutter_project_add_target = 'flutter_project_add_target'
    settings_hint = 'settings_hint'


def hint(*hints: Hint):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            value = function(*args, **kwargs)
            settings_val = cache_settings_get(CacheSettingsKey.hint)
            if settings_val is not None and not settings_val:
                return value
            for key in hints:
                for key_fun in TextHint.__dict__:
                    if key.value == key_fun:
                        hint_fun = getattr(TextHint, key_fun)
                        text_hint = hint_fun()
                        if text_hint:
                            value = '{text}\n<hint>{hint}</hint>'.format(
                                text=value,
                                hint=hint_fun()
                            )
            return value

        return wrapper

    return decorator


class TextHint(Enum):
    @staticmethod
    @localization
    def emulator_run():
        return '<i>You can start the emulator with the following command:</i> aurora-cli emulator start'

    @staticmethod
    @localization
    def install_app():
        return f'<i>You need to install application.</i>'

    @staticmethod
    @localization
    def not_install_emulator():
        return '<i>You may not have an emulator installed; it can be installed with the Aurora SDK.</i>'

    @staticmethod
    @localization
    def emulator_recording_on():
        return '<i>You can disable recording in the VirtualBox window; you can see a rotating icon at the bottom.</i>'

    @staticmethod
    @localization
    def route_error_hint():
        return '<i>The application has an API for use in other applications, and the CLI is provided for people.</i>'

    @staticmethod
    @localization
    def documentation_link():
        return ('<i>More details can be found in the application documentation:</i> '
                'https://keygenqt.github.io/aurora-cli')

    @staticmethod
    @localization
    def device_config():
        return '<i>You may have incorrectly configured device parameters in the configuration file.</i>'

    @staticmethod
    @localization
    def flutter_documentation_link():
        return ('<i>More details can be found in the Flutter documentation:</i> '
                'https://omprussia.gitlab.io/flutter/flutter')

    @staticmethod
    @localization
    def psdk_documentation_link():
        return ('<i>More details can be found in the Aurora Platform SDK documentation:</i> '
                'https://developer.auroraos.ru/doc/software_development/psdk')

    @staticmethod
    @localization
    def sdk_documentation_link():
        return ('<i>More details can be found in the Aurora SDK documentation:</i> '
                'https://developer.auroraos.ru/doc/software_development/sdk')

    @staticmethod
    @localization
    def psdk_documentation_keys_link():
        return ('<i>More information can be found in the documentation:</i> '
                'https://developer.auroraos.ru/doc/software_development/guides/package_signing')

    @staticmethod
    @localization
    def flutter_install():
        return '<i>You can install the Flutter with the following command:</i> aurora-cli flutter install'

    @staticmethod
    @localization
    def psdk_install():
        return '<i>You can install the Aurora Platform SDK with the following command:</i> aurora-cli psdk install'

    @staticmethod
    @localization
    def sdk_install():
        return '<i>You can install the Aurora SDK with the following command:</i> aurora-cli sdk install'

    @staticmethod
    @localization
    def sdk_reinstall():
        return '<i>If you want to install a new version, you need to remove the old one:</i> aurora-cli sdk tool'

    @staticmethod
    @localization
    def hint_download_error():
        return '<i>Check your internet connection or try again later.</i>'

    @staticmethod
    @localization
    def hint_check_download_error():
        return '<i>The download will not start until all errors are resolved.</i>'

    @staticmethod
    @localization
    def use_select():
        if argv_is_select() or argv_is_api():
            return ''
        return '<i>To select other versions use flag:</i> --select'

    @staticmethod
    @localization
    def use_verbose():
        if argv_is_verbose() or argv_is_api():
            return ''
        return '<i>For more detailed output, use the flag:</i> --verbose'

    @staticmethod
    @localization
    def use_apm():
        if argv_is_apm() or argv_is_api():
            return ''
        return '<i>You might enable apm mode:</i> --apm'

    @staticmethod
    @localization
    def psdk_keys_info():
        return '<i>You can add your keys, if you have some, to the application configuration file.</i>'

    @staticmethod
    @localization
    def ssh_key():
        return '<i>For example: auth: ~/.ssh/id_rsa. You can create a key using the command: ssh-keygen -t rsa</i>'

    @staticmethod
    @localization
    def ssh_copy_id():
        return '<i>To register the key on the device, use the command:</i> aurora-cli device ssh-copy-id'

    @staticmethod
    @localization
    def ssh_forward_port():
        return '<i>Try deleting the old connection:</i> rm ~/.ssh/known_hosts'

    @staticmethod
    @localization
    def custom_devices():
        return ('<i>To run the debug, you will need to add custom-devices if you have not already done so:</i> '
                'aurora-cli flutter custom-devices')

    @staticmethod
    @localization
    def debug_aurora():
        return ('<i>To debug Aurora applications, use Aurora SDK:</i> '
                'https://developer.auroraos.ru/doc/software_development/sdk')

    @staticmethod
    @localization
    def workdir():
        return '<i>You can specify</i> workdir <i>in the configuration file, this will make the search easier.</i>'

    @staticmethod
    @localization
    def flutter_project_add_target():
        return '<i>Platform support may not have been added:</i> flutter-aurora create --platforms=aurora --org={org} .'

    @staticmethod
    @localization
    def settings_hint():
        return ('<i>You can read more about additional settings on the documentation page:</i> '
                'https://aurora-cli.keygenqt.com')
