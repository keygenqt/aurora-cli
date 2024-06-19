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

from aurora_cli.src.base.common.groups.psdk.psdk_features import (
    psdk_available_common,
    psdk_installed_common,
    psdk_install_common,
    psdk_remove_common,
    psdk_targets_common,
    psdk_clear_common,
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.output import echo_verbose
from aurora_cli.src.base.utils.prompt import prompt_psdk_select_version
from aurora_cli.src.base.utils.tests import tests_exit
from aurora_cli.src.cli.psdk.__tools import cli_psdk_tool_select_model_psdk, cli_psdk_tool_select_target_psdk
from aurora_cli.src.cli.psdk.subgroup_psdk_package import subgroup_psdk_package
from aurora_cli.src.cli.psdk.subgroup_psdk_project import subgroup_psdk_project
from aurora_cli.src.cli.psdk.subgroup_psdk_sudoers import subgroup_psdk_sudoers


# noinspection PyTypeChecker
def init_subgroups_psdk():
    group_psdk.add_command(subgroup_psdk_package)
    group_psdk.add_command(subgroup_psdk_project)
    group_psdk.add_command(subgroup_psdk_sudoers)


@click.group(name='psdk', help=TextGroup.group_psdk())
def group_psdk():
    AppConfig.create_test()


@group_psdk.command(name='available', help=TextCommand.command_psdk_available())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def available(verbose: bool):
    psdk_available_common()
    echo_verbose(verbose)


@group_psdk.command(name='installed', help=TextCommand.command_psdk_installed())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def installed(verbose: bool):
    psdk_installed_common()
    echo_verbose(verbose)


@group_psdk.command(name='targets', help=TextCommand.command_psdk_targets())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def targets(
        select: bool,
        index: int,
        verbose: bool
):
    model = cli_psdk_tool_select_model_psdk(select, index)
    psdk_targets_common(model)
    echo_verbose(verbose)


@group_psdk.command(name='install', help=TextCommand.command_psdk_install())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def install(
        select: bool,
        verbose: bool
):
    version = prompt_psdk_select_version(select)
    psdk_install_common(version)
    echo_verbose(verbose)


@group_psdk.command(name='remove', help=TextCommand.command_psdk_remove())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def remove(verbose: bool):
    tests_exit()
    model = cli_psdk_tool_select_model_psdk(True, None)
    psdk_remove_common(model)
    echo_verbose(verbose)


@group_psdk.command(name='clear', help=TextCommand.command_psdk_clear())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def clear(
        select: bool,
        index: int,
        verbose: bool
):
    model = cli_psdk_tool_select_model_psdk(select, index)
    target = cli_psdk_tool_select_target_psdk(model)
    psdk_clear_common(model, target)
    echo_verbose(verbose)
