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
from aurora_cli.src.base.constants.app import APP_NAME, APP_VERSION, APP_INFO
from aurora_cli.src.cli.group_abort import abort
from aurora_cli.src.cli.group_device import group_device
from aurora_cli.src.cli.group_emulator import group_emulator


# @todo
# tab
# ru localisation
@click.group(invoke_without_command=True)
@click.version_option(version=APP_VERSION, prog_name=APP_NAME)
@click.option('--config', help='Specify config path.', type=click.STRING, required=False)
@click.pass_context
def main(ctx: {}, config: str):
    f"""{APP_INFO}"""
    ctx.obj = AppConfig.create(config, ctx.invoked_subcommand == 'api')
    if not ctx.invoked_subcommand:
        print(ctx.get_help())


# noinspection PyTypeChecker
main.add_command(group_api)
# noinspection PyTypeChecker
main.add_command(group_emulator)
# noinspection PyTypeChecker
main.add_command(group_device)

if __name__ == '__main__':
    try:
        try:
            # Run app
            main(standalone_mode=False)
        except click.exceptions.UsageError:
            # Show error usage
            main()
        except click.exceptions.Abort:
            # Cleaning up after the application
            abort(standalone_mode=False)
    except (Exception,):
        print(click.style('An unexpected error occurred in the application.', fg='red'))
