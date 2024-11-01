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

from aurora_cli.src.base.common.features.image_features import image_crop_for_project
from aurora_cli.src.base.common.features.search_files import search_project_application_id
from aurora_cli.src.base.common.features.shell_features import shell_cpp_format
from aurora_cli.src.base.common.groups.psdk.__tools import psdk_tool_check_is_project, psdk_tool_get_clang_format
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import echo_stdout, OutResult
from aurora_cli.src.base.utils.tests import tests_exit


def psdk_project_format_common(
        project: Path,
        is_bar: bool = True
):
    tests_exit()
    psdk_tool_check_is_project(project)

    files_h = project.rglob('*.h')
    files_cpp = project.rglob('*.cpp')

    # if C++ files exist run clang-format format
    if files_h or files_cpp:
        files = []
        files.extend(files_h)
        files.extend(files_cpp)
        result = shell_cpp_format(files, psdk_tool_get_clang_format(is_bar))
        if not result.is_error():
            echo_stdout(result)
        else:
            echo_stdout(result)
            app_exit()

    echo_stdout(OutResult(TextSuccess.project_format_success()))


def psdk_project_icons_common(
        project: Path,
        image: Path
):
    tests_exit()
    psdk_tool_check_is_project(project)
    path_icons = project / 'icons'
    result = image_crop_for_project(image, path_icons, search_project_application_id(project))
    echo_stdout(result)
