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

from aurora_cli.src.api.group_api import group_api
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.constants.app import APP_NAME, APP_VERSION
from aurora_cli.src.base.localization.localization import localization_app, localization_abort
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.app import app_crash_handler, app_help_handler, app_abort_handler
from aurora_cli.src.base.utils.argv import argv_is_verbose

from aurora_cli.src.base.utils.cache_func import cache_func_clear
from aurora_cli.src.base.utils.output import echo_stdout, echo_verbose, OutResult
from aurora_cli.src.cli.device.group_device import group_device, init_subgroups_device
from aurora_cli.src.cli.emulator.group_emulator import group_emulator, init_subgroups_emulator
from aurora_cli.src.cli.flutter.group_flutter import group_flutter, init_subgroups_flutter
from aurora_cli.src.cli.psdk.group_psdk import group_psdk, init_subgroups_psdk
from aurora_cli.src.cli.sdk.group_sdk import group_sdk
from aurora_cli.src.cli.settings.group_settings import group_settings
from aurora_cli.src.cli.vscode.group_vscode import group_vscode


@click.group(invoke_without_command=True, help=TextGroup.group_main())
@click.version_option(version=APP_VERSION, prog_name=APP_NAME)
@click.option('--config', help=TextArgument.argument_config(), type=click.STRING, required=False)
@click.option('--clear-cache', is_flag=True, help=TextArgument.argument_clear_cache())
@click.pass_context
def main(
        ctx: {},
        config: str,
        clear_cache: bool
):
    ctx.obj = AppConfig.create(config)

    if clear_cache:
        cache_func_clear()
        echo_stdout(OutResult(TextInfo.cache_clear()))
        exit(0)

    if not ctx.invoked_subcommand:
        localization_app(ctx.get_help())


# noinspection PyTypeChecker
def _init_groups():
    # group API
    main.add_command(group_api)
    # group Devices via ssh
    main.add_command(group_device)
    init_subgroups_device()
    # group Emulator VM
    main.add_command(group_emulator)
    init_subgroups_emulator()
    # group Flutter SDK
    main.add_command(group_flutter)
    init_subgroups_flutter()
    # group Aurora Platform SDK
    main.add_command(group_psdk)
    init_subgroups_psdk()
    # group Aurora SDK
    main.add_command(group_sdk)
    # group Settings
    main.add_command(group_settings)
    # group Visual Studio Code
    main.add_command(group_vscode)


# Init app commands
_init_groups()

# Catch traceback
app_crash_handler(lambda exception: echo_verbose(argv_is_verbose(), exception))
# Catch help for localization
app_help_handler(lambda out: localization_app(out))
# Catch abort
app_abort_handler(lambda: localization_abort(is_exit=True))

if __name__ == '__main__':
    main()
