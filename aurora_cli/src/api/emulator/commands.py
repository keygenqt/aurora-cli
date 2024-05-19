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
from aurora_cli.src.base.output import echo_stdout_json
from aurora_cli.src.common.emulator.ssh_features import (
    ssh_command,
    get_ssh_client_emulator
)
from aurora_cli.src.common.emulator.vm_features import (
    vm_emulator_start,
    vm_emulator_screenshot,
    vm_emulator_record_start,
    vm_emulator_record_stop,
    vm_emulator_record_is_on
)


def vm_emulator_start_api(verbose: bool):
    """Start emulator."""
    echo_stdout_json(vm_emulator_start(), verbose)


def vm_emulator_screenshot_api(verbose: bool):
    """Emulator take screenshot."""
    echo_stdout_json(vm_emulator_screenshot(), verbose)


def vm_emulator_record_start_api(verbose: bool):
    """Start recording video from emulator."""
    echo_stdout_json(vm_emulator_record_start(), verbose)


def vm_emulator_record_stop_api(verbose: bool):
    """Stop recording video from emulator."""
    echo_stdout_json(vm_emulator_record_stop(), verbose)


def vm_emulator_record_is_on_api(verbose: bool):
    """Check recording video from emulator."""
    echo_stdout_json(vm_emulator_record_is_on(), verbose)


def ssh_emulator_command_api(execute: str, verbose: bool):
    """Execute the command on the emulator."""
    # Get path to key
    result = get_ssh_client_emulator()
    if result.is_error():
        echo_stdout_json(result)
        exit(1)
    # Run base command
    echo_stdout_json(ssh_command(
        client=result.value,
        execute=execute
    ), verbose)


def ssh_emulator_run_api(package: str, verbose: bool):
    """Run package on emulator in container."""
    pass
    # echo_stdout_json(ssh_run(package), verbose)


def ssh_emulator_upload_api(path: [], verbose: bool):
    """Upload file to ~/Download directory emulator."""
    pass
    # echo_stdout_json(ssh_upload(path), verbose)


def ssh_emulator_install_api(path: [], apm: bool, verbose: bool):
    """Install RPM package on emulator."""
    pass
    # echo_stdout_json(ssh_install(path, apm), verbose)


def ssh_emulator_remove_api(package: str, apm: bool, verbose: bool):
    """Remove package from emulator."""
    pass
    # echo_stdout_json(ssh_remove(package, apm), verbose)


def ssh_device_command_api(execute: str, verbose: bool):
    """Execute the command on the device."""
    pass
    # echo_stdout_json(ssh_command(execute), verbose)


def ssh_device_run_api(package: str, verbose: bool):
    """Run package on device in container."""
    pass
    # echo_stdout_json(ssh_run(package), verbose)


def ssh_device_upload_api(path: [], verbose: bool):
    """Upload file to ~/Download directory device."""
    pass
    # echo_stdout_json(ssh_upload(path), verbose)


def ssh_device_install_api(path: [], apm: bool, verbose: bool):
    """Install RPM package on device."""
    pass
    # echo_stdout_json(ssh_install(path, apm), verbose)


def ssh_device_remove_api(package: str, apm: bool, verbose: bool):
    """Remove package from device."""
    pass
    # echo_stdout_json(ssh_remove(package, apm), verbose)
