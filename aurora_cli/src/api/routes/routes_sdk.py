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

from aurora_cli.src.base.common.groups.sdk.sdk_features import (
    sdk_available_common,
    sdk_installed_common,
    sdk_install_common,
    sdk_tool_common
)
from aurora_cli.src.base.models.sdk_model import SdkModel
from aurora_cli.src.base.utils.route import get_route_root, get_arg_bool, get_arg_str


def search_route_sdk(route: str) -> bool:
    root = get_route_root(route)
    if root == '/sdk/available':
        sdk_available_common()
    elif root == '/sdk/installed':
        sdk_installed_common()
    elif root == '/sdk/install':
        sdk_install_common(
            version=get_arg_str(route, 'version'),
            offline=get_arg_bool(route, 'offline'),
            is_bar=False
        )
    elif root == '/sdk/tool':
        sdk_tool_common(SdkModel.get_model())
    else:
        return False

    return True
