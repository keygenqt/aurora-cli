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
    psdk_project_build_common,
    psdk_project_icons_common
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, echo_verbose
from aurora_cli.src.cli.device.__tools import cli_device_tool_select_model
from aurora_cli.src.cli.psdk.__tools import (
    cli_psdk_tool_select_model_psdk,
    cli_psdk_tool_select_target_psdk,
    cli_psdk_tool_select_model_sign
)


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


@subgroup_psdk_project.command(name='build', help=TextCommand.command_project_build())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-d', '--debug', is_flag=True, help=TextArgument.argument_debug())
@click.option('-c', '--clean', is_flag=True, help=TextArgument.argument_clean())
@click.option('-i', '--install', is_flag=True, help=TextArgument.argument_install())
@click.option('-a', '--apm', is_flag=True, help=TextArgument.argument_apm())
@click.option('-r', '--run', is_flag=True, help=TextArgument.argument_run())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_build(
        path: Any,
        debug: bool,
        clean: bool,
        install: bool,
        apm: bool,
        run: bool,
        select: bool,
        verbose: bool
):
    if install and apm and debug:
        echo_stdout(OutResultError(TextError.debug_apm_error()))
        app_exit()

    if run and not install:
        echo_stdout(OutResultError(TextError.run_without_install_error()))
        app_exit(1)

    path = Path(path) if path else Path.cwd()
    model_psdk = cli_psdk_tool_select_model_psdk(select, None)
    target = cli_psdk_tool_select_target_psdk(model_psdk)

    model_keys = None
    if install:
        model_keys = cli_psdk_tool_select_model_sign(select, None)

    model_device = None
    if (install or run) and '86_64' not in target:
        model_device = cli_device_tool_select_model(select, None)

    psdk_project_build_common(
        model_psdk=model_psdk,
        model_device=model_device,
        model_keys=model_keys,
        target=target,
        debug=debug,
        clean=clean,
        project=path,
        is_install=install,
        is_apm=apm,
        is_run=run,
        verbose=verbose,
    )

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
