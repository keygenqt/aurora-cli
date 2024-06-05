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

from aurora_cli.src.base.common.groups.device_features import (
    device_command_common,
    device_upload_common,
    device_package_run_common,
    device_package_install_common,
    device_package_remove_common
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.output import echo_stdout


def _select_model(
        select: bool,
        index: int | None,
        verbose: bool
) -> DeviceModel:
    result_model = DeviceModel.get_model_select(select, index)
    if result_model.is_error():
        echo_stdout(result_model, verbose)
        exit(1)
    return DeviceModel.get_model_by_host(result_model.value, verbose)


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
def command(execute: str, select: bool, index: int | None, verbose: bool):
    device_command_common(
        model=_select_model(select, index, verbose),
        execute=execute,
        verbose=verbose
    )


@group_device.command(name='upload', help=TextCommand.command_device_upload())
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help=TextArgument.argument_path())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def upload(path: [], select: bool, index: int, verbose: bool):
    device_upload_common(
        model=_select_model(select, index, verbose),
        path=path,
        verbose=verbose
    )


@group_device.command(name='package-run', help=TextCommand.command_device_package_run())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_run(package: str, select: bool, index: int, verbose: bool):
    device_package_run_common(
        model=_select_model(select, index, verbose),
        package=package,
        verbose=verbose
    )


@group_device.command(name='package-install', help=TextCommand.command_device_package_install())
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
@click.option('-a', '--apm', is_flag=True, help=TextArgument.argument_apm())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_install(path: [], apm: bool, select: bool, index: int, verbose: bool):
    device_package_install_common(
        model=_select_model(select, index, verbose),
        path=path,
        apm=apm,
        verbose=verbose,
    )


@group_device.command(name='package-remove', help=TextCommand.command_device_package_remove())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-a', '--apm', is_flag=True, help=TextArgument.argument_apm())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_remove(package: str, apm: bool, select: bool, index: int, verbose: bool):
    device_package_remove_common(
        model=_select_model(select, index, verbose),
        package=package,
        apm=apm,
        verbose=verbose,
    )
