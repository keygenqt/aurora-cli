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

from aurora_cli.src.base.common.groups.psdk.psdk_features import (
    psdk_available_common,
    psdk_installed_common,
    psdk_install_common,
    psdk_remove_common,
    psdk_targets_common,
    psdk_clear_common,
)
from aurora_cli.src.base.common.groups.psdk.psdk_package_features import (
    psdk_package_search_common,
    psdk_package_install_common,
    psdk_package_remove_common,
    psdk_package_validate_common,
    psdk_package_sign_common,
)
from aurora_cli.src.base.common.groups.psdk.psdk_project_features import (
    psdk_project_format_common,
    psdk_project_debug_common,
    psdk_project_build_common,
    psdk_project_icons_common
)
from aurora_cli.src.base.common.groups.psdk.psdk_sudoers_features import (
    psdk_sudoers_add_common,
    psdk_sudoers_remove_common
)
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.models.psdk_model import PsdkModel
from aurora_cli.src.base.models.sign_model import SignModel
from aurora_cli.src.base.utils.route import get_route_root, get_arg_str, get_arg_str_optional, get_arg_bool


def search_route_psdk(route: str) -> bool:
    match get_route_root(route):
        case '/psdk/available':
            psdk_available_common()
        case '/psdk/installed':
            psdk_installed_common()
        case '/psdk/targets':
            psdk_targets_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
            )
        case '/psdk/install':
            psdk_install_common(
                version=get_arg_str(route, 'version'),
                is_bar=False
            )
        case '/psdk/remove':
            psdk_remove_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
            )
        case '/psdk/clear':
            psdk_clear_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
                target=get_arg_str(route, 'target'),
            )
        case '/psdk/sudoers/add':
            psdk_sudoers_add_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
            )
        case '/psdk/sudoers/remove':
            psdk_sudoers_remove_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
            )
        case '/psdk/package/search':
            psdk_package_search_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
                target=get_arg_str(route, 'target'),
                package=get_arg_str(route, 'package'),
            )
        case '/psdk/package/install':
            psdk_package_install_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
                target=get_arg_str(route, 'target'),
                path=get_arg_str(route, 'path'),
            )
        case '/psdk/package/remove':
            psdk_package_remove_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
                target=get_arg_str(route, 'target'),
                package=get_arg_str(route, 'package'),
            )
        case '/psdk/package/validate':
            psdk_package_validate_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
                target=get_arg_str(route, 'target'),
                path=get_arg_str(route, 'path'),
                profile=get_arg_str(route, 'profile'),
            )
        case '/psdk/package/sign':
            psdk_package_sign_common(
                model_psdk=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
                model_keys=SignModel.get_model_by_name(get_arg_str_optional(route, 'name')),
                paths=[get_arg_str(route, 'path')],
                is_bar=False
            )
        case '/psdk/project/format':
            psdk_project_format_common(
                project=Path(get_arg_str(route, 'path')),
                is_bar=False
            )
        case '/psdk/project/build':
            model_device = None
            host = get_arg_str_optional(route, 'host')
            if host:
                model_device = DeviceModel.get_model_by_host(host)
            psdk_project_build_common(
                model_psdk=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
                model_device=model_device,
                model_keys=SignModel.get_model_by_name(get_arg_str_optional(route, 'name')),
                target=get_arg_str(route, 'target'),
                debug=get_arg_bool(route, 'debug'),
                clean=get_arg_bool(route, 'clean'),
                project=Path(get_arg_str(route, 'path')),
                is_apm=get_arg_bool(route, 'is_apm'),
                is_install=get_arg_bool(route, 'is_install'),
                is_run=get_arg_bool(route, 'is_run'),
                is_bar=False,
            )
        case '/psdk/project/debug':
            psdk_project_debug_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
                target=get_arg_str(route, 'target'),
                project=Path(get_arg_str(route, 'path')),
            )
        case '/psdk/project/icon':
            psdk_project_icons_common(
                project=Path(get_arg_str(route, 'path')),
                image=Path(get_arg_str(route, 'image')),
            )
        case _:
            return False
    return True
