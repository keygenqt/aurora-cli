from pathlib import Path

from aurora_cli.src.base.common.flutter_features import get_version_flutter_from_file, \
    get_tool_flutter_from_file_with_version, get_tool_dart_from_file_with_version
from aurora_cli.src.base.common.psdk_features import get_version_psdk_from_file, get_tool_psdk_from_file_with_version
from aurora_cli.src.base.common.sdk_features import get_version_sdk_from_file, get_tool_sdk_from_file_with_version
from aurora_cli.src.base.models.workdir_model import WorkdirModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.disk_cache import disk_cache
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.path import path_convert_relative


def _search_files(workdir: Path, pattern: str) -> [str]:
    files = []
    for file in workdir.rglob(pattern):
        if file.is_file():
            files.append(file)
    return files


@disk_cache()
def search_installed_flutter() -> OutResult:
    path = path_convert_relative('~/.local/opt')
    files = _search_files(path, 'flutter*/CHANGELOG.md')
    versions = []
    flutters = []
    darts = []
    files = sorted(files)
    files = reversed(files)
    for file in files:
        version = get_version_flutter_from_file(file)
        flutter = get_tool_flutter_from_file_with_version(file)
        dart = get_tool_dart_from_file_with_version(file)
        if version and flutter and dart:
            versions.append(version)
            flutters.append(flutter)
            darts.append(dart)
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
            tools.append(tool)
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
            tools.append(tool)
    if not versions:
        return OutResultError(TextError.just_empty_error())
    return OutResult(TextInfo.installed_versions_sdk(versions), value={
        'versions': versions,
        'tools': tools,
    })
