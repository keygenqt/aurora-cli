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

from aurora_cli.src.base.common.groups.flutter_features import (
    flutter_available_common,
    flutter_installed_common,
    flutter_install_common,
    flutter_remove_common,
    flutter_project_report_common,
    flutter_project_format_common,
    flutter_project_build_common,
    flutter_project_debug_common,
)
from aurora_cli.src.base.models.flutter_model import FlutterModel
from aurora_cli.src.base.utils.route import get_route_root, get_arg_str


def search_route_flutter(route: str, verbose: bool) -> bool:
    match get_route_root(route):
        case '/flutter/available':
            flutter_available_common(verbose)
        case '/flutter/installed':
            flutter_installed_common(verbose)
        case '/flutter/install':
            flutter_install_common(
                version=get_arg_str(route, 'version'),
                verbose=verbose,
                is_bar=False
            )
        case '/flutter/remove':
            flutter_remove_common(
                model=FlutterModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                verbose=verbose
            )
        case '/flutter/project/report':
            flutter_project_report_common(
                project=Path(get_arg_str(route, 'path')),
                verbose=verbose
            )
        case '/flutter/project/format':
            flutter_project_format_common(
                model=FlutterModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                project=Path(get_arg_str(route, 'path')),
                verbose=verbose
            )
        case '/flutter/project/build':
            flutter_project_build_common(
                model=FlutterModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                project=Path(get_arg_str(route, 'path')),
                verbose=verbose
            )
        case '/flutter/project/debug':
            flutter_project_debug_common(
                model=FlutterModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                project=Path(get_arg_str(route, 'path')),
                verbose=verbose
            )
        case _:
            return False
    return True
