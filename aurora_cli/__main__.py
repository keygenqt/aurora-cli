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

from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.constants.app import APP_NAME, APP_VERSION
from aurora_cli.src.base.localization.localization import localization_help, localization_usage_error
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.app import app_crash_out
from aurora_cli.src.base.utils.capturing_std import CapturingStderr, CapturingStdout
from aurora_cli.src.base.utils.click import click_init_groups
from aurora_cli.src.base.utils.disk_cache import disk_cache_clear
from aurora_cli.src.base.utils.output import echo_stdout
from aurora_cli.src.cli.group_abort import clear_after_force_close


@click.group(invoke_without_command=True, help=TextGroup.group_main())
@click.version_option(version=APP_VERSION, prog_name=APP_NAME)
@click.option('--config', help=TextArgument.argument_config(), type=click.STRING, required=False)
@click.option('--clear-cache', is_flag=True, help=TextArgument.argument_clear_cache())
@click.pass_context
def main(ctx: {}, config: str, clear_cache: bool):
    ctx.obj = AppConfig.create(config)

    if clear_cache:
        disk_cache_clear()
        echo_stdout(TextInfo.cache_clear())
        exit(0)

    if not ctx.invoked_subcommand:
        localization_help(ctx.get_help())


if __name__ == '__main__':
    try:
        click_init_groups(main)
        try:
            with CapturingStdout(arg='--help', callback=localization_help):
                main(standalone_mode=False)
        except click.exceptions.UsageError:
            with CapturingStderr(callback=localization_usage_error):
                main()
        except click.exceptions.Abort:
            clear_after_force_close()
    except Exception as e:
        app_crash_out(e)
