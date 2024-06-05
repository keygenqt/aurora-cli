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
from aurora_cli.src.base.common.groups.psdk_features import psdk_installed_common, psdk_available_common
from aurora_cli.src.base.utils.route import get_route_root, get_arg_bool


def search_route_psdk(route: str) -> bool:
    match get_route_root(route):
        case '/psdk/available':
            psdk_available_common(
                verbose=get_arg_bool(route, 'verbose')
            )
        case '/psdk/installed':
            psdk_installed_common(
                verbose=get_arg_bool(route, 'verbose')
            )
        case _:
            return False
    return True
