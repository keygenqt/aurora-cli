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
from typing import Any
from urllib.parse import urlparse


def get_route_root(route: str) -> str:
    return route.split('?')[0]


def get_arg_bool(
        route: str,
        arg: str
) -> bool:
    try:
        return get_arg_str(route, arg).lower() == 'true'
    except (Exception,):
        return False


def get_arg_int(
        route: str,
        arg: str
) -> int:
    return int(get_arg_str(route, arg))


def get_arg_str(
        route: str,
        arg: str
) -> str:
    result = get_arg_str_optional(route, arg)
    if not result:
        raise Exception(f"Argument `{arg}` is required.")
    return result


def get_arg_int_optional(
        route: str,
        arg: str
) -> Any:
    value = get_arg_str_optional(route, arg)
    if value:
        return int(value)
    return value


def get_arg_str_optional(
        route: str,
        arg: str
) -> Any:
    result = None
    for arg_value in urlparse(route).query.split('&'):
        if f'{arg}=' in arg_value:
            result = arg_value.replace(f'{arg}=', '')
    return result
