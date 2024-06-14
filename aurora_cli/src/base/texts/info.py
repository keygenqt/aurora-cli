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
        return '<blue>The emulator is already running.</blue>'

    @staticmethod
    @localization
    def emulator_recording_video_stop_already():
        return '<blue>The emulator recording video is already off.</blue>'

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
    def ssh_install_rpm():
        return '<blue>Starting install RPM package...</blue>'

    @staticmethod
    @localization
    def select_array_out(key: str, names: []):
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
        return f'<blue>File already exists:</blue> {path}'

    @staticmethod
    @localization
    def flutter_project_format_cpp_done():
        return '<blue>Aurora formatting is complete.</blue>'

    @staticmethod
    @localization
    def flutter_project_format_dart_done():
        return '<blue>Dart formatting is complete.</blue>'

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
        return '<blue>Packages not found.</blue>'

    @staticmethod
    @localization
    def psdk_package_search(values: []):
        return (f'<blue>Packages found:</blue>\n'
                + '\n'.join([f'{value["Name"]} ({value["Version"]})' for value in values]))

    @staticmethod
    @localization
    def psdk_package_already_installed():
        return '<blue>The package is already installed.</blue>'

    @staticmethod
    @localization
    def psdk_sudoers_exist(version: str, path: str):
        return f'<blue>Version</blue> {version} <blue>is already specified in the file:</blue> {path}'

    @staticmethod
    @localization
    def psdk_sudoers_not_found(version: str, path: str):
        return f'<blue>Version</blue> {version} <blue>not found in file:</blue> {path}'

    @staticmethod
    @localization
    def psdk_install_start():
        return f'<blue>Installation Aurora Platform SDK started.</blue>'

    @staticmethod
    @localization
    def psdk_remove_start():
        return f'<blue>Remove Aurora Platform SDK started.</blue>'

    @staticmethod
    @localization
    def psdk_download_start():
        return f'<blue>The download of Aurora Platform SDK files has begun.</blue>'
