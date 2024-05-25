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
from aurora_cli.src.base.constants.app import APP_NAME, APP_VERSION, APP_INFO
from aurora_cli.src.base.utils.app import app_init_groups, app_crash_out
from aurora_cli.src.cli.group_abort import clear_after_force_close


@click.group(invoke_without_command=True)
@click.version_option(version=APP_VERSION, prog_name=APP_NAME)
@click.option('--config', help='Specify config path.', type=click.STRING, required=False)
@click.pass_context
def main(ctx: {}, config: str):
    f"""{APP_INFO}"""
    ctx.obj = AppConfig.create(config)
    if not ctx.invoked_subcommand:
        print(ctx.get_help())


if __name__ == '__main__':
    try:
        app_init_groups(main)
        try:
            main(standalone_mode=False)
        except click.exceptions.UsageError:
            main()
        except click.exceptions.Abort:
            clear_after_force_close()
    except Exception as e:
        app_crash_out(e)
