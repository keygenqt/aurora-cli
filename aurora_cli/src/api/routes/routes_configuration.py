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

from aurora_cli.src.base.constants.config import CONFIG_PATH
from aurora_cli.src.base.utils.output import echo_stdout, OutResult
from aurora_cli.src.base.utils.path import path_convert_relative
from aurora_cli.src.base.utils.route import get_route_root


def search_route_configuration(route: str) -> bool:
    root = get_route_root(route)
    if root == '/configuration/path':
        echo_stdout(OutResult(value='{}'.format(path_convert_relative(CONFIG_PATH))))
    else:
        return False

    return True
