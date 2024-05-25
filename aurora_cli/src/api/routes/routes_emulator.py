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

from aurora_cli.src.api.features.emulator import (
    vm_emulator_start_api,
    vm_emulator_screenshot_api,
    vm_emulator_record_start_api,
    vm_emulator_record_stop_api,
    vm_emulator_record_is_on_api,
    ssh_emulator_command_api,
    ssh_emulator_run_api,
    ssh_emulator_rpm_install_api,
    ssh_emulator_upload_api,
    ssh_emulator_package_remove_api,
)
from aurora_cli.src.api.routes.helper_route import get_route_root, get_arg_bool, get_arg_str


def search_route_emulator(route: str) -> bool:
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
        case '/emulator/vm/recording/is-on':
            vm_emulator_record_is_on_api(
                verbose=get_arg_bool(route, 'verbose')
            )
        # Emulator ssh
        case '/emulator/ssh/command':
            ssh_emulator_command_api(
                execute=get_arg_str(route, 'execute'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/emulator/ssh/upload':
            ssh_emulator_upload_api(
                path=get_arg_str(route, 'path'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/emulator/ssh/package-run':
            ssh_emulator_run_api(
                package=get_arg_str(route, 'package'),
                nohup=get_arg_bool(route, 'nohup'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/emulator/ssh/package-install':
            ssh_emulator_rpm_install_api(
                path=get_arg_str(route, 'path'),
                apm=get_arg_bool(route, 'apm'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/emulator/ssh/package-remove':
            ssh_emulator_package_remove_api(
                package=get_arg_str(route, 'package'),
                apm=get_arg_bool(route, 'apm'),
                verbose=get_arg_bool(route, 'verbose')
            )
        case _:
            return False
    return True
