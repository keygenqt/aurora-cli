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

from aurora_cli.src.base.common.groups.psdk.psdk_sudoers_features import (
    psdk_sudoers_add_common,
    psdk_sudoers_remove_common
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.output import echo_verbose
from aurora_cli.src.cli.psdk.__tools import cli_psdk_tool_select_model_psdk


@click.group(name='sudoers', help=TextGroup.subgroup_psdk_sudoers())
def subgroup_psdk_sudoers():
    AppConfig.create_test()


@subgroup_psdk_sudoers.command(name='add', help=TextCommand.command_psdk_sudoers_add())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def sudoers_add(
        select: bool,
        index: int,
        verbose: bool
):
    model = cli_psdk_tool_select_model_psdk(select, index)
    psdk_sudoers_add_common(model)
    echo_verbose(verbose)


@subgroup_psdk_sudoers.command(name='remove', help=TextCommand.command_psdk_sudoers_remove())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def sudoers_remove(
        select: bool,
        index: int,
        verbose: bool
):
    model = cli_psdk_tool_select_model_psdk(select, index)
    psdk_sudoers_remove_common(model)
    echo_verbose(verbose)
