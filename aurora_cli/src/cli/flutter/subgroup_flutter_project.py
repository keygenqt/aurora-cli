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
from typing import Any

import click

from aurora_cli.src.base.common.groups.flutter.flutter_project_features import (
    flutter_project_report_common,
    flutter_project_format_common,
    flutter_project_icons_common,
    flutter_project_check_format_common,
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.output import echo_verbose
from aurora_cli.src.cli.flutter.__tools import cli_flutter_tool_select_model


@click.group(name='project', help=TextGroup.subgroup_flutter_project())
def subgroup_flutter_project():
    AppConfig.create_test()


@subgroup_flutter_project.command(name='format', help=TextCommand.command_project_format())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, default=None, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_format(
        path: Any,
        select: bool,
        index: Any,
        verbose: bool
):
    path = Path(path) if path else Path.cwd()
    model = cli_flutter_tool_select_model(select, index)
    flutter_project_format_common(model, path)
    echo_verbose(verbose)


@subgroup_flutter_project.command(name='check-format', help=TextCommand.command_project_check_format())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, default=None, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_check_format(
        path: Any,
        select: bool,
        index: Any,
        verbose: bool
):
    path = Path(path) if path else Path.cwd()
    model = cli_flutter_tool_select_model(select, index)
    flutter_project_check_format_common(model, path)
    echo_verbose(verbose)

@subgroup_flutter_project.command(name='report', help=TextCommand.command_flutter_project_report())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, default=None, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_report(
        path: Any,
        select: bool,
        index: Any,
        verbose: bool
):
    path = Path(path) if path else Path.cwd()
    model = cli_flutter_tool_select_model(select, index)
    flutter_project_report_common(model, path)
    echo_verbose(verbose)


@subgroup_flutter_project.command(name='icons', help=TextCommand.command_project_icon())
@click.option('-i', '--image', type=click.STRING, required=True, help=TextArgument.argument_path_to_image())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_icons(
        image: str,
        path: Any,
        verbose: bool
):
    path = Path(path) if path else Path.cwd()
    flutter_project_icons_common(path, Path(image))
    echo_verbose(verbose)
