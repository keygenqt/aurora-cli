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
import sys

import click

from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.output import echo_stdout
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.cli.ssh_commands import (
    ssh_common_command_cli,
    ssh_common_run_cli,
    ssh_common_upload_cli,
    ssh_common_install_cli,
    ssh_common_remove_cli
)


def _get_device_ssh_client(
        select: bool,
        index: int | None,
        verbose: bool
):
    if select and index is None:
        echo_stdout(TextInfo.select_array_out(
            key='devices',
            names=DeviceModel.get_names_devices(),
        ))
    result_model = DeviceModel.get_model_select(select, index)
    if result_model.is_error():
        echo_stdout(result_model, verbose)
        exit(1)
    result_client = result_model.value.get_ssh_client()
    if result_client.is_error():
        echo_stdout(result_client, verbose)
        exit(1)
    return result_client.value, result_model.value.devel_su


@click.group(name='device')
@click.pass_context
def group_device(ctx: {}):
    """Working with the device."""
    if argv_is_test():
        ctx.obj = AppConfig.create_test()


@group_device.command(name='command')
@click.option('-e', '--execute', type=click.STRING, required=True, help='The command to be executed on the device')
@click.option('-s', '--select', is_flag=True, help='Select from available')
@click.option('-i', '--index', type=click.INT, default=None, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_device_command_cli(execute: str, select: bool, index: int | None, verbose: bool):
    """Execute the command on the device."""
    client, _ = _get_device_ssh_client(select, index, verbose)
    ssh_common_command_cli(
        client=client,
        execute=execute,
        verbose=verbose
    )


@group_device.command(name='upload')
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to file')
@click.option('-s', '--select', is_flag=True, help='Select from available')
@click.option('-i', '--index', type=click.INT, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_device_upload_cli(path: [], select: bool, index: int, verbose: bool):
    """Upload file to ~/Download directory device."""
    client, _ = _get_device_ssh_client(select, index, verbose)
    ssh_common_upload_cli(
        client=client,
        path=path,
        verbose=verbose
    )


@group_device.command(name='package-run')
@click.option('-p', '--package', type=click.STRING, required=True, help='Package name')
@click.option('-n', '--nohup', is_flag=True, help='Exit after run')
@click.option('-s', '--select', is_flag=True, help='Select from available')
@click.option('-i', '--index', type=click.INT, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_device_run_cli(package: str, nohup: bool, select: bool, index: int, verbose: bool):
    """Run package on device in container."""
    client, _ = _get_device_ssh_client(select, index, verbose)
    ssh_common_run_cli(
        client=client,
        package=package,
        nohup=nohup,
        verbose=verbose
    )


@group_device.command(name='package-install')
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to RPM file')
@click.option('-a', '--apm', is_flag=True, help='Use new install APM')
@click.option('-s', '--select', is_flag=True, help='Select from available')
@click.option('-i', '--index', type=click.INT, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_device_install_cli(path: [], apm: bool, select: bool, index: int, verbose: bool):
    """Install RPM package on device."""
    client, devel_su = _get_device_ssh_client(select, index, verbose)
    ssh_common_install_cli(
        client=client,
        path=path,
        apm=apm,
        verbose=verbose,
        devel_su=devel_su
    )


@group_device.command(name='package-remove')
@click.option('-p', '--package', type=click.STRING, required=True, help='Package name')
@click.option('-a', '--apm', is_flag=True, help='Use new install APM')
@click.option('-s', '--select', is_flag=True, help='Select from available')
@click.option('-i', '--index', type=click.INT, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_device_remove_cli(package: str, apm: bool, select: bool, index: int, verbose: bool):
    """Install RPM package on device."""
    client, devel_su = _get_device_ssh_client(select, index, verbose)
    ssh_common_remove_cli(
        client=client,
        package=package,
        apm=apm,
        verbose=verbose,
        devel_su=devel_su
    )
