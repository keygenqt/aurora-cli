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

from aurora_cli.src.base.common.groups.vscode.vscode_features import (
    vscode_extensions_list_common,
    vscode_extensions_flutter_check_common,
    vscode_extensions_cpp_check_common,
    vscode_extensions_other_check_common, vscode_extensions_install, vscode_settings_common, vscode_version_common
)
from aurora_cli.src.base.utils.output import echo_stdout, OutResult
from aurora_cli.src.base.utils.route import get_route_root, get_arg_str


def search_route_vscode(route: str) -> bool:
    root = get_route_root(route)
    if root == '/vscode/info':
        echo_stdout(OutResult(value=vscode_version_common()))
    elif root == '/vscode/extensions/list':
        echo_stdout(OutResult(value=vscode_extensions_list_common()))
    elif root == '/vscode/extensions/install':
        vscode_extensions_install(extensions=[get_arg_str(route, 'extension')])
    elif root == '/vscode/settings/update':
        vscode_settings_common()
    else:
        return False

    return True
