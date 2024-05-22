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
from aurora_cli.src.base.models.emulator_model import EmulatorModel
from aurora_cli.src.base.output import echo_stdout_json
from aurora_cli.src.common.ssh_features import (
    ssh_command,
    ssh_run,
    ssh_upload,
    ssh_rpm_install,
    ssh_package_remove
)
from aurora_cli.src.common.vm_features import (
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
    result = EmulatorModel.get_model_user().get_ssh_client()
    if result.is_error():
        echo_stdout_json(result, verbose)
        exit(1)
    echo_stdout_json(ssh_command(
        client=result.value,
        execute=execute
    ), verbose)


def ssh_emulator_run_api(package: str, verbose: bool):
    """Run package on emulator in container."""
    result = EmulatorModel.get_model_user().get_ssh_client()
    if result.is_error():
        echo_stdout_json(result, verbose)
        exit(1)
    echo_stdout_json(ssh_run(
        client=result.value,
        package=package,
        listen_stdout=lambda stdout: echo_stdout_json(stdout),
        listen_stderr=lambda stderr: echo_stdout_json(stderr),
    ), verbose)


def ssh_emulator_upload_api(path: str, verbose: bool):
    """Upload file to ~/Download directory emulator."""
    result = EmulatorModel.get_model_user().get_ssh_client()
    if result.is_error():
        echo_stdout_json(result, verbose)
        exit(1)
    echo_stdout_json(ssh_upload(
        client=result.value,
        path=path,
        listen_progress=lambda stdout: echo_stdout_json(stdout)
    ), verbose)


def ssh_emulator_rpm_install_api(path: str, apm: bool, verbose: bool):
    """Install RPM package on emulator."""
    result = EmulatorModel.get_model_root().get_ssh_client()
    if result.is_error():
        echo_stdout_json(result, verbose)
        exit(1)
    echo_stdout_json(ssh_rpm_install(
        client=result.value,
        path=path,
        apm=apm,
        listen_progress=lambda stdout: echo_stdout_json(stdout)
    ), verbose)


def ssh_emulator_package_remove_api(package: str, apm: bool, verbose: bool):
    """Remove package from emulator."""
    result = EmulatorModel.get_model_root().get_ssh_client()
    if result.is_error():
        echo_stdout_json(result, verbose)
        exit(1)
    echo_stdout_json(ssh_package_remove(
        client=result.value,
        package=package,
        apm=apm,
    ), verbose)
