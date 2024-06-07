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
from aurora_cli.src.base.utils.path import path_convert_relative


class TextInfo(Enum):
    @staticmethod
    @localization
    def command_execute(command: str):
        return f'<blue>Command execute:</blue> `{command}`'

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
    def shh_download_start(path: str):
        path = path_convert_relative(path)
        if path and path.is_file():
            return f'<blue>Starting file download:</blue> {path}'

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
    def git_clone_progress(title: str):
        return f'<blue>Repository cloning progress:</blue> {title}'

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
        return f'<blue>The file will not be downloaded, it already exists:</blue> {path}'
