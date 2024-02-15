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
from paramiko.client import SSHClient

from aurora_cli.src.support.helper import check_array_with_exit, prompt_index, get_by_index, check_empty_with_exit
from aurora_cli.src.support.output import echo_stdout
from aurora_cli.src.support.sdk import find_folder_sdk
from aurora_cli.src.support.ssh import get_ssh_client
from aurora_cli.src.support.texts import AppTexts
from aurora_cli.src.support.vbox import vm_search_emulator_aurora, vm_check_is_run


# Get emulator ssh client
def emulator_ssh_select(is_root: bool = False) -> SSHClient:
    # Get name emulator
    emulator_name = vm_search_emulator_aurora(False)

    # Check emulator is running
    if not vm_check_is_run(emulator_name):
        echo_stdout(AppTexts.vm_is_not_running())
        exit(1)

    # Get emulator client
    client = get_ssh_client_emulator(is_root)

    # Check emulator is running
    if not client:
        echo_stdout(AppTexts.vm_error_connect())
        exit(1)

    return client


# Select device and get ssh client
def device_ssh_select(
        ctx: {},
        index: int
) -> [SSHClient | None, {}]:
    # Get devices
    devices = check_array_with_exit(
        ctx.obj.get_devices(),
        AppTexts.devices_not_found()
    )

    # Output indexes array
    echo_stdout(AppTexts.select_device(devices))
    echo_stdout(AppTexts.array_indexes(devices.keys()), 2)

    # Query index
    index = prompt_index(devices, index)

    # Get device data
    ip, data = get_by_index(devices, index)

    # Get ssh client
    return [
        check_empty_with_exit(
            get_ssh_client_device(ip, data['port'], data['pass']),
            AppTexts.device_not_active(ip),
        ),
        data
    ]


# Get ssh client device
def get_ssh_client_device(
        ip: str,
        port: int,
        password: str
) -> SSHClient | None:
    return get_ssh_client(ip, 'defaultuser', port, password)


# Get ssh client emulator
def get_ssh_client_emulator(is_root: bool) -> SSHClient | None:
    path = find_folder_sdk()
    if not path:
        return None
    return get_ssh_client(
        'localhost',
        'root' if is_root else 'defaultuser',
        2223,
        path / 'vmshare' / 'ssh' / 'private_keys' / 'sdk'
    )
