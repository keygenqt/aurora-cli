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

from aurora_cli.src.api.routes.device_route import search_route_device
from aurora_cli.src.api.routes.emulator_route import search_route_emulator
from aurora_cli.src.base.output import echo_stdout_json, OutResultError
from aurora_cli.src.base.texts.error import TextError


def group_api(route: str):
    try:
        if search_route_emulator(route):
            return
        if search_route_device(route):
            return
        echo_stdout_json(OutResultError(TextError.route_not_found()))
    except Exception as e:
        echo_stdout_json(OutResultError(str(e)))
