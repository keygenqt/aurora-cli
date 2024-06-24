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

from aurora_cli.src.base.common.groups.sdk.sdk_features import (
    sdk_available_common,
    sdk_installed_common,
    sdk_install_common,
    sdk_tool_common
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.models.sdk_model import SdkModel
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.output import echo_verbose
from aurora_cli.src.base.utils.prompt import prompt_sdk_select_version


@click.group(name='sdk', help=TextGroup.group_sdk())
def group_sdk():
    AppConfig.create_test()


@group_sdk.command(name='available', help=TextCommand.command_sdk_available())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def available(verbose: bool):
    sdk_available_common()
    echo_verbose(verbose)


@group_sdk.command(name='installed', help=TextCommand.command_sdk_installed())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def installed(verbose: bool):
    sdk_installed_common()
    echo_verbose(verbose)


@group_sdk.command(name='install', help=TextCommand.command_sdk_install())
@click.option('-l', '--offline', is_flag=True, help=TextArgument.argument_sdk_installer_type())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def install(
        offline: bool,
        select: bool,
        verbose: bool
):
    version = prompt_sdk_select_version(select)
    sdk_install_common(version, offline)
    echo_verbose(verbose)


@group_sdk.command(name='tool', help=TextCommand.command_sdk_tool())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def tool(verbose: bool):
    sdk_tool_common(SdkModel.get_model())
    echo_verbose(verbose)
