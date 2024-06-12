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

from pathlib import Path

import click

from aurora_cli.src.base.common.groups.psdk.psdk_project_features import (
    psdk_project_format_common,
    psdk_project_debug_common,
    psdk_project_build_common,
    psdk_project_icons_common
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.cli.psdk.__tools import cli_psdk_tool_select_model_psdk, cli_psdk_tool_select_target_psdk


@click.group(name='project', help=TextGroup.subgroup_psdk_project())
def subgroup_psdk_project():
    AppConfig.create_test()


@subgroup_psdk_project.command(name='format', help=TextCommand.command_project_format())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_format(path: str | None, verbose: bool):
    path = Path(path) if path else Path.cwd()
    psdk_project_format_common(path, verbose)


@subgroup_psdk_project.command(name='build', help=TextCommand.command_project_build())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, default=None, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_build(path: str | None, select: bool, index: int | None, verbose: bool):
    path = Path(path) if path else Path.cwd()
    model = cli_psdk_tool_select_model_psdk(select, index, verbose)
    target = cli_psdk_tool_select_target_psdk(model, verbose)
    psdk_project_build_common(model, target, path, verbose)


@subgroup_psdk_project.command(name='debug', help=TextCommand.command_project_debug())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, default=None, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_debug(path: str | None, select: bool, index: int | None, verbose: bool):
    path = Path(path) if path else Path.cwd()
    model = cli_psdk_tool_select_model_psdk(select, index, verbose)
    target = cli_psdk_tool_select_target_psdk(model, verbose)
    psdk_project_debug_common(model, target, path, verbose)


@subgroup_psdk_project.command(name='icon', help=TextCommand.command_project_icon())
@click.option('-p', '--icon', type=click.STRING, help=TextArgument.argument_path_to_icon())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_report(icon: str, path: str | None, verbose: bool):
    path = Path(path) if path else Path.cwd()
    psdk_project_icons_common(path, Path(icon), verbose)
