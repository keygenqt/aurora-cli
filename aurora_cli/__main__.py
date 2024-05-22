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

from aurora_cli.src.api.routes.group_api import group_api
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.constants.app import APP_NAME, APP_VERSION, APP_INFO
from aurora_cli.src.cli.device import group_device
from aurora_cli.src.cli.emulator import group_emulator


@click.group(invoke_without_command=True)
@click.version_option(version=APP_VERSION, prog_name=APP_NAME)
@click.option('--config', help='Specify config path.', type=click.STRING, required=False)
@click.option('--api', default=None, help='Application Programming Interface.', type=click.STRING, required=False)
@click.pass_context
def main(ctx: {}, config: str, api: str | None):
    f"""{APP_INFO}"""

    ctx.obj = AppConfig.create(config, api is not None)
    if api:
        group_api(api)
    else:
        if not ctx.invoked_subcommand:
            print(ctx.get_help())


# new
main.add_command(group_emulator)
main.add_command(group_device)

if __name__ == '__main__':
    main()
