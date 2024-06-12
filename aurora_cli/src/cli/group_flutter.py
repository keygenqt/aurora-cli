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

from aurora_cli.src.base.common.groups.flutter.flutter_features import (
    flutter_available_common,
    flutter_installed_common,
    flutter_install_common,
    flutter_remove_common,
)
from aurora_cli.src.base.common.groups.flutter.flutter_project_features import (
    flutter_project_report_common,
    flutter_project_format_common,
    flutter_project_build_common,
    flutter_project_debug_common,
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.models.flutter_model import FlutterModel
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.output import echo_stdout
from aurora_cli.src.base.utils.prompt import prompt_flutter_select


def _select_model(
        select: bool,
        index: int | None,
        verbose: bool
) -> FlutterModel:
    result_model = FlutterModel.get_model_select(select, index)
    if result_model.is_error():
        echo_stdout(result_model, verbose)
        exit(1)
    return FlutterModel.get_model_by_version(result_model.value, verbose)


@click.group(name='flutter', help=TextGroup.group_flutter())
@click.pass_context
def group_flutter(ctx: {}):
    if argv_is_test():
        ctx.obj = AppConfig.create_test()


@group_flutter.command(name='available', help=TextCommand.command_flutter_available())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def available(verbose: bool):
    flutter_available_common(verbose)


@group_flutter.command(name='installed', help=TextCommand.command_flutter_installed())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def installed(verbose: bool):
    flutter_installed_common(verbose)


@group_flutter.command(name='install', help=TextCommand.command_flutter_install())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def install(select: bool, verbose: bool):
    version = prompt_flutter_select(select)
    flutter_install_common(version, verbose)


@group_flutter.command(name='remove', help=TextCommand.command_flutter_remove())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def remove(verbose: bool):
    model = _select_model(True, None, verbose)
    flutter_remove_common(model, verbose)


@group_flutter.command(name='project-format', help=TextCommand.command_project_format())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, default=None, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_format(path: str | None, select: bool, index: int | None, verbose: bool):
    path = Path(path) if path else Path.cwd()
    model = _select_model(select, index, verbose)
    flutter_project_format_common(model, path, verbose)


@group_flutter.command(name='project-build', help=TextCommand.command_project_build())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, default=None, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_build(path: str | None, select: bool, index: int | None, verbose: bool):
    path = Path(path) if path else Path.cwd()
    model = _select_model(select, index, verbose)
    flutter_project_build_common(model, path, verbose)


@group_flutter.command(name='project-debug', help=TextCommand.command_project_debug())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, default=None, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_debug(path: str | None, select: bool, index: int | None, verbose: bool):
    path = Path(path) if path else Path.cwd()
    model = _select_model(select, index, verbose)
    flutter_project_debug_common(model, path, verbose)


@group_flutter.command(name='project-report', help=TextCommand.command_flutter_project_report())
@click.option('-p', '--path', type=click.STRING, required=False, help=TextArgument.argument_path_to_project())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def project_report(path: str | None, verbose: bool):
    flutter_project_report_common(path if Path(path) else Path.cwd(), verbose)
