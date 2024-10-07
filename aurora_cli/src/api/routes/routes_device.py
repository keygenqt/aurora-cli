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
from pathlib import Path

from aurora_cli.src.base.common.groups.device.device_features import (
    device_command_common,
    device_upload_common, device_info_common,
)
from aurora_cli.src.base.common.groups.device.device_package_features import (
    device_package_run_common,
    device_package_install_common,
    device_package_remove_common
)
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.utils.output import echo_stdout, OutResult
from aurora_cli.src.base.utils.route import get_route_root, get_arg_bool, get_arg_str, get_arg_str_optional


def search_route_device(route: str) -> bool:
    root = get_route_root(route)
    if root == '/device/list':
        echo_stdout(OutResult(
            value=[device.to_dict() for device in DeviceModel.get_models_list()]
        ))
    elif root == '/device/info':
        device_info_common(
            model=DeviceModel.get_model_by_host(get_arg_str(route, 'host')),
        )
    elif root == '/device/command':
        device_command_common(
            execute=get_arg_str(route, 'execute'),
            model=DeviceModel.get_model_by_host(get_arg_str(route, 'host')),
        )
    elif root == '/device/upload':
        device_upload_common(
            path=get_arg_str(route, 'path'),
            model=DeviceModel.get_model_by_host(get_arg_str(route, 'host')),
        )
    elif root == '/device/package/run':
        path_project = get_arg_str_optional(route, 'project')
        run_mode = get_arg_str_optional(route, 'mode')
        device_package_run_common(
            package=get_arg_str(route, 'package'),
            run_mode=run_mode if run_mode else 'sandbox',
            path_project=path_project if path_project else str(Path.cwd()),
            model=DeviceModel.get_model_by_host(get_arg_str(route, 'host')),
        )
    elif root == '/device/package/install':
        device_package_install_common(
            path=get_arg_str(route, 'path'),
            apm=get_arg_bool(route, 'apm'),
            model=DeviceModel.get_model_by_host(get_arg_str(route, 'host')),
        )
    elif root == '/device/package/remove':
        device_package_remove_common(
            package=get_arg_str(route, 'package'),
            apm=get_arg_bool(route, 'apm'),
            model=DeviceModel.get_model_by_host(get_arg_str(route, 'host')),
        )
    else:
        return False

    return True
