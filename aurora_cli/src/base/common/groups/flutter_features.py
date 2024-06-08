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
from aurora_cli.src.base.models.flutter_model import FlutterModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.git import git_clone
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResult
from aurora_cli.src.base.utils.text_file import file_remove_line
from aurora_cli.src.base.utils.url import get_url_git_flutter


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


# @todo
def flutter_project_format_common(
        model: FlutterModel,
        project: Path,
        verbose: bool
):
    print(project)
    print(model.get_tools_dart())
    echo_stdout(OutResult(TextSuccess.flutter_project_format_success()), verbose)


# @todo
def flutter_project_build_common(
        model: FlutterModel,
        project: Path,
        verbose: bool
):
    print(project)
    print(model.get_tools_flutter())
    echo_stdout(OutResult(TextSuccess.flutter_project_build_success()), verbose)


# @todo
def flutter_project_report_common(project: Path, verbose: bool):
    print(project)
    echo_stdout(OutResult(TextSuccess.flutter_project_report_success()), verbose)
