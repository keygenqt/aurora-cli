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

from aurora_cli.src.base.common.groups.psdk_features import (
    psdk_available_common,
    psdk_installed_common,
    psdk_install_common,
    psdk_remove_common,
    psdk_package_search_common,
    psdk_sudoers_add_common,
    psdk_sudoers_remove_common,
    psdk_targets_common,
    psdk_package_install_common,
    psdk_package_remove_common,
    psdk_package_validate_common,
    psdk_package_sign_common,
    psdk_snapshot_remove_common,
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.models.psdk_model import PsdkModel
from aurora_cli.src.base.models.sign_model import SignModel
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.output import echo_stdout
from aurora_cli.src.base.utils.prompt import prompt_psdk_select


def _select_model_psdk(
        select: bool,
        index: int | None,
        verbose: bool
) -> PsdkModel:
    result_model = PsdkModel.get_model_select(select, index)
    if result_model.is_error():
        echo_stdout(result_model, verbose)
        exit(1)
    return PsdkModel.get_model_by_version(result_model.value, verbose)


def _select_target_psdk(
        model: PsdkModel,
        verbose: bool
) -> str:
    result_target = model.get_model_targets_select()
    if not result_target.is_success():
        echo_stdout(result_target, verbose)
        exit(1)
    return result_target.value


def _select_model_sign(
        select: bool,
        index: int | None,
) -> SignModel | None:
    result_model = SignModel.get_model_select(select, index)
    if result_model.is_error():
        return None
    return SignModel.get_model_by_name(result_model.value)


@click.group(name='psdk', help=TextGroup.group_psdk())
@click.pass_context
def group_psdk(ctx: {}):
    if argv_is_test():
        ctx.obj = AppConfig.create_test()


@group_psdk.command(name='available', help=TextCommand.command_psdk_available())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def available(verbose: bool):
    psdk_available_common(verbose)


@group_psdk.command(name='installed', help=TextCommand.command_psdk_installed())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def installed(verbose: bool):
    psdk_installed_common(verbose)


@group_psdk.command(help=TextCommand.command_psdk_targets())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def targets(select: bool, index: int, verbose: bool):
    model = _select_model_psdk(select, index, verbose)
    psdk_targets_common(model, verbose)


@group_psdk.command(name='install', help=TextCommand.command_psdk_install())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def install(select: bool, verbose: bool):
    version = prompt_psdk_select(select)
    psdk_install_common(version, verbose)


@group_psdk.command(name='remove', help=TextCommand.command_psdk_remove())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def remove(select: bool, index: int, verbose: bool):
    model = _select_model_psdk(select, index, verbose)
    psdk_remove_common(model, verbose)


@group_psdk.command(name='snapshot-remove', help=TextCommand.command_psdk_snapshot_remove())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def snapshot_remove(select: bool, index: int, verbose: bool):
    model = _select_model_psdk(select, index, verbose)
    target = _select_target_psdk(model, select)
    psdk_snapshot_remove_common(model, target, verbose)


@group_psdk.command(name='package-search', help=TextCommand.command_psdk_package_search())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_search(package: str, select: bool, index: int, verbose: bool):
    model = _select_model_psdk(select, index, verbose)
    target = _select_target_psdk(model, select)
    psdk_package_search_common(model, target, package, verbose)


@group_psdk.command(name='package-install', help=TextCommand.command_psdk_package_install())
@click.option('-p', '--path', type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_install(path: str, select: bool, index: int, verbose: bool):
    model = _select_model_psdk(select, index, verbose)
    target = _select_target_psdk(model, verbose)
    psdk_package_install_common(model, target, path, verbose)


@group_psdk.command(name='package-remove', help=TextCommand.command_psdk_package_remove())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_remove(package: str, select: bool, index: int, verbose: bool):
    model = _select_model_psdk(select, index, verbose)
    target = _select_target_psdk(model, verbose)
    psdk_package_remove_common(model, target, package, verbose)


@group_psdk.command(name='package-validate', help=TextCommand.command_psdk_validate())
@click.option('-p', '--path', type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
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
def package_validate(path: str, profile: str, select: bool, index: int, verbose: bool):
    model = _select_model_psdk(select, index, verbose)
    target = _select_target_psdk(model, verbose)
    psdk_package_validate_common(model, target, path, profile, verbose)


@group_psdk.command(name='package-sign', help=TextCommand.command_psdk_sign())
@click.option('-p', '--path', type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_sign(path: str, select: bool, index: int, verbose: bool):
    model_psdk = _select_model_psdk(select, index, verbose)
    model_keys = _select_model_sign(select, index)
    psdk_package_sign_common(model_psdk, model_keys, path, verbose)


@group_psdk.command(help=TextCommand.command_psdk_sudoers_add())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def sudoers_add(select: bool, index: int, verbose: bool):
    model = _select_model_psdk(select, index, verbose)
    psdk_sudoers_add_common(model, verbose)


@group_psdk.command(help=TextCommand.command_psdk_sudoers_remove())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-i', '--index', type=click.INT, help=TextArgument.argument_index())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def sudoers_remove(select: bool, index: int, verbose: bool):
    model = _select_model_psdk(select, index, verbose)
    psdk_sudoers_remove_common(model, verbose)
