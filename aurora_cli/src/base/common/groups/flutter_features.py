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
from aurora_cli.src.base.constants.app import PATH_CLANG_FORMAT_CONF
from aurora_cli.src.base.constants.url import URL_CLANG_FORMAT_CONF
from aurora_cli.src.base.models.flutter_model import FlutterModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.download import downloads
from aurora_cli.src.base.utils.git import git_clone
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResult, OutResultInfo
from aurora_cli.src.base.utils.path import path_convert_relative, path_get_download_path
from aurora_cli.src.base.utils.shell import shell_exec_command
from aurora_cli.src.base.utils.text_file import file_remove_line
from aurora_cli.src.base.utils.url import get_url_git_flutter


def _check_path_project(path: Path):
    if not path.is_dir() or not (path / 'pubspec.yaml').is_file():
        echo_stdout(OutResultError(TextError.flutter_project_not_found(str(path))))
        exit(1)


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


@check_dependency(DependencyApps.clang_format)
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

    # if dart files exist run dart format
    if files_dart:
        echo_stdout(OutResultInfo(TextInfo.flutter_project_format_start_dart()))
        stdout, stderr = shell_exec_command([
            model.get_tool_dart(),
            'format',
            '--line-length=120',
            str(project),
        ])
        if stdout and 'Could not format' in stdout[0]:
            echo_stdout(OutResultError(TextError.flutter_project_format_error()), verbose)
            exit(1)

    # if C++ files exist run clang-format format
    if files_h or files_cpp:
        # check config file clang-format, download if not exist
        clang_format = path_convert_relative(PATH_CLANG_FORMAT_CONF)
        if not clang_format.is_file():
            echo_stdout(OutResultInfo(TextInfo.flutter_project_format_config_download()))
            downloads([URL_CLANG_FORMAT_CONF], verbose, is_bar)
            path_download = path_get_download_path(URL_CLANG_FORMAT_CONF)
            path_download.replace(clang_format)

        echo_stdout(OutResultInfo(TextInfo.flutter_project_format_start_c()))
        files_format = []
        files_format.extend(files_h)
        files_format.extend(files_cpp)
        for file in files_format:
            shell_exec_command([
                'clang-format',
                f'--style=file:{clang_format}',
                '-i',
                str(file)
            ])

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
