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
    flutter_add_custom_devices_common,
)
from aurora_cli.src.base.common.groups.flutter.flutter_project_features import (
    flutter_project_report_common,
    flutter_project_format_common,
    flutter_project_build_common,
    flutter_project_icons_common,
)
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.models.flutter_model import FlutterModel
from aurora_cli.src.base.models.psdk_model import PsdkModel
from aurora_cli.src.base.models.sign_model import SignModel
from aurora_cli.src.base.utils.route import get_route_root, get_arg_str, get_arg_str_optional, get_arg_bool


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
    elif root == '/flutter/custom-devices':
        flutter_add_custom_devices_common(
            model=FlutterModel.get_model_by_version(get_arg_str(route, 'version')),
        )
    elif root == '/flutter/project/format':
        flutter_project_format_common(
            project=Path(get_arg_str(route, 'path')),
            is_bar=False,
            model=FlutterModel.get_model_by_version(get_arg_str(route, 'version')),
        )
    elif root == '/flutter/project/build':
        model_device = None
        host = get_arg_str_optional(route, 'host')
        if host:
            model_device = DeviceModel.get_model_by_host(host)
        flutter_project_build_common(
            model_device=model_device,
            target=get_arg_str(route, 'target'),
            debug=get_arg_bool(route, 'debug'),
            clean=get_arg_bool(route, 'clean'),
            pub_get=get_arg_bool(route, 'pub_get'),
            build_runner=get_arg_bool(route, 'build_runner'),
            run_mode=get_arg_str_optional(route, 'run_mode'),
            project=Path(get_arg_str(route, 'path')),
            is_apm=get_arg_bool(route, 'apm'),
            is_install=get_arg_bool(route, 'install'),
            verbose=get_arg_bool(route, 'verbose'),
            is_bar=False,
            model_flutter=FlutterModel.get_model_by_version(get_arg_str(route, 'version')),
            model_psdk=PsdkModel.get_model_by_version(get_arg_str(route, 'psdk')),
            model_keys=SignModel.get_model_by_name(get_arg_str_optional(route, 'key')),
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
