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
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.output import OutResult, OutResultError, OutResultInfo
from aurora_cli.src.base.utils.percent_cli import percent_start, percent_counter, percent_end
from aurora_cli.src.base.utils.shell import shell_exec_command, shell_check_error_out


def shell_ssh_copy_id(
        ip: str,
        ssh_key: Path,
) -> OutResult:
    stdout, stderr = shell_exec_command([
        'ssh-copy-id',
        '-i',
        str(ssh_key),
        f'defaultuser@{ip}',
    ])

    result = shell_check_error_out(stdout, stderr, ['Permission denied'])
    if result.is_error():
        return OutResultError(TextError.ssh_copy_id_error())

    return OutResult(TextSuccess.ssh_copy_id_success())


def shell_dart_format(
        dart: str,
        path: str
) -> OutResult:
    stdout, stderr = shell_exec_command([
        dart,
        'format',
        '--line-length=120',
        path,
    ])

    result = shell_check_error_out(stdout, stderr, ['Could not format'])
    if result.is_error():
        return OutResultError(TextError.project_format_error())

    return OutResultInfo(TextInfo.flutter_project_format_dart_done())


@check_dependency(DependencyApps.clang_format)
def shell_cpp_format(
        files: [Path],
        config: Path
) -> OutResult:
    for file in files:
        stdout, stderr = shell_exec_command([
            'clang-format',
            f'--style=file:{config}',
            '-i',
            str(file)
        ])
        result = shell_check_error_out(stdout, stderr)
        if result.is_error():
            return OutResultError(TextError.project_format_error())

    return OutResultInfo(TextInfo.flutter_project_format_cpp_done())


@check_dependency(DependencyApps.sudo, DependencyApps.tar)
def shell_tar_sudo_unpack(
        archive_path: str,
        unpack_path: str,
        progress: Callable[[int], None],
        password=None
) -> OutResult:
    percents = []
    percent_start(percents, progress)
    size = Path(archive_path).stat().st_size
    count = int(size * 130 / 439822186)

    stdout, stderr = shell_exec_command([
        'sudo',
        'tar',
        '--numeric-owner',
        '-p',
        '-xjf',
        archive_path,
        '--totals',
        '--checkpoint=1000',
        '--checkpoint-action=echo="#%u"',
        '-C',
        unpack_path
    ], listen=lambda out: percent_counter(count, percents, progress), disable_sigint=False, password=password)

    percent_end(percents, progress)

    result = shell_check_error_out(stdout, stderr, ['error'])
    if result.is_error():
        return result

    return OutResultInfo(TextSuccess.tar_unpack_success(), value=archive_path)


@check_dependency(DependencyApps.sudo)
def shell_psdk_tooling_create(
        tool: str,
        version: str,
        path: str,
        progress: Callable[[int], None],
        password=None
) -> OutResult:
    percents = []
    percent_start(percents, progress)

    stdout, stderr = shell_exec_command([
        tool,
        'sdk-assistant',
        'tooling',
        'create',
        '-y',
        'AuroraOS-{}-base'.format(version),
        path
    ], listen=lambda _: percent_counter(15, percents, progress), disable_sigint=False, password=password)

    percent_end(percents, progress)

    result = shell_check_error_out(stdout, stderr, ['error', 'permitted'])
    if result.is_error():
        return result

    return OutResultInfo(TextSuccess.psdk_tooling_install_success(), value=path)


@check_dependency(DependencyApps.sudo)
def shell_psdk_target_create(
        tool: str,
        version: str,
        path: str,
        arch: str,
        progress: Callable[[int], None],
        password=None
) -> OutResult:
    percents = []
    percent_start(percents, progress)

    stdout, stderr = shell_exec_command([
        tool,
        'sdk-assistant',
        'target',
        'create',
        '-y',
        'AuroraOS-{}-base-{}'.format(version, arch),
        path
    ], listen=lambda out: percent_counter(30, percents, progress), disable_sigint=False, password=password)

    percent_end(percents, progress)

    result = shell_check_error_out(stdout, stderr, ['error', 'permitted'])
    if result.is_error():
        return result

    return OutResultInfo(TextSuccess.psdk_target_install_success(), value=path)


