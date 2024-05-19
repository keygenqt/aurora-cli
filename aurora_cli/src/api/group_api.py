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
from urllib.parse import urlparse

from aurora_cli.src.api.emulator.commands import (
    vm_emulator_start_api,
    vm_emulator_screenshot_api,
    vm_emulator_record_start_api,
    vm_emulator_record_stop_api,
    vm_emulator_record_is_on_api,
    ssh_emulator_command_api,
    ssh_emulator_run_api,
    ssh_emulator_upload_api,
    ssh_emulator_install_api,
    ssh_emulator_remove_api,
    ssh_device_command_api,
    ssh_device_run_api,
    ssh_device_upload_api,
    ssh_device_install_api,
    ssh_device_remove_api,
)
from aurora_cli.src.base.common.texts.error import TextError
from aurora_cli.src.base.output import echo_stdout_json, OutResult404, OutResult400


def get_route_root(route: str) -> str:
    return route.split('?')[0]


def get_route_arg(route: str, arg: str, is_required: bool = True) -> str:
    result = urlparse(route).query.replace(f'{arg}=', '')
    if not result and is_required:
        raise Exception(f"Argument `{arg}` is required.")
    return result


def group_api(route: str):
    is_verbose = get_route_arg(route, 'verbose', False).lower() == 'true'
    try:
        match get_route_root(route):
            # Emulator vm
            case '/emulator/vm/start':
                vm_emulator_start_api(is_verbose)
            case '/emulator/vm/screenshot':
                vm_emulator_screenshot_api(is_verbose)
            case '/emulator/vm/recording/start':
                vm_emulator_record_start_api(is_verbose)
            case '/emulator/vm/recording/stop':
                vm_emulator_record_stop_api(is_verbose)
            case '/emulator/vm/recording/is_on':
                vm_emulator_record_is_on_api(is_verbose)
            # Emulator ssh
            case '/emulator/ssh/command':
                execute = get_route_arg(route, 'execute')
                ssh_emulator_command_api(execute, is_verbose)
            case '/emulator/ssh/run':
                package = get_route_arg(route, 'package')
                ssh_emulator_run_api(package, is_verbose)
            case '/emulator/ssh/upload':
                path = get_route_arg(route, 'path')
                ssh_emulator_upload_api([path], is_verbose)
            case '/emulator/ssh/install':
                path = get_route_arg(route, 'path')
                apm = get_route_arg(route, 'apm').lower() == 'true'
                ssh_emulator_install_api([path], apm, is_verbose)
            case '/emulator/ssh/remove':
                package = get_route_arg(route, 'package')
                apm = get_route_arg(route, 'apm').lower() == 'true'
                ssh_emulator_remove_api(package, apm, is_verbose)
            # Device ssh
            case '/device/ssh/command':
                execute = get_route_arg(route, 'execute')
                ssh_device_command_api(execute, is_verbose)
            case '/device/ssh/run':
                package = get_route_arg(route, 'package')
                ssh_device_run_api(package, is_verbose)
            case '/device/ssh/upload':
                path = get_route_arg(route, 'path')
                ssh_device_upload_api([path], is_verbose)
            case '/device/ssh/install':
                path = get_route_arg(route, 'path')
                apm = get_route_arg(route, 'apm').lower() == 'true'
                ssh_device_install_api([path], apm, is_verbose)
            case '/device/ssh/remove':
                package = get_route_arg(route, 'package')
                apm = get_route_arg(route, 'apm').lower() == 'true'
                ssh_device_remove_api(package, apm, is_verbose)
            case _:
                echo_stdout_json(OutResult404(TextError.route_not_found()))
    except Exception as e:
        echo_stdout_json(OutResult400(str(e)))
