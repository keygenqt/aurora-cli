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

from aurora_cli.src.base.common.request_features import get_versions_sdk, get_version_latest_by_url, \
    get_download_url_by_version
from aurora_cli.src.base.common.search_features import search_installed_sdk
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.models.sdk_model import SdkModel
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.download import downloads, check_downloads
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError
from aurora_cli.src.base.utils.prompt import prompt_sdk_select
from aurora_cli.src.base.utils.shell import shell_exec_app


def _get_sdk_model(
        select: bool,
        index: int | None,
        verbose: bool
) -> SdkModel:
    result_model = SdkModel.get_model_select(select, index)
    if result_model.is_error():
        echo_stdout(result_model, verbose)
        exit(1)
    model = SdkModel.get_model_by_version(result_model.value)
    if not model:
        echo_stdout(OutResultError(TextError.sdk_not_found_error()), verbose)
        exit(0)
    return model


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
@click.option('-l', '--offline', is_flag=True, help=TextArgument.argument_sdk_installer_type())
@click.option('-s', '--select', is_flag=True, help=TextArgument.argument_select())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def install(offline: bool, select: bool, verbose: bool):
    if SdkModel.get_versions_sdk():
        echo_stdout(TextError.sdk_already_installed_error(), verbose)
        exit(1)

    # prompt major version
    version_url = prompt_sdk_select(select)
    # get full latest version
    version_full = get_version_latest_by_url(version_url)
    # get url path to files
    download_url = get_download_url_by_version(version_url, version_full)
    # get by type
    urls = [item for item in download_url if (offline and 'offline' in item) or (not offline and 'online' in item)]
    # check download urls
    urls, files = check_downloads(urls)

    if not download_url or not files:
        echo_stdout(TextError.get_install_info_error())
        exit(1)

    if urls:
        downloads(urls, verbose)

    run = Path(files[0])

    if shell_exec_app(run):
        echo_stdout(TextSuccess.shell_run_app_success(run.name), verbose)
    else:
        echo_stdout(TextError.shell_run_app_error(run.name), verbose)


@group_sdk.command(help=TextCommand.command_sdk_tool())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def tool(verbose: bool):
    result = _get_sdk_model(False, None, verbose)
    if shell_exec_app(result.get_tool_path()):
        echo_stdout(TextSuccess.shell_run_app_success(result.get_tool_path().name), verbose)
    else:
        echo_stdout(TextError.shell_run_app_error(result.get_tool_path().name), verbose)
