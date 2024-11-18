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
from typing import Callable

from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.output import OutResult
from aurora_cli.src.base.utils.percent_cli import percent_point, percent_start, percent_end
from aurora_cli.src.base.utils.shell import shell_exec_command, shell_check_error_out


def flutter_project_get_pub(
        flutter: str,
        path: Path,
        progress: Callable[[int], None]
) -> OutResult:
    percents = []
    percent_start(percents, progress)
    points = [
        'Resolving dependencies',
        'Got dependencies',
    ]
    stdout, stderr = shell_exec_command(
        [
            flutter,
            'pub',
            'get',
        ],
        cwd=path,
        listen=lambda out: percent_point(out, points, percents, progress),
        disable_sigint=False
    )

    percent_end(percents, progress)

    result = shell_check_error_out(stdout, stderr, ['crash', 'unknown revision'])
    if result.is_error():
        return result

    return OutResult(TextSuccess.flutter_get_pub_success())
