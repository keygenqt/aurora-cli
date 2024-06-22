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

from aurora_cli.src.base.common.groups.flutter.flutter_features import (
    flutter_available_common,
    flutter_installed_common,
    flutter_install_common,
    flutter_remove_common,
    flutter_add_custom_devices_common,
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.prompt import TextPrompt
from aurora_cli.src.base.utils.output import echo_verbose, echo_stdout, OutResultInfo
from aurora_cli.src.base.utils.prompt import prompt_flutter_select_version
from aurora_cli.src.base.utils.tests import tests_exit
from aurora_cli.src.cli.flutter.__tools import cli_flutter_tool_select_model
from aurora_cli.src.cli.flutter.subgroup_flutter_project import subgroup_flutter_project


# noinspection PyTypeChecker
def init_subgroups_flutter():
    group_flutter.add_command(subgroup_flutter_project)


@click.group(name='flutter', help=TextGroup.group_flutter())
def group_flutter():
    AppConfig.create_test()


@group_flutter.command(name='available', help=TextCommand.command_flutter_available())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def available(verbose: bool):
    flutter_available_common()
    echo_verbose(verbose)


@group_flutter.command(name='installed', help=TextCommand.command_flutter_installed())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def installed(verbose: bool):
    flutter_installed_common()
    echo_verbose(verbose)


@group_flutter.command(name='install', help=TextCommand.command_flutter_install())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def install(
        select: bool,
        verbose: bool
):
    version = prompt_flutter_select_version(select)
    flutter_install_common(version)
    echo_verbose(verbose)


@group_flutter.command(name='remove', help=TextCommand.command_flutter_remove())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def remove(verbose: bool):
    tests_exit()
    model = cli_flutter_tool_select_model(True, None)
    flutter_remove_common(model)
    echo_verbose(verbose)


@group_flutter.command(name='custom-devices', help=TextCommand.command_flutter_custom_devices())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, default=None, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def custom_devices(
        select: bool,
        index: Any,
        verbose: bool
):
    echo_stdout(OutResultInfo(TextInfo.devices_turn_on()))

    click.prompt(
        text=TextPrompt.is_ready(),
        prompt_suffix='',
        default='Enter',
        hide_input=True
    )

    model = cli_flutter_tool_select_model(select, index)
    flutter_add_custom_devices_common(model)
    echo_verbose(verbose)
