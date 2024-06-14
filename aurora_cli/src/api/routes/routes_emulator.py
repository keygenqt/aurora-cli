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

from aurora_cli.src.base.common.groups.emulator.emulator_features import (
    emulator_command_common,
    emulator_upload_common,
    emulator_start_common,
    emulator_screenshot_common,
    emulator_recording_start_common,
    emulator_recording_stop_common,
)
from aurora_cli.src.base.common.groups.emulator.emulator_package_features import (
    emulator_package_run_common,
    emulator_package_install_common,
    emulator_package_remove_common
)
from aurora_cli.src.base.models.emulator_model import EmulatorModel
from aurora_cli.src.base.utils.route import get_route_root, get_arg_bool, get_arg_str


def search_route_emulator(route: str) -> bool:
    match get_route_root(route):
        case '/emulator/command':
            emulator_command_common(
                model=EmulatorModel.get_model_user(),
                execute=get_arg_str(route, 'execute'),
            )
        case '/emulator/upload':
            emulator_upload_common(
                model=EmulatorModel.get_model_user(),
                path=get_arg_str(route, 'path'),
            )
        case '/emulator/package/run':
            emulator_package_run_common(
                model=EmulatorModel.get_model_user(),
                package=get_arg_str(route, 'package'),
            )
        case '/emulator/package/install':
            emulator_package_install_common(
                model=EmulatorModel.get_model_root(),
                path=get_arg_str(route, 'path'),
                apm=get_arg_bool(route, 'apm'),
            )
        case '/emulator/package/remove':
            emulator_package_remove_common(
                model=EmulatorModel.get_model_root(),
                package=get_arg_str(route, 'package'),
                apm=get_arg_bool(route, 'apm'),
            )
        case '/emulator/start':
            emulator_start_common(
                model=EmulatorModel.get_model_user(),
            )
        case '/emulator/screenshot':
            emulator_screenshot_common(
                model=EmulatorModel.get_model_user(),
            )
        case '/emulator/recording/start':
            emulator_recording_start_common(
                model=EmulatorModel.get_model_user(),
            )
        case '/emulator/recording/stop':
            emulator_recording_stop_common(
                model=EmulatorModel.get_model_user(),
            )
        case _:
            return False
    return True
