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
from time import sleep

from aurora_cli.src.base.utils.output import echo_stdout, OutResult, OutResultInfo, OutResultError
from aurora_cli.src.base.utils.route import get_route_root, get_arg_int_optional


def search_route_tests(route: str) -> bool:
    root = get_route_root(route)
    if root == '/tests/answer':
        time = get_arg_int_optional(route, 'time')
        code = get_arg_int_optional(route, 'code')
        iterate = get_arg_int_optional(route, 'iterate')
        if not iterate:
            iterate = 1
        for x in range(iterate):
            if time:
                sleep(time/1000)
            if code == 100:
                echo_stdout(OutResultInfo('Test answer', value={}))
            elif code == 500:
                echo_stdout(OutResultError('Test answer', value={}))
            else:
                echo_stdout(OutResult('Test answer', value={}))
    else:
        return False

    return True
