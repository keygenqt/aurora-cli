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
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.output import echo_stdout, OutResult, OutResultError


def device_list_api(verbose: bool):
    devices = DeviceModel.get_lists_devices()
    echo_stdout(OutResult(
        value=[device.to_dict() for device in devices]
    ), verbose)


def ssh_device_command_api(
        host: str,
        execute: str,
        verbose: bool
):
    model = DeviceModel.get_model_by_host(host)
    if not model:
        echo_stdout(OutResultError(TextError.device_not_found_error(host)), verbose)
        exit(1)
    result = model.get_ssh_client()
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    echo_stdout(ssh_command(
        client=result.value,
        execute=execute
    ), verbose)


def ssh_device_run_api(
        host: str,
        package: str,
        nohup: bool,
        verbose: bool
):
    def echo_stdout_with_check_close(stdout: OutResult | None):
        if stdout and nohup and not stdout.is_error() and 'nohup:' in stdout.value:
            echo_stdout(OutResult(TextSuccess.ssh_run_package(package)))
        else:
            echo_stdout(stdout)

    model = DeviceModel.get_model_by_host(host)
    if not model:
        echo_stdout(OutResultError(TextError.device_not_found_error(host)), verbose)
        exit(1)
    result = model.get_ssh_client()
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


def ssh_device_upload_api(
        host: str,
        path: str,
        verbose: bool
):
    model = DeviceModel.get_model_by_host(host)
    if not model:
        echo_stdout(OutResultError(TextError.device_not_found_error(host)), verbose)
        exit(1)
    result = model.get_ssh_client()
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    echo_stdout(ssh_upload(
        client=result.value,
        path=path,
        listen_progress=lambda stdout: echo_stdout(stdout)
    ), verbose)


def ssh_device_rpm_install_api(
        host: str,
        path: str,
        apm: bool,
        verbose: bool
):
    model = DeviceModel.get_model_by_host(host)
    if not model:
        echo_stdout(OutResultError(TextError.device_not_found_error(host)), verbose)
        exit(1)
    result = model.get_ssh_client()
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    echo_stdout(ssh_rpm_install(
        client=result.value,
        path=path,
        apm=apm,
        listen_progress=lambda stdout: echo_stdout(stdout),
        devel_su=model.devel_su
    ), verbose)


def ssh_device_package_remove_api(
        host: str,
        package: str,
        apm: bool,
        verbose: bool
):
    model = DeviceModel.get_model_by_host(host)
    if not model:
        echo_stdout(OutResultError(TextError.device_not_found_error(host)), verbose)
        exit(1)
    result = model.get_ssh_client()
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    echo_stdout(ssh_package_remove(
        client=result.value,
        package=package,
        apm=apm,
        devel_su=model.devel_su
    ), verbose)
