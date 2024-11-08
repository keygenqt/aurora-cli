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
)
from aurora_cli.src.base.common.groups.device.device_package_features import device_package_install_common
from aurora_cli.src.base.common.groups.emulator.emulator_package_features import emulator_package_install_common
from aurora_cli.src.base.common.groups.psdk.psdk_package_features import psdk_package_sign_common
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.output import echo_verbose
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
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def available(verbose: bool):
    apps_available_common()
    echo_verbose(verbose)


@group_apps.command(name='install', help=TextCommand.command_flutter_install())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def install(
        verbose: bool
):
    app_name = prompt_apps_id_select()
    app_id = app_name.split('(')[-1].strip(')')
    app_arch = prompt_apps_arch_select(app_id)

    if app_arch == 'x86_64':
        model = cli_emulator_tool_select_model(is_root=True)
    else:
        model = cli_device_tool_select_model(True, None)

    model_psdk = cli_psdk_tool_select_model_psdk(False, None)
    model_keys = cli_psdk_tool_select_model_sign(False, None)

    file = apps_download_common(app_id, app_arch)
    psdk_package_sign_common(model_psdk, model_keys, None, [str(file)])

    if app_arch == 'x86_64':
        emulator_package_install_common(model, str(file), True, True)
    else:
        device_package_install_common(model, str(file), True, True)

    echo_verbose(verbose)
