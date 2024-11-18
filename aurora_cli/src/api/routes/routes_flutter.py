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

from pathlib import Path

from aurora_cli.src.base.common.groups.flutter.flutter_features import (
    flutter_available_common,
    flutter_installed_common,
    flutter_install_common,
    flutter_remove_common,
)
from aurora_cli.src.base.common.groups.flutter.flutter_project_features import (
    flutter_project_report_common,
    flutter_project_format_common,
    flutter_project_icons_common,
    flutter_project_check_format_common,
)
from aurora_cli.src.base.models.flutter_model import FlutterModel
from aurora_cli.src.base.utils.route import get_route_root, get_arg_str


def search_route_flutter(route: str) -> bool:
    root = get_route_root(route)
    if root == '/flutter/available':
        flutter_available_common()
    elif root == '/flutter/installed':
        flutter_installed_common()
    elif root == '/flutter/install':
        flutter_install_common(
            version=get_arg_str(route, 'version'),
            is_bar=False
        )
    elif root == '/flutter/remove':
        flutter_remove_common(
            model=FlutterModel.get_model_by_version(get_arg_str(route, 'version')),
        )
    elif root == '/flutter/project/format':
        flutter_project_format_common(
            project=Path(get_arg_str(route, 'path')),
            is_bar=False,
            model=FlutterModel.get_model_by_version(get_arg_str(route, 'version')),
        )
    elif root == '/flutter/project/check-format':
        flutter_project_check_format_common(
            project=Path(get_arg_str(route, 'path')),
            is_bar=False,
            model=FlutterModel.get_model_by_version(get_arg_str(route, 'version')),
        )
    elif root == '/flutter/project/report':
        flutter_project_report_common(
            project=Path(get_arg_str(route, 'path')),
            is_bar=False,
            model=FlutterModel.get_model_by_version(get_arg_str(route, 'version')),
        )
    elif root == '/flutter/project/icons':
        flutter_project_icons_common(
            project=Path(get_arg_str(route, 'path')),
            image=Path(get_arg_str(route, 'image')),
        )
    else:
        return False

    return True
