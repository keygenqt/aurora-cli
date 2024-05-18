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
from urllib.parse import urlparse

from aurora_cli.src.api.emulator.commands import command_start, command_screenshot
from aurora_cli.src.base.common.texts.error import TextError
from aurora_cli.src.base.output import echo_stdout_json, Out404


def get_route_root(route: str) -> str:
    return route.split('?')[0]


def get_route_arg(route: str, arg: str) -> str:
    return urlparse(route).query.replace(f'{arg}=', '')


def group_api(route: str):
    match get_route_root(route):
        case '/emulator/start':
            command_start(get_route_arg(route, 'verbose').lower() == 'true')
        case '/emulator/screenshot':
            command_screenshot(get_route_arg(route, 'verbose').lower() == 'true')
        case _:
            echo_stdout_json(Out404(TextError.route_not_found()))
