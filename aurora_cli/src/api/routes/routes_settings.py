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
from aurora_cli.src.base.common.groups.settings.settings_features import (
    settings_list_common,
    settings_clear_common,
    settings_localization_common,
    settings_verbose_common,
    settings_select_common,
    settings_hint_common
)
from aurora_cli.src.base.utils.route import get_route_root, get_arg_str, get_arg_bool


def search_route_settings(route: str) -> bool:
    root = get_route_root(route)
    if root == '/settings/list':
        settings_list_common()
    elif root == '/settings/clear':
        settings_clear_common()
    elif root == '/settings/localization':
        language = get_arg_str(route, 'language')
        if 'ru' in language:
            language = 'ru'
        else:
            language = 'en'
        settings_localization_common(language)
    elif root == '/settings/verbose':
        settings_verbose_common(get_arg_bool(route, 'enable'))
    elif root == '/settings/select':
        settings_select_common(get_arg_bool(route, 'enable'))
    elif root == '/settings/hint':
        settings_hint_common(get_arg_bool(route, 'enable'))
    else:
        return False

    return True
