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
    psdk_clear_common, psdk_info_common,
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
    root = get_route_root(route)
    if root == '/psdk/available':
        psdk_available_common()
    elif root == '/psdk/installed':
        psdk_installed_common()
    elif root == '/psdk/info':
        psdk_info_common(
            model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
        )
    elif root == '/psdk/targets':
        psdk_targets_common(
            model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
            password=get_arg_str_optional(route, 'password')
        )
    elif root == '/psdk/download':
        psdk_install_common(
            version=get_arg_str(route, 'version'),
            is_bar=False,
            mode='download',
        )
    elif root == '/psdk/install':
        psdk_install_common(
            version=get_arg_str(route, 'version'),
            is_bar=False,
            mode='install',
            password = get_arg_str_optional(route, 'password')
        )
    elif root == '/psdk/remove':
        psdk_remove_common(
            model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
            password = get_arg_str_optional(route, 'password')
        )
    elif root == '/psdk/clear':
        psdk_clear_common(
            target=get_arg_str(route, 'target'),
            model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
            password=get_arg_str_optional(route, 'password')
        )
    elif root == '/psdk/sudoers/add':
        psdk_sudoers_add_common(
            model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
            password=get_arg_str_optional(route, 'password')
        )
    elif root == '/psdk/sudoers/remove':
        psdk_sudoers_remove_common(
            model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
            password=get_arg_str_optional(route, 'password')
        )
    elif root == '/psdk/package/search':
        psdk_package_search_common(
            target=get_arg_str(route, 'target'),
            package=get_arg_str(route, 'package'),
            model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
        )
    elif root == '/psdk/package/install':
        psdk_package_install_common(
            target=get_arg_str(route, 'target'),
            path=get_arg_str(route, 'path'),
            model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
            password=get_arg_str_optional(route, 'password')
        )
    elif root == '/psdk/package/remove':
        psdk_package_remove_common(
            target=get_arg_str(route, 'target'),
            package=get_arg_str(route, 'package'),
            model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
            password=get_arg_str_optional(route, 'password')
        )
    elif root == '/psdk/package/validate':
        psdk_package_validate_common(
            target=get_arg_str(route, 'target'),
            path=get_arg_str(route, 'path'),
            profile=get_arg_str(route, 'profile'),
            model=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
        )
    elif root == '/psdk/package/sign':
        psdk_package_sign_common(
            paths=[get_arg_str(route, 'path')],
            is_bar=False,
            model_psdk=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
            model_keys=SignModel.get_model_by_name(get_arg_str_optional(route, 'key')),
            password = get_arg_str_optional(route, 'password')
        )
    elif root == '/psdk/project/format':
        psdk_project_format_common(
            project=Path(get_arg_str(route, 'path')),
            is_bar=False
        )
    elif root == '/psdk/project/build':
        model_device = None
        host = get_arg_str_optional(route, 'host')
        if host:
            model_device = DeviceModel.get_model_by_host(host)
        psdk_project_build_common(
            model_device=model_device,
            target=get_arg_str(route, 'target'),
            debug=get_arg_bool(route, 'debug'),
            clean=get_arg_bool(route, 'clean'),
            project=Path(get_arg_str(route, 'path')),
            is_apm=get_arg_bool(route, 'apm'),
            is_install=get_arg_bool(route, 'install'),
            is_run=get_arg_bool(route, 'run'),
            verbose=get_arg_bool(route, 'verbose'),
            is_bar=False,
            model_psdk=PsdkModel.get_model_by_version(get_arg_str(route, 'version')),
            model_keys=SignModel.get_model_by_name(get_arg_str_optional(route, 'key')),
        )
    elif root == '/psdk/project/icons':
        psdk_project_icons_common(
            project=Path(get_arg_str(route, 'path')),
            image=Path(get_arg_str(route, 'image')),
        )
    else:
        return False

    return True
