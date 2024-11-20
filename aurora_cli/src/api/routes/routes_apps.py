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

from aurora_cli.src.base.common.groups.apps.apps_features import apps_available_common, apps_download_common
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.output import echo_stdout, OutResult
from aurora_cli.src.base.utils.route import get_route_root, get_arg_str_optional


def search_route_apps(route: str) -> bool:
    root = get_route_root(route)
    if root == '/apps/available':
        apps_available_common(
            search=get_arg_str_optional(route, 'search'),
            group=get_arg_str_optional(route, 'group'),
        )
    elif root == '/apps/download':
        echo_stdout(OutResult(TextSuccess.download_success(), value=str(apps_download_common(
            app_id=get_arg_str_optional(route, 'app_id'),
            arch=get_arg_str_optional(route, 'arch'),
        ))))
    else:
        return False

    return True
