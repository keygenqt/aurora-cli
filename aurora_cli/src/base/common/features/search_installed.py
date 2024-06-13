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

from aurora_cli.src.base.common.features.load_by_version import (
    get_version_psdk_from_file,
    get_tool_psdk_from_file_with_version,
    get_version_sdk_from_file,
    get_tool_sdk_from_file_with_version,
    get_version_flutter_from_path
)
from aurora_cli.src.base.models.workdir_model import WorkdirModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.disk_cache import disk_cache
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.path import path_convert_relative
from aurora_cli.src.base.utils.verbose import verbose_command_start, verbose_add_map


def _search_files(workdir: Path, pattern: str) -> [Path]:
    files = []
    command = verbose_command_start(f'rglob: {pattern}')
    for file in workdir.rglob(pattern):
        if file.is_file():
            files.append(file)
    verbose_add_map(
        command=command,
        stdout=[],
        stderr=[],
    )
    return files


def search_file_for_check_is_flutter_project(path: Path) -> bool:
    desktop = _search_files(path, '*.desktop')
    pubspec = _search_files(path, 'pubspec.yaml')
    dart = _search_files(path, '*.dart')
    return len(desktop) != 0 and len(dart) != 0 and len(pubspec) == 1


def search_file_for_check_is_aurora_project(path: Path) -> bool:
    desktop = _search_files(path, '*.desktop')
    pro = _search_files(path, '*.pro')
    qml = _search_files(path, '*.qml')
    return len(desktop) != 0 and len(pro) != 0 and len(qml) != 0


def search_project_application_id(path: Path) -> str | None:
    desktop = _search_files(path, '*.desktop')
    if not desktop:
        return None
    org = ''
    app = ''
    with open(desktop[0]) as f:
        for line in f:
            if 'OrganizationName=' in line:
                org = line.replace('OrganizationName=', '').strip()
            if 'ApplicationName=' in line:
                app = line.replace('ApplicationName=', '').strip()

    if org and app:
        return f'{org}.{app}'
    return None


def search_flutter_project_pubspec_key(path: Path, key: str) -> bool:
    pubspec = _search_files(path, 'pubspec.yaml')
    if not pubspec:
        return False
    with open(pubspec[0]) as f:
        for line in f:
            if key in line:
                return True
    return False


@disk_cache()
def search_installed_flutter() -> OutResult:
    path = path_convert_relative('~/.local/opt')
    files = _search_files(path, 'flutter-*/bin/flutter')

    versions = []
    flutters = []
    darts = []
    files = sorted(files)
    files = reversed(files)
    for flutter in files:
        version = get_version_flutter_from_path(flutter)
        if version:
            versions.append(version)
            flutters.append(str(flutter))
            darts.append(str(flutter.parent / 'dart'))
    if not versions:
        return OutResultError(TextError.just_empty_error())
    return OutResult(TextInfo.installed_versions_flutter(versions), value={
        'versions': versions,
        'flutters': flutters,
        'darts': darts,
    })


@disk_cache()
def search_installed_psdk() -> OutResult:
    workdir = WorkdirModel.get_workdir()
    files = _search_files(workdir, 'sdks/aurora_psdk/etc/os-release')
    versions = []
    tools = []
    files = sorted(files)
    files = reversed(files)
    for file in files:
        version = get_version_psdk_from_file(file)
        tool = get_tool_psdk_from_file_with_version(file)
        if version and tool:
            versions.append(version)
            tools.append(str(tool))
    if not versions:
        return OutResultError(TextError.just_empty_error())
    return OutResult(TextInfo.installed_versions_psdk(versions), value={
        'versions': versions,
        'tools': tools,
    })


@disk_cache()
def search_installed_sdk() -> OutResult:
    workdir = WorkdirModel.get_workdir()
    files = _search_files(workdir, 'sdk-release')
    versions = []
    tools = []
    files = sorted(files)
    files = reversed(files)
    for file in files:
        version = get_version_sdk_from_file(file)
        tool = get_tool_sdk_from_file_with_version(file)
        if version and tool:
            versions.append(version)
            tools.append(str(tool))
    if not versions:
        return OutResultError(TextError.just_empty_error())
    return OutResult(TextInfo.installed_versions_sdk(versions), value={
        'versions': versions,
        'tools': tools,
    })
