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

from aurora_cli.src.base.common.groups.psdk.psdk_project_features import (
    psdk_project_format_common,
    psdk_project_icons_common,
    psdk_project_check_format_common,
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.output import echo_verbose


@click.group(name='project', help=TextGroup.subgroup_psdk_project())
def subgroup_psdk_project():
    AppConfig.create_test()


@subgroup_psdk_project.command(name='format', help=TextCommand.command_project_format())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_format(
        path: Any,
        verbose: bool
):
    path = Path(path) if path else Path.cwd()
    psdk_project_format_common(path)
    echo_verbose(verbose)


@subgroup_psdk_project.command(name='check-format', help=TextCommand.command_project_check_format())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_format(
        path: Any,
        verbose: bool
):
    path = Path(path) if path else Path.cwd()
    psdk_project_check_format_common(path)
    echo_verbose(verbose)


@subgroup_psdk_project.command(name='icons', help=TextCommand.command_project_icon())
@click.option('-i', '--image', type=click.STRING, required=True, help=TextArgument.argument_path_to_image())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_icons(
        image: str,
        path: Any,
        verbose: bool
):
    path = Path(path) if path else Path.cwd()
    psdk_project_icons_common(path, Path(image))
    echo_verbose(verbose)
