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

from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.output import OutResult, OutResultError, OutResultInfo
from aurora_cli.src.base.utils.shell import shell_exec_command


def shell_dart_format(
        dart: str,
        path: str,
) -> OutResult:
    stdout, stderr = shell_exec_command([
        dart,
        'format',
        '--line-length=120',
        path,
    ])
    if stdout and 'Could not format' in stdout[0]:
        return OutResultError(TextError.flutter_project_format_error())
    return OutResult()


@check_dependency(DependencyApps.clang_format)
def shell_cpp_format(
        files: [Path],
        config: Path,
) -> OutResult:
    for file in files:
        _, stderr = shell_exec_command([
            'clang-format',
            f'--style=file:{config}',
            '-i',
            str(file)
        ])
        if stderr:
            return OutResultError(TextError.flutter_project_format_error())
    return OutResult()


def shell_psdk_resign(
        tool: str,
        key: str,
        cert: str,
        paths: [str],
) -> OutResult:
    is_error = False
    for path in paths:
        shell_exec_command([
            tool,
            'rpmsign-external',
            'delete',
            path
        ])
        _, stderr = shell_exec_command([
            tool,
            'rpmsign-external',
            'sign',
            f'--key={key}',
            f'--cert={cert}',
            path
        ])
        if stderr:
            is_error = True

    if is_error:
        return OutResultError(TextError.psdk_sign_error())

    return OutResult()


def shell_psdk_targets(version: str, tool: str) -> OutResult:
    targets = []
    stdout, stderr = shell_exec_command([
        tool,
        'sdk-assistant',
        'list',
    ])

    if stderr:
        return OutResultError(TextError.psdk_targets_get_error())

    for line in stdout:
        if '─' in line and 'default' not in line:
            targets.append(line[2:])

    if not targets:
        return OutResultInfo(TextInfo.psdk_targets_empty_success(version))

    return OutResult(TextSuccess.psdk_targets_get_success(version, targets), value=targets)
