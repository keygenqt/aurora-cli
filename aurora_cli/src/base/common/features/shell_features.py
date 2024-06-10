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


def shell_dart_format(dart: str, path: str) -> OutResult:
    stdout, stderr = shell_exec_command([
        dart,
        'format',
        '--line-length=120',
        path,
    ])
    if stdout and 'Could not format' in stdout[0]:
        return OutResultError(TextError.flutter_project_format_error())

    return OutResultInfo(TextInfo.flutter_project_format_dart_done())


@check_dependency(DependencyApps.clang_format)
def shell_cpp_format(files: [Path], config: Path) -> OutResult:
    for file in files:
        _, stderr = shell_exec_command([
            'clang-format',
            f'--style=file:{config}',
            '-i',
            str(file)
        ])
        if stderr:
            return OutResultError(TextError.flutter_project_format_error())

    return OutResultInfo(TextInfo.flutter_project_format_cpp_done())


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
        return OutResultInfo(TextInfo.psdk_targets_empty(version))

    return OutResult(TextSuccess.psdk_targets_get_success(version, targets), value=targets)


def shell_psdk_snapshot_remove(tool: str, target: str) -> OutResult:
    stdout, stderr = shell_exec_command([
        tool,
        'sdk-assistant',
        'target',
        'remove',
        '-y',
        '--snapshots-of',
        target
    ])
    if stderr:
        return OutResultError(TextError.exec_command_error())
    else:
        for line in stdout:
            if 'No such target' in line:
                return OutResultError(TextError.exec_command_error())

    return OutResult(TextSuccess.psdk_snapshot_remove_success())


def shell_psdk_package_search(
        tool: str,
        target: str,
        package: str,
) -> OutResult:
    stdout, stderr = shell_exec_command([
        tool,
        'sb2',
        '-t',
        target,
        '-R',
        'zypper',
        'search',
        '--installed-only',
        '-s',
        package
    ])
    if stderr:
        return OutResultError(TextError.exec_command_error())

    for line in stdout:
        if 'Invalid target specified' in line:
            return OutResultError(TextError.exec_command_error())

    keys = []
    values = []
    for line in stdout:
        if keys and '-+-' not in line:
            fond = [val.strip() for val in line.split('|')]
            val = {}
            for i, key in enumerate(keys):
                if len(fond) > i:
                    val[key] = fond[i]
            if val:
                values.append(val)

        if '| Version |' in line:
            keys = [key.strip() for key in line.split('|')]

    if not values:
        return OutResultInfo(TextInfo.psdk_package_not_found())

    return OutResultInfo(TextInfo.psdk_package_search(values), value=values)


def shell_psdk_package_install(
        tool: str,
        target: str,
        path: str,
) -> OutResult:
    stdout, stderr = shell_exec_command([
        tool,
        'sb2',
        '-t',
        target,
        '-m',
        'sdk-install',
        '-R',
        'zypper',
        '--no-gpg-checks',
        'in',
        '-y',
        path
    ])
    if stderr:
        return OutResultError(TextError.exec_command_error())
    else:
        for line in stdout:
            if 'No provider of' in line:
                return OutResultError(TextError.file_not_found_error(path))
            if 'Invalid target specified' in line:
                return OutResultError(TextError.exec_command_error())
            if 'Problem with the RPM' in line:
                return OutResultError(TextError.exec_command_error())
            if 'is already installed' in line:
                return OutResultInfo(TextInfo.psdk_package_already_installed())

    return OutResult(TextSuccess.psdk_package_install_success())


def shell_psdk_package_remove(
        tool: str,
        target: str,
        package: str,
) -> OutResult:
    stdout, stderr = shell_exec_command([
        tool,
        'sb2',
        '-t',
        target,
        '-m',
        'sdk-install',
        '-R',
        'zypper',
        'rm',
        '-y',
        package
    ])
    if stderr:
        return OutResultError(TextError.exec_command_error())
    else:
        for line in stdout:
            if 'Invalid target specified' in line:
                return OutResultError(TextError.exec_command_error())
            if 'not found in package names' in line:
                return OutResultInfo(TextInfo.psdk_package_not_found())

    return OutResult(TextSuccess.psdk_package_remove_success())


def shell_psdk_package_validate(
        tool: str,
        target: str,
        path: str,
        profile: str,
) -> OutResult:
    stdout, stderr = shell_exec_command([
        tool,
        'sb2',
        '-t',
        target,
        '-m',
        'emulate',
        'rpm-validator',
        '-p',
        profile,
        path
    ])
    if stderr:
        return OutResultError(TextError.exec_command_error())
    else:
        for line in stdout:
            if 'read failed' in line:
                return OutResultError(TextError.file_not_found_error(path))
            if 'ERROR' in line:
                return OutResultError(TextError.psdk_validate_error())

    return OutResult(TextSuccess.psdk_validate_success())


def shell_psdk_resign(
        tool: str,
        key: str,
        cert: str,
        path: str,
) -> OutResult:
    shell_exec_command([
        tool,
        'rpmsign-external',
        'delete',
        path
    ])
    stdout, stderr = shell_exec_command([
        tool,
        'rpmsign-external',
        'sign',
        f'--key={key}',
        f'--cert={cert}',
        path
    ])
    if stderr:
        return OutResultError(TextError.psdk_sign_error())
    else:
        for line in stdout:
            if 'is a directory' in line:
                return OutResultError(TextError.file_not_found_error(path))

    return OutResult(TextSuccess.psdk_sign_success())
