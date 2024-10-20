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
from aurora_cli.src.base.common.groups.app.app_features import (
    app_info_common,
    app_versions_common,
    app_auth_check_common,
    app_auth_password_common
)
from aurora_cli.src.base.models.psdk_model import PsdkModel
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.cache_func import cache_func_clear
from aurora_cli.src.base.utils.output import echo_stdout, OutResult
from aurora_cli.src.base.utils.route import get_route_root, get_arg_str, get_arg_str_optional


def search_route_app(route: str) -> bool:
    root = get_route_root(route)
    if root == '/app/info':
        echo_stdout(app_info_common())
    elif root == '/app/clear':
        cache_func_clear()
        echo_stdout(OutResult(TextInfo.cache_clear()))
    elif root == '/app/versions':
        echo_stdout(app_versions_common())
    elif root == '/app/auth/check':
        version = get_arg_str_optional(route, 'version')
        model = PsdkModel.get_model_by_version(version) if version else None
        echo_stdout(app_auth_check_common(model))
    elif root == '/app/auth/root':
        echo_stdout(app_auth_password_common(get_arg_str(route, 'password')))
    else:
        return False

    return True
