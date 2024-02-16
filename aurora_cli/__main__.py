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

from aurora_cli.src.support.dependency_required import check_dependency_init

check_dependency_init()

from aurora_cli.src.features.devices.group_device import group_device  # noqa: E402
from aurora_cli.src.features.devices.group_emulator import group_emulator  # noqa: E402
from aurora_cli.src.features.flutter.group_flutter import group_flutter  # noqa: E402
from aurora_cli.src.features.psdk.group_psdk import group_psdk  # noqa: E402
from aurora_cli.src.features.sdk.group_sdk import group_sdk  # noqa: E402
from aurora_cli.src.support.conf import Conf  # noqa: E402


@click.group(invoke_without_command=True)
@click.version_option(version=Conf.get_app_version(), prog_name=Conf.get_app_name())
@click.option('--conf', '-c', default=None, help='Specify config path.', type=click.STRING, required=False)
@click.pass_context
def main(ctx: {}, conf: {}):
    ctx.obj = Conf(conf)
    if not ctx.invoked_subcommand:
        print(ctx.get_help())


main.add_command(group_sdk)
main.add_command(group_psdk)
main.add_command(group_device)
main.add_command(group_flutter)
main.add_command(group_emulator)

if __name__ == '__main__':
    main()
