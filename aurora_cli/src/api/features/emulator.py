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

from aurora_cli.src.base.common.ssh_features import (
    ssh_command,
    ssh_run,
    ssh_upload,
    ssh_rpm_install,
    ssh_package_remove
)
from aurora_cli.src.base.common.vm_features import (
    vm_emulator_start,
    vm_emulator_screenshot,
    vm_emulator_record_start,
    vm_emulator_record_stop,
    vm_emulator_is_on_record
)
from aurora_cli.src.base.models.emulator_model import EmulatorModel
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.output import echo_stdout, OutResult


def vm_emulator_start_api(verbose: bool):
    echo_stdout(vm_emulator_start(), verbose)


def vm_emulator_screenshot_api(verbose: bool):
    echo_stdout(vm_emulator_screenshot(), verbose)


def vm_emulator_record_start_api(verbose: bool):
    echo_stdout(vm_emulator_record_start(), verbose)


def vm_emulator_record_stop_api(verbose: bool):
    echo_stdout(vm_emulator_record_stop(), verbose)


def vm_emulator_record_is_on_api(verbose: bool):
    echo_stdout(vm_emulator_is_on_record(), verbose)


def ssh_emulator_command_api(execute: str, verbose: bool):
    result = EmulatorModel.get_model_user().get_ssh_client()
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    echo_stdout(ssh_command(
        client=result.value,
        execute=execute
    ), verbose)


def ssh_emulator_run_api(
        package: str,
        nohup: bool,
        verbose: bool
):
    def echo_stdout_with_check_close(stdout: OutResult | None):
        if stdout and nohup and not stdout.is_error() and 'nohup:' in stdout.value:
            echo_stdout(OutResult(TextSuccess.ssh_run_package(package)))
        else:
            echo_stdout(stdout)

    result = EmulatorModel.get_model_user().get_ssh_client()
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    echo_stdout(ssh_run(
        client=result.value,
        package=package,
        nohup=nohup,
        listen_stdout=lambda stdout: echo_stdout_with_check_close(stdout),
        listen_stderr=lambda stderr: echo_stdout(stderr),
    ), verbose)


def ssh_emulator_upload_api(path: str, verbose: bool):
    result = EmulatorModel.get_model_user().get_ssh_client()
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    echo_stdout(ssh_upload(
        client=result.value,
        path=path,
        listen_progress=lambda stdout: echo_stdout(stdout)
    ), verbose)


def ssh_emulator_rpm_install_api(path: str, apm: bool, verbose: bool):
    result = EmulatorModel.get_model_root().get_ssh_client()
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    echo_stdout(ssh_rpm_install(
        client=result.value,
        path=path,
        apm=apm,
        listen_progress=lambda stdout: echo_stdout(stdout)
    ), verbose)


def ssh_emulator_package_remove_api(package: str, apm: bool, verbose: bool):
    result = EmulatorModel.get_model_root().get_ssh_client()
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    echo_stdout(ssh_package_remove(
        client=result.value,
        package=package,
        apm=apm,
    ), verbose)
