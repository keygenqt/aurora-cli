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
    get_version_flutter_from_path,
    get_run_sdk_from_file_with_version,
)
from aurora_cli.src.base.common.features.search_files import search_files
from aurora_cli.src.base.models.workdir_model import WorkdirModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.cache_func import cache_func
from aurora_cli.src.base.utils.output import OutResult, OutResultError, echo_stdout, OutResultInfo
from aurora_cli.src.base.utils.path import path_convert_relative


@cache_func()
def search_installed_flutter() -> OutResult:
    path = path_convert_relative('~/.local/opt')
    files = search_files(path, 'flutter-*/bin/flutter')
    echo_stdout(OutResultInfo(TextInfo.search_installed_flutter_sdk(str(path))))
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


@cache_func()
def search_installed_psdk() -> OutResult:
    workdir = WorkdirModel.get_workdir()

    if workdir == Path.home():
        echo_stdout(OutResultInfo(TextInfo.search_installed_aurora_psdk_hint(str(workdir))))
    else:
        echo_stdout(OutResultInfo(TextInfo.search_installed_aurora_psdk(str(workdir))))

    files = search_files(workdir, 'sdks/aurora_psdk/etc/os-release')
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


@cache_func()
def search_installed_sdk() -> OutResult:
    workdir = WorkdirModel.get_workdir()

    if workdir == Path.home():
        echo_stdout(OutResultInfo(TextInfo.search_installed_aurora_sdk_hint(str(workdir))))
    else:
        echo_stdout(OutResultInfo(TextInfo.search_installed_aurora_sdk(str(workdir))))

    files = search_files(workdir, 'sdk-release')
    versions = []
    tools = []
    runs = []
    files = sorted(files)
    files = reversed(files)
    for file in files:
        version = get_version_sdk_from_file(file)
        tool = get_tool_sdk_from_file_with_version(file)
        run = get_run_sdk_from_file_with_version(file)
        if version and tool:
            versions.append(version)
            tools.append(str(tool))
            runs.append(str(run))
    if not versions:
        return OutResultError(TextError.just_empty_error())
    return OutResult(TextInfo.installed_versions_sdk(versions), value={
        'versions': versions,
        'tools': tools,
        'runs': runs,
    })
