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

from aurora_cli.src.base.common.features.shell_features import shell_dart_format, shell_cpp_format
from aurora_cli.src.base.common.groups.flutter.__tools import (
    flutter_tool_get_clang_format,
    flutter_tool_check_is_project
)
from aurora_cli.src.base.models.flutter_model import FlutterModel
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.output import echo_stdout, OutResult


def flutter_project_format_common(
        model: FlutterModel,
        project: Path,
        verbose: bool,
        is_bar: bool = True
):
    flutter_tool_check_is_project(project)

    files_dart = project.rglob('*.dart')
    files_h = project.rglob('*.h')
    files_cpp = project.rglob('*.cpp')

    # if C++ files exist run clang-format format
    if files_h or files_cpp:
        files = []
        files.extend(files_h)
        files.extend(files_cpp)
        result = shell_cpp_format(files, flutter_tool_get_clang_format(verbose, is_bar))
        if not result.is_error():
            echo_stdout(result)
        else:
            echo_stdout(result, verbose)
            exit(1)

    # if dart files exist run dart format
    if files_dart:
        result = shell_dart_format(model.get_tool_dart(), str(project))
        if not result.is_error():
            echo_stdout(result)
        else:
            echo_stdout(result, verbose)
            exit(1)

    echo_stdout(OutResult(TextSuccess.project_format_success()), verbose)


def flutter_project_build_common(
        model: FlutterModel,
        project: Path,
        verbose: bool
):
    flutter_tool_check_is_project(project)

    print('Coming soon')

    echo_stdout(OutResult(TextSuccess.project_build_success()), verbose)


def flutter_project_debug_common(
        model: FlutterModel,
        project: Path,
        verbose: bool
):
    flutter_tool_check_is_project(project)

    print('Coming soon')


def flutter_project_report_common(project: Path, verbose: bool):
    flutter_tool_check_is_project(project)

    print('Coming soon')

    echo_stdout(OutResult(TextSuccess.flutter_project_report_success()), verbose)
