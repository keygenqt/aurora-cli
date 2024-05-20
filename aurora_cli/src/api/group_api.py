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
    ssh_emulator_rpm_install_api,
    ssh_emulator_upload_api,
    ssh_emulator_rpm_remove_api,
)
from aurora_cli.src.base.common.texts.error import TextError
from aurora_cli.src.base.output import echo_stdout_json, OutResultError


def get_route_root(route: str) -> str:
    return route.split('?')[0]


def get_arg_bool(route: str, arg: str) -> bool:
    try:
        return get_arg_str(route, arg).lower() == 'true'
    except (Exception,):
        return False


def get_arg_str(route: str, arg: str) -> str | None:
    result = None
    for arg_value in urlparse(route).query.split('&'):
        if f'{arg}=' in arg_value:
            result = arg_value.replace(f'{arg}=', '')
    if not result:
        raise Exception(f"Argument `{arg}` is required.")
    return result


def group_api(route: str):
    try:
        match get_route_root(route):
            # Emulator vm
            case '/emulator/vm/start':
                vm_emulator_start_api(
                    verbose=get_arg_bool(route, 'verbose')
                )
            case '/emulator/vm/screenshot':
                vm_emulator_screenshot_api(
                    verbose=get_arg_bool(route, 'verbose')
                )
            case '/emulator/vm/recording/start':
                vm_emulator_record_start_api(
                    verbose=get_arg_bool(route, 'verbose')
                )
            case '/emulator/vm/recording/stop':
                vm_emulator_record_stop_api(
                    verbose=get_arg_bool(route, 'verbose')
                )
            case '/emulator/vm/recording/is_on':
                vm_emulator_record_is_on_api(
                    verbose=get_arg_bool(route, 'verbose')
                )
            # Emulator ssh
            case '/emulator/ssh/command':
                ssh_emulator_command_api(
                    execute=get_arg_str(route, 'execute'),
                    verbose=get_arg_bool(route, 'verbose')
                )
            case '/emulator/ssh/run':
                ssh_emulator_run_api(
                    package=get_arg_str(route, 'package'),
                    verbose=get_arg_bool(route, 'verbose')
                )
            case '/emulator/ssh/upload':
                ssh_emulator_upload_api(
                    path=get_arg_str(route, 'path'),
                    verbose=get_arg_bool(route, 'verbose')
                )
            case '/emulator/ssh/rpm_install':
                ssh_emulator_rpm_install_api(
                    path=get_arg_str(route, 'path'),
                    apm=get_arg_str(route, 'apm').lower() == 'true',
                    verbose=get_arg_bool(route, 'verbose')
                )
            case '/emulator/ssh/rpm_remove':
                ssh_emulator_rpm_remove_api(
                    package=get_arg_str(route, 'package'),
                    apm=get_arg_str(route, 'apm').lower() == 'true',
                    verbose=get_arg_bool(route, 'verbose')
                )
            case _:
                echo_stdout_json(OutResultError(TextError.route_not_found()))
    except Exception as e:
        echo_stdout_json(OutResultError(str(e)))
