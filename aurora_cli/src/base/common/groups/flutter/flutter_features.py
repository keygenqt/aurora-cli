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

from aurora_cli.src.base.common.features.request_version import request_versions_flutter
from aurora_cli.src.base.common.features.search_installed import search_installed_flutter
from aurora_cli.src.base.models.flutter_model import FlutterModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.cache_func import cache_func_clear
from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResult
from aurora_cli.src.base.utils.tests import tests_exit
from aurora_cli.src.base.utils.text_file import file_remove_line
from aurora_cli.src.base.utils.url import get_url_git_flutter


def flutter_available_common():
    echo_stdout(request_versions_flutter())


def flutter_installed_common():
    echo_stdout(search_installed_flutter())


@check_dependency(DependencyApps.git)
def flutter_install_common(
        version: str,
        is_bar: bool = True
):
    tests_exit()
    # url major version
    git_url = get_url_git_flutter()
    # path install
    flutter_path = Path.home() / '.local' / 'opt' / f'flutter-{version}'
    # check path
    if flutter_path.is_dir() or flutter_path.is_file():
        echo_stdout(OutResultError(TextError.flutter_already_installed_error(version)))
        app_exit()

    from aurora_cli.src.base.utils.git import git_clone
    repo = git_clone(git_url, flutter_path, is_bar)
    repo.git.checkout(version)

    # clear cache
    cache_func_clear()
    # end
    echo_stdout(OutResult(TextSuccess.flutter_install_success(str(flutter_path), version)))


def flutter_remove_common(model: FlutterModel):
    tests_exit()
    path: str = model.get_path()
    version: str = model.get_version()
    shutil.rmtree(path)
    file_remove_line(Path.home() / '.bashrc', path)
    cache_func_clear()
    echo_stdout(OutResult(TextSuccess.flutter_remove_success(version)))
