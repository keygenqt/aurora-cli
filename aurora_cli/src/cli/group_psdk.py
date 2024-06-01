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

from aurora_cli.src.base.common.request_features import get_versions_psdk
from aurora_cli.src.base.common.search_features import search_installed_psdk
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.models.psdk_model import PsdkModel
from aurora_cli.src.base.models.sign_model import SignModel
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.output import echo_stdout


def _get_psdk_model(
        select: bool,
        index: int | None,
        verbose: bool
) -> PsdkModel:
    result_model = PsdkModel.get_model_select(select, index)
    if result_model.is_error():
        echo_stdout(result_model, verbose)
        exit(1)
    return PsdkModel.get_model_by_version(result_model.value)


def _get_sign_model(
        select: bool,
        index: int | None,
        verbose: bool
) -> SignModel:
    result_model = SignModel.get_model_select(select, index)
    if result_model.is_error():
        echo_stdout(result_model, verbose)
        exit(1)
    return SignModel.get_model_by_name(result_model.value)


@click.group(name='psdk', help=TextGroup.group_psdk())
@click.pass_context
def group_psdk(ctx: {}):
    if argv_is_test():
        ctx.obj = AppConfig.create_test()


@group_psdk.command(help=TextCommand.command_psdk_available())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def available(verbose: bool):
    echo_stdout(get_versions_psdk(), verbose)


@group_psdk.command(help=TextCommand.command_psdk_installed())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def installed(verbose: bool):
    echo_stdout(search_installed_psdk(), verbose)


@group_psdk.command(help=TextCommand.command_psdk_install())
@click.option('-l', '--latest', is_flag=True, help=TextArgument.argument_latest_version())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def install(latest: bool, verbose: bool):
    print('Coming soon')


@group_psdk.command(help=TextCommand.command_psdk_remove())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def remove(verbose: bool):
    print('Coming soon')


@group_psdk.command(help=TextCommand.command_psdk_clear())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def clear(select: bool, index: int, verbose: bool):
    print('Coming soon')


@group_psdk.command(help=TextCommand.command_psdk_package_search())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_search(package: str, select: bool, index: int, verbose: bool):
    result = _get_psdk_model(select, index, verbose)
    print(result)


@group_psdk.command(help=TextCommand.command_psdk_package_install())
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_install(path: [], select: bool, index: int, verbose: bool):
    print('Coming soon')


@group_psdk.command(help=TextCommand.command_psdk_package_remove())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_remove(package: str, select: bool, index: int, verbose: bool):
    print('Coming soon')


@group_psdk.command(help=TextCommand.command_psdk_sign())
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def sign(path: [], select: bool, index: int, verbose: bool):
    result = _get_sign_model(select, index, verbose)
    print(result)


@group_psdk.command(help=TextCommand.command_psdk_sudoers_add())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def sudoers_add(verbose: bool):
    print('Coming soon')


@group_psdk.command(help=TextCommand.command_psdk_sudoers_remove())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def sudoers_remove(verbose: bool):
    print('Coming soon')


@group_psdk.command(help=TextCommand.command_psdk_targets())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def targets(select: bool, index: int, verbose: bool):
    print('Coming soon')


@group_psdk.command(help=TextCommand.command_psdk_validate())
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
@click.option('-pr', '--profile', default='regular', type=click.Choice([
    'regular',
    'extended',
    'mdm',
    'antivirus',
    'auth',
], case_sensitive=False), help=TextArgument.argument_validate_profile())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def validate(path: [], profile: str, select: bool, index: int, verbose: bool):
    print('Coming soon')
