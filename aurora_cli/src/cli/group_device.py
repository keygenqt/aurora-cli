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

import click

from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.output import echo_stdout
from aurora_cli.src.cli.impl.ssh_commands import (
    ssh_common_command_cli,
    ssh_common_upload_cli,
    ssh_common_run_cli,
    ssh_common_install_cli,
    ssh_common_remove_cli
)


def _get_device_model(
        select: bool,
        index: int | None,
        verbose: bool
) -> DeviceModel:
    result_model = DeviceModel.get_model_select(select, index)
    if result_model.is_error():
        echo_stdout(result_model, verbose)
        exit(1)
    return DeviceModel.get_model_by_host(result_model.value)


def _get_device_ssh_client(
        select: bool,
        index: int | None,
        verbose: bool
):
    model = _get_device_model(select, index, verbose)
    result = model.get_ssh_client()
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    return result.value, model.devel_su


@click.group(name='device', help=TextGroup.group_device())
@click.pass_context
def group_device(ctx: {}):
    if argv_is_test():
        ctx.obj = AppConfig.create_test()


@group_device.command(name='command', help=TextCommand.command_device_command())
@click.option('-e', '--execute', type=click.STRING, required=True, help=TextArgument.argument_execute_device())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, default=None, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def ssh_device_command_cli(execute: str, select: bool, index: int | None, verbose: bool):
    client, _ = _get_device_ssh_client(select, index, verbose)
    ssh_common_command_cli(
        client=client,
        execute=execute,
        verbose=verbose
    )


@group_device.command(name='upload', help=TextCommand.command_device_upload())
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help=TextArgument.argument_path())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def ssh_device_upload_cli(path: [], select: bool, index: int, verbose: bool):
    client, _ = _get_device_ssh_client(select, index, verbose)
    ssh_common_upload_cli(
        client=client,
        path=path,
        verbose=verbose
    )


@group_device.command(name='package-run', help=TextCommand.command_device_package_run())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-n', '--nohup', is_flag=True, help=TextArgument.argument_exit_after_run())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def ssh_device_run_cli(package: str, nohup: bool, select: bool, index: int, verbose: bool):
    client, _ = _get_device_ssh_client(select, index, verbose)
    ssh_common_run_cli(
        client=client,
        package=package,
        nohup=nohup,
        verbose=verbose
    )


@group_device.command(name='package-install', help=TextCommand.command_device_package_install())
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
@click.option('-a', '--apm', is_flag=True, help=TextArgument.argument_apm())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def ssh_device_install_cli(path: [], apm: bool, select: bool, index: int, verbose: bool):
    client, devel_su = _get_device_ssh_client(select, index, verbose)
    ssh_common_install_cli(
        client=client,
        path=path,
        apm=apm,
        verbose=verbose,
        devel_su=devel_su
    )


@group_device.command(name='package-remove', help=TextCommand.command_device_package_remove())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-a', '--apm', is_flag=True, help=TextArgument.argument_apm())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def ssh_device_remove_cli(package: str, apm: bool, select: bool, index: int, verbose: bool):
    client, devel_su = _get_device_ssh_client(select, index, verbose)
    ssh_common_remove_cli(
        client=client,
        package=package,
        apm=apm,
        verbose=verbose,
        devel_su=devel_su
    )
