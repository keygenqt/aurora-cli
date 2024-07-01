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

from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.percent_cli import percent_point, percent_counter, percent_start, percent_end
from aurora_cli.src.base.utils.shell import shell_exec_command, shell_check_error_out


def flutter_project_clear(
        flutter: str,
        path: Path,
        progress: Callable[[int], None]
) -> OutResult:
    percents = []
    percent_start(percents, progress)

    stdout, stderr = shell_exec_command([
        flutter,
        'clean',
    ], cwd=path, disable_sigint=False)

    percent_end(percents, progress)

    result = shell_check_error_out(stdout, stderr, ['crash'])
    if result.is_error():
        return result

    return OutResult(TextSuccess.flutter_clear_success())


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


def flutter_project_run_build_runner(
        flutter: str,
        path: Path,
        progress: Callable[[int], None]
) -> OutResult:
    percents = []
    percent_start(percents, progress)

    stdout, stderr = shell_exec_command(
        [
            flutter,
            'pub',
            'run',
            'build_runner',
            'build',
            '--delete-conflicting-outputs',
        ],
        cwd=path,
        listen=lambda _: percent_counter(25, percents, progress),
        disable_sigint=False
    )

    percent_end(percents, progress)

    result = shell_check_error_out(stdout, stderr, ['crash'])
    if result.is_error():
        return result

    return OutResult(TextSuccess.flutter_run_build_runner_success())


def flutter_project_build(
        psdk_dir: str,
        target: str,
        flutter: str,
        debug: bool,
        path: Path,
        progress: Callable[[int], None]
) -> OutResult:
    percents = []
    percent_start(percents, progress)
    points = [
        'Building Aurora application',
        'Mounting system directories',
        'Loading repository data',
        'Building target platforms',
        'Build files have been written',
        'Executing(%install)',
        'Install configuration',
        'Checking for unpackaged',
        'rpmlint session starts',
        'Result',
    ]

    def get_platform() -> str:
        if 'aarch64' in target:
            return 'aurora-arm64'
        if 'x86_64' in target:
            return 'aurora-x64'
        return 'aurora-arm'

    mode = 'debug' if debug else 'release'

    stdout, _ = shell_exec_command([
        flutter,
        'build',
        'aurora',
        f'--psdk-dir={psdk_dir}',
        f'--target-platform={get_platform()}',
        f'--{mode}',
    ], cwd=path, listen=lambda out: percent_point(out, points, percents, progress), disable_sigint=False)

    percent_end(percents, progress)

    result = shell_check_error_out(stdout, None, ['crash'])
    if result.is_error():
        return result

    builds = []
    for line in stdout:
        if '│ ' in line:
            builds.append(line.strip('│').replace(' ', ''))

    builds_paths = []
    for i, build in enumerate(builds):
        if './build' in build:
            builds_paths.append(build.replace('./build', f'{path}/build'))
        else:
            builds_paths[-1] += build

    if not builds_paths:
        return OutResultError(TextError.exec_command_error(), value=-1)

    builds_paths.sort()
    builds_paths.reverse()

    return OutResult(TextSuccess.flutter_build_success(builds_paths), value=builds_paths)


def flutter_enable_custom_device(flutter: str):
    stdout, stderr = shell_exec_command([flutter, 'config', '--enable-custom-devices'])
    result = shell_check_error_out(stdout)
    if result.is_error():
        return result
    return OutResult(TextSuccess.flutter_enable_custom_device_success())
