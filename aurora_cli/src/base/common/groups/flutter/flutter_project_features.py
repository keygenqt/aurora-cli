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
import filecmp
import json
import re
import shutil
from pathlib import Path

from aurora_cli.src.base.common.features.flutter_features import flutter_project_get_pub
from aurora_cli.src.base.common.features.image_features import image_crop_for_project
from aurora_cli.src.base.common.features.request_version import request_flutter_plugins
from aurora_cli.src.base.common.features.search_files import (
    search_flutter_project_pubspec_key
)
from aurora_cli.src.base.common.features.shell_features import shell_dart_format, shell_cpp_format
from aurora_cli.src.base.common.groups.flutter.__tools import (
    flutter_tool_get_clang_format,
    flutter_tool_check_is_project
)
from aurora_cli.src.base.models.flutter_model import FlutterModel
from aurora_cli.src.base.out.flutter_report_plugins import gen_flutter_report_plugins
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.output import echo_stdout, OutResult, OutResultInfo, OutResultError
from aurora_cli.src.base.utils.path import path_temp_copy, path_temp_folder
from aurora_cli.src.base.utils.tests import tests_exit


def flutter_project_format_common(
        model: FlutterModel,
        project: Path,
        is_bar: bool = True
):
    tests_exit()

    flutter_tool_check_is_project(project)

    files_dart = project.rglob('*.dart')
    files_h = project.rglob('*.h')
    files_cpp = project.rglob('*.cpp')

    # if C++ files exist run clang-format format
    if files_h or files_cpp:
        files = []
        files.extend(files_h)
        files.extend(files_cpp)
        result = shell_cpp_format(files, flutter_tool_get_clang_format(is_bar))
        echo_stdout(result)
        if result.is_error():
            app_exit()

    # if dart files exist run dart format
    if files_dart:
        result = shell_dart_format(model.get_tool_dart(), str(project))
        echo_stdout(result)
        if result.is_error():
            app_exit()

    echo_stdout(OutResult(TextSuccess.project_format_success()))


def flutter_project_check_format_common(
        model: FlutterModel,
        project: Path,
        is_bar: bool = True
):
    tests_exit()

    temp_folder = path_temp_folder()
    flutter_tool_check_is_project(project)

    files_dart = project.rglob('*.dart')
    files_h = project.rglob('*.h')
    files_cpp = project.rglob('*.cpp')

    # if C++ files exist run clang-format format
    if files_h or files_cpp:
        for file in files_h:
            copy_file = path_temp_copy(file, temp_folder)
            shell_cpp_format([copy_file], flutter_tool_get_clang_format(is_bar))
            if not filecmp.cmp(file, copy_file):
                shutil.rmtree(temp_folder)
                echo_stdout(OutResultInfo(TextInfo.project_format_needs()))
                return False
        for file in files_cpp:
            copy_file = path_temp_copy(file, temp_folder)
            shell_cpp_format([copy_file], flutter_tool_get_clang_format(is_bar))
            if not filecmp.cmp(file, copy_file):
                shutil.rmtree(temp_folder)
                echo_stdout(OutResultInfo(TextInfo.project_format_needs()))
                return False

    # if dart files exist run dart format
    if files_dart:
        for file in files_dart:
            path_temp_copy(file, temp_folder)
        result = shell_dart_format(model.get_tool_dart(), str(temp_folder))
        if result.value:
            shutil.rmtree(temp_folder)
            echo_stdout(OutResultInfo(TextInfo.project_format_needs()))
            return False

    shutil.rmtree(temp_folder)
    echo_stdout(OutResult(TextSuccess.project_format_no_needs()))
    return True


def flutter_project_report_common(
        model: FlutterModel,
        project: Path,
        is_bar: bool = True
):
    from weasyprint import HTML

    tests_exit()

    flutter_tool_check_is_project(project)

    bar = AliveBarPercentage()

    def out_check_result(out: OutResult):
        echo_stdout(out)
        if out.is_error():
            app_exit()

    def out_progress(percent: int):
        if is_bar:
            bar.update(percent)
        else:
            echo_stdout(OutResultInfo(TextInfo.install_progress(), value=percent))

    available = [
        'dbus',
        'build_runner',
        'build_runner_core',
        'flutter_cache_manager',
        'cached_network_image',
        'google_fonts',
    ]

    result = request_flutter_plugins()
    if result.is_error():
        available_impl = []
    else:
        available_impl = list(dict.fromkeys(
            [plugin.split('-')[0].replace('_aurora', '') for plugin in result.value if '_aurora' in plugin]))

    echo_stdout(OutResultInfo(TextInfo.flutter_project_pub_get()))

    out_check_result(flutter_project_get_pub(
        flutter=model.get_tool_flutter(),
        path=project,
        progress=lambda percent: out_progress(percent)
    ))

    package_config = project / '.dart_tool' / 'package_config.json'

    with open(package_config, 'r') as file:
        data = json.loads(file.read())

    if not data and not data['packages']:
        echo_stdout(OutResultError(TextError.flutter_read_json_error()))
        app_exit()

    find_plugins_nps = []
    find_plugins_ps = []

    keys = '|'.join([
        '_android',
        '_ios',
        '_linux',
        '_macos',
        '_web',
        '_windows',
        '_aurora'
    ])

    for item in data['packages']:
        plugin = Path(item['rootUri'].replace('file://', '')) / 'pubspec.yaml'
        if plugin.is_file():
            with open(plugin, 'r') as file:
                if item['name'][0] != '_':
                    if file.read().find("platforms:") == -1:
                        find_plugins_nps.append(item['name'])
                    else:
                        find_plugins_ps.append(item['name'])

    find_plugins_nps = list(dict.fromkeys(find_plugins_nps))
    find_plugins_ps = list(dict.fromkeys([re.sub(f'(.+)({keys})', r'\1', plugin) for plugin in find_plugins_ps]))
    find_plugins_aps = [plugin for plugin in find_plugins_ps if plugin in available or plugin in available_impl]

    line_name = search_flutter_project_pubspec_key(project, 'name')
    line_desc = search_flutter_project_pubspec_key(project, 'description')

    if not line_name:
        echo_stdout(OutResultError(TextError.flutter_read_yaml_error()))
        app_exit()
    else:
        line_name = line_name.replace('name: ', '')

    if line_desc:
        line_desc = line_desc.replace('description: ', '')

    echo_stdout(OutResultInfo(TextInfo.flutter_gen_plugins_report()))

    path_out = project / 'plugins_report.pdf'
    html_out = gen_flutter_report_plugins(
        name=line_name,
        description=line_desc,
        find_plugins_nps=find_plugins_nps,
        find_plugins_ps=find_plugins_ps,
        find_plugins_aps=find_plugins_aps,
    )

    HTML(string=html_out).write_pdf(path_out)

    echo_stdout(OutResult(TextSuccess.flutter_project_report_success(str(path_out)), value=path_out))


def flutter_project_icons_common(
        project: Path,
        image: Path
):
    if argv_is_test():
        echo_stdout(OutResult())
        app_exit(0)

    flutter_tool_check_is_project(project)

    if (project / 'example').is_dir():
        project = project / 'example'

    path_icons = project / 'aurora' / 'icons'
    result = image_crop_for_project(image, path_icons)
    echo_stdout(result)
