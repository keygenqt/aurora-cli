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

from aurora_cli.src.api.routes.routes_device import search_route_device
from aurora_cli.src.api.routes.routes_emulator import search_route_emulator
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.output import echo_stdout, OutResultError
from aurora_cli.src.base.texts.error import TextError


@click.group(name='api', invoke_without_command=True)
@click.option('--route', help='Route API', type=click.STRING, required=True)
@click.option('--test', is_flag=True, default=False)
@click.pass_context
def group_api(ctx: {}, route: str, test: bool):
    """Application Programming Interface."""
    if test:
        ctx.obj = AppConfig.create_test(is_api=True)
    try:
        if search_route_emulator(route):
            return
        if search_route_device(route):
            return
        echo_stdout(OutResultError(TextError.route_not_found()))
    except Exception as e:
        echo_stdout(OutResultError(str(e)))
