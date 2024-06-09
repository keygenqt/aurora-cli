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

from aurora_cli.src.base.common.groups.psdk_features import (
    psdk_installed_common,
    psdk_available_common,
    psdk_install_common,
    psdk_sign_common,
    psdk_remove_common,
    psdk_clear_common,
    psdk_package_search_common,
    psdk_package_install_common,
    psdk_package_remove_common,
    psdk_sudoers_add_common,
    psdk_sudoers_remove_common,
    psdk_targets_common,
    psdk_validate_common
)
from aurora_cli.src.base.models.psdk_model import PsdkModel
from aurora_cli.src.base.models.sign_model import SignModel
from aurora_cli.src.base.utils.route import get_route_root, get_arg_str, get_arg_str_optional


def search_route_psdk(route: str, verbose: bool) -> bool:
    match get_route_root(route):
        case '/psdk/available':
            psdk_available_common(verbose)
        case '/psdk/installed':
            psdk_installed_common(verbose)
        case '/psdk/install':
            psdk_install_common(
                version=get_arg_str(route, 'version'),
                verbose=verbose,
                is_bar=False
            )
        case '/psdk/remove':
            psdk_remove_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                verbose=verbose
            )
        case '/psdk/clear':
            psdk_clear_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                verbose=verbose
            )
        case '/psdk/package/search':
            psdk_package_search_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                package=get_arg_str(route, 'package'),
                verbose=verbose
            )
        case '/psdk/package/install':
            psdk_package_install_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                path=[get_arg_str(route, 'path')],
                verbose=verbose
            )
        case '/psdk/package/remove':
            psdk_package_remove_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                package=get_arg_str(route, 'package'),
                verbose=verbose
            )
        case '/psdk/sign':
            psdk_sign_common(
                model_psdk=PsdkModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                model_keys=SignModel.get_model_by_name(get_arg_str_optional(route, 'name')),
                paths=[get_arg_str(route, 'path')],
                verbose=verbose,
                is_bar=False
            )
        case '/psdk/sudoers/add':
            psdk_sudoers_add_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                verbose=verbose
            )
        case '/psdk/sudoers/remove':
            psdk_sudoers_remove_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                verbose=verbose
            )
        case '/psdk/targets':
            psdk_targets_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                verbose=verbose
            )
        case '/psdk/validate':
            psdk_validate_common(
                model=PsdkModel.get_model_by_version(get_arg_str(route, 'version'), verbose),
                path=[get_arg_str(route, 'path')],
                profile=get_arg_str(route, 'profile'),
                verbose=verbose
            )
        case _:
            return False
    return True
