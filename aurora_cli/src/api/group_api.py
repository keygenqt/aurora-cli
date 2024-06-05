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
import sys

import click

from aurora_cli.src.api.routes.routes_device import search_route_device
from aurora_cli.src.api.routes.routes_emulator import search_route_emulator
from aurora_cli.src.api.routes.routes_flutter import search_route_flutter
from aurora_cli.src.api.routes.routes_psdk import search_route_psdk
from aurora_cli.src.api.routes.routes_sdk import search_route_sdk
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError
from aurora_cli.src.base.utils.route import get_arg_bool


@click.group(name='api', invoke_without_command=True, help=TextGroup.group_api())
@click.option('--route', help='Route API', type=click.STRING, required=True)
@click.pass_context
def group_api(ctx: {}, route: str):
    if argv_is_test():
        sys.argv.append('api')
        ctx.obj = AppConfig.create_test()
    try:
        verbose = get_arg_bool(route, 'verbose')
        if search_route_device(route, verbose):
            return
        if search_route_emulator(route, verbose):
            return
        if search_route_flutter(route, verbose):
            return
        if search_route_psdk(route, verbose):
            return
        if search_route_sdk(route, verbose):
            return
        echo_stdout(OutResultError(TextError.route_not_found()))
    except Exception as e:
        echo_stdout(OutResultError(str(e)))
