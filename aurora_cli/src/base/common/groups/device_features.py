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
from aurora_cli.src.base.utils.output import echo_stdout
from aurora_cli.src.cli.impl.ssh_commands import ssh_command_common, ssh_run_common, ssh_upload_common, \
    ssh_install_common, ssh_remove_common


def _get_ssh_client(
        model: DeviceModel,
        verbose: bool
):
    result = model.get_ssh_client()
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    return result.value


def device_command_common(
        model: DeviceModel,
        execute: str,
        verbose: bool
):
    ssh_command_common(
        client=_get_ssh_client(model, verbose),
        execute=execute,
        verbose=verbose
    )


def device_upload_common(
        model: DeviceModel,
        path: [],
        verbose: bool
):
    ssh_upload_common(
        client=_get_ssh_client(model, verbose),
        path=path,
        verbose=verbose
    )


def device_package_run_common(
        model: DeviceModel,
        package: str,
        verbose: bool
):
    ssh_run_common(
        client=_get_ssh_client(model, verbose),
        package=package,
        verbose=verbose
    )


def device_package_install_common(
        model: DeviceModel,
        path: [], apm: bool,
        verbose: bool
):
    ssh_install_common(
        client=_get_ssh_client(model, verbose),
        path=path,
        apm=apm,
        verbose=verbose,
        devel_su=model.devel_su
    )


def device_package_remove_common(
        model: DeviceModel,
        package: str,
        apm: bool,
        verbose: bool
):
    ssh_remove_common(
        client=_get_ssh_client(model, verbose),
        package=package,
        apm=apm,
        verbose=verbose,
        devel_su=model.devel_su
    )