@check_dependency(DependencyApps.sudo)
def shell_psdk_targets(
        tool: str,
        version: str,
        password = None
) -> OutResult:
    targets = []
    stdout, stderr = shell_exec_command([
        tool,
        'sdk-assistant',
        'list',
    ], password=password)
    if stderr:
        return OutResultError(TextError.psdk_targets_get_error())

    for line in stdout:
        if '─' in line and 'default' not in line:
            targets.append(line[2:])

    if not targets:
        return OutResultInfo(TextInfo.psdk_targets_empty(version))

    return OutResult(TextSuccess.psdk_targets_get_success(version, targets), value=targets)


@check_dependency(DependencyApps.sudo)
def shell_psdk_clear(
        tool: str,
        target: str,
        password = None
) -> OutResult:
    stdout, stderr = shell_exec_command([
        tool,
        'sdk-assistant',
        'target',
        'remove',
        '-y',
        '--snapshots-of',
        target
    ], password=password)

    result = shell_check_error_out(stdout, stderr, ['No such target'])
    if result.is_error():
        return result

    return OutResult(TextSuccess.psdk_clear_success())


@check_dependency(DependencyApps.sudo)
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

    result = shell_check_error_out(stdout, stderr, ['Invalid target specified'])
    if result.is_error():
        return result

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


@check_dependency(DependencyApps.sudo)
def shell_psdk_package_install(
        tool: str,
        target: str,
        path: str,
        password = None
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
    ], password=password)

    result = shell_check_error_out(stdout, stderr, [
        'No provider of',
        'is already installed',
        'Invalid target specified',
        'Problem with the RPM',
    ])
    if result.is_error():
        if result.value == 0:
            return OutResultError(TextError.file_not_found_error(path))
        if result.value == 1:
            return OutResultInfo(TextInfo.psdk_package_already_installed())
        return result

    return OutResult(TextSuccess.psdk_package_install_success())


@check_dependency(DependencyApps.sudo)
def shell_psdk_package_remove(
        tool: str,
        target: str,
        package: str,
        password = None
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
    ], password=password)

    result = shell_check_error_out(stdout, stderr, [
        'not found in package names',
        'Invalid target specified',
    ])
    if result.is_error():
        if result.value == 0:
            return OutResultInfo(TextInfo.psdk_package_not_found())
        return result

    return OutResult(TextSuccess.psdk_package_remove_success())


@check_dependency(DependencyApps.sudo)
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

    result = shell_check_error_out(stdout, stderr, [
        'read failed',
        'ERROR',
    ])
    if result.is_error():
        if result.value == 0:
            return OutResultError(TextError.file_not_found_error(path))
        if result.value == 1:
            return OutResultError(TextError.psdk_validate_error())
        return result

    return OutResult(TextSuccess.psdk_validate_success())


@check_dependency(DependencyApps.sudo)
def shell_psdk_resign(
        tool: str,
        key: str,
        cert: str,
        path: str,
        password = None
) -> OutResult:
    shell_exec_command([
        tool,
        'rpmsign-external',
        'delete',
        path
    ], password=password)
    stdout, stderr = shell_exec_command([
        tool,
        'rpmsign-external',
        'sign',
        f'--key={key}',
        f'--cert={cert}',
        path
    ], password=password)

    result = shell_check_error_out(stdout, stderr, [
        'is a directory',
    ])
    if result.is_error():
        if result.value == 0:
            return OutResultError(TextError.file_not_found_error(path))
        return result

    return OutResult(TextSuccess.psdk_sign_success(Path(path).name))


@check_dependency(DependencyApps.sudo)
def shell_remove_root_folder(
        path: str,
        password = None
) -> OutResult:
    stdout, stderr = shell_exec_command(['sudo', 'rm', '-rf', path], password=password)
    if stderr:
        return OutResultError(TextError.exec_command_error())
    return OutResult()
