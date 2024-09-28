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

from aurora_cli.src.base.common.groups.emulator.emulator_package_features import (
    emulator_package_run_common,
    emulator_package_install_common,
    emulator_package_remove_common
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.output import echo_verbose, echo_stdout
from aurora_cli.src.cli.emulator.__tools import cli_emulator_tool_select_model


@click.group(name='package', help=TextGroup.subgroup_emulator_package())
def subgroup_emulator_package():
    AppConfig.create_test()


@subgroup_emulator_package.command(name='run', help=TextCommand.command_emulator_package_run())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-m', '--mode', type=click.Choice(['dart', 'gdb'], case_sensitive=False),
              help=TextArgument.argument_run_mode())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_run(
        package: str,
        mode: str,
        verbose: bool
):
    if mode:
        echo_stdout(TextInfo.run_mode_debug_info())
    model = cli_emulator_tool_select_model()
    emulator_package_run_common(model, package, mode if mode else 'sandbox', str(Path.cwd()))
    echo_verbose(verbose)


@subgroup_emulator_package.command(name='install', help=TextCommand.command_emulator_package_install())
@click.option('-p', '--path', type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
@click.option('-a', '--apm', is_flag=True, help=TextArgument.argument_apm())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_install(
        path: str,
        apm: bool,
        verbose: bool
):
    model = cli_emulator_tool_select_model(is_root=True)
    emulator_package_install_common(model, path, apm)
    echo_verbose(verbose)


@subgroup_emulator_package.command(name='remove', help=TextCommand.command_emulator_package_remove())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-a', '--apm', is_flag=True, help=TextArgument.argument_apm())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_remove(
        package: str,
        apm: bool,
        verbose: bool
):
    model = cli_emulator_tool_select_model(is_root=True)
    emulator_package_remove_common(model, package, apm)
    echo_verbose(verbose)
