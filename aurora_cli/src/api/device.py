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
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.output import echo_stdout_json, OutResult
from aurora_cli.src.common.ssh_features import (
    ssh_command,
    ssh_run,
    ssh_upload,
    ssh_rpm_install,
    ssh_package_remove
)


def device_list_api(verbose: bool):
    """Get list devices."""
    devices = DeviceModel.get_lists_devices()
    echo_stdout_json(OutResult(
        value=[device.to_dict() for device in devices]
    ), verbose)


def ssh_device_command_api(
        host: str,
        port: int,
        auth: str,
        execute: str,
        verbose: bool
):
    """Execute the command on the device."""
    result = DeviceModel.get_model(
        host=host,
        port=port,
        auth=auth,
    ).get_ssh_client()
    if result.is_error():
        echo_stdout_json(result, verbose)
        exit(1)
    echo_stdout_json(ssh_command(
        client=result.value,
        execute=execute
    ), verbose)


def ssh_device_run_api(
        host: str,
        port: int,
        auth: str,
        package: str,
        verbose: bool
):
    """Run package on device in container."""
    result = DeviceModel.get_model(
        host=host,
        port=port,
        auth=auth,
    ).get_ssh_client()
    if result.is_error():
        echo_stdout_json(result, verbose)
        exit(1)
    echo_stdout_json(ssh_run(
        client=result.value,
        package=package,
        listen_stdout=lambda stdout: echo_stdout_json(stdout),
        listen_stderr=lambda stderr: echo_stdout_json(stderr),
    ), verbose)


def ssh_device_upload_api(
        host: str,
        port: int,
        auth: str,
        path: str,
        verbose: bool
):
    """Upload file to ~/Download directory device."""
    result = DeviceModel.get_model(
        host=host,
        port=port,
        auth=auth,
    ).get_ssh_client()
    if result.is_error():
        echo_stdout_json(result, verbose)
        exit(1)
    echo_stdout_json(ssh_upload(
        client=result.value,
        path=path,
        listen_progress=lambda stdout: echo_stdout_json(stdout)
    ), verbose)


def ssh_device_rpm_install_api(
        host: str,
        port: int,
        auth: str,
        devel_su: str,
        path: str,
        apm: bool,
        verbose: bool
):
    """Install RPM package on device."""
    result = DeviceModel.get_model(
        host=host,
        port=port,
        auth=auth,
        devel_su=devel_su,
    ).get_ssh_client()
    if result.is_error():
        echo_stdout_json(result, verbose)
        exit(1)
    echo_stdout_json(ssh_rpm_install(
        client=result.value,
        path=path,
        apm=apm,
        listen_progress=lambda stdout: echo_stdout_json(stdout),
        devel_su=devel_su
    ), verbose)


def ssh_device_package_remove_api(
        host: str,
        port: int,
        auth: str,
        devel_su: str,
        package: str,
        apm: bool,
        verbose: bool
):
    """Remove package from device."""
    result = DeviceModel.get_model(
        host=host,
        port=port,
        auth=auth,
        devel_su=devel_su,
    ).get_ssh_client()
    if result.is_error():
        echo_stdout_json(result, verbose)
        exit(1)
    echo_stdout_json(ssh_package_remove(
        client=result.value,
        package=package,
        apm=apm,
        devel_su=devel_su
    ), verbose)
