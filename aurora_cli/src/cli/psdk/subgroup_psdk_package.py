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

from aurora_cli.src.base.common.groups.psdk.psdk_package_features import (
    psdk_package_search_common,
    psdk_package_install_common,
    psdk_package_remove_common,
    psdk_package_validate_common,
    psdk_package_sign_common,
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.output import echo_verbose
from aurora_cli.src.cli.psdk.__tools import (
    cli_psdk_tool_select_model_psdk,
    cli_psdk_tool_select_model_sign,
    cli_psdk_tool_select_target_psdk
)


@click.group(name='package', help=TextGroup.subgroup_psdk_package())
def subgroup_psdk_package():
    AppConfig.create_test()


@subgroup_psdk_package.command(name='search', help=TextCommand.command_psdk_package_search())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_search(
        package: str,
        select: bool,
        index: int,
        verbose: bool
):
    model = cli_psdk_tool_select_model_psdk(select, index)
    target = cli_psdk_tool_select_target_psdk(model)
    psdk_package_search_common(model, target, package)
    echo_verbose(verbose)


@subgroup_psdk_package.command(name='install', help=TextCommand.command_psdk_package_install())
@click.option('-p', '--path', type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_install(
        path: str,
        select: bool,
        index: int,
        verbose: bool
):
    model = cli_psdk_tool_select_model_psdk(select, index)
    target = cli_psdk_tool_select_target_psdk(model)
    psdk_package_install_common(model, target, path)
    echo_verbose(verbose)


@subgroup_psdk_package.command(name='remove', help=TextCommand.command_psdk_package_remove())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_remove(
        package: str,
        select: bool,
        index: int,
        verbose: bool
):
    model = cli_psdk_tool_select_model_psdk(select, index)
    target = cli_psdk_tool_select_target_psdk(model)
    psdk_package_remove_common(model, target, package)
    echo_verbose(verbose)


@subgroup_psdk_package.command(name='validate', help=TextCommand.command_psdk_validate())
@click.option('-p', '--path', type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
@click.option('-pr', '--profile', default='regular',
              type=click.Choice(['regular', 'extended', 'mdm', 'antivirus', 'auth'], case_sensitive=False),
              help=TextArgument.argument_validate_profile())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_validate(
        path: str,
        profile: str,
        select: bool,
        index: int,
        verbose: bool
):
    model = cli_psdk_tool_select_model_psdk(select, index)
    target = cli_psdk_tool_select_target_psdk(model)
    psdk_package_validate_common(model, target, path, profile)
    echo_verbose(verbose)


@subgroup_psdk_package.command(name='sign', help=TextCommand.command_psdk_sign())
@click.option('-p', '--path', type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_sign(
        path: str,
        select: bool,
        index: int,
        verbose: bool
):
    model_psdk = cli_psdk_tool_select_model_psdk(select, index)
    model_keys = cli_psdk_tool_select_model_sign(select, index)
    psdk_package_sign_common(model_psdk, model_keys, [path])
    echo_verbose(verbose)
