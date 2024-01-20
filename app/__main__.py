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

from app.src.base.helper import get_app_name, get_app_version
from app.src.base.conf import Conf

from app.src.features.device.group_device import group_device
from app.src.features.embedder.group_embedder import group_embedder
from app.src.features.flutter.group_flutter import group_flutter
from app.src.features.sdk.group_psdk import group_psdk
from app.src.features.sdk.group_sdk import group_sdk


@click.group()
@click.version_option(version=get_app_version(), prog_name=get_app_name())
@click.option('--conf', '-c', default=None, help='Specify config path.', type=click.STRING, required=False)
@click.pass_context
def main(ctx, conf):
    ctx.obj = Conf(conf)


main.add_command(group_sdk)
main.add_command(group_psdk)
main.add_command(group_flutter)
main.add_command(group_embedder)
main.add_command(group_device)

if __name__ == '__main__':
    main()
