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
from typing import Any

import click

from aurora_cli.src.base.common.groups.device.device_features import (
    device_command_common,
    device_upload_common, device_ssh_copy_id_common
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.output import echo_verbose
from aurora_cli.src.cli.device.__tools import cli_device_tool_select_model
from aurora_cli.src.cli.device.subgroup_device_package import subgroup_device_package


# noinspection PyTypeChecker
def init_subgroups_device():
    group_device.add_command(subgroup_device_package)


@click.group(name='device', help=TextGroup.group_device())
def group_device():
    AppConfig.create_test()


@group_device.command(name='command', help=TextCommand.command_device_command())
@click.option('-e', '--execute', type=click.STRING, required=True, help=TextArgument.argument_execute_device())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, default=None, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def command(
        execute: str,
        select: bool,
        index: Any,
        verbose: bool
):
    model = cli_device_tool_select_model(select, index)
    device_command_common(model, execute)
    echo_verbose(verbose)


@group_device.command(name='upload', help=TextCommand.command_device_upload())
@click.option('-p', '--path', type=click.STRING, required=True, help=TextArgument.argument_path())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def upload(
        path: str,
        select: bool,
        index: int,
        verbose: bool
):
    model = cli_device_tool_select_model(select, index)
    device_upload_common(model, path)
    echo_verbose(verbose)


@group_device.command(name='ssh-copy-id', help=TextCommand.command_device_ssh_copy_id())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def ssh_copy_id(verbose: bool):
    model = cli_device_tool_select_model(True, None)
    device_ssh_copy_id_common(model)
    echo_verbose(verbose)
