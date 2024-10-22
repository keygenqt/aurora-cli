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

import fcntl
import json
import shutil
from pathlib import Path

from aurora_cli.src.base.common.features.flutter_features import flutter_enable_custom_device
from aurora_cli.src.base.common.features.request_version import request_versions_flutter
from aurora_cli.src.base.common.features.search_installed import search_installed_flutter
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.models.emulator_model import EmulatorModel
from aurora_cli.src.base.models.flutter_model import FlutterModel
from aurora_cli.src.base.out.flutter_custom_devices import gen_custom_device
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.hint import TextHint
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.cache_func import cache_func_clear
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResult, OutResultInfo
from aurora_cli.src.base.utils.tests import tests_exit
from aurora_cli.src.base.utils.text_file import file_remove_line
from aurora_cli.src.base.utils.url import get_url_git_flutter


def flutter_available_common():
    echo_stdout(request_versions_flutter())


def flutter_installed_common():
    echo_stdout(search_installed_flutter())


def flutter_install_common(
        version: str,
        is_bar: bool = True
):
    tests_exit()
    # url major version
    git_url = get_url_git_flutter()
    # path install
    flutter_path = Path.home() / '.local' / 'opt' / f'flutter-{version}'
    # check path
    if flutter_path.is_dir() or flutter_path.is_file():
        echo_stdout(OutResultError(TextError.flutter_already_installed_error(version)))
        app_exit()

    from aurora_cli.src.base.utils.git import git_clone
    repo = git_clone(git_url, flutter_path, is_bar)
    repo.git.checkout(version)

    # clear cache
    cache_func_clear()
    # end
    echo_stdout(OutResult(TextSuccess.flutter_install_success(str(flutter_path), version)))



def flutter_remove_common(model: FlutterModel):
    tests_exit()
    path: str = model.get_path()
    version: str = model.get_version()
    shutil.rmtree(path)
    file_remove_line(Path.home() / '.bashrc', path)
    cache_func_clear()
    echo_stdout(OutResult(TextSuccess.flutter_remove_success(version)))


def flutter_add_custom_devices_common(model: FlutterModel):
    def out_check_result(out: OutResult):
        echo_stdout(out)
        if out.is_error():
            app_exit()

    out_check_result(flutter_enable_custom_device(model.get_tool_flutter()))

    config_emulators = EmulatorModel.get_models_list()
    config_devices = DeviceModel.get_models_list()

    if not config_emulators and not config_devices:
        echo_stdout(OutResultInfo(TextInfo.devices_not_found()))
        app_exit()

    path_folder = Path.home() / '.config' / 'flutter'
    path_config = path_folder / 'custom_devices.json'

    if not path_folder.is_dir():
        path_folder.mkdir(parents=True)

    if not path_config.is_file():
        path_config.write_text('{}')

    with open(path_config, 'r+') as file:
        fcntl.lockf(file, fcntl.LOCK_EX)
        config = json.loads(file.read())
        devices = []

        if 'custom-devices' in config.keys():
            for device in config['custom-devices']:
                if 'custom-aurora-' not in device['id']:
                    devices.append(device)

        config['custom-devices'] = []

        for emulator in config_emulators:
            platform_name, platform_arch = emulator.get_emulator_info()
            config['custom-devices'].append(gen_custom_device(
                key='Aurora Custom Emulator',
                ip=emulator.get_host(),
                port=emulator.get_port(),
                ssh_key=emulator.get_ssh_key(),
                platform_name=platform_name,
                platform_arch=platform_arch
            ))
            echo_stdout(OutResult(TextSuccess.devices_add_to_config_emulator()))

        not_added = False
        for device in config_devices:
            if device.is_password():
                echo_stdout(OutResultInfo(TextInfo.devices_password_not_connect(device.get_host())))
                not_added = True
            else:
                platform_name, platform_arch = device.get_device_info()
                config['custom-devices'].append(gen_custom_device(
                    key=f'Aurora Custom Device ({device.get_host()})',
                    ip=device.get_host(),
                    port=device.get_port(),
                    ssh_key=device.get_ssh_key(),
                    platform_name=platform_name,
                    platform_arch=platform_arch
                ))
                echo_stdout(OutResult(TextSuccess.devices_add_to_config_devices(device.get_host())))

        if not_added:
            echo_stdout(OutResultInfo(TextHint.ssh_copy_id()))

        for device in devices:
            config['custom-devices'].append(device)

        file.seek(0)
        file.write(json.dumps(config, indent=2, ensure_ascii=False))
        file.truncate()
