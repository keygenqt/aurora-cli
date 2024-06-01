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

from aurora_cli.src.base.common.request_features import get_versions_sdk
from aurora_cli.src.base.common.search_features import search_installed_sdk
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.models.sdk_model import SdkModel
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.output import echo_stdout


def _get_sdk_model(
        select: bool,
        index: int | None,
        verbose: bool
) -> SdkModel:
    result_model = SdkModel.get_model_select(select, index)
    if result_model.is_error():
        echo_stdout(result_model, verbose)
        exit(1)
    return SdkModel.get_model_by_version(result_model.value)


@click.group(name='sdk', help=TextGroup.group_sdk())
@click.pass_context
def group_sdk(ctx: {}):
    if argv_is_test():
        ctx.obj = AppConfig.create_test()


@group_sdk.command(help=TextCommand.command_sdk_available())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def available(verbose: bool):
    echo_stdout(get_versions_sdk(), verbose)


@group_sdk.command(help=TextCommand.command_sdk_installed())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def installed(verbose: bool):
    echo_stdout(search_installed_sdk(), verbose)


@group_sdk.command(help=TextCommand.command_sdk_install())
@click.option('-l', '--latest', is_flag=True, help=TextArgument.argument_latest_version())
@click.option('-l', '--offline', is_flag=True, help=TextArgument.argument_sdk_installer_type())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def install(latest: bool, offline: bool, verbose: bool):
    print('Coming soon')


@group_sdk.command(help=TextCommand.command_sdk_tool())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def tool(verbose: bool):
    result = _get_sdk_model(False, None, verbose)
    print(result)
