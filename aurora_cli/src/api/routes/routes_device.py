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
from aurora_cli.src.base.common.groups.device_features import device_command_common, device_upload_common, \
    device_package_run_common, device_package_install_common, device_package_remove_common
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.utils.output import echo_stdout, OutResult
from aurora_cli.src.base.utils.route import get_route_root, get_arg_bool, get_arg_str


def search_route_device(route: str) -> bool:
    match get_route_root(route):
        case '/device/list':
            echo_stdout(OutResult(
                value=[device.to_dict() for device in DeviceModel.get_lists_devices()]
            ), get_arg_bool(route, 'verbose'))
        case '/device/ssh/command':
            device_command_common(
                model=DeviceModel.get_model_by_host(get_arg_str(route, 'host')),
                execute=get_arg_str(route, 'execute'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/device/ssh/upload':
            device_upload_common(
                model=DeviceModel.get_model_by_host(get_arg_str(route, 'host')),
                path=[get_arg_str(route, 'path')],
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/device/ssh/package-run':
            device_package_run_common(
                model=DeviceModel.get_model_by_host(get_arg_str(route, 'host')),
                package=get_arg_str(route, 'package'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/device/ssh/package-install':
            device_package_install_common(
                model=DeviceModel.get_model_by_host(get_arg_str(route, 'host')),
                path=[get_arg_str(route, 'path')],
                apm=get_arg_bool(route, 'apm'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/device/ssh/package-remove':
            device_package_remove_common(
                model=DeviceModel.get_model_by_host(get_arg_str(route, 'host')),
                package=get_arg_str(route, 'package'),
                apm=get_arg_bool(route, 'apm'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case _:
            return False
    return True
