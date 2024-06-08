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
import shutil
from pathlib import Path

from aurora_cli.src.base.common.features.request_version import get_versions_flutter
from aurora_cli.src.base.common.features.search_installed import search_installed_flutter
from aurora_cli.src.base.common.features.shell_features import shell_dart_format, shell_cpp_format
from aurora_cli.src.base.constants.app import PATH_CLANG_FORMAT_CONF
from aurora_cli.src.base.constants.url import URL_CLANG_FORMAT_CONF
from aurora_cli.src.base.models.flutter_model import FlutterModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.download import check_with_download_files
from aurora_cli.src.base.utils.git import git_clone
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResult, OutResultInfo
from aurora_cli.src.base.utils.text_file import file_remove_line
from aurora_cli.src.base.utils.url import get_url_git_flutter


def _check_path_project(path: Path):
    if not path.is_dir() or not (path / 'pubspec.yaml').is_file():
        echo_stdout(OutResultError(TextError.flutter_project_not_found(str(path))))
        exit(1)


@check_dependency(DependencyApps.clang_format)
def _get_clang_format(verbose: bool, is_bar: bool) -> Path:
    return check_with_download_files(
        files=[PATH_CLANG_FORMAT_CONF],
        urls=[URL_CLANG_FORMAT_CONF],
        verbose=verbose,
        is_bar=is_bar
    )[0]


def flutter_available_common(verbose: bool):
    echo_stdout(get_versions_flutter(), verbose)


def flutter_installed_common(verbose: bool):
    echo_stdout(search_installed_flutter(), verbose)


def flutter_install_common(
        version: str,
        verbose: bool,
        is_bar: bool = True
):
    # url major version
    git_url = get_url_git_flutter()
    # path install
    flutter_path = Path.home() / '.local' / 'opt' / f'flutter-{version}'
    # check path
    if flutter_path.is_dir() or flutter_path.is_file():
        echo_stdout(OutResultError(TextError.flutter_already_installed_error(version)), verbose)
        exit(1)

    repo = git_clone(git_url, flutter_path, verbose, is_bar)
    repo.git.checkout(version)

    echo_stdout(OutResult(TextSuccess.flutter_install_success(str(flutter_path), version)), verbose)


def flutter_remove_common(model: FlutterModel, verbose: bool):
    path: str = model.get_path()
    version: str = model.get_version()
    # remove folder
    shutil.rmtree(path)
    # remove alias
    file_remove_line(
        file=Path.home() / '.bashrc',
        search=path
    )
    echo_stdout(OutResult(TextSuccess.flutter_remove_success(version)), verbose)


def flutter_project_report_common(project: Path, verbose: bool):
    _check_path_project(project)

    # @todo
    print(project)
    echo_stdout(OutResult(TextSuccess.flutter_project_report_success()), verbose)


def flutter_project_format_common(
        model: FlutterModel,
        project: Path,
        verbose: bool,
        is_bar: bool = True
):
    _check_path_project(project)

    files_dart = project.rglob('*.dart')
    files_h = project.rglob('*.h')
    files_cpp = project.rglob('*.cpp')

    # if C++ files exist run clang-format format
    if files_h or files_cpp:
        files = []
        files.extend(files_h)
        files.extend(files_cpp)
        result = shell_cpp_format(files, _get_clang_format(verbose, is_bar))
        if result.is_error():
            echo_stdout(result, verbose)
            exit(1)
        echo_stdout(OutResultInfo(TextInfo.flutter_project_format_cpp_done()), verbose)

    # if dart files exist run dart format
    if files_dart:
        result = shell_dart_format(model.get_tool_dart(), str(project))
        if result.is_error():
            echo_stdout(result, verbose)
            exit(1)
        echo_stdout(OutResultInfo(TextInfo.flutter_project_format_dart_done()), verbose)

    echo_stdout(OutResult(TextSuccess.flutter_project_format_success()), verbose)


def flutter_project_build_common(
        model: FlutterModel,
        project: Path,
        verbose: bool
):
    _check_path_project(project)

    # @todo
    print(project)
    print(model.get_tool_flutter())
    echo_stdout(OutResult(TextSuccess.flutter_project_build_success()), verbose)


def flutter_project_debug_common(
        model: FlutterModel,
        project: Path,
        verbose: bool
):
    _check_path_project(project)

    # @todo
    print(project)
    print(model.get_tool_flutter())
    echo_stdout(OutResult(TextSuccess.flutter_project_build_success()), verbose)
