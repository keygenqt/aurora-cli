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

import shutil
from pathlib import Path

from aurora_cli.src.base.common.features.flutter_features import flutter_enable_custom_device
from aurora_cli.src.base.common.features.request_version import request_versions_flutter
from aurora_cli.src.base.common.features.search_installed import search_installed_flutter
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.models.emulator_model import EmulatorModel
from aurora_cli.src.base.models.flutter_model import FlutterModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.disk_cache import disk_cache_clear
from aurora_cli.src.base.utils.git import git_clone
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResult
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
    # url major version
    git_url = get_url_git_flutter()
    # path install
    flutter_path = Path.home() / '.local' / 'opt' / f'flutter-{version}'
    # check path
    if flutter_path.is_dir() or flutter_path.is_file():
        echo_stdout(OutResultError(TextError.flutter_already_installed_error(version)))
        app_exit()

    repo = git_clone(git_url, flutter_path, is_bar)
    repo.git.checkout(version)

    echo_stdout(OutResult(TextSuccess.flutter_install_success(str(flutter_path), version)))
    # clear cache
    disk_cache_clear()


def flutter_remove_common(model: FlutterModel):
    path: str = model.get_path()
    version: str = model.get_version()
    shutil.rmtree(path)
    file_remove_line(Path.home() / '.bashrc', path)
    echo_stdout(OutResult(TextSuccess.flutter_remove_success(version)))
    disk_cache_clear()


def flutter_add_custom_devices(model: FlutterModel):
    def out_check_result(out: OutResult):
        echo_stdout(out)
        if out.is_error():
            app_exit()

    out_check_result(flutter_enable_custom_device(model.get_tool_flutter()))

    emulators = EmulatorModel.get_models_list()
    devices = DeviceModel.get_models_list()

    print(emulators)
    print(devices)
