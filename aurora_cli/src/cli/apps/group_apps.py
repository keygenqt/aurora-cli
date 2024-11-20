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

from aurora_cli.src.base.common.groups.apps.apps_features import (
    apps_available_common,
    apps_download_common,
    apps_filter_common,
)
from aurora_cli.src.base.common.groups.device.device_package_features import device_package_install_common
from aurora_cli.src.base.common.groups.emulator.emulator_package_features import emulator_package_install_common
from aurora_cli.src.base.common.groups.psdk.psdk_package_features import psdk_package_sign_common
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import echo_verbose, echo_stdout, OutResultError
from aurora_cli.src.base.utils.prompt import (
    prompt_apps_id_select,
    prompt_apps_arch_select,
)
from aurora_cli.src.cli.device.__tools import cli_device_tool_select_model
from aurora_cli.src.cli.emulator.__tools import cli_emulator_tool_select_model
from aurora_cli.src.cli.psdk.__tools import cli_psdk_tool_select_model_psdk, cli_psdk_tool_select_model_sign


@click.group(name='apps', help=TextGroup.group_apps())
def group_apps():
    AppConfig.create_test()


@group_apps.command(name='available', help=TextCommand.command_apps_available())
@click.option('-s', '--search', type=click.STRING, help=TextArgument.argument_apps_search())
@click.option('-g', '--group',
              type=click.Choice(['flutter', 'kmp', 'pwa', 'qt', 'example', 'demo', 'game', 'plugin'],
                                case_sensitive=False),
              help=TextArgument.argument_apps_filter())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def available(
        search: str,
        group: str,
        verbose: bool
):
    apps_available_common(search, group)
    echo_verbose(verbose)


@group_apps.command(name='install', help=TextCommand.command_apps_install())
@click.option('-s', '--search', type=click.STRING, help=TextArgument.argument_apps_search())
@click.option('-g', '--group',
              type=click.Choice(['flutter', 'kmp', 'pwa', 'qt', 'example', 'demo', 'game', 'plugin'],
                                case_sensitive=False),
              help=TextArgument.argument_apps_filter())
@click.option('-ai', '--app-id', type=click.STRING, help=TextArgument.argument_app_id())
@click.option('-a', '--arch', type=click.Choice(['aarch64', 'armv7hl', 'x86_64'], case_sensitive=False),
              help=TextArgument.argument_arch())
@click.option('-id', '--index-device', type=click.INT, help=TextArgument.argument_app_device_index())
@click.option('-is', '--index-sign', type=click.INT, help=TextArgument.argument_app_sign_index())
@click.option('-ph', '--phrase', type=click.STRING, help=TextArgument.argument_path_phrase())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def install(
        search: str,
        group: str,
        app_id: str,
        arch: str,
        index_device: int,
        index_sign: int,
        phrase: str,
        verbose: bool
):
    apps = apps_filter_common(search, group)

    if group and not apps:
        echo_stdout(TextInfo.available_apps_empty())
        app_exit()

    if not app_id:
        app_name = prompt_apps_id_select(apps)
        app_id = [key for key in apps.keys() if apps[key]['spec']['name'] == app_name][0]

    if not app_id in apps.keys():
        echo_stdout(OutResultError(TextError.error_application_id(app_id)))
        app_exit()

    if not arch:
        arch = prompt_apps_arch_select(apps, app_id)

    model_psdk = cli_psdk_tool_select_model_psdk(False, None)
    model_keys = cli_psdk_tool_select_model_sign(False if index_sign else True, index_sign)

    build = [build for build in apps[app_id]['versions'] if build['arch'] == arch]

    if not build:
        echo_stdout(OutResultError(TextError.error_application_arch(arch)))
        app_exit()

    is_apm = build[0]['psdk'][0] == '5'
    is_emulator = True if 'x86_64' in arch else False

    if is_emulator:
        model = cli_emulator_tool_select_model(is_root=True)
        file = apps_download_common(app_id, arch)
        psdk_package_sign_common(model_psdk, model_keys, phrase, [str(file)])
        emulator_package_install_common(model, str(file), is_apm, is_apm)
    else:
        model = cli_device_tool_select_model(False if index_device else True, index_device)
        file = apps_download_common(app_id, arch)
        psdk_package_sign_common(model_psdk, model_keys, phrase, [str(file)])
        device_package_install_common(model, str(file), is_apm, is_apm)

    echo_verbose(verbose)
